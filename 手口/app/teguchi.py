from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
import pandas as pd
import numpy as np
import io

app = FastAPI(title="JPX Derivatives Delta Analysis App")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Participant Mapping
broker_mapping = {
    "goldman": {"cat": "US", "rank": 10},
    "jpmorgan": {"cat": "US", "rank": 20},
    "bofa": {"cat": "US", "rank": 30},
    "citigroup": {"cat": "US", "rank": 40},
    "morgan": {"cat": "US", "rank": 50},
    "abn amro": {"cat": "EU", "rank": 10},
    "societe": {"cat": "EU", "rank": 20},
    "barclays": {"cat": "EU", "rank": 30},
    "bnp": {"cat": "EU", "rank": 40},
    "ubs": {"cat": "EU", "rank": 50},
    "deutsche": {"cat": "EU", "rank": 60},
    "nomura": {"cat": "JP", "rank": 10},
    "daiwa": {"cat": "JP", "rank": 20},
    "mizuho": {"cat": "JP", "rank": 30},
    "mitsubishi": {"cat": "JP", "rank": 40},
    "smbc": {"cat": "JP", "rank": 50},
    "sbi": {"cat": "Net", "rank": 10},
    "rakuten": {"cat": "Net", "rank": 20},
    "monex": {"cat": "Net", "rank": 30},
    "matsui": {"cat": "Net", "rank": 40},
}

cat_order = {"US": 1, "EU": 2, "JP": 3, "Net": 4, "Others": 5}

def get_broker_info(name_en: str):
    if not isinstance(name_en, str):
        return "Others", cat_order["Others"] * 1000 + 999
    name_lower = name_en.lower()
    for key, val in broker_mapping.items():
        if key in name_lower:
            return val["cat"], cat_order[val["cat"]] * 1000 + val["rank"]
    return "Others", cat_order["Others"] * 1000 + 999

@app.get("/", response_class=FileResponse)
async def serve_dashboard(request: Request):
    return FileResponse("templates/dashboard.html")

@app.get("/teguchi_view", response_class=FileResponse)
async def serve_teguchi(request: Request):
    return FileResponse("templates/teguchi.html")

@app.get("/option_view", response_class=FileResponse)
async def serve_option(request: Request):
    return FileResponse("templates/option.html")

@app.post("/api/analyze")
async def analyze_data(
    file: UploadFile = File(None),
    nikkei_price: float = Form(55000.0),
    topix_price: float = Form(3700.0),
    delta_atm: float = Form(0.5)
):
    try:
        dataframes = []
        if file and file.filename:
            content = await file.read()
            df = pd.read_excel(io.BytesIO(content), sheet_name="手口上位一覧", header=5, engine='openpyxl')
            cols = df.columns.tolist()
            df = df.rename(columns={
                cols[0]: 'Product_Class',
                cols[2]: 'Contract_Issue',
                cols[5]: 'JP_Name',
                cols[6]: 'EN_Name',
                cols[7]: 'Volume'
            })
            df = df[['Product_Class', 'Contract_Issue', 'EN_Name', 'JP_Name', 'Volume']].dropna(subset=['Volume'])
            df['Net'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0)
            
            df = df[df['Product_Class'].astype(str).str.strip() != '']
            df = df[df['EN_Name'].notna()]
            
            dataframes.append(df)
        
        if not dataframes:
            return JSONResponse({"error": "No files uploaded"}, status_code=400)
            
        return process_dataframes(dataframes, nikkei_price, topix_price, delta_atm)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

import requests
import re

@app.post("/api/fetch_latest")
async def fetch_latest(
    nikkei_price: float = Form(55000.0),
    topix_price: float = Form(3700.0),
    delta_atm: float = Form(0.5)
):
    try:
        from datetime import datetime
        import dateutil.relativedelta
        
        now = datetime.now()
        months_to_try = [now, now - dateutil.relativedelta.relativedelta(months=1)]
        
        xlsx_path = None
        for m in months_to_try:
            yyyymm = m.strftime('%Y%m')
            url = f"https://www.jpx.co.jp/automation/markets/derivatives/participant-volume/json/participant_volume_{yyyymm}.json"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for row in data.get('TableDatas', []):
                    path = row.get('WholeDay')
                    if path and str(path).strip() != '-' and 'xlsx' in str(path):
                        xlsx_path = path
                        break
            if xlsx_path:
                break
                
        if not xlsx_path:
            return JSONResponse({"error": "Failed to find Excel file URL on JPX website."}, status_code=400)
            
        if not xlsx_path.startswith('http'):
            xlsx_path = "https://www.jpx.co.jp" + xlsx_path
            
        resp = requests.get(xlsx_path, timeout=10)
        resp.raise_for_status()
        
        df = pd.read_excel(io.BytesIO(resp.content), sheet_name="手口上位一覧", header=5, engine='openpyxl')
        cols = df.columns.tolist()
        df = df.rename(columns={
            cols[0]: 'Product_Class',
            cols[2]: 'Contract_Issue',
            cols[5]: 'JP_Name',
            cols[6]: 'EN_Name',
            cols[7]: 'Volume'
        })
        df = df[['Product_Class', 'Contract_Issue', 'EN_Name', 'JP_Name', 'Volume']].dropna(subset=['Volume'])
        # Webから1ファイルの取得なので、基本出来高をポジティブなNetとして扱う簡易実装
        df['Net'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0) * 1
        
        df = df[df['Product_Class'].astype(str).str.strip() != '']
        df = df[df['EN_Name'].notna()]
        
        return process_dataframes([df], nikkei_price, topix_price, delta_atm)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": f"Auto-fetch failed: {str(e)}"}, status_code=500)


def process_dataframes(dataframes, nikkei_price, topix_price, delta_atm):
    try:
        combined = pd.concat(dataframes, ignore_index=True)
        # Drop rows where EN_Name is NaN/empty after concat
        combined = combined[combined['EN_Name'].astype(str).str.strip() != '']
        # Group by Participant and Contract for netting
        grouped = combined.groupby(['EN_Name', 'JP_Name', 'Product_Class', 'Contract_Issue'], as_index=False)['Net'].sum()

        results = []
        op_matrix = []
        firm_info = {}

        # Process each firm
        firms = grouped['EN_Name'].unique()
        for firm in firms:
            firm_data = grouped[grouped['EN_Name'] == firm]
            jp_name = firm_data['JP_Name'].iloc[0]
            display_name = jp_name[:10] if isinstance(jp_name, str) else str(firm)[:10]
            category, rank = get_broker_info(firm)
            
            firm_info[firm] = {
                "display": display_name,
                "category": category,
                "rank": rank
            }
            
            nk_large = firm_data[firm_data['Product_Class'] == 'NK225F']['Net'].sum()
            nk_mini = firm_data[firm_data['Product_Class'] == 'NK225MF']['Net'].sum()  # Check for mini code
            topix_f = firm_data[(firm_data['Product_Class'] == 'TOPIXF') | (firm_data['Product_Class'] == 'TOPIX')]['Net'].sum()
            
            # Options: NK225E, NK225 OOP, etc. Mock option delta calculation
            options = firm_data[firm_data['Contract_Issue'].str.contains(' OP | OOP ', na=False, case=False)]
            op_delta_amount = options['Net'].sum() * delta_atm * 1000  # simplified
            
            # Extract options matrix data
            for _, row in options.iterrows():
                # Extract Strike and Call/Put roughly
                # Format: NIKKEI 225 OOP P2602-52375
                issue = str(row['Contract_Issue'])
                cp = 'P' if ' P' in issue else ('C' if ' C' in issue else None)
                strike = 0
                import re
                match = re.search(r'-(\d+)', issue)
                if match:
                    strike = int(match.group(1))
                if cp and strike:
                    op_matrix.append({
                        "Firm": firm,
                        "Type": cp,
                        "Strike": strike,
                        "Net": row['Net']
                    })
            
            # デルタ金額計算 (円)
            delta_amount_yen = (nk_large * nikkei_price * 1000) + \
                               (nk_mini * nikkei_price * 100) + \
                               (topix_f * topix_price * 1000) + \
                               op_delta_amount
                               
            delta_amount_oku = delta_amount_yen / 100000000.0
            
            results.append({
                "Company": display_name,
                "Category": category,
                "NK225F": int(nk_large),
                "NK225M": int(nk_mini),
                "TOPIXF": int(topix_f),
                "DeltaOku": round(delta_amount_oku, 2),
                "Rank": rank
            })

        # Process OP Matrix
        op_df = pd.DataFrame(op_matrix)
        matrix_data = []
        strikes = []
        if not op_df.empty:
            # 異常値（150-2800など）を除外するため、10000以上の権利行使価格に絞る
            valid_strikes = [int(s) for s in op_df['Strike'].unique() if int(s) >= 10000]
            strikes = sorted(valid_strikes)
            
            for firm in op_df['Firm'].unique():
                firm_ops = op_df[op_df['Firm'] == firm]
                info = firm_info.get(firm, {"display": str(firm)[:10], "category": "Others", "rank": 9999})
                row_data = {
                    "Company": info["display"],
                    "Category": info["category"],
                    "Rank": info["rank"]
                }
                for s in strikes:
                    call_net = firm_ops[(firm_ops['Strike'] == s) & (firm_ops['Type'] == 'C')]['Net'].sum()
                    put_net = firm_ops[(firm_ops['Strike'] == s) & (firm_ops['Type'] == 'P')]['Net'].sum()
                    row_data[f"C_{s}"] = int(call_net)
                    row_data[f"P_{s}"] = int(put_net)
                row_data["C_Total"] = int(firm_ops[firm_ops['Type'] == 'C']['Net'].sum())
                row_data["P_Total"] = int(firm_ops[firm_ops['Type'] == 'P']['Net'].sum())
                row_data["Net_Total"] = row_data["C_Total"] + row_data["P_Total"]
                matrix_data.append(row_data)

        results.sort(key=lambda x: x["Rank"])
        if matrix_data:
            matrix_data.sort(key=lambda x: x["Rank"])

        return JSONResponse({"status": "success", "results": results, "matrix": matrix_data, "strikes": strikes if not op_df.empty else []})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("teguchi:app", host="127.0.0.1", port=8000)
