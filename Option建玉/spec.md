
## 目的1
以下のデリバティブ建玉残高表を使って日々の日経225,TOPIX,日経225mini、日経225マイクロのオプションの増減を見やすいビジュアルで可視化して把握する

## 目的2
当日のプット・コールでどの価格での増減があったのかを可視化する

##　目的３
日々のデータを蓄積して、後からも振り替えれるようにする

## 抽出にいくHP
https://www.jpx.co.jp/markets/derivatives/trading-volume/index.html

### 抽出したいURL
注意毎日ファイル名が変わるのでアドレスが変わるため、セレクターは要注意
https://www.jpx.co.jp/markets/derivatives/trading-volume/tvdivq00000014nn-att/20260310open_interest.xlsx

## データサンプル
C:\Users\HCY\OneDrive\投資\97.東証\Option建玉\specimage\20260310open_interest.xlsx

### 取得タブ名
１：デリバティブ建玉残高状況→目的１で利用
２：別紙1　（日経225のプットとコール）→目的2で利用
３：別紙2 (日経225ミニのプットとコール)→目的2で利用


## データ抽出の参考ソースコード
C:\Users\HCY\OneDrive\投資\97.東証\github_reference\main.py



