# 日経先物・オプション分析 (GitHub対応完全自動化版)

このプロジェクトは、JPX（日本取引所グループ）で公開されている日次データを毎日自動で取得・解析し、静的な「アナリティクスダッシュボード」として閲覧できるようにするものです。

## アーキテクチャ構成
* **バッチ処理**: GitHub Actionsを活用し、毎営業日の夜（UTC 11:00 / JST 20:00）にPythonスクリプト(`scripts/fetch_teguchi.py`)を実行し、最新データを `docs/data.json` に上書き保存します。
* **フロントエンド**: HTML・JS（Vue.js / Tailwind CSS）で記述され、サーバー機能不要の「GitHub Pages」で動作します。

---

## 🚀 GitHubへの連携と自動化セットアップ方法

現在VS CodeとGitHubアカウントが未連携とのことですので、**GitHub Desktopあるいはブラウザのみを使って簡単にアップロード・設定する方法を記載します。**

### ステップ 1: GitHubで新規リポジトリを作成
1. ブラウザで [GitHub](https://github.com/) にログインします。
2. 画面右上のアイコン横の **[+]** ボタンをクリックし、「**New repository**」を選択します。
3. リポジトリの各種項目を入力します。
   - **Repository name**: 例）`nf_option` 
   - **Public/Private**: お好みに合わせて選択します。（無料版GitHub Pagesを使う場合は `Public` である必要があります※）
   - ※有料版（Pro）の方は Private でも Pages 公開可能です。
   - README の追加チェックは **オフ** にしてください（後で上書きされるのを防ぐため）。
4. 「**Create repository**」ボタンを押します。

### ステップ 2: ローカルのファイルをGitHubへアップロード
VS Codeを利用せずにアップロードする一番簡単な方法は、GitHubの画面からのドラッグ＆ドロップです。

1. 新しく作成したリポジトリ画面で「**uploading an existing file**」のリンク（"Get started by creating a new file or..." の行にあります）をクリックします。
2. 開いたアップロード画面で、お使いのパソコンの `日経先物・オプション分析` フォルダを開き、**中身のファイルとフォルダ全て（`docs`、`scripts`、`.github`フォルダ、など）** をドラッグ＆ドロップでまとめてアップロードします。
   * ※ `.github` などの隠しフォルダが見えない場合は、Windowsエクスプローラーの「表示」タブで「隠しファイル」にチェックを入れてください。
3. アップロード完了後、画面下部の「**Commit changes**」ボタンを押します。

> **【注意点】**  
> GitHubのドラッグ＆ドロップ機能は、大量のファイルには向いていません。ファイル数が多い・フォルダ階層が深い場合はエラーになることがあります。  
> もし上手くいかない場合は、[GitHub Desktop](https://desktop.github.com/)（GUIツール）をインストールし、既存のフォルダをリポジトリとして「Add Local Repository」することで簡単にプッシュ可能です。

### ステップ 3: GitHub Actions（自動処理）の認証許可設定
このプロジェクトでは、Actionsが自動で `data.json` を更新（コミット）します。そのための権限を付与します。

1. GitHubリポジトリ画面上部の「**Settings**（歯車アイコン）」をクリック。
2. 左メニューの `Actions` > `General` をクリック。
3. 最下部の **Workflow permissions** セクションで、
   **「Read and write permissions」** のラジオボタンを選択します。
4. 「**Save**」をクリックします。

### ステップ 4: GitHub Actionsの動作確認（最初のデータ取得）
1. リポジトリ上部の「**Actions**」タブをクリックします。
2. 初回はワークフローの有効化を求められる場合があるので、緑色のボタン（I understand my workflows, go ahead and enable them等）を押します。
3. 左メニューの **「JPX Data Fetch」** をクリックします。
4. 画面右上の「**Run workflow**」ボタンを押し、プルダウンメニューで再度「**Run workflow**」をクリックします。
5. 処理が開始され、緑色のチェックがつけば成功です！（`docs/data.json`が作成・更新されます）

### ステップ 5: GitHub Pagesの公開設定
最後に、スマホやブラウザからどこからでもアクセスできるように公開設定を行います。

1. リポジトリ上部の「**Settings**」タブをクリック。
2. 左メニューから「**Pages**」をクリック。
3. 「**Build and deployment**」セクションの「**Source**」で「**Deploy from a branch**」を選択（デフォルト）。
4. 「**Branch**」のドロップダウンから「**main**」を選択し、その右のフォルダセレクトで「**/docs**」を選択します。（ココが重要です！）
5. 「**Save**」をクリック。
6. 数分待つと、画面上部に**公開URL**（`https://ユーザー名.github.io/リポジトリ名/`）が表示されるのでアクセスして確認します！

---

## 📝 開発者向け: ローカルでの連携 (Git/VS Code利用の場合)
今後、機能のカスタマイズ等のためVS Code連携を行う場合は以下の手順を行います。

1. このフォルダでコマンドプロンプトを開き、Git初期化
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. GitHubと繋ぐ（ユーザー認証が必要です。ポップアップが出ます）
   ```bash
   git branch -M main
   git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
   git push -u origin main
   ```
3. VS Codeの「ソース管理（ブランチアイコン）」タブで、変更箇所を見ながら GUI でコミットやPushが可能になります。
