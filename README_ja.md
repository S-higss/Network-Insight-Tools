# Network-Insight-Tools

English version is [here](/README.md)

## 概要

`Network-Insight-Tools` は，基本的なネットワーク分析と情報収集を行うためのPythonスクリプト集です．ポートスキャンによるサービスの発見や，ドメインの登録情報・DNS情報の調査など，ネットワークの基礎的な振る舞いを理解し，トラブルシューティングやセキュリティ学習に役立てることを目的としています．

## 目的

このリポジトリは，以下の目的のために開発されました．

1.  **ネットワークの可視化**: TCPポートスキャンを通じて，ターゲットホスト上で公開されているサービスを特定する．
2.  **ドメイン情報の収集**: ドメインのWHOIS登録情報や，DNSレコード（IPアドレス，MXレコード，NSレコードなど）を調査する．
3.  **学習と研究**: ネットワークの仕組み，基本的なプロトコル（TCP/IP，DNS，WHOIS），およびセキュリティ防御策（ASLR, SSPなど）の動作原理を実践的に理解するためのサンプルコードを提供する．
4.  **開発環境**: `tcp_server.py` のようなサンプルサーバーを提供することで，`tcp_port_scanner.py` のようなクライアントツールの動作検証を容易にする．

## 機能

* **TCP ポートスキャナー (`tcp_port_scanner.py`)**:
    * 指定したホストのTCPポート範囲をスキャンし，ポートが `OPEN` か `CLOSED` かを判定します．
    * `concurrent.futures.ThreadPoolExecutor` を利用した並行処理により，高速なスキャンが可能です．
    * オープンなポートから受信したデータ（例: サーバーからのウェルカムメッセージ）を表示します．
* **ドメイン情報ツール (`domain_info.py`)**:
    * ユーザーが入力したドメイン名に対し，WHOISクエリを実行して登録情報（レジストラ，登録日，有効期限，ネームサーバーなど）を取得します．
    * NSLOOKUP（DNSクエリ）を実行して，ドメインに関連付けられたIPアドレス（IPv4/IPv6），メールサーバー（MXレコード），およびネームサーバー（NSレコード）を取得します．
* **TCP サンプルサーバー (`tcp_server.py`)**:
    * 複数の指定されたTCPポートでリッスンするシンプルなマルチスレッドサーバーです．
    * `tcp_port_scanner.py` の動作確認や，基本的なTCP通信の挙動調査のためのサンプルとして使用できます．

## ファイル構成

```
.
├── network_insight_tools
|   ├── tcp_server.py
|   ├── tcp_port_scanner.py
|   └── domain_info.py
├── README_ja.md
└── README.md
```

## セットアップ

### 前提条件

* Python 3.6+ がインストールされていること．
* `pip` パッケージマネージャーが利用可能であること．

### 必要なライブラリのインストール

以下のコマンドを実行して，必要なPythonライブラリをインストールしてください．

```bash
pip install python-whois dnspython
```

## 各ツールの使用方法

### 1. TCP サンプルサーバー (`tcp_server.py`)

これは `tcp_port_scanner.py` の動作確認のための補助的なツールです．

1.  **サーバーを起動する:**
    新しいターミナルを開き，以下のコマンドを実行します．
    ```bash
    python3 tcp_server.py
    ```
    サーバーは `127.0.0.1` (localhost) のポート `8000, 8001, 8002, 8080` でリッスンを開始します．
    
    *サーバー出力例:*
    ```
    Starting TCP/IP Server...
    Server listening on 127.0.0.1:8000...
    Server listening on 127.0.0.1:8001...
    ...
    All server threads started. Listening on ports: [8000, 8001, 8002, 8080]
    Press Ctrl+C to stop the server.
    ```
2.  サーバーを停止するには，ターミナルで `Ctrl+C` を押します．

### 2. TCP ポートスキャナー (`tcp_port_scanner.py`)

1.  **クライアントを起動する:**
    サーバーが実行中の状態で，別のターミナルを開き，以下のコマンドを実行します．
    ```bash
    python3 tcp_port_scanner.py
    ```
    
    *クライアント出力例:*
    ```
    Starting TCP Port Scan on 127.0.0.1 from port 7999 to 8081...

    --- Scan Results ---
    Target: 127.0.0.1
    Scanned Ports: 7999-8081

    Open Ports:
      8000: OPEN (Service: Hello from TCP server on port 8000!)
      8001: OPEN (Service: Hello from TCP server on port 8001!)
      8002: OPEN (Service: Hello from TCP server on port 8002!)
      8080: OPEN (Service: Hello from TCP server on port 8080!)

    Closed/Filtered Ports:
      7999: CLOSED (Connection refused)
      8003: CLOSED (Connection refused)
      ... (多くの閉鎖ポート) ...

    Scan complete.
    ```
    *サーバーのターミナルでは，スキャン中に接続ログが表示されます．*

### 3. ドメイン情報ツール (`domain_info.py`)

1.  **ツールを起動する:**
    任意のターミナルで以下のコマンドを実行します．
    ```bash
    python3 domain_info.py
    ```
2.  **ドメイン名を入力する:**
    プロンプトが表示されたら，調査したいドメイン名（例: `google.com`, `example.org`）を入力してEnterキーを押します．
    *終了するには `exit` と入力します．*
    
    *ツール出力例:*
    ```
    --- Domain Information Tool (WHOIS & NSLOOKUP) ---
    This tool fetches registration details and IP addresses for a given domain.

    Enter a domain name (e.g., example.com) or 'exit' to quit: example.com

    Processing domain: example.com

    --- WHOIS Information for example.com ---
    Domain Name: EXAMPLE.COM
    Registrar: IANA
    WHOIS Server: whois.iana.org
    ... (WHOIS登録情報) ...

    --- NSLOOKUP (DNS Information) for example.com ---
    IPv4 Addresses (A records):
      93.184.216.34

    IPv6 Addresses (AAAA records):
      2606:2800:220:1:248:1893:25c8:1946

    Mail Exchange (MX) Records:
      No MX records found.

    Name Server (NS) Records:
      a.iana-servers.net.
      b.iana-servers.net.

    ============================================================
    Enter a domain name (e.g., example.com) or 'exit' to quit: exit
    Exiting tool. Goodbye!
    ```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています．詳細については `LICENSE` ファイルを参照してください．（もし `LICENSE` ファイルを別途作成する場合は，この行を残してください．なければ削除可）
