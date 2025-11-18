# ASP.NET Core appsettings.json 設定ガイド

このドキュメントは、ASP.NET Core の appsettings.json 設定項目の完全なリファレンスガイドです。

## まとめ

このガイドでは、ASP.NET Core アプリケーションの appsettings.json で使用可能なすべての設定項目を、JSONスキーマの definitions セクションの定義順に説明しています。

### 設定のポイント

1. **階層構造**: JSONの階層構造を使用して設定を整理します
2. **環境別設定**: appsettings.Development.json、appsettings.Production.json などで環境別の設定を上書きできます
3. **環境変数**: 環境変数を使用して設定を上書きできます（階層は `__` で区切ります）
4. **機密情報の管理**: 接続文字列やAPIキーなどは User Secrets や Azure Key Vault を使用することを推奨します
5. **スキーマ参照**: 各設定項目には元のJSONスキーマファイルへの参照を記載しています

### 設定カテゴリ別サマリー

- **webOptimizer**: 2設定 (CSS/JavaScript最適化)
- **cdn**: 2設定 (CDN配信)
- **pwa**: 6設定 (Progressive Web App)
- **ElmahIo**: 6設定 (エラーログ)
- **protocols**: 共通定義 (6 enum値)
- **certificate**: 7設定 (証明書)
- **sslProtocols**: 共通定義 (5 enum値)
- **clientCertificateMode**: 共通定義 (3 enum値)
- **kestrel**: 3主要セクション (Webサーバー)
- **logLevelThreshold**: 共通定義 (7 enum値)
- **logLevel**: 共通定義 (ログレベル)
- **logging**: 8プロバイダー (ロギング)
- **allowedHosts**: ホストフィルタリング
- **connectionStrings**: データベース接続
- **NLog**: 14主要設定 (NLogフレームワーク)
- **NLogRulesItem**: 12プロパティ (NLogルール)
- **Serilog**: 11主要設定 + 12サブ定義 (Serilogフレームワーク)

**合計**: 17 definitions、100項目以上の詳細設定

### 参考リンク

- [ASP.NET Core の構成](https://learn.microsoft.com/ja-jp/aspnet/core/fundamentals/configuration/)
- [ASP.NET Core の Kestrel Web サーバー](https://learn.microsoft.com/ja-jp/aspnet/core/fundamentals/servers/kestrel)
- [ASP.NET Core のログ記録](https://learn.microsoft.com/ja-jp/aspnet/core/fundamentals/logging/)
- [NLog Documentation](https://nlog-project.org/)
- [Serilog Documentation](https://serilog.net/)
- [Elmah.io Documentation](https://docs.elmah.io/)

---

## 目次

- [まとめ](#まとめ)
  - [設定のポイント](#設定のポイント)
  - [設定カテゴリ別サマリー](#設定カテゴリ別サマリー)
  - [参考リンク](#参考リンク)
- [1. webOptimizer (Web最適化)](#1-weboptimizer-web最適化)
  - [1.1 enableCaching](#11-enablecaching)
  - [1.2 enableTagHelperBundling](#12-enabletaghelperbundling)
- [2. cdn (CDN設定)](#2-cdn-cdn設定)
  - [2.1 url](#21-url)
  - [2.2 prefetch](#22-prefetch)
- [3. pwa (PWA設定)](#3-pwa-pwa設定)
  - [3.1 cacheId](#31-cacheid)
  - [3.2 offlineRoute](#32-offlineroute)
  - [3.3 registerServiceWorker](#33-registerserviceworker)
  - [3.4 registerWebmanifest](#34-registerwebmanifest)
  - [3.5 routesToPreCache](#35-routestoprecache)
  - [3.6 strategy](#36-strategy)
- [4. ElmahIo (エラーログ設定)](#4-elmahio-エラーログ設定)
  - [4.1 ApiKey (必須)](#41-apikey-必須)
  - [4.2 LogId (必須)](#42-logid-必須)
  - [4.3 Application](#43-application)
  - [4.4 HandledStatusCodesToLog](#44-handledstatuscodestolog)
  - [4.5 TreatLoggingAsBreadcrumbs](#45-treatloggingasbreadcrumbs)
  - [4.6 HeartbeatId](#46-heartbeatid)
- [5. protocols (プロトコル設定)](#5-protocols-プロトコル設定)
- [6. certificate (証明書設定)](#6-certificate-証明書設定)
  - [6.1 Path](#61-path)
  - [6.2 KeyPath](#62-keypath)
  - [6.3 Password](#63-password)
  - [6.4 Subject](#64-subject)
  - [6.5 Store](#65-store)
  - [6.6 Location](#66-location)
  - [6.7 AllowInvalid](#67-allowinvalid)
- [7. sslProtocols (SSL/TLSプロトコル設定)](#7-sslprotocols-ssltlsプロトコル設定)
- [8. clientCertificateMode (クライアント証明書モード)](#8-clientcertificatemode-クライアント証明書モード)
- [9. kestrel (Webサーバー設定)](#9-kestrel-webサーバー設定)
  - [9.1 Endpoints (エンドポイント設定)](#91-endpoints-エンドポイント設定)
    - [9.1.1 Url (必須)](#911-url-必須)
    - [9.1.2 Protocols](#912-protocols)
    - [9.1.3 SslProtocols](#913-sslprotocols)
    - [9.1.4 Certificate](#914-certificate)
    - [9.1.5 ClientCertificateMode](#915-clientcertificatemode)
    - [9.1.6 Sni (Server Name Indication)](#916-sni-server-name-indication)
  - [9.2 EndpointDefaults (エンドポイントデフォルト設定)](#92-endpointdefaults-エンドポイントデフォルト設定)
  - [9.3 Certificates (証明書設定)](#93-certificates-証明書設定)
- [10. logLevelThreshold (ログレベルしきい値)](#10-loglevelthreshold-ログレベルしきい値)
- [11. logLevel (ログレベル設定)](#11-loglevel-ログレベル設定)
- [12. logging (ロギング設定)](#12-logging-ロギング設定)
  - [12.1 LogLevel](#121-loglevel)
  - [12.2 Console (コンソールログプロバイダー)](#122-console-コンソールログプロバイダー)
    - [12.2.1 LogLevel](#1221-loglevel)
    - [12.2.2 FormatterName](#1222-formattername)
    - [12.2.3 FormatterOptions (フォーマッタオプション)](#1223-formatteroptions-フォーマッタオプション)
      - [12.2.3.1 IncludeScopes](#12231-includescopes)
      - [12.2.3.2 TimestampFormat](#12232-timestampformat)
      - [12.2.3.3 UseUtcTimestamp](#12233-useutctimestamp)
    - [12.2.4 LogToStandardErrorThreshold](#1224-logtostandarderrorthreshold)
  - [12.3 EventSource (EventSourceログプロバイダー)](#123-eventsource-eventsourceログプロバイダー)
    - [12.3.1 LogLevel](#1231-loglevel)
  - [12.4 Debug (Debugログプロバイダー)](#124-debug-debugログプロバイダー)
    - [12.4.1 LogLevel](#1241-loglevel)
  - [12.5 EventLog (Windowsイベントログプロバイダー)](#125-eventlog-windowsイベントログプロバイダー)
    - [12.5.1 LogLevel](#1251-loglevel)
  - [12.6 ElmahIo (Elmah.ioログプロバイダー)](#126-elmahio-elmahioログプロバイダー)
    - [12.6.1 LogLevel](#1261-loglevel)
  - [12.7 ElmahIoBreadcrumbs (Elmah.ioパンくずログプロバイダー)](#127-elmahiobreadcrumbs-elmahioパンくずログプロバイダー)
    - [12.7.1 LogLevel](#1271-loglevel)
  - [12.8 additionalProperties (追加のログプロバイダー)](#128-additionalproperties-追加のログプロバイダー)
    - [12.8.1 LogLevel](#1281-loglevel)
- [13. allowedHosts (許可されたホスト)](#13-allowedhosts-許可されたホスト)
- [14. connectionStrings (接続文字列)](#14-connectionstrings-接続文字列)
  - [主要なデータベースの接続文字列](#主要なデータベースの接続文字列)
    - [SQL Server](#sql-server)
    - [PostgreSQL](#postgresql)
    - [MySQL](#mysql)
    - [SQLite](#sqlite)
    - [Oracle](#oracle)
  - [NoSQLデータベース](#nosqlデータベース)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Azure Cosmos DB (SQL API)](#azure-cosmos-db-sql-api)
  - [Entity Framework Core での使用例](#entity-framework-core-での使用例)
  - [セキュリティのベストプラクティス](#セキュリティのベストプラクティス)
  - [環境別設定例](#環境別設定例)
  - [複数の接続文字列](#複数の接続文字列)
  - [接続文字列のテスト](#接続文字列のテスト)
  - [注意事項](#注意事項)
  - [完全な設定例](#完全な設定例)
- [15. NLog (NLogフレームワーク設定)](#15-nlog-nlogフレームワーク設定)
  - [NLogの基本構造](#nlogの基本構造)
  - [15.1 autoReload](#151-autoreload)
  - [15.2 throwConfigExceptions](#152-throwconfigexceptions)
  - [15.3 throwExceptions](#153-throwexceptions)
  - [15.4 internalLogLevel](#154-internalloglevel)
  - [15.5 internalLogFile](#155-internallogfile)
  - [15.6 internalLogToConsole](#156-internallogtoconsole)
  - [15.7 internalLogToConsoleError](#157-internallogtoconsoleerror)
  - [15.8 globalThreshold](#158-globalthreshold)
  - [15.9 autoShutdown](#159-autoshutdown)
  - [15.10 extensions (拡張機能)](#1510-extensions-拡張機能)
    - [15.10.1 assembly](#15101-assembly)
    - [15.10.2 prefix](#15102-prefix)
    - [15.10.3 assemblyFile](#15103-assemblyfile)
  - [15.11 variables (変数)](#1511-variables-変数)
  - [15.12 targetDefaultWrapper (デフォルトラッパー)](#1512-targetdefaultwrapper-デフォルトラッパー)
  - [15.13 targets (ターゲット)](#1513-targets-ターゲット)
    - [15.13.1 async](#15131-async)
  - [15.14 rules (ロギングルール)](#1514-rules-ロギングルール)
- [16. NLogRulesItem (NLogルール項目)](#16-nlogrulesitem-nlogルール項目)
  - [16.1 logger (必須)](#161-logger-必須)
  - [16.2 ruleName](#162-rulename)
  - [16.3 level](#163-level)
  - [16.4 levels](#164-levels)
  - [16.5 minLevel](#165-minlevel)
  - [16.6 maxLevel](#166-maxlevel)
  - [16.7 finalMinLevel](#167-finalminlevel)
  - [16.8 writeTo](#168-writeto)
  - [16.9 final](#169-final)
  - [16.10 enabled](#1610-enabled)
  - [16.11 filters](#1611-filters)
  - [16.12 filterDefaultAction](#1612-filterdefaultaction)
- [17. Serilog (Serilogフレームワーク設定)](#17-serilog-serilogフレームワーク設定)
  - [Serilogの基本構造](#serilogの基本構造)
  - [17.1 Using](#171-using)
  - [17.2 MinimumLevel (最小ログレベル)](#172-minimumlevel-最小ログレベル)
    - [17.2.1 Default](#1721-default)
    - [17.2.2 Override](#1722-override)
  - [17.3 Enrich (エンリッチメント)](#173-enrich-エンリッチメント)
  - [17.4 WriteTo (出力先)](#174-writeto-出力先)
    - [Console Sink (コンソール出力)](#console-sink-コンソール出力)
    - [File Sink (ファイル出力)](#file-sink-ファイル出力)
    - [Seq Sink (Seq出力)](#seq-sink-seq出力)
    - [Elasticsearch Sink](#elasticsearch-sink)
    - [Application Insights Sink](#application-insights-sink)
    - [SQL Server Sink](#sql-server-sink)
  - [17.5 Filter (フィルター)](#175-filter-フィルター)
  - [17.6 Properties (グローバルプロパティ)](#176-properties-グローバルプロパティ)
  - [17.7 Destructure (デストラクチャリング)](#177-destructure-デストラクチャリング)
  - [17.8 LevelSwitch (レベルスイッチ)](#178-levelswitch-レベルスイッチ)
  - [完全なSerilog設定例](#完全なserilog設定例)
  - [Program.cs での Serilog 設定](#programcs-での-serilog-設定)
  - [Serilogの使用例](#serilogの使用例)
  - [構造化ロギングの例](#構造化ロギングの例)
  - [注意事項](#注意事項)

---

## 1. webOptimizer (Web最適化)

CSS/JavaScriptの最適化設定です。`LigerShark.WebOptimizer.Core` パッケージが必要です。

### 1.1 enableCaching

**スキーマ参照**: [appsettings_schema_translated.json:5](appsettings_schema_translated.json#L5)

**説明**: 「キャッシュコントロール」HTTPヘッダーを設定するか、条件付きGET（304）リクエストをサポートする必要があるかどうかを判断します。これは、開発モード中に無効にするのに役立ちます。

**デフォルト値**: 未設定

**環境変数名**: `webOptimizer__enableCaching`

**設定例（appsettings.json）**:
```json
{
  "webOptimizer": {
    "enableCaching": true
  }
}
```

**環境変数での設定**:
```bash
webOptimizer__enableCaching=true
```

**推奨設定**:
- 開発環境: `false` (常に最新ファイルを取得)
- 本番環境: `true` (パフォーマンス向上、帯域幅削減)

**環境別設定例**:

**appsettings.Development.json**:
```json
{
  "webOptimizer": {
    "enableCaching": false
  }
}
```

**appsettings.Production.json**:
```json
{
  "webOptimizer": {
    "enableCaching": true
  }
}
```

---

### 1.2 enableTagHelperBundling

**スキーマ参照**: [appsettings_schema_translated.json:10](appsettings_schema_translated.json#L10)

**説明**: `<script>`および `<link>`要素がバンドルされたパスを指すか、ソースファイルごとの参照を作成する必要があるかどうかを判断します。これは、開発モードのときに無効にするのに役立ちます。

**デフォルト値**: `true`

**環境変数名**: `webOptimizer__enableTagHelperBundling`

**設定例（appsettings.json）**:
```json
{
  "webOptimizer": {
    "enableTagHelperBundling": true
  }
}
```

**環境変数での設定**:
```bash
webOptimizer__enableTagHelperBundling=true
```

**推奨設定**:
- 開発環境: `false` (デバッグしやすい個別ファイル)
- 本番環境: `true` (バンドルでHTTPリクエスト削減、パフォーマンス向上)

**コードでの使用例** (Startup.cs または Program.cs):
```csharp
services.AddWebOptimizer(pipeline =>
{
    pipeline.AddCssBundle("/css/bundle.css", "css/site.css", "css/custom.css");
    pipeline.AddJavaScriptBundle("/js/bundle.js", "js/site.js", "js/custom.js");
    pipeline.MinifyCssFiles();
    pipeline.MinifyJsFiles();
});
```

**Razorビューでの使用**:
```html
<!-- バンドルされたCSS -->
<link rel="stylesheet" href="/css/bundle.css" asp-append-version="true" />

<!-- バンドルされたJavaScript -->
<script src="/js/bundle.js" asp-append-version="true"></script>
```

---

## 2. cdn (CDN設定)

CDN配信の設定です。`WebEssentials.AspNetCore.CdnTagHelpers` パッケージが必要です。

### 2.1 url

**スキーマ参照**: [appsettings_schema_translated.json:24](appsettings_schema_translated.json#L24)

**説明**: 静的リソースのプレフィックスとして使用される絶対URL

**デフォルト値**: 未設定 (空文字列)

**環境変数名**: `cdn__url`

**形式**: `^((//|https?://).+|)$`

**設定例（appsettings.json）**:
```json
{
  "cdn": {
    "url": "https://cdn.example.com"
  }
}
```

**環境変数での設定**:
```bash
cdn__url=https://cdn.example.com
```

**推奨設定**:
- 開発環境: `""` (CDN無効、ローカルファイル使用)
- 本番環境: `"https://cdn.example.com"` (CDN有効)

**Azure CDN使用例**:
```json
{
  "cdn": {
    "url": "https://yourstorageaccount.azureedge.net"
  }
}
```

**CloudFlare使用例**:
```json
{
  "cdn": {
    "url": "https://your-zone.cloudflare.com"
  }
}
```

**環境別設定例**:

**appsettings.Development.json** (CDN無効):
```json
{
  "cdn": {
    "url": ""
  }
}
```

**appsettings.Production.json** (CDN有効):
```json
{
  "cdn": {
    "url": "https://cdn.production.example.com"
  }
}
```

**Razorビューでの使用**:
```html
<!-- CDNタグヘルパーを使用 -->
<link rel="stylesheet" href="~/css/site.css" asp-append-version="true" />
<script src="~/js/site.js" asp-append-version="true"></script>

<!-- 設定したCDN URLがプレフィックスとして追加されます -->
<!-- 出力: <link rel="stylesheet" href="https://cdn.example.com/css/site.css?v=hash" /> -->
```

---

### 2.2 prefetch

**スキーマ参照**: [appsettings_schema_translated.json:29](appsettings_schema_translated.json#L29)

**説明**: trueの場合、dns解像度をcdnに高速化するa <link rel = 'dns-prefetch'>タグを注入します。

**デフォルト値**: `true`

**環境変数名**: `cdn__prefetch`

**設定例（appsettings.json）**:
```json
{
  "cdn": {
    "url": "https://cdn.example.com",
    "prefetch": true
  }
}
```

**環境変数での設定**:
```bash
cdn__prefetch=true
```

**推奨設定**:
- CDN使用時: `true` (DNS解決を事前に実行してパフォーマンス向上)
- CDN未使用時: `false`

**出力されるHTMLタグ例**:
```html
<link rel="dns-prefetch" href="//cdn.example.com">
```

**完全な設定例**:
```json
{
  "cdn": {
    "url": "https://cdn.example.com",
    "prefetch": true
  }
}
```

---

## 3. pwa (PWA設定)

Progressive Web App (PWA) の設定です。サービスワーカー、Webマニフェスト、オフライン対応などを構成します。

### 3.1 cacheId

**スキーマ参照**: [appsettings_schema_translated.json:37](appsettings_schema_translated.json#L37)

**説明**: サービスワーカーのキャッシュ識別子（任意の文字列にすることができます）。このプロパティを変更して、サービスワーカーにブラウザでリロードするように強制します。

**デフォルト値**: `"v1.0"`

**環境変数名**: `pwa__cacheId`

**設定例（appsettings.json）**:
```json
{
  "pwa": {
    "cacheId": "v1.0"
  }
}
```

**環境変数での設定**:
```bash
pwa__cacheId=v1.0
```

**推奨設定**:
- セマンティックバージョニング: `"v1.2.3"` (アプリのバージョンと同期)
- 日付ベース: `"2024-01-15"` (デプロイ日付)
- ビルド番号: `"build-12345"` (CI/CDビルド番号)

**バージョン更新時の動作**:
```json
{
  "pwa": {
    "cacheId": "v2.0"  // バージョン変更でキャッシュがクリアされる
  }
}
```

**注意**: cacheIdを変更すると、すべてのユーザーのブラウザキャッシュが無効化され、新しいキャッシュが作成されます。

---

### 3.2 offlineRoute

**スキーマ参照**: [appsettings_schema_translated.json:42](appsettings_schema_translated.json#L42)

**説明**: オフライン時に表示するページへのルート。

**デフォルト値**: `"/offline.html"`

**環境変数名**: `pwa__offlineRoute`

**設定例（appsettings.json）**:
```json
{
  "pwa": {
    "offlineRoute": "/offline.html"
  }
}
```

**環境変数での設定**:
```bash
pwa__offlineRoute=/offline.html
```

**推奨設定**:
- シンプルな静的ページ: `"/offline.html"`
- MVCビュー: `"/error/offline"`
- カスタムページ: `"/pages/no-connection"`

**オフラインページの例** (wwwroot/offline.html):
```html
<!DOCTYPE html>
<html>
<head>
    <title>オフライン</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
    </style>
</head>
<body>
    <h1>オフラインです</h1>
    <p>インターネット接続を確認してください。</p>
</body>
</html>
```

---

### 3.3 registerServiceWorker

**スキーマ参照**: [appsettings_schema_translated.json:47](appsettings_schema_translated.json#L47)

**説明**: サービスワーカーを登録するスクリプトをHTMLページの下部に注入する必要があるかどうかを判断します。

**デフォルト値**: `true`

**環境変数名**: `pwa__registerServiceWorker`

**設定例（appsettings.json）**:
```json
{
  "pwa": {
    "registerServiceWorker": true
  }
}
```

**環境変数での設定**:
```bash
pwa__registerServiceWorker=true
```

**推奨設定**:
- 開発環境: `false` (デバッグしやすくする)
- 本番環境: `true` (PWA機能を有効化)

**環境別設定例**:

**appsettings.Development.json**:
```json
{
  "pwa": {
    "registerServiceWorker": false
  }
}
```

**appsettings.Production.json**:
```json
{
  "pwa": {
    "registerServiceWorker": true
  }
}
```

**注入されるスクリプト例**:
```html
<script>
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/serviceworker.js')
        .then(reg => console.log('Service Worker registered', reg))
        .catch(err => console.log('Service Worker registration failed', err));
}
</script>
```

---

### 3.4 registerWebmanifest

**スキーマ参照**: [appsettings_schema_translated.json:52](appsettings_schema_translated.json#L52)

**説明**: Webマニフェストを指すメタタグをヘッド要素の端に挿入する必要があるかどうかを判断します。

**デフォルト値**: `true`

**環境変数名**: `pwa__registerWebmanifest`

**設定例（appsettings.json）**:
```json
{
  "pwa": {
    "registerWebmanifest": true
  }
}
```

**環境変数での設定**:
```bash
pwa__registerWebmanifest=true
```

**推奨設定**: PWAとして機能させる場合は常に `true`

**注入されるメタタグ例**:
```html
<link rel="manifest" href="/manifest.json">
```

**manifest.jsonの例** (wwwroot/manifest.json):
```json
{
  "name": "My Application",
  "short_name": "MyApp",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/images/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/images/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

---

### 3.5 routesToPreCache

**スキーマ参照**: [appsettings_schema_translated.json:57](appsettings_schema_translated.json#L57)

**説明**: サービスワーカーがブラウザにインストールされたときに、キャッシュ前のルートのコンマ分離リスト。

**デフォルト値**: `""` (空文字列)

**環境変数名**: `pwa__routesToPreCache`

**形式**: コンマ区切りのルートリスト

**設定例（appsettings.json）**:
```json
{
  "pwa": {
    "routesToPreCache": "/,/about,/contact,/products"
  }
}
```

**環境変数での設定**:
```bash
pwa__routesToPreCache="/,/about,/contact,/products"
```

**推奨設定**:
- よくアクセスされるページのみ: `"/,/about,/contact"`
- 重要な静的コンテンツ: `"/,/css/site.css,/js/site.js"`
- 空: `""` (事前キャッシュなし、オンデマンドキャッシュのみ)

**注意**:
- 多すぎるルートを指定すると初期ロードが遅くなります
- ファイルサイズが大きいページは避ける
- 頻繁に更新されるページは避ける

**完全な設定例**:
```json
{
  "pwa": {
    "routesToPreCache": "/,/about,/services,/css/site.css,/js/site.js,/images/logo.png"
  }
}
```

---

### 3.6 strategy

**スキーマ参照**: [appsettings_schema_translated.json:62](appsettings_schema_translated.json#L62)

**説明**: 事前定義されたサービスワーカータイプの1つを選択します。

**デフォルト値**: `"cacheFirstSafe"`

**環境変数名**: `pwa__strategy`

**設定例（appsettings.json）**:
```json
{
  "pwa": {
    "strategy": "cacheFirstSafe"
  }
}
```

**環境変数での設定**:
```bash
pwa__strategy=cacheFirstSafe
```

**可能な値** (enum):
- `"cacheFirst"`: キャッシュ優先（最速、古いコンテンツの可能性あり）
- `"cacheFirstSafe"`: 安全なキャッシュ優先（推奨）
- `"minimal"`: 最小限のキャッシュ
- `"networkFirst"`: ネットワーク優先（常に最新データを取得）

**戦略の選択ガイド**:

| 戦略 | 動作 | メリット | デメリット | 使用ケース |
|------|------|----------|------------|------------|
| `cacheFirst` | キャッシュから取得、失敗時のみネットワーク | 最速 | 古いデータの可能性 | 静的コンテンツが多いサイト |
| `cacheFirstSafe` | キャッシュ優先、バックグラウンドで更新 | 速度と鮮度のバランス | 複雑な実装 | ほとんどのWebアプリ（推奨） |
| `networkFirst` | ネットワーク優先、失敗時にキャッシュ | 常に最新データ | 遅い、オフライン弱い | 常に最新データが必要なアプリ |
| `minimal` | 最小限のキャッシュ機能のみ | シンプル | オフライン機能限定 | シンプルなPWA |

**推奨設定**: `"cacheFirstSafe"` (バランスが良い)

**完全なPWA設定例**:
```json
{
  "pwa": {
    "cacheId": "myapp-v1.2.3",
    "offlineRoute": "/offline",
    "registerServiceWorker": true,
    "registerWebmanifest": true,
    "routesToPreCache": "/,/about,/products,/contact",
    "strategy": "cacheFirstSafe"
  }
}
```
## 4. ElmahIo (エラーログ設定)

Elmah.io エラーロギングサービスの設定です。`Elmah.Io.AspNetCore` パッケージが必要です。

### 4.1 ApiKey (必須)

**スキーマ参照**: [appsettings_schema_translated.json:77](appsettings_schema_translated.json#L77)

**説明**: メッセージ付きのelmah.io apiキー|書き込み許可

**デフォルト値**: 未設定

**環境変数名**: `ElmahIo__ApiKey`

**形式**: `^([0-9a-f]{32})|(#\\{.*\\}#?)$` (32文字の16進数)

**設定例（appsettings.json）**:
```json
{
  "ElmahIo": {
    "ApiKey": "YOUR_API_KEY_HERE_32_CHARACTERS"
  }
}
```

**環境変数での設定**:
```bash
ElmahIo__ApiKey=YOUR_API_KEY_HERE_32_CHARACTERS
```

**推奨設定**:
- **本番環境**: 環境変数または Azure Key Vault で管理
- **開発環境**: User Secrets で管理

**User Secretsでの設定** (開発環境推奨):
```bash
dotnet user-secrets set "ElmahIo:ApiKey" "YOUR_API_KEY_HERE"
```

**Azure Key Vaultからの取得例**:
```csharp
// Program.cs
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{keyVaultName}.vault.azure.net/"),
    new DefaultAzureCredential());
```

**セキュリティのベストプラクティス**:
- ? User Secrets (開発)
- ? 環境変数 (本番)
- ? Azure Key Vault (推奨)
- ? appsettings.json に直接記載（Git にコミットしない）

---

### 4.2 LogId (必須)

**スキーマ参照**: [appsettings_schema_translated.json:82](appsettings_schema_translated.json#L82)

**説明**: メッセージを保存するためのelmah.ioのIDログ

**デフォルト値**: 未設定

**環境変数名**: `ElmahIo__LogId`

**形式**: `^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})|(#\\{.*\\}#?)$` (GUID)

**設定例（appsettings.json）**:
```json
{
  "ElmahIo": {
    "ApiKey": "YOUR_API_KEY_HERE",
    "LogId": "12345678-1234-1234-1234-123456789abc"
  }
}
```

**環境変数での設定**:
```bash
ElmahIo__LogId=12345678-1234-1234-1234-123456789abc
```

**推奨設定**:
- 環境ごとに異なるLogIdを使用（開発、ステージング、本番）
- Elmah.io ダッシュボードから取得

**環境別設定例**:

**appsettings.Development.json**:
```json
{
  "ElmahIo": {
    "LogId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
  }
}
```

**appsettings.Production.json**:
```json
{
  "ElmahIo": {
    "LogId": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
  }
}
```

---

### 4.3 Application

**スキーマ参照**: [appsettings_schema_translated.json:87](appsettings_schema_translated.json#L87)

**説明**: すべてのエラーメッセージを表示するアプリケーション名

**デフォルト値**: 未設定

**環境変数名**: `ElmahIo__Application`

**設定例（appsettings.json）**:
```json
{
  "ElmahIo": {
    "ApiKey": "YOUR_API_KEY_HERE",
    "LogId": "12345678-1234-1234-1234-123456789abc",
    "Application": "MyWebApp"
  }
}
```

**環境変数での設定**:
```bash
ElmahIo__Application=MyWebApp
```

**推奨設定**:
- アプリケーション名を明確に: `"MyWebApp"`, `"OrderService"`, `"PaymentAPI"`
- 環境を含める: `"MyWebApp-Production"`, `"MyWebApp-Staging"`

**環境別設定例**:
```json
{
  "ElmahIo": {
    "Application": "MyWebApp-Production"
  }
}
```

---

### 4.4 HandledStatusCodesToLog

**スキーマ参照**: [appsettings_schema_translated.json:92](appsettings_schema_translated.json#L92)

**説明**: 例外がスローされていない場合でも、ログを記録するHTTPステータスコードのリスト

**デフォルト値**: `[]` (空配列)

**環境変数名**: `ElmahIo__HandledStatusCodesToLog__0`, `ElmahIo__HandledStatusCodesToLog__1`, ...

**設定例（appsettings.json）**:
```json
{
  "ElmahIo": {
    "HandledStatusCodesToLog": [400, 401, 403, 404, 500, 502, 503]
  }
}
```

**環境変数での設定**:
```bash
ElmahIo__HandledStatusCodesToLog__0=400
ElmahIo__HandledStatusCodesToLog__1=401
ElmahIo__HandledStatusCodesToLog__2=403
ElmahIo__HandledStatusCodesToLog__3=404
```

**推奨設定**:
- **最小限**: `[500, 502, 503]` (サーバーエラーのみ)
- **標準**: `[400, 401, 403, 404, 500, 502, 503]` (クライアントエラー + サーバーエラー)
- **詳細**: `[400, 401, 403, 404, 405, 408, 429, 500, 502, 503, 504]` (すべての主要エラー)

**HTTPステータスコード解説**:
- `400`: Bad Request (不正なリクエスト)
- `401`: Unauthorized (認証エラー)
- `403`: Forbidden (権限エラー)
- `404`: Not Found (ページが見つからない)
- `500`: Internal Server Error (サーバー内部エラー)
- `502`: Bad Gateway (ゲートウェイエラー)
- `503`: Service Unavailable (サービス利用不可)

---

### 4.5 TreatLoggingAsBreadcrumbs

**スキーマ参照**: [appsettings_schema_translated.json:99](appsettings_schema_translated.json#L99)

**説明**: microsoft.extensions.loggingからのログメッセージをパン粉として含めます

**デフォルト値**: `false`

**環境変数名**: `ElmahIo__TreatLoggingAsBreadcrumbs`

**設定例（appsettings.json）**:
```json
{
  "ElmahIo": {
    "TreatLoggingAsBreadcrumbs": true
  }
}
```

**環境変数での設定**:
```bash
ElmahIo__TreatLoggingAsBreadcrumbs=true
```

**推奨設定**:
- **有効** (`true`): エラー前のログメッセージをパンくずとして記録（デバッグしやすい）
- **無効** (`false`): ログ量を削減

**パンくず（Breadcrumbs）とは**:
エラーが発生する前のアプリケーションの動作履歴を追跡する機能です。エラーの原因を特定しやすくなります。

**例**:
```csharp
_logger.LogInformation("User attempting to login");
_logger.LogInformation("Validating credentials");
_logger.LogError("Login failed: Invalid password");
```

`TreatLoggingAsBreadcrumbs: true` の場合、エラー発生時に上記のすべてのログがElmah.ioに記録されます。

---

### 4.6 HeartbeatId

**スキーマ参照**: [appsettings_schema_translated.json:104](appsettings_schema_translated.json#L104)

**説明**: 通知するElmah.io HeartbeatのID

**デフォルト値**: 未設定

**環境変数名**: `ElmahIo__HeartbeatId`

**形式**: `^([0-9a-f]{32})|(#\\{.*\\}#?)$` (32文字の16進数)

**設定例（appsettings.json）**:
```json
{
  "ElmahIo": {
    "ApiKey": "YOUR_API_KEY_HERE",
    "LogId": "12345678-1234-1234-1234-123456789abc",
    "HeartbeatId": "abcdef0123456789abcdef0123456789"
  }
}
```

**環境変数での設定**:
```bash
ElmahIo__HeartbeatId=abcdef0123456789abcdef0123456789
```

**推奨設定**:
- アプリケーションの死活監視が必要な場合に設定
- Elmah.io Heartbeat 機能を使用する場合のみ

**Heartbeat機能とは**:
定期的に「生存している」ことをElmah.ioに通知する機能です。通知が途絶えるとアラートが発生します。

**コードでの使用例**:
```csharp
// Program.cs または Startup.cs
services.AddElmahIo(options =>
{
    options.ApiKey = Configuration["ElmahIo:ApiKey"];
    options.LogId = new Guid(Configuration["ElmahIo:LogId"]);
    options.HeartbeatId = Configuration["ElmahIo:HeartbeatId"];
});
```

---

**完全なElmah.io設定例**:
```json
{
  "ElmahIo": {
    "ApiKey": "YOUR_API_KEY_HERE_32_CHARACTERS",
    "LogId": "12345678-1234-1234-1234-123456789abc",
    "Application": "MyWebApp-Production",
    "HandledStatusCodesToLog": [400, 401, 403, 404, 500, 502, 503],
    "TreatLoggingAsBreadcrumbs": true,
    "HeartbeatId": "abcdef0123456789abcdef0123456789"
  }
}
```

---

## 5. protocols (プロトコル設定)

**スキーマ参照**: [appsettings_schema_translated.json:109](appsettings_schema_translated.json#L109)

**説明**: エンドポイントでプロトコルが有効になっています

**type**: string (enum)

**使用場所**:
- `Kestrel.Endpoints.<name>.Protocols`
- `Kestrel.Endpoints.<name>.Sni.<hostname>.Protocols`
- `Kestrel.EndpointDefaults.Protocols`

**可能な値**:
- `"None"`: プロトコルなし
- `"Http1"`: HTTP/1.1 のみ
- `"Http2"`: HTTP/2 のみ
- `"Http1AndHttp2"`: HTTP/1.1 と HTTP/2 の両方（デフォルト）
- `"Http3"`: HTTP/3 のみ
- `"Http1AndHttp2AndHttp3"`: HTTP/1.1、HTTP/2、HTTP/3 のすべて

**デフォルト値**: `"Http1AndHttp2"`

**環境変数名**: `Kestrel__EndpointDefaults__Protocols`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "EndpointDefaults": {
      "Protocols": "Http1AndHttp2"
    }
  }
}
```

**環境変数での設定**:
```bash
Kestrel__EndpointDefaults__Protocols=Http1AndHttp2
```

**推奨設定**:

| シナリオ | 推奨値 | 理由 |
|---------|--------|------|
| 標準Webアプリ | `Http1AndHttp2` | ほとんどのブラウザで動作 |
| gRPCサービス | `Http2` | gRPC は HTTP/2 が必須 |
| レガシーブラウザ対応 | `Http1` | 古いブラウザのサポート |
| 最新技術採用 | `Http1AndHttp2AndHttp3` | 最高のパフォーマンス |

**エンドポイント別設定例**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000",
        "Protocols": "Http1AndHttp2"
      },
      "Https": {
        "Url": "https://localhost:5001",
        "Protocols": "Http1AndHttp2"
      },
      "gRPC": {
        "Url": "https://localhost:5002",
        "Protocols": "Http2"
      }
    }
  }
}
```

---

## 6. certificate (証明書設定)

**スキーマ参照**: [appsettings_schema_translated.json:121](appsettings_schema_translated.json#L121)

**説明**: HTTPS エンドポイントで使用する証明書の設定

**使用場所**:
- `Kestrel.Endpoints.<name>.Certificate`
- `Kestrel.Endpoints.<name>.Sni.<hostname>.Certificate`
- `Kestrel.Certificates.<name>`

### 6.1 Path

**スキーマ参照**: [appsettings_schema_translated.json:126](appsettings_schema_translated.json#L126)

**説明**: 証明書ファイルパス (.pfx または .crt)

**デフォルト値**: 未設定

**環境変数名**: `Kestrel__Certificates__Default__Path`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Certificates": {
      "Default": {
        "Path": "certs/certificate.pfx",
        "Password": "your-password"
      }
    }
  }
}
```

**環境変数での設定**:
```bash
Kestrel__Certificates__Default__Path=certs/certificate.pfx
Kestrel__Certificates__Default__Password=your-password
```

**推奨設定**:
- **開発環境**: `dotnet dev-certs https` で生成した証明書
- **本番環境**: Let's Encrypt または有料SSL証明書

---

### 6.2 KeyPath

**スキーマ参照**: [appsettings_schema_translated.json:131](appsettings_schema_translated.json#L131)

**説明**: 証明書キーファイルパス (.key) - .NET 5以降

**デフォルト値**: 未設定

**環境変数名**: `Kestrel__Certificates__Default__KeyPath`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Certificates": {
      "Default": {
        "Path": "certs/certificate.crt",
        "KeyPath": "certs/private.key"
      }
    }
  }
}
```

**使用ケース**:
- PEMフォーマットの証明書 (.crt + .key)
- Let's Encrypt証明書

---

### 6.3 Password

**スキーマ参照**: [appsettings_schema_translated.json:136](appsettings_schema_translated.json#L136)

**説明**: 秘密鍵にアクセスするために使用される証明書パスワード

**デフォルト値**: 未設定

**環境変数名**: `Kestrel__Certificates__Default__Password`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Certificates": {
      "Default": {
        "Path": "certificate.pfx",
        "Password": "your-secure-password"
      }
    }
  }
}
```

**環境変数での設定**:
```bash
Kestrel__Certificates__Default__Password=your-secure-password
```

**セキュリティのベストプラクティス**:
- ? 環境変数で管理
- ? Azure Key Vault で管理
- ? User Secrets (開発環境)
- ? appsettings.json に直接記載

---

### 6.4 Subject

**スキーマ参照**: [appsettings_schema_translated.json:141](appsettings_schema_translated.json#L141)

**説明**: 証明書の件名（証明書ストアから読み込む場合）

**デフォルト値**: 未設定

**環境変数名**: `Kestrel__Certificates__Default__Subject`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Certificates": {
      "Default": {
        "Subject": "CN=example.com",
        "Store": "My",
        "Location": "CurrentUser"
      }
    }
  }
}
```

**使用ケース**:
- Windows証明書ストアから証明書を読み込む

---

### 6.5 Store

**スキーマ参照**: [appsettings_schema_translated.json:146](appsettings_schema_translated.json#L146)

**説明**: 証明書ストア名

**デフォルト値**: `"My"`

**環境変数名**: `Kestrel__Certificates__Default__Store`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Certificates": {
      "Default": {
        "Subject": "CN=localhost",
        "Store": "My",
        "Location": "CurrentUser"
      }
    }
  }
}
```

**一般的なストア名**:
- `"My"`: 個人用ストア（デフォルト）
- `"Root"`: ルート証明機関ストア
- `"CA"`: 中間証明機関ストア

---

### 6.6 Location

**スキーマ参照**: [appsettings_schema_translated.json:151](appsettings_schema_translated.json#L151)

**説明**: 証明書ストアの場所

**デフォルト値**: `"CurrentUser"`

**環境変数名**: `Kestrel__Certificates__Default__Location`

**可能な値**:
- `"CurrentUser"`: 現在のユーザー（デフォルト）
- `"LocalMachine"`: ローカルマシン（管理者権限が必要）

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Certificates": {
      "Default": {
        "Subject": "CN=localhost",
        "Store": "My",
        "Location": "CurrentUser"
      }
    }
  }
}
```

**推奨設定**:
- **開発環境**: `CurrentUser`
- **本番環境（Windows Service）**: `LocalMachine`

---

### 6.7 AllowInvalid

**スキーマ参照**: [appsettings_schema_translated.json:159](appsettings_schema_translated.json#L159)

**説明**: 無効と見なされる証明書を読み込むかどうかを示す値

**デフォルト値**: `false`

**環境変数名**: `Kestrel__Certificates__Default__AllowInvalid`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Certificates": {
      "Default": {
        "Path": "certificate.pfx",
        "Password": "password",
        "AllowInvalid": true
      }
    }
  }
}
```

**推奨設定**:
- **開発環境**: `true` (自己署名証明書を使用可能)
- **本番環境**: `false` (常に有効な証明書を使用)

**警告**: 本番環境で `true` にしないでください。セキュリティリスクがあります。

---

**完全な証明書設定例**:

**ファイルから読み込む場合** (.pfx):
```json
{
  "Kestrel": {
    "Endpoints": {
      "Https": {
        "Url": "https://localhost:5001",
        "Certificate": {
          "Path": "certs/certificate.pfx",
          "Password": "your-password"
        }
      }
    }
  }
}
```

**PEMフォーマットの場合** (.NET 5以降):
```json
{
  "Kestrel": {
    "Endpoints": {
      "Https": {
        "Url": "https://localhost:5001",
        "Certificate": {
          "Path": "certs/certificate.crt",
          "KeyPath": "certs/private.key"
        }
      }
    }
  }
}
```

**証明書ストアから読み込む場合**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Https": {
        "Url": "https://localhost:5001",
        "Certificate": {
          "Subject": "CN=localhost",
          "Store": "My",
          "Location": "CurrentUser",
          "AllowInvalid": false
        }
      }
    }
  }
}
```

---

## 7. sslProtocols (SSL/TLSプロトコル設定)

**スキーマ参照**: [appsettings_schema_translated.json:165](appsettings_schema_translated.json#L165)

**説明**: 許容SSLプロトコルを指定します。デフォルトは「なし」であり、オペレーティングシステムが使用するのに最適なプロトコルを選択し、安全でないプロトコルをブロックすることができます。(.NET 5以降)

**type**: array of enum

**使用場所**:
- `Kestrel.Endpoints.<name>.SslProtocols`
- `Kestrel.Endpoints.<name>.Sni.<hostname>.SslProtocols`
- `Kestrel.EndpointDefaults.SslProtocols`

**可能な値** (items):
- `"None"`: OSのデフォルト設定を使用（推奨）
- `"Tls"`: TLS 1.0（非推奨、脆弱性あり）
- `"Tls11"`: TLS 1.1（非推奨、脆弱性あり）
- `"Tls12"`: TLS 1.2（推奨）
- `"Tls13"`: TLS 1.3（最新、推奨）

**デフォルト値**: `["None"]` (OSのデフォルト)

**環境変数名**: `Kestrel__EndpointDefaults__SslProtocols__0`, `Kestrel__EndpointDefaults__SslProtocols__1`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "EndpointDefaults": {
      "SslProtocols": ["Tls12", "Tls13"]
    }
  }
}
```

**環境変数での設定**:
```bash
Kestrel__EndpointDefaults__SslProtocols__0=Tls12
Kestrel__EndpointDefaults__SslProtocols__1=Tls13
```

**推奨設定**:

| 環境 | 推奨値 | 理由 |
|------|--------|------|
| 最新環境 | `["None"]` | OSに任せる（推奨） |
| セキュリティ重視 | `["Tls12", "Tls13"]` | 最新プロトコルのみ |
| 互換性重視 | `["Tls", "Tls11", "Tls12", "Tls13"]` | 古いクライアント対応（非推奨） |
| 本番環境 | `["Tls12", "Tls13"]` | バランスが良い |

**セキュリティガイド**:
- ? TLS 1.2以上のみを使用
- ? 可能な限りTLS 1.3を有効化
- ? TLS 1.0/1.1は脆弱性があるため使用しない
- ? SSL 2.0/3.0は完全に廃止されている

**完全な設定例**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Https": {
        "Url": "https://localhost:5001",
        "Protocols": "Http1AndHttp2",
        "SslProtocols": ["Tls12", "Tls13"],
        "Certificate": {
          "Path": "certificate.pfx",
          "Password": "your-password"
        }
      }
    }
  }
}
```

**注意**:
- TLS 1.0/1.1は2020年に主要ブラウザでサポート終了
- PCI DSS 準拠にはTLS 1.2以上が必須
- 政府機関や金融機関ではTLS 1.3の使用を推奨
## 8. clientCertificateMode (クライアント証明書モード)

**スキーマ参照**: [appsettings_schema_translated.json:177](appsettings_schema_translated.json#L177)

**説明**: HTTPS接続のクライアント証明書要件を指定します (.NET 5以降)

**type**: string (enum)

**使用場所**:
- `Kestrel.Endpoints.<name>.ClientCertificateMode`
- `Kestrel.Endpoints.<name>.Sni.<hostname>.ClientCertificateMode`
- `Kestrel.EndpointDefaults.ClientCertificateMode`

**可能な値**:
- `"NoCertificate"`: クライアント証明書不要（デフォルト）
- `"AllowCertificate"`: クライアント証明書を許可（オプション）
- `"RequireCertificate"`: クライアント証明書を必須

**デフォルト値**: `"NoCertificate"`

**環境変数名**: `Kestrel__EndpointDefaults__ClientCertificateMode`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "EndpointDefaults": {
      "ClientCertificateMode": "NoCertificate"
    }
  }
}
```

**環境変数での設定**:
```bash
Kestrel__EndpointDefaults__ClientCertificateMode=NoCertificate
```

**推奨設定**:

| シナリオ | 推奨値 | 理由 |
|---------|--------|------|
| 標準Webアプリ | `NoCertificate` | 通常は不要 |
| 相互TLS認証API | `RequireCertificate` | セキュリティ強化 |
| オプション認証 | `AllowCertificate` | 柔軟性 |
| 企業内部システム | `RequireCertificate` | 強固な認証 |

**相互TLS（mTLS）設定例**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "HttpsWithMutualTls": {
        "Url": "https://localhost:5001",
        "ClientCertificateMode": "RequireCertificate",
        "Certificate": {
          "Path": "server-certificate.pfx",
          "Password": "your-password"
        }
      }
    }
  }
}
```

**コードでの証明書検証例** (Program.cs):
```csharp
builder.Services.AddCertificateForwarding(options =>
{
    options.CertificateHeader = "X-SSL-CERT";
});

var app = builder.Build();

app.UseCertificateForwarding();
app.UseAuthentication();
app.UseAuthorization();
```

**クライアント証明書の検証例**:
```csharp
// Startup.cs または Program.cs
services.AddAuthentication(CertificateAuthenticationDefaults.AuthenticationScheme)
    .AddCertificate(options =>
    {
        options.AllowedCertificateTypes = CertificateTypes.All;
        options.Events = new CertificateAuthenticationEvents
        {
            OnCertificateValidated = context =>
            {
                // カスタム検証ロジック
                var claims = new[]
                {
                    new Claim(ClaimTypes.NameIdentifier,
                        context.ClientCertificate.Subject,
                        ClaimValueTypes.String,
                        context.Options.ClaimsIssuer),
                    new Claim(ClaimTypes.Name,
                        context.ClientCertificate.Subject,
                        ClaimValueTypes.String,
                        context.Options.ClaimsIssuer)
                };

                context.Principal = new ClaimsPrincipal(
                    new ClaimsIdentity(claims, context.Scheme.Name));
                context.Success();

                return Task.CompletedTask;
            }
        };
    });
```

**注意**:
- `RequireCertificate` を使用する場合、クライアントは有効な証明書を提供する必要があります
- Azure App Service や IIS では追加の構成が必要です
- ロードバランサー経由の場合、証明書転送の設定が必要です

---

## 9. kestrel (Webサーバー設定)

**スキーマ参照**: [appsettings_schema_translated.json:185](appsettings_schema_translated.json#L185)

**説明**: ASP.NETコアケストレルサーバー構成。Kestrelは、ASP.NET Core のクロスプラットフォーム Web サーバーです。

### 9.1 Endpoints (エンドポイント設定)

**スキーマ参照**: [appsettings_schema_translated.json:190](appsettings_schema_translated.json#L190)

**説明**: ケストレルがネットワークリクエストのために耳を傾けるエンドポイント。各エンドポイントには、JSONプロパティ名で指定された名前があります。

**環境変数名パターン**: `Kestrel__Endpoints__<EndpointName>__<Property>`

#### 9.1.1 Url (必須)

**スキーマ参照**: [appsettings_schema_translated.json:198](appsettings_schema_translated.json#L198)

**説明**: スキーム、ホスト名、およびポートエンドポイントが聞こえます

**形式**: `<scheme>://<hostname>:<port>`

**環境変数名**: `Kestrel__Endpoints__<EndpointName>__Url`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      },
      "Https": {
        "Url": "https://localhost:5001"
      }
    }
  }
}
```

**環境変数での設定**:
```bash
Kestrel__Endpoints__Http__Url=http://localhost:5000
Kestrel__Endpoints__Https__Url=https://localhost:5001
```

**URLパターン例**:
- `http://localhost:5000`: ローカルホストHTTP
- `https://localhost:5001`: ローカルホストHTTPS
- `http://0.0.0.0:80`: すべてのIPアドレスでHTTP
- `https://0.0.0.0:443`: すべてのIPアドレスでHTTPS
- `http://+:5000`: すべてのホスト名でHTTP
- `http://*:5000`: すべてのホスト名でHTTP（Windows HTTP.sys）

**推奨設定**:

**開発環境**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      },
      "Https": {
        "Url": "https://localhost:5001"
      }
    }
  }
}
```

**本番環境（Dockerコンテナ）**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://0.0.0.0:80"
      }
    }
  }
}
```

**本番環境（リバースプロキシ背後）**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      }
    }
  }
}
```

#### 9.1.2 Protocols

**スキーマ参照**: [appsettings_schema_translated.json:203](appsettings_schema_translated.json#L203)

**説明**: エンドポイントで有効にするプロトコル

**$ref**: `#/definitions/protocols` (詳細は「5. protocols」を参照)

**環境変数名**: `Kestrel__Endpoints__<EndpointName>__Protocols`

#### 9.1.3 SslProtocols

**スキーマ参照**: [appsettings_schema_translated.json:206](appsettings_schema_translated.json#L206)

**説明**: 許容SSLプロトコル

**$ref**: `#/definitions/sslProtocols` (詳細は「7. sslProtocols」を参照)

**環境変数名**: `Kestrel__Endpoints__<EndpointName>__SslProtocols__0`, `Kestrel__Endpoints__<EndpointName>__SslProtocols__1`

#### 9.1.4 Certificate

**スキーマ参照**: [appsettings_schema_translated.json:209](appsettings_schema_translated.json#L209)

**説明**: HTTPS エンドポイントで使用する証明書

**$ref**: `#/definitions/certificate` (詳細は「6. certificate」を参照)

**環境変数名パターン**: `Kestrel__Endpoints__<EndpointName>__Certificate__<Property>`

#### 9.1.5 ClientCertificateMode

**スキーマ参照**: [appsettings_schema_translated.json:212](appsettings_schema_translated.json#L212)

**説明**: HTTPS接続のクライアント証明書要件

**$ref**: `#/definitions/clientCertificateMode` (詳細は「8. clientCertificateMode」を参照)

**環境変数名**: `Kestrel__Endpoints__<EndpointName>__ClientCertificateMode`

#### 9.1.6 Sni (Server Name Indication)

**スキーマ参照**: [appsettings_schema_translated.json:215](appsettings_schema_translated.json#L215)

**説明**: サーバー名表示（SNI）構成 (.NET 5以降)。複数のドメイン名に対して異なる証明書を使用できます。

**環境変数名パターン**: `Kestrel__Endpoints__<EndpointName>__Sni__<Hostname>__<Property>`

**SNI設定例**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Https": {
        "Url": "https://*:5001",
        "Sni": {
          "example.com": {
            "Protocols": "Http1AndHttp2",
            "Certificate": {
              "Path": "certs/example.com.pfx",
              "Password": "password1"
            }
          },
          "another.com": {
            "Protocols": "Http1AndHttp2",
            "Certificate": {
              "Path": "certs/another.com.pfx",
              "Password": "password2"
            }
          }
        }
      }
    }
  }
}
```

**完全なエンドポイント設定例**:
```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      },
      "Https": {
        "Url": "https://localhost:5001",
        "Protocols": "Http1AndHttp2",
        "SslProtocols": ["Tls12", "Tls13"],
        "Certificate": {
          "Path": "certificate.pfx",
          "Password": "your-password"
        },
        "ClientCertificateMode": "NoCertificate"
      },
      "gRPC": {
        "Url": "https://localhost:5002",
        "Protocols": "Http2",
        "Certificate": {
          "Path": "certificate.pfx",
          "Password": "your-password"
        }
      }
    }
  }
}
```

---

### 9.2 EndpointDefaults (エンドポイントデフォルト設定)

**スキーマ参照**: [appsettings_schema_translated.json:250](appsettings_schema_translated.json#L250)

**説明**: すべてのエンドポイントに適用されるデフォルトの構成。名前付きエンドポイント固有の構成はデフォルトをオーバーライドします。

**環境変数名パターン**: `Kestrel__EndpointDefaults__<Property>`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "EndpointDefaults": {
      "Protocols": "Http1AndHttp2",
      "SslProtocols": ["Tls12", "Tls13"],
      "ClientCertificateMode": "NoCertificate"
    },
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      },
      "Https": {
        "Url": "https://localhost:5001",
        "Certificate": {
          "Path": "certificate.pfx",
          "Password": "your-password"
        }
      }
    }
  }
}
```

**環境変数での設定**:
```bash
Kestrel__EndpointDefaults__Protocols=Http1AndHttp2
Kestrel__EndpointDefaults__SslProtocols__0=Tls12
Kestrel__EndpointDefaults__SslProtocols__1=Tls13
Kestrel__EndpointDefaults__ClientCertificateMode=NoCertificate
```

**推奨設定**:
```json
{
  "Kestrel": {
    "EndpointDefaults": {
      "Protocols": "Http1AndHttp2",
      "SslProtocols": ["Tls12", "Tls13"]
    }
  }
}
```

---

### 9.3 Certificates (証明書設定)

**スキーマ参照**: [appsettings_schema_translated.json:269](appsettings_schema_translated.json#L269)

**説明**: KestrelがHTTPSエンドポイントで使用する証明書。各証明書には、JSONプロパティ名で指定された名前があります。

**環境変数名パターン**: `Kestrel__Certificates__<CertificateName>__<Property>`

**設定例（appsettings.json）**:
```json
{
  "Kestrel": {
    "Certificates": {
      "Default": {
        "Path": "certs/default.pfx",
        "Password": "password1"
      },
      "Example": {
        "Path": "certs/example.com.pfx",
        "Password": "password2"
      }
    },
    "Endpoints": {
      "Https": {
        "Url": "https://localhost:5001",
        "Certificate": {
          "Path": "certs/default.pfx",
          "Password": "password1"
        }
      }
    }
  }
}
```

**環境変数での設定**:
```bash
Kestrel__Certificates__Default__Path=certs/default.pfx
Kestrel__Certificates__Default__Password=password1
```

---

## 10. logLevelThreshold (ログレベルしきい値)

**スキーマ参照**: [appsettings_schema_translated.json:278](appsettings_schema_translated.json#L278)

**説明**: ログレベルのしきい値

**type**: string (enum)

**使用場所**:
- `Logging.LogLevel.<Category>`
- `Logging.Console.LogToStandardErrorThreshold`

**可能な値**:
- `"Trace"`: 最も詳細な情報（デバッグ用、すべてを記録）
- `"Debug"`: デバッグ情報
- `"Information"`: 一般的な情報メッセージ
- `"Warning"`: 警告メッセージ（問題の可能性）
- `"Error"`: エラーメッセージ（処理の失敗）
- `"Critical"`: クリティカルなエラー（システムクラッシュ）
- `"None"`: ログを無効化

**環境変数名**: `Logging__LogLevel__<Category>`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Information"
    }
  }
}
```

**環境変数での設定**:
```bash
Logging__LogLevel__Default=Information
Logging__LogLevel__Microsoft=Warning
Logging__LogLevel__Microsoft.AspNetCore=Warning
```

**ログレベル詳細**:

| レベル | 説明 | 使用例 | 本番環境 | 開発環境 |
|--------|------|--------|----------|----------|
| `Trace` | 最も詳細 | 変数の値、ループの反復 | ? | ? |
| `Debug` | デバッグ情報 | メソッドの呼び出し、パラメータ | ? | ? |
| `Information` | 一般情報 | リクエスト受信、処理完了 | ? | ? |
| `Warning` | 警告 | リトライ、非推奨機能 | ? | ? |
| `Error` | エラー | 例外、処理失敗 | ? | ? |
| `Critical` | 致命的 | システムクラッシュ | ? | ? |
| `None` | 無効 | ログ出力なし | ? | ? |

**推奨設定**:

**開発環境** (appsettings.Development.json):
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft": "Information",
      "Microsoft.AspNetCore": "Information",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  }
}
```

**本番環境** (appsettings.Production.json):
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft": "Warning",
      "Microsoft.AspNetCore": "Warning",
      "YourApp": "Information"
    }
  }
}
```

**カテゴリ別設定例**:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.AspNetCore.Hosting": "Information",
      "Microsoft.AspNetCore.Routing": "Warning",
      "Microsoft.EntityFrameworkCore": "Information",
      "Microsoft.EntityFrameworkCore.Database.Command": "Warning",
      "System": "Warning",
      "YourApp.Controllers": "Debug",
      "YourApp.Services": "Information"
    }
  }
}
```

**コードでの使用例**:
```csharp
public class MyService
{
    private readonly ILogger<MyService> _logger;

    public MyService(ILogger<MyService> logger)
    {
        _logger = logger;
    }

    public void DoWork()
    {
        _logger.LogTrace("Trace: 変数 x = {X}", 123);
        _logger.LogDebug("Debug: メソッド DoWork が呼ばれました");
        _logger.LogInformation("Information: 処理を開始します");
        _logger.LogWarning("Warning: 古いAPIを使用しています");
        _logger.LogError("Error: 処理に失敗しました");
        _logger.LogCritical("Critical: システムクラッシュ");
    }
}
```
## 11. logLevel (ログレベル設定)

**スキーマ参照**: [appsettings_schema_translated.json:291](appsettings_schema_translated.json#L291)

**説明**: ログを作成するときに使用されるログレベルの構成。カテゴリごとにログレベルを設定できます。

**type**: object

**additionalProperties**: `$ref: #/definitions/logLevelThreshold` (詳細は「10. logLevelThreshold」を参照)

**使用場所**:
- `Logging.LogLevel`
- `Logging.Console.LogLevel`
- `Logging.EventSource.LogLevel`
- `Logging.Debug.LogLevel`
- `Logging.EventLog.LogLevel`
- `Logging.ElmahIo.LogLevel`
- `Logging.ElmahIoBreadcrumbs.LogLevel`
- `Logging.<Provider>.LogLevel`

**環境変数名パターン**: `Logging__LogLevel__<Category>`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

**カテゴリの概念**:
カテゴリは通常、ログを出力するクラスの完全修飾名です。カテゴリを使用することで、特定の名前空間やクラスのログレベルを個別に制御できます。

**カテゴリの階層例**:
```
MyApp
├── MyApp.Controllers
│   ├── MyApp.Controllers.HomeController
│   └── MyApp.Controllers.UserController
├── MyApp.Services
│   ├── MyApp.Services.EmailService
│   └── MyApp.Services.PaymentService
└── MyApp.Data
    └── MyApp.Data.ApplicationDbContext
```

**階層的なログレベル設定例**:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "MyApp": "Debug",
      "MyApp.Controllers": "Information",
      "MyApp.Controllers.UserController": "Trace",
      "MyApp.Services": "Warning",
      "MyApp.Data": "Information"
    }
  }
}
```

**主要なMicrosoftカテゴリ**:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",

      // ASP.NET Core全般
      "Microsoft": "Warning",
      "Microsoft.AspNetCore": "Warning",

      // ホスティング関連
      "Microsoft.Hosting.Lifetime": "Information",

      // ルーティング
      "Microsoft.AspNetCore.Routing": "Warning",
      "Microsoft.AspNetCore.Routing.EndpointMiddleware": "Information",

      // 認証・認可
      "Microsoft.AspNetCore.Authentication": "Information",
      "Microsoft.AspNetCore.Authorization": "Information",

      // Entity Framework Core
      "Microsoft.EntityFrameworkCore": "Information",
      "Microsoft.EntityFrameworkCore.Database.Command": "Warning",
      "Microsoft.EntityFrameworkCore.Infrastructure": "Warning",
      "Microsoft.EntityFrameworkCore.Migrations": "Information",

      // HTTP Client
      "System.Net.Http.HttpClient": "Warning",

      // その他のSystem
      "System": "Warning"
    }
  }
}
```

**環境別設定の完全例**:

**appsettings.json** (共通):
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  }
}
```

**appsettings.Development.json** (開発環境):
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft": "Information",
      "Microsoft.AspNetCore": "Information",
      "Microsoft.EntityFrameworkCore.Database.Command": "Information",
      "MyApp": "Trace"
    }
  }
}
```

**appsettings.Production.json** (本番環境):
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft": "Error",
      "Microsoft.AspNetCore": "Error",
      "Microsoft.Hosting.Lifetime": "Information",
      "MyApp": "Information",
      "MyApp.Controllers": "Warning",
      "MyApp.Services.CriticalService": "Information"
    }
  }
}
```

---

## 12. logging (ロギング設定)

**スキーマ参照**: [appsettings_schema_translated.json:298](appsettings_schema_translated.json#L298)

**説明**: microsoft.extensions.loggingの構成。ASP.NET Core のロギングシステム全体の設定です。

**使用場所**: `Logging`

### 12.1 LogLevel

**スキーマ参照**: [appsettings_schema_translated.json:303](appsettings_schema_translated.json#L303)

**$ref**: `#/definitions/logLevel` (詳細は「11. logLevel」を参照)

**環境変数名パターン**: `Logging__LogLevel__<Category>`

---

### 12.2 Console (コンソールログプロバイダー)

**スキーマ参照**: [appsettings_schema_translated.json:306](appsettings_schema_translated.json#L306)

**説明**: コンソールログプロバイダーの構成。標準出力（stdout）またはエラー出力（stderr）にログを出力します。

#### 12.2.1 LogLevel

**スキーマ参照**: [appsettings_schema_translated.json:311](appsettings_schema_translated.json#L311)

**$ref**: `#/definitions/logLevel`

**環境変数名パターン**: `Logging__Console__LogLevel__<Category>`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "Console": {
      "LogLevel": {
        "Default": "Information",
        "Microsoft": "Warning"
      }
    }
  }
}
```

#### 12.2.2 FormatterName

**スキーマ参照**: [appsettings_schema_translated.json:314](appsettings_schema_translated.json#L314)

**説明**: 使用するログメッセージフォーマッタの名前

**デフォルト値**: `"simple"`

**環境変数名**: `Logging__Console__FormatterName`

**可能な値**:
- `"simple"`: シンプルなテキストフォーマット（デフォルト）
- `"systemd"`: systemd形式
- `"json"`: JSON形式

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "Console": {
      "FormatterName": "json"
    }
  }
}
```

**環境変数での設定**:
```bash
Logging__Console__FormatterName=json
```

**フォーマッタの選択ガイド**:

| フォーマッタ | 出力形式 | 使用ケース |
|-------------|----------|------------|
| `simple` | テキスト | 開発環境、人間が読む |
| `json` | JSON | 本番環境、ログ集約ツール |
| `systemd` | systemd | Linux systemdサービス |

#### 12.2.3 FormatterOptions (フォーマッタオプション)

**スキーマ参照**: [appsettings_schema_translated.json:319](appsettings_schema_translated.json#L319)

**説明**: ログメッセージフォーマッタオプション

##### 12.2.3.1 IncludeScopes

**スキーマ参照**: [appsettings_schema_translated.json:324](appsettings_schema_translated.json#L324)

**説明**: 本当の場合はスコープを含めます

**デフォルト値**: `false`

**環境変数名**: `Logging__Console__FormatterOptions__IncludeScopes`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "Console": {
      "FormatterOptions": {
        "IncludeScopes": true
      }
    }
  }
}
```

**スコープの使用例**:
```csharp
using (_logger.BeginScope("Processing request {RequestId}", requestId))
{
    _logger.LogInformation("Starting operation");
    // ... 処理 ...
    _logger.LogInformation("Operation completed");
}
```

**IncludeScopes = true の場合の出力**:
```
info: MyApp.Controllers.HomeController[0]
      => RequestId:0HN1GKAVVJ123 => Processing request 12345
      Starting operation
info: MyApp.Controllers.HomeController[0]
      => RequestId:0HN1GKAVVJ123 => Processing request 12345
      Operation completed
```

##### 12.2.3.2 TimestampFormat

**スキーマ参照**: [appsettings_schema_translated.json:329](appsettings_schema_translated.json#L329)

**説明**: ロギングメッセージのタイムスタンプをフォーマットするために使用されるフォーマット文字列

**デフォルト値**: 未設定

**環境変数名**: `Logging__Console__FormatterOptions__TimestampFormat`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "Console": {
      "FormatterOptions": {
        "TimestampFormat": "yyyy-MM-dd HH:mm:ss.fff "
      }
    }
  }
}
```

**環境変数での設定**:
```bash
Logging__Console__FormatterOptions__TimestampFormat="yyyy-MM-dd HH:mm:ss.fff "
```

**推奨フォーマット**:
- ISO 8601: `"yyyy-MM-ddTHH:mm:ss.fffZ "`
- 日本標準: `"yyyy-MM-dd HH:mm:ss.fff "`
- 短縮版: `"HH:mm:ss "`
- カスタム: `"[yyyy-MM-dd HH:mm:ss.fff] "`

##### 12.2.3.3 UseUtcTimestamp

**スキーマ参照**: [appsettings_schema_translated.json:334](appsettings_schema_translated.json#L334)

**説明**: ロギングメッセージのタイムスタンプにUTC TimeZoneを使用する必要があるかどうかを示しています

**デフォルト値**: `false`

**環境変数名**: `Logging__Console__FormatterOptions__UseUtcTimestamp`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "Console": {
      "FormatterOptions": {
        "UseUtcTimestamp": true,
        "TimestampFormat": "yyyy-MM-ddTHH:mm:ss.fffZ "
      }
    }
  }
}
```

**環境変数での設定**:
```bash
Logging__Console__FormatterOptions__UseUtcTimestamp=true
```

**推奨設定**:
- **本番環境**: `true` (タイムゾーンの混乱を避ける)
- **開発環境**: `false` (ローカルタイムゾーンで見やすい)

#### 12.2.4 LogToStandardErrorThreshold

**スキーマ参照**: [appsettings_schema_translated.json:339](appsettings_schema_translated.json#L339)

**説明**: メッセージの最小レベルは、Console.Errorに書き込まれます

**$ref**: `#/definitions/logLevelThreshold`

**デフォルト値**: 未設定（すべてstdoutに出力）

**環境変数名**: `Logging__Console__LogToStandardErrorThreshold`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "Console": {
      "LogToStandardErrorThreshold": "Error"
    }
  }
}
```

**環境変数での設定**:
```bash
Logging__Console__LogToStandardErrorThreshold=Error
```

**推奨設定**:
- `"Error"`: エラー以上をstderrに出力（推奨）
- `"Warning"`: 警告以上をstderrに出力
- `"Critical"`: クリティカルのみstderrに出力

**完全なConsole設定例**:
```json
{
  "Logging": {
    "Console": {
      "LogLevel": {
        "Default": "Information",
        "Microsoft": "Warning"
      },
      "FormatterName": "json",
      "FormatterOptions": {
        "IncludeScopes": true,
        "TimestampFormat": "yyyy-MM-ddTHH:mm:ss.fffZ ",
        "UseUtcTimestamp": true
      },
      "LogToStandardErrorThreshold": "Error"
    }
  }
}
```

---

### 12.3 EventSource (EventSourceログプロバイダー)

**スキーマ参照**: [appsettings_schema_translated.json:346](appsettings_schema_translated.json#L346)

**説明**: EventSourceログプロバイダーの構成。Windows Event Tracing (ETW) に対応しています。

#### 12.3.1 LogLevel

**スキーマ参照**: [appsettings_schema_translated.json:351](appsettings_schema_translated.json#L351)

**$ref**: `#/definitions/logLevel`

**環境変数名パターン**: `Logging__EventSource__LogLevel__<Category>`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "EventSource": {
      "LogLevel": {
        "Default": "Warning"
      }
    }
  }
}
```

---

### 12.4 Debug (Debugログプロバイダー)

**スキーマ参照**: [appsettings_schema_translated.json:358](appsettings_schema_translated.json#L358)

**説明**: デバッグログプロバイダーの構成。Visual Studio のデバッグ出力ウィンドウにログを出力します。

#### 12.4.1 LogLevel

**スキーマ参照**: [appsettings_schema_translated.json:363](appsettings_schema_translated.json#L363)

**$ref**: `#/definitions/logLevel`

**環境変数名パターン**: `Logging__Debug__LogLevel__<Category>`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "Debug": {
      "LogLevel": {
        "Default": "Debug",
        "Microsoft": "Information"
      }
    }
  }
}
```

**推奨設定**:
- **開発環境**: `"Debug"` または `"Trace"`
- **本番環境**: 通常は無効（Debugプロバイダーは使用しない）

---

### 12.5 EventLog (Windowsイベントログプロバイダー)

**スキーマ参照**: [appsettings_schema_translated.json:370](appsettings_schema_translated.json#L370)

**説明**: Windowsイベントログプロバイダーの構成。Windows イベント ビューアーにログを記録します。

#### 12.5.1 LogLevel

**スキーマ参照**: [appsettings_schema_translated.json:375](appsettings_schema_translated.json#L375)

**$ref**: `#/definitions/logLevel`

**環境変数名パターン**: `Logging__EventLog__LogLevel__<Category>`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "EventLog": {
      "LogLevel": {
        "Default": "Warning",
        "Microsoft": "Error"
      }
    }
  }
}
```

**推奨設定**:
- **Windowsサービス**: `"Warning"` 以上
- **重要なアプリケーション**: `"Error"` 以上
- **開発環境**: 通常は無効

**注意**:
- Windows専用（Linux/macOSでは使用不可）
- NuGetパッケージ `Microsoft.Extensions.Logging.EventLog` が必要
- アプリケーションのイベントソースを事前に登録する必要がある場合があります

---

### 12.6 ElmahIo (Elmah.ioログプロバイダー)

**スキーマ参照**: [appsettings_schema_translated.json:382](appsettings_schema_translated.json#L382)

**説明**: Elmah.ioロギングプロバイダーの構成

#### 12.6.1 LogLevel

**スキーマ参照**: [appsettings_schema_translated.json:387](appsettings_schema_translated.json#L387)

**$ref**: `#/definitions/logLevel`

**環境変数名パターン**: `Logging__ElmahIo__LogLevel__<Category>`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "ElmahIo": {
      "LogLevel": {
        "Default": "Warning",
        "Microsoft": "Error"
      }
    }
  }
}
```

**推奨設定**:
- `"Warning"` 以上: コスト効率的（Elmah.ioは有料）
- `"Error"` 以上: エラーのみ記録

---

### 12.7 ElmahIoBreadcrumbs (Elmah.ioパンくずログプロバイダー)

**スキーマ参照**: [appsettings_schema_translated.json:394](appsettings_schema_translated.json#L394)

**説明**: Elmah.ioパンくずログプロバイダーの構成

#### 12.7.1 LogLevel

**スキーマ参照**: [appsettings_schema_translated.json:399](appsettings_schema_translated.json#L399)

**$ref**: `#/definitions/logLevel`

**環境変数名パターン**: `Logging__ElmahIoBreadcrumbs__LogLevel__<Category>`

**設定例（appsettings.json）**:
```json
{
  "Logging": {
    "ElmahIoBreadcrumbs": {
      "LogLevel": {
        "Default": "Trace",
        "Microsoft": "Debug"
      }
    }
  }
}
```

**推奨設定**:
- `"Trace"` または `"Debug"`: エラー前の詳細なコンテキストを記録

---

### 12.8 additionalProperties (追加のログプロバイダー)

**スキーマ参照**: [appsettings_schema_translated.json:406](appsettings_schema_translated.json#L406)

**説明**: プロバイダーのロギング構成。サードパーティのロギングプロバイダー用の設定です。

#### 12.8.1 LogLevel

**スキーマ参照**: [appsettings_schema_translated.json:411](appsettings_schema_translated.json#L411)

**$ref**: `#/definitions/logLevel`

**環境変数名パターン**: `Logging__<ProviderName>__LogLevel__<Category>`

**サードパーティプロバイダーの例**:

**Serilogの場合**:
```json
{
  "Logging": {
    "Serilog": {
      "LogLevel": {
        "Default": "Information"
      }
    }
  }
}
```

**NLogの場合**:
```json
{
  "Logging": {
    "NLog": {
      "LogLevel": {
        "Default": "Information"
      }
    }
  }
}
```

---

**完全なLogging設定例**:

**本番環境向け包括的設定**:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft": "Error",
      "Microsoft.Hosting.Lifetime": "Information",
      "MyApp": "Information"
    },
    "Console": {
      "LogLevel": {
        "Default": "Information"
      },
      "FormatterName": "json",
      "FormatterOptions": {
        "IncludeScopes": true,
        "TimestampFormat": "yyyy-MM-ddTHH:mm:ss.fffZ ",
        "UseUtcTimestamp": true
      },
      "LogToStandardErrorThreshold": "Error"
    },
    "EventSource": {
      "LogLevel": {
        "Default": "Warning"
      }
    },
    "EventLog": {
      "LogLevel": {
        "Default": "Error"
      }
    }
  }
}
```

**開発環境向け設定**:
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft": "Information",
      "Microsoft.AspNetCore": "Information",
      "MyApp": "Trace"
    },
    "Console": {
      "LogLevel": {
        "Default": "Debug"
      },
      "FormatterName": "simple",
      "FormatterOptions": {
        "IncludeScopes": true,
        "TimestampFormat": "HH:mm:ss ",
        "UseUtcTimestamp": false
      }
    },
    "Debug": {
      "LogLevel": {
        "Default": "Debug"
      }
    }
  }
}
```
## 13. allowedHosts (許可されたホスト)

**スキーマ参照**: [appsettings_schema_translated.json:418](appsettings_schema_translated.json#L418)

**説明**: ASP.NETコアホストフィルタリングミドルウェア構成。許可されたホストは、ポート番号のないホスト名のセミコロン削除リストです。

**type**: string

**デフォルト値**: `"*"` (すべてのホストを許可)

**環境変数名**: `AllowedHosts`

**設定例（appsettings.json）**:
```json
{
  "AllowedHosts": "*"
}
```

**環境変数での設定**:
```bash
AllowedHosts=*
```

**セミコロン区切りの複数ホスト**:
```json
{
  "AllowedHosts": "example.com;www.example.com;api.example.com"
}
```

**推奨設定**:

| 環境 | 推奨値 | 理由 |
|------|--------|------|
| 開発環境 | `*` | すべてのホストを許可（localhost含む） |
| 本番環境 | `example.com;www.example.com` | 特定のドメインのみ許可（セキュリティ向上） |
| Dockerコンテナ | `*` | コンテナ内部で動的ホスト名 |
| Azure App Service | `youra pp.azurewebsites.net` | Azureのホスト名を指定 |

**ホストヘッダーインジェクション攻撃の防止**:

ホストフィルタリングミドルウェアは、悪意のあるホストヘッダーを使用した攻撃を防ぎます。

**攻撃例**:
```http
GET / HTTP/1.1
Host: evil.com
```

この場合、`AllowedHosts` に `evil.com` が含まれていなければ、リクエストは拒否されます（HTTP 400エラー）。

**環境別設定例**:

**appsettings.json** (共通):
```json
{
  "AllowedHosts": "*"
}
```

**appsettings.Development.json** (開発環境):
```json
{
  "AllowedHosts": "*"
}
```

**appsettings.Production.json** (本番環境):
```json
{
  "AllowedHosts": "example.com;www.example.com;api.example.com"
}
```

**Azure App Service環境**:
```json
{
  "AllowedHosts": "myapp.azurewebsites.net;myapp-staging.azurewebsites.net"
}
```

**カスタムドメインとAzureの両方**:
```json
{
  "AllowedHosts": "example.com;www.example.com;myapp.azurewebsites.net"
}
```

**ワイルドカードの使用**:

特定のサブドメインをすべて許可する場合:
```json
{
  "AllowedHosts": "*.example.com"
}
```

これにより、`api.example.com`、`app.example.com`、`blog.example.com` などすべてのサブドメインが許可されます。

**コードでの使用** (Program.cs):
```csharp
var builder = WebApplication.CreateBuilder(args);

// AllowedHostsは自動的に適用されます
// builder.Configuration["AllowedHosts"] で取得可能

var app = builder.Build();

app.Run();
```

**注意事項**:
- ポート番号は含めないでください（例: `example.com:5000` ではなく `example.com`）
- `localhost` は開発環境でのみ使用してください
- 本番環境では必ず特定のドメインを指定してください
- リバースプロキシ（Nginx、IIS）を使用する場合、プロキシのホスト名も含める必要があります

**リバースプロキシ使用時の設定例**:
```json
{
  "AllowedHosts": "example.com;www.example.com",
  "ForwardedHeaders": {
    "ForwardedHeaders": "XForwardedFor, XForwardedProto, XForwardedHost",
    "KnownNetworks": [],
    "KnownProxies": []
  }
}
```

---

## 14. connectionStrings (接続文字列)

**スキーマ参照**: [appsettings_schema_translated.json:425](appsettings_schema_translated.json#L425)

**説明**: 接続文字列構成。IConfiguration.GetConnectionString（String）拡張法で接続文字列を取得します

**type**: object

**additionalProperties**: string (各接続文字列)

**環境変数名パターン**: `ConnectionStrings__<Name>`

**設定例（appsettings.json）**:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=MyApp;Trusted_Connection=True;MultipleActiveResultSets=true",
    "RedisConnection": "localhost:6379",
    "CosmosDbConnection": "AccountEndpoint=https://myaccount.documents.azure.com:443/;AccountKey=..."
  }
}
```

**環境変数での設定**:
```bash
ConnectionStrings__DefaultConnection="Server=myserver;Database=MyApp;User Id=myuser;Password=mypassword;"
ConnectionStrings__RedisConnection="localhost:6379"
```

**コードでの取得方法**:
```csharp
// Program.cs または Startup.cs
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// または
var connectionString = builder.Configuration["ConnectionStrings:DefaultConnection"];
```

### 主要なデータベースの接続文字列

#### SQL Server

**Windows認証**:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;Trusted_Connection=True;MultipleActiveResultSets=true"
  }
}
```

**SQL Server認証**:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;User Id=myuser;Password=mypassword;MultipleActiveResultSets=true"
  }
}
```

**Azure SQL Database**:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=tcp:myserver.database.windows.net,1433;Database=MyApp;User Id=myuser@myserver;Password=mypassword;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  }
}
```

#### PostgreSQL

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=myapp;Username=myuser;Password=mypassword"
  }
}
```

**Azure Database for PostgreSQL**:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=myserver.postgres.database.azure.com;Database=myapp;Username=myuser@myserver;Password=mypassword;SslMode=Require"
  }
}
```

#### MySQL

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=myapp;User=myuser;Password=mypassword;"
  }
}
```

**Azure Database for MySQL**:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=myserver.mysql.database.azure.com;Database=myapp;User Id=myuser@myserver;Password=mypassword;SslMode=Required"
  }
}
```

#### SQLite

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=myapp.db"
  }
}
```

**メモリ内データベース（テスト用）**:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=:memory:"
  }
}
```

#### Oracle

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ORCL)));User Id=myuser;Password=mypassword;"
  }
}
```

### NoSQLデータベース

#### MongoDB

```json
{
  "ConnectionStrings": {
    "MongoDb": "mongodb://localhost:27017/myapp"
  }
}
```

**Azure Cosmos DB (MongoDB API)**:
```json
{
  "ConnectionStrings": {
    "MongoDb": "mongodb://myaccount:mypassword@myaccount.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
  }
}
```

#### Redis

```json
{
  "ConnectionStrings": {
    "Redis": "localhost:6379"
  }
}
```

**Azure Cache for Redis**:
```json
{
  "ConnectionStrings": {
    "Redis": "myaccount.redis.cache.windows.net:6380,password=mypassword,ssl=True,abortConnect=False"
  }
}
```

#### Azure Cosmos DB (SQL API)

```json
{
  "ConnectionStrings": {
    "CosmosDb": "AccountEndpoint=https://myaccount.documents.azure.com:443/;AccountKey=myaccountkey=="
  }
}
```

### Entity Framework Core での使用例

**SQL Server**:
```csharp
// Program.cs
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("DefaultConnection")));
```

**PostgreSQL**:
```csharp
// Program.cs
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("DefaultConnection")));
```

**MySQL**:
```csharp
// Program.cs
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseMySql(
        builder.Configuration.GetConnectionString("DefaultConnection"),
        ServerVersion.AutoDetect(builder.Configuration.GetConnectionString("DefaultConnection"))));
```

**SQLite**:
```csharp
// Program.cs
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlite(
        builder.Configuration.GetConnectionString("DefaultConnection")));
```

### セキュリティのベストプラクティス

**1. User Secrets（開発環境）**:
```bash
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=localhost;Database=MyApp;User Id=dev;Password=DevPassword123;"
```

**2. 環境変数（本番環境）**:
```bash
export ConnectionStrings__DefaultConnection="Server=prod-server;Database=MyApp;User Id=prod;Password=ProdPassword123;"
```

**3. Azure Key Vault（推奨）**:
```csharp
// Program.cs
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{keyVaultName}.vault.azure.net/"),
    new DefaultAzureCredential());
```

**Key Vault に保存**:
- Secret名: `ConnectionStrings--DefaultConnection`
- 値: `Server=...;Password=...`

**4. Azure App Configuration**:
```csharp
// Program.cs
builder.Configuration.AddAzureAppConfiguration(options =>
{
    options.Connect(Environment.GetEnvironmentVariable("AppConfigConnection"))
           .ConfigureKeyVault(kv =>
           {
               kv.SetCredential(new DefaultAzureCredential());
           });
});
```

### 環境別設定例

**appsettings.json** (共通、ダミー値):
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;Trusted_Connection=True;"
  }
}
```

**appsettings.Development.json** (開発環境、User Secretsを推奨):
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=MyApp-Dev;Trusted_Connection=True;MultipleActiveResultSets=true"
  }
}
```

**appsettings.Production.json** (本番環境、環境変数またはKey Vaultを使用):
```json
{
  "ConnectionStrings": {
    "DefaultConnection": ""
  }
}
```

### 複数の接続文字列

複数のデータベースを使用する場合:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;Trusted_Connection=True;",
    "ReadOnlyConnection": "Server=readonly-server;Database=MyApp;User Id=readonly;Password=password;",
    "LoggingConnection": "Server=log-server;Database=Logs;User Id=logger;Password=password;",
    "CacheConnection": "localhost:6379",
    "DocumentConnection": "mongodb://localhost:27017/documents"
  }
}
```

**コードでの使用**:
```csharp
// 複数のDbContextを登録
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddDbContext<LoggingDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("LoggingConnection")));

// Redis
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("CacheConnection");
});

// MongoDB
builder.Services.AddSingleton<IMongoClient>(sp =>
{
    var connectionString = builder.Configuration.GetConnectionString("DocumentConnection");
    return new MongoClient(connectionString);
});
```

### 接続文字列のテスト

**接続テストコード例**:
```csharp
public class DatabaseHealthCheck : IHealthCheck
{
    private readonly string _connectionString;

    public DatabaseHealthCheck(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("DefaultConnection");
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            using var connection = new SqlConnection(_connectionString);
            await connection.OpenAsync(cancellationToken);
            return HealthCheckResult.Healthy("Database connection is healthy");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Database connection failed", ex);
        }
    }
}
```

**ヘルスチェックの登録**:
```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database");

var app = builder.Build();

app.MapHealthChecks("/health");
```

### 注意事項

- ? **絶対にやってはいけないこと**: appsettings.json に本番環境の接続文字列を直接記載してGitにコミット
- ? **推奨**: User Secrets（開発）、環境変数（本番）、Azure Key Vault（最推奨）
- ? 接続プールを有効にして最適化
- ? 接続タイムアウトを適切に設定
- ? SSL/TLS暗号化を有効化（本番環境）
- ? 最小権限の原則に従ってデータベースユーザーを作成

### 完全な設定例

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;Trusted_Connection=True;MultipleActiveResultSets=true;Connection Timeout=30;",
    "ReadOnlyConnection": "Server=replica-server;Database=MyApp;User Id=readonly;Password=password;ApplicationIntent=ReadOnly;",
    "Redis": "localhost:6379,ssl=False,abortConnect=False,connectTimeout=5000,syncTimeout=5000",
    "MongoDb": "mongodb://localhost:27017/myapp?connectTimeoutMS=5000&socketTimeoutMS=5000",
    "CosmosDb": "AccountEndpoint=https://myaccount.documents.azure.com:443/;AccountKey=key=="
  }
}
```
## 15. NLog (NLogフレームワーク設定)

**スキーマ参照**: [appsettings_schema_translated.json:432](appsettings_schema_translated.json#L432)

**説明**: nlog構成。NLogは、.NET向けの柔軟で強力なロギングフレームワークです。

**NuGetパッケージ**: `NLog.Web.AspNetCore`

**使用場所**: `NLog`, `Nlog`, `nlog`（大文字小文字を区別しない）

### NLogの基本構造

NLogの設定は主に以下の要素で構成されます：
1. **extensions**: 拡張機能の読み込み
2. **variables**: 変数の定義
3. **targets**: ログの出力先
4. **rules**: ロ ギングルール（どのログをどこに出力するか）

### 15.1 autoReload

**スキーマ参照**: [appsettings_schema_translated.json:440](appsettings_schema_translated.json#L440)

**説明**: appsettings.jsonファイルが変更されたことを通知すると、nlog構成を自動的にリロードします

**デフォルト値**: `false`

**環境変数名**: `NLog__autoReload`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "autoReload": true
  }
}
```

**環境変数での設定**:
```bash
NLog__autoReload=true
```

**推奨設定**:
- **開発環境**: `true` (設定変更を即座に反映)
- **本番環境**: `false` (パフォーマンス優先)

---

### 15.2 throwConfigExceptions

**スキーマ参照**: [appsettings_schema_translated.json:445](appsettings_schema_translated.json#L445)

**説明**: 構成エラーがある場合、例外をスローしますか？nullの場合、内部ログのログレベルがOffであるかどうかに基づきます。

**デフォルト値**: `false`

**環境変数名**: `NLog__throwConfigExceptions`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "throwConfigExceptions": true
  }
}
```

**推奨設定**:
- **開発環境**: `true` (設定ミスを早期発見)
- **本番環境**: `false` または `null` (アプリのクラッシュを防ぐ)

---

### 15.3 throwExceptions

**スキーマ参照**: [appsettings_schema_translated.json:450](appsettings_schema_translated.json#L450)

**説明**: エラーが発生したときに例外をスローします

**デフォルト値**: `false`

**環境変数名**: `NLog__throwExceptions`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "throwExceptions": false
  }
}
```

**推奨設定**:
- 常に `false` (ロギングエラーでアプリをクラッシュさせない)

---

### 15.4 internalLogLevel

**スキーマ参照**: [appsettings_schema_translated.json:455](appsettings_schema_translated.json#L455)

**説明**: 内部ロガーの最小ログレベル

**デフォルト値**: `"Off"`

**環境変数名**: `NLog__internalLogLevel`

**可能な値**: `"Trace"`, `"Debug"`, `"Info"`, `"Warn"`, `"Error"`, `"Fatal"`, `"Off"`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "internalLogLevel": "Off"
  }
}
```

**推奨設定**:
- **開発環境**: `"Info"` または `"Debug"` (NLog自体のデバッグ用)
- **本番環境**: `"Off"` または `"Warn"`
- **トラブルシューティング時**: `"Trace"`

---

### 15.5 internalLogFile

**スキーマ参照**: [appsettings_schema_translated.json:467](appsettings_schema_translated.json#L467)

**説明**: 指定されたFilepathに内部ログを書き込みます

**デフォルト値**: 未設定

**環境変数名**: `NLog__internalLogFile`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "internalLogLevel": "Info",
    "internalLogFile": "logs/nlog-internal.log"
  }
}
```

**推奨設定**:
```json
{
  "NLog": {
    "internalLogFile": "${basedir}/logs/nlog-internal-${shortdate}.log"
  }
}
```

---

### 15.6 internalLogToConsole

**スキーマ参照**: [appsettings_schema_translated.json:472](appsettings_schema_translated.json#L472)

**説明**: 内部ログをコンソールに書き込みます

**デフォルト値**: `false`

**環境変数名**: `NLog__internalLogToConsole`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "internalLogToConsole": true
  }
}
```

**推奨設定**:
- **開発環境**: `true`
- **本番環境**: `false`

---

### 15.7 internalLogToConsoleError

**スキーマ参照**: [appsettings_schema_translated.json:477](appsettings_schema_translated.json#L477)

**説明**: エラーストリームで内部ログをコンソールに書き込みます

**デフォルト値**: `false`

**環境変数名**: `NLog__internalLogToConsoleError`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "internalLogToConsoleError": true
  }
}
```

---

### 15.8 globalThreshold

**スキーマ参照**: [appsettings_schema_translated.json:482](appsettings_schema_translated.json#L482)

**説明**: このしきい値以下のログイベントは記録されていません

**デフォルト値**: `"Off"`

**環境変数名**: `NLog__globalThreshold`

**可能な値**: `"Trace"`, `"Debug"`, `"Info"`, `"Warn"`, `"Error"`, `"Fatal"`, `"Off"`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "globalThreshold": "Info"
  }
}
```

**推奨設定**:
- **開発環境**: `"Trace"` または `"Debug"`
- **本番環境**: `"Info"` または `"Warn"`

---

### 15.9 autoShutdown

**スキーマ参照**: [appsettings_schema_translated.json:494](appsettings_schema_translated.json#L494)

**説明**: appdomain.unloadまたはappdomain.processexitで「logactory.shutdown」を自動的に呼び出します

**デフォルト値**: `true`

**環境変数名**: `NLog__autoShutdown`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "autoShutdown": true
  }
}
```

**推奨設定**: 常に `true`（デフォルトのまま）

---

### 15.10 extensions (拡張機能)

**スキーマ参照**: [appsettings_schema_translated.json:499](appsettings_schema_translated.json#L499)

**説明**: 追加のターゲットとレイアウトにNLOG拡張機能パッケージをロードします

**デフォルト値**: `[]`

**環境変数名パターン**: `NLog__extensions__<index>__<property>`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "extensions": [
      {
        "assembly": "NLog.Web.AspNetCore"
      },
      {
        "assembly": "NLog.Targets.ElasticSearch"
      }
    ]
  }
}
```

#### 15.10.1 assembly

**スキーマ参照**: [appsettings_schema_translated.json:507](appsettings_schema_translated.json#L507)

**説明**: NLOG拡張機能パッケージのアセンブリ名

**設定例**:
```json
{
  "NLog": {
    "extensions": [
      { "assembly": "NLog.Web.AspNetCore" },
      { "assembly": "NLog.Database" },
      { "assembly": "NLog.Targets.Seq" }
    ]
  }
}
```

**一般的な拡張機能**:
- `NLog.Web.AspNetCore`: ASP.NET Core統合
- `NLog.Database`: データベースターゲット
- `NLog.Targets.Seq`: Seqターゲット
- `NLog.Targets.ElasticSearch`: Elasticsearchターゲット
- `NLog.Targets.Syslog`: Syslogターゲット

#### 15.10.2 prefix

**スキーマ参照**: [appsettings_schema_translated.json:512](appsettings_schema_translated.json#L512)

**説明**: アセンブリからロードされたすべてのタイプ名にプレフィックスを追加します

**デフォルト値**: `""`

**設定例**:
```json
{
  "NLog": {
    "extensions": [
      {
        "assembly": "NLog.CustomTargets",
        "prefix": "Custom"
      }
    ]
  }
}
```

#### 15.10.3 assemblyFile

**スキーマ参照**: [appsettings_schema_translated.json:517](appsettings_schema_translated.json#L517)

**説明**: NLOG拡張パッケージのアセンブリファイルへの絶対的なfilepath

**デフォルト値**: `""`

**設定例**:
```json
{
  "NLog": {
    "extensions": [
      {
        "assemblyFile": "C:\\MyApp\\NLog.CustomTargets.dll"
      }
    ]
  }
}
```

---

### 15.11 variables (変数)

**スキーマ参照**: [appsettings_schema_translated.json:526](appsettings_schema_translated.json#L526)

**説明**: 変数のキー価値ペア。ターゲットやレイアウトで使用できる変数を定義します。

**propertyNames.pattern**: `^[A-Za-z0-9_.-]+$`

**環境変数名パターン**: `NLog__variables__<VariableName>`

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "variables": {
      "logDirectory": "logs",
      "applicationName": "MyApp",
      "logLevel": "Info"
    }
  }
}
```

**環境変数での設定**:
```bash
NLog__variables__logDirectory=logs
NLog__variables__applicationName=MyApp
```

**変数の使用例**:
```json
{
  "NLog": {
    "variables": {
      "logDir": "${basedir}/logs",
      "appName": "MyApp"
    },
    "targets": {
      "logfile": {
        "type": "File",
        "fileName": "${var:logDir}/${var:appName}-${shortdate}.log"
      }
    }
  }
}
```

**推奨変数**:
```json
{
  "NLog": {
    "variables": {
      "logDirectory": "${basedir}/logs",
      "applicationName": "${processname}",
      "archiveDirectory": "${basedir}/logs/archive"
    }
  }
}
```

---

### 15.12 targetDefaultWrapper (デフォルトラッパー)

**スキーマ参照**: [appsettings_schema_translated.json:543](appsettings_schema_translated.json#L543)

**説明**: このカスタムターゲットラッパーで定義されたすべてのターゲットをラップします

**required**: ["type"]

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "targetDefaultWrapper": {
      "type": "AsyncWrapper",
      "overflowAction": "Block"
    }
  }
}
```

**一般的なラッパー**:
- `AsyncWrapper`: 非同期書き込み（パフォーマンス向上）
- `BufferingWrapper`: バッファリング
- `RetryingWrapper`: リトライ機能
- `FallbackGroup`: フォールバック

---

### 15.13 targets (ターゲット)

**スキーマ参照**: [appsettings_schema_translated.json:556](appsettings_schema_translated.json#L556)

**説明**: ログの出力先を定義します

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "targets": {
      "logfile": {
        "type": "File",
        "fileName": "logs/nlog-${shortdate}.log",
        "layout": "${longdate}|${level:uppercase=true}|${logger}|${message} ${exception:format=tostring}"
      },
      "logconsole": {
        "type": "Console",
        "layout": "${longdate}|${level:uppercase=true}|${logger}|${message}"
      }
    }
  }
}
```

**完全なターゲット設定例**:
```json
{
  "NLog": {
    "targets": {
      "async": true,
      "allfile": {
        "type": "File",
        "fileName": "logs/nlog-all-${shortdate}.log",
        "layout": "${longdate}|${event-properties:item=EventId_Id:whenEmpty=0}|${level:uppercase=true}|${logger}|${message} ${exception:format=tostring}",
        "archiveFileName": "logs/archive/nlog-all-${shortdate}.{#}.log",
        "archiveEvery": "Day",
        "archiveNumbering": "Rolling",
        "maxArchiveFiles": 7,
        "concurrentWrites": true,
        "keepFileOpen": false
      },
      "ownFile-web": {
        "type": "File",
        "fileName": "logs/nlog-own-${shortdate}.log",
        "layout": "${longdate}|${event-properties:item=EventId_Id:whenEmpty=0}|${level:uppercase=true}|${logger}|${message} ${exception:format=tostring}|url: ${aspnet-request-url}|action: ${aspnet-mvc-action}"
      },
      "console": {
        "type": "Console",
        "layout": "${longdate}|${level:uppercase=true}|${logger}|${message}"
      },
      "database": {
        "type": "Database",
        "connectionString": "${var:connectionString}",
        "commandText": "INSERT INTO Logs(Timestamp, Level, Logger, Message, Exception) VALUES(@timestamp, @level, @logger, @message, @exception)",
        "parameters": [
          {
            "name": "@timestamp",
            "layout": "${longdate}"
          },
          {
            "name": "@level",
            "layout": "${level}"
          },
          {
            "name": "@logger",
            "layout": "${logger}"
          },
          {
            "name": "@message",
            "layout": "${message}"
          },
          {
            "name": "@exception",
            "layout": "${exception:format=tostring}"
          }
        ]
      }
    }
  }
}
```

#### 15.13.1 async

**スキーマ参照**: [appsettings_schema_translated.json:561](appsettings_schema_translated.json#L561)

**説明**: Overflowactionを使用してAsyncWrapperを使用してすべての定義されたターゲットをラップして、パフォーマンスを向上させるために破棄します

**設定例**:
```json
{
  "NLog": {
    "targets": {
      "async": true
    }
  }
}
```

**推奨設定**: 本番環境では `true` に設定してパフォーマンスを向上

---

### 15.14 rules (ロギングルール)

**スキーマ参照**: [appsettings_schema_translated.json:569](appsettings_schema_translated.json#L569)

**説明**: ロギングルール設定。どのログをどのターゲットに出力するかを定義します。

**設定例（appsettings.json）**:
```json
{
  "NLog": {
    "rules": [
      {
        "logger": "*",
        "minLevel": "Trace",
        "writeTo": "allfile"
      },
      {
        "logger": "Microsoft.*",
        "maxLevel": "Info",
        "final": true
      },
      {
        "logger": "*",
        "minLevel": "Debug",
        "writeTo": "ownFile-web"
      }
    ]
  }
}
```

**完全なNLog設定例**:

```json
{
  "NLog": {
    "autoReload": true,
    "throwConfigExceptions": true,
    "internalLogLevel": "Info",
    "internalLogFile": "logs/nlog-internal.log",
    "extensions": [
      {
        "assembly": "NLog.Web.AspNetCore"
      }
    ],
    "variables": {
      "logDirectory": "${basedir}/logs"
    },
    "targets": {
      "async": true,
      "allfile": {
        "type": "File",
        "fileName": "${var:logDirectory}/nlog-all-${shortdate}.log",
        "layout": "${longdate}|${event-properties:item=EventId_Id:whenEmpty=0}|${level:uppercase=true}|${logger}|${message} ${exception:format=tostring}",
        "archiveFileName": "${var:logDirectory}/archive/nlog-all-${shortdate}.{#}.log",
        "archiveEvery": "Day",
        "archiveNumbering": "Rolling",
        "maxArchiveFiles": 7
      },
      "ownFile-web": {
        "type": "File",
        "fileName": "${var:logDirectory}/nlog-own-${shortdate}.log",
        "layout": "${longdate}|${event-properties:item=EventId_Id:whenEmpty=0}|${level:uppercase=true}|${logger}|${message} ${exception:format=tostring}|url: ${aspnet-request-url}|action: ${aspnet-mvc-action}"
      },
      "console": {
        "type": "Console",
        "layout": "${longdate}|${level:uppercase=true}|${logger}|${message}"
      }
    },
    "rules": [
      {
        "logger": "*",
        "minLevel": "Trace",
        "writeTo": "allfile"
      },
      {
        "logger": "Microsoft.Hosting.Lifetime",
        "minLevel": "Info",
        "writeTo": "console",
        "final": true
      },
      {
        "logger": "Microsoft.*",
        "maxLevel": "Info",
        "final": true
      },
      {
        "logger": "*",
        "minLevel": "Debug",
        "writeTo": "ownFile-web,console"
      }
    ]
  }
}
```

---

## 16. NLogRulesItem (NLogルール項目)

**スキーマ参照**: [appsettings_schema_translated.json:605](appsettings_schema_translated.json#L605)

**説明**: Logeventsを一致するロガーオブジェクトから指定されたターゲットにリダイレクトします

**required**: ["logger"]

### 16.1 logger (必須)

**スキーマ参照**: [appsettings_schema_translated.json:613](appsettings_schema_translated.json#L613)

**説明**: ロガー名に基づいてロガーオブジェクトを一致させます。ワイルドカード文字（ '*'または '？'）を使用できます

**設定例**:
```json
{
  "logger": "MyApp.Controllers.*"
}
```

**ワイルドカードパターン例**:
- `"*"`: すべてのロガー
- `"MyApp.*"`: MyAppで始まるすべてのロガー
- `"MyApp.Controllers.*"`: MyApp.Controllersで始まるすべてのロガー
- `"MyApp.Services.UserService"`: 特定のロガー
- `"Microsoft.*"`: Microsoftで始まるすべてのロガー

---

### 16.2 ruleName

**スキーマ参照**: [appsettings_schema_translated.json:618](appsettings_schema_translated.json#L618)

**説明**: ルール識別子

**設定例**:
```json
{
  "logger": "*",
  "ruleName": "AllFilesRule",
  "writeTo": "allfile"
}
```

---

### 16.3 level

**スキーマ参照**: [appsettings_schema_translated.json:623](appsettings_schema_translated.json#L623)

**説明**: 単一の一致レベル

**可能な値**: `"Trace"`, `"Debug"`, `"Info"`, `"Warn"`, `"Error"`, `"Fatal"`

**設定例**:
```json
{
  "logger": "*",
  "level": "Error",
  "writeTo": "errorfile"
}
```

---

### 16.4 levels

**スキーマ参照**: [appsettings_schema_translated.json:634](appsettings_schema_translated.json#L634)

**説明**: このルールが一致するレベルのリストを分離しました

**設定例**:
```json
{
  "logger": "*",
  "levels": "Error,Fatal",
  "writeTo": "errorfile"
}
```

---

### 16.5 minLevel

**スキーマ参照**: [appsettings_schema_translated.json:639](appsettings_schema_translated.json#L639)

**説明**: 最小ログレベル

**可能な値**: `"Trace"`, `"Debug"`, `"Info"`, `"Warn"`, `"Error"`, `"Fatal"`

**設定例**:
```json
{
  "logger": "*",
  "minLevel": "Info",
  "writeTo": "allfile"
}
```

---

### 16.6 maxLevel

**スキーマ参照**: [appsettings_schema_translated.json:650](appsettings_schema_translated.json#L650)

**説明**: 最大ログレベル

**可能な値**: `"Trace"`, `"Debug"`, `"Info"`, `"Warn"`, `"Error"`, `"Fatal"`

**設定例**:
```json
{
  "logger": "Microsoft.*",
  "maxLevel": "Info",
  "final": true
}
```

---

### 16.7 finalMinLevel

**スキーマ参照**: [appsettings_schema_translated.json:661](appsettings_schema_translated.json#L661)

**説明**: 最終的な最小レベル

**設定例**:
```json
{
  "logger": "*",
  "finalMinLevel": "Warn"
}
```

---

### 16.8 writeTo

**スキーマ参照**: [appsettings_schema_translated.json:672](appsettings_schema_translated.json#L672)

**説明**: ターゲットの名前または名前 - コンマで区切られています

**設定例**:
```json
{
  "logger": "*",
  "minLevel": "Info",
  "writeTo": "allfile,console"
}
```

---

### 16.9 final

**スキーマ参照**: [appsettings_schema_translated.json:677](appsettings_schema_translated.json#L677)

**説明**: これが一致する場合、さらなるルールを無視します

**デフォルト値**: `false`

**設定例**:
```json
{
  "logger": "Microsoft.*",
  "maxLevel": "Info",
  "final": true
}
```

---

### 16.10 enabled

**スキーマ参照**: [appsettings_schema_translated.json:682](appsettings_schema_translated.json#L682)

**説明**: ルールを有効にするかどうか

**デフォルト値**: `true`

**設定例**:
```json
{
  "logger": "*",
  "minLevel": "Debug",
  "writeTo": "debugfile",
  "enabled": false
}
```

---

### 16.11 filters

**スキーマ参照**: [appsettings_schema_translated.json:687](appsettings_schema_translated.json#L687)

**説明**: フィルター設定

**設定例**:
```json
{
  "logger": "*",
  "minLevel": "Info",
  "writeTo": "allfile",
  "filters": [
    {
      "type": "when",
      "condition": "contains('${message}','password')",
      "action": "Ignore"
    }
  ]
}
```

---

### 16.12 filterDefaultAction

**スキーマ参照**: [appsettings_schema_translated.json:714](appsettings_schema_translated.json#L714)

**説明**: フィルターが一致しない場合、デフォルトのアクション

**デフォルト値**: `"Ignore"`

**可能な値**: `"Neutral"`, `"Log"`, `"Ignore"`, `"LogFinal"`, `"IgnoreFinal"`

**設定例**:
```json
{
  "logger": "*",
  "filters": [...],
  "filterDefaultAction": "Log"
}
```

---

**完全なNLogルール設定例**:

```json
{
  "NLog": {
    "rules": [
      {
        "logger": "*",
        "minLevel": "Trace",
        "writeTo": "allfile"
      },
      {
        "logger": "Microsoft.Hosting.Lifetime",
        "minLevel": "Info",
        "writeTo": "console",
        "final": true
      },
      {
        "logger": "Microsoft.*",
        "maxLevel": "Info",
        "final": true
      },
      {
        "logger": "System.*",
        "maxLevel": "Info",
        "final": true
      },
      {
        "logger": "MyApp.*",
        "minLevel": "Debug",
        "writeTo": "ownFile-web,console"
      },
      {
        "logger": "*",
        "minLevel": "Warn",
        "writeTo": "errorfile"
      }
    ]
  }
}
```
## 17. Serilog (Serilogフレームワーク設定)

**スキーマ参照**: [appsettings_schema_translated.json:726](appsettings_schema_translated.json#L726)

**説明**: Serilog構成。Serilogは、.NET向けの診断ロギングライブラリです。

**NuGetパッケージ**: `Serilog.AspNetCore`

**使用場所**: `Serilog`

### Serilogの基本構造

Serilogの設定は主に以下の要素で構成されます：
1. **MinimumLevel**: 最小ログレベル
2. **Enrich**: ログの追加情報
3. **WriteTo**: ログの出力先（Sinks）
4. **Filter**: ログフィルター
5. **Properties**: グローバルプロパティ

### 17.1 Using

**スキーマ参照**: [appsettings_schema_translated.json:731](appsettings_schema_translated.json#L731)

**説明**: セリロッグを構成するときにロードされるセリロッグシンクとエンリッチャー。アセンブリ名、またはNuGetパッケージ名のリスト。

**type**: array of strings

**環境変数名**: `Serilog__Using__0`, `Serilog__Using__1`, ...

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "Using": [
      "Serilog.Sinks.Console",
      "Serilog.Sinks.File",
      "Serilog.Sinks.Seq",
      "Serilog.Enrichers.Environment",
      "Serilog.Enrichers.Thread"
    ]
  }
}
```

**環境変数での設定**:
```bash
Serilog__Using__0=Serilog.Sinks.Console
Serilog__Using__1=Serilog.Sinks.File
Serilog__Using__2=Serilog.Sinks.Seq
```

**一般的なSerilogパッケージ**:

**Sinks（出力先）**:
- `Serilog.Sinks.Console`: コンソール出力
- `Serilog.Sinks.File`: ファイル出力
- `Serilog.Sinks.Seq`: Seqサーバー
- `Serilog.Sinks.Elasticsearch`: Elasticsearch
- `Serilog.Sinks.MSSqlServer`: SQL Server
- `Serilog.Sinks.ApplicationInsights`: Application Insights
- `Serilog.Sinks.Email`: メール通知

**Enrichers（エンリッチャー）**:
- `Serilog.Enrichers.Environment`: マシン名、ユーザー名など
- `Serilog.Enrichers.Thread`: スレッドID
- `Serilog.Enrichers.Process`: プロセスID
- `Serilog.Enrichers.ClientInfo`: クライアント情報

---

### 17.2 MinimumLevel (最小ログレベル)

**スキーマ参照**: [appsettings_schema_translated.json:739](appsettings_schema_translated.json#L739)

**説明**: 最小ログレベル構成

#### 17.2.1 Default

**スキーマ参照**: [appsettings_schema_translated.json:744](appsettings_schema_translated.json#L744)

**説明**: デフォルトの最小レベル

**環境変数名**: `Serilog__MinimumLevel__Default`

**可能な値**: `"Verbose"`, `"Debug"`, `"Information"`, `"Warning"`, `"Error"`, `"Fatal"`

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information"
    }
  }
}
```

**環境変数での設定**:
```bash
Serilog__MinimumLevel__Default=Information
```

**ログレベルの対応**:

| Serilog | NLog | Microsoft.Extensions.Logging |
|---------|------|------------------------------|
| Verbose | Trace | Trace |
| Debug | Debug | Debug |
| Information | Info | Information |
| Warning | Warn | Warning |
| Error | Error | Error |
| Fatal | Fatal | Critical |

#### 17.2.2 Override

**スキーマ参照**: [appsettings_schema_translated.json:756](appsettings_schema_translated.json#L756)

**説明**: 最小レベルは、名前空間によってオーバーライドされます

**type**: object (additionalProperties: logLevel)

**環境変数名パターン**: `Serilog__MinimumLevel__Override__<Namespace>`

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.AspNetCore": "Warning",
        "System": "Warning",
        "MyApp": "Debug",
        "MyApp.Controllers": "Information"
      }
    }
  }
}
```

**環境変数での設定**:
```bash
Serilog__MinimumLevel__Override__Microsoft=Warning
Serilog__MinimumLevel__Override__Microsoft.AspNetCore=Warning
Serilog__MinimumLevel__Override__MyApp=Debug
```

---

### 17.3 Enrich (エンリッチメント)

**スキーマ参照**: [appsettings_schema_translated.json:767](appsettings_schema_translated.json#L767)

**説明**: すべてのLogEventsに追加情報を追加します

**type**: array of strings

**環境変数名パターン**: `Serilog__Enrich__0`, `Serilog__Enrich__1`, ...

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "Enrich": [
      "FromLogContext",
      "WithMachineName",
      "WithThreadId",
      "WithEnvironmentName",
      "WithProcessId"
    ]
  }
}
```

**環境変数での設定**:
```bash
Serilog__Enrich__0=FromLogContext
Serilog__Enrich__1=WithMachineName
Serilog__Enrich__2=WithThreadId
```

**一般的なEnricher**:
- `"FromLogContext"`: ログコンテキストからプロパティを追加
- `"WithMachineName"`: マシン名を追加
- `"WithThreadId"`: スレッドIDを追加
- `"WithEnvironmentName"`: 環境名（Development/Production）を追加
- `"WithProcessId"`: プロセスIDを追加
- `"WithProcessName"`: プロセス名を追加
- `"WithEnvironmentUserName"`: ユーザー名を追加

---

### 17.4 WriteTo (出力先)

**スキーマ参照**: [appsettings_schema_translated.json:775](appsettings_schema_translated.json#L775)

**説明**: Sinksリスト（ログ出力先）

**type**: array of objects

**環境変数名パターン**: `Serilog__WriteTo__<index>__Name`, `Serilog__WriteTo__<index>__Args__<property>`

#### Console Sink (コンソール出力)

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "theme": "Serilog.Sinks.SystemConsole.Themes.AnsiConsoleTheme::Code, Serilog.Sinks.Console",
          "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}"
        }
      }
    ]
  }
}
```

**環境変数での設定**:
```bash
Serilog__WriteTo__0__Name=Console
Serilog__WriteTo__0__Args__theme="Serilog.Sinks.SystemConsole.Themes.AnsiConsoleTheme::Code, Serilog.Sinks.Console"
Serilog__WriteTo__0__Args__outputTemplate="[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}"
```

#### File Sink (ファイル出力)

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "WriteTo": [
      {
        "Name": "File",
        "Args": {
          "path": "logs/log-.txt",
          "rollingInterval": "Day",
          "retainedFileCountLimit": 7,
          "outputTemplate": "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] {Message:lj}{NewLine}{Exception}"
        }
      }
    ]
  }
}
```

**環境変数での設定**:
```bash
Serilog__WriteTo__1__Name=File
Serilog__WriteTo__1__Args__path=logs/log-.txt
Serilog__WriteTo__1__Args__rollingInterval=Day
Serilog__WriteTo__1__Args__retainedFileCountLimit=7
```

**File Sinkの主要パラメータ**:
- `path`: ファイルパス（例: `"logs/log-.txt"`, `"logs/log-{Date}.txt"`）
- `rollingInterval`: ローリング間隔（`"Day"`, `"Hour"`, `"Minute"`, `"Infinite"`）
- `retainedFileCountLimit`: 保持するファイル数（例: `7`）
- `fileSizeLimitBytes`: ファイルサイズ制限（例: `1073741824` = 1GB）
- `rollOnFileSizeLimit`: サイズ制限でロール（`true`/`false`）
- `shared`: 複数プロセスでの共有（`true`/`false`）

#### Seq Sink (Seq出力)

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "WriteTo": [
      {
        "Name": "Seq",
        "Args": {
          "serverUrl": "http://localhost:5341",
          "apiKey": "your-api-key"
        }
      }
    ]
  }
}
```

#### Elasticsearch Sink

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "WriteTo": [
      {
        "Name": "Elasticsearch",
        "Args": {
          "nodeUris": "http://localhost:9200",
          "indexFormat": "myapp-logs-{0:yyyy.MM}",
          "autoRegisterTemplate": true,
          "numberOfShards": 2,
          "numberOfReplicas": 1
        }
      }
    ]
  }
}
```

#### Application Insights Sink

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "WriteTo": [
      {
        "Name": "ApplicationInsights",
        "Args": {
          "connectionString": "InstrumentationKey=your-key",
          "telemetryConverter": "Serilog.Sinks.ApplicationInsights.TelemetryConverters.TraceTelemetryConverter, Serilog.Sinks.ApplicationInsights"
        }
      }
    ]
  }
}
```

#### SQL Server Sink

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "WriteTo": [
      {
        "Name": "MSSqlServer",
        "Args": {
          "connectionString": "Server=localhost;Database=Logs;Trusted_Connection=True;",
          "tableName": "Logs",
          "autoCreateSqlTable": true,
          "restrictedToMinimumLevel": "Warning"
        }
      }
    ]
  }
}
```

---

### 17.5 Filter (フィルター)

**スキーマ参照**: [appsettings_schema_translated.json:797](appsettings_schema_translated.json#L797)

**説明**: ログイベントフィルター

**type**: array of objects

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "Filter": [
      {
        "Name": "ByExcluding",
        "Args": {
          "expression": "Contains(RequestPath, '/health')"
        }
      }
    ]
  }
}
```

**一般的なフィルター**:

**特定のメッセージを除外**:
```json
{
  "Filter": [
    {
      "Name": "ByExcluding",
      "Args": {
        "expression": "Contains(SourceContext, 'Microsoft.EntityFrameworkCore')"
      }
    }
  ]
}
```

**特定のメッセージのみ含める**:
```json
{
  "Filter": [
    {
      "Name": "ByIncludingOnly",
      "Args": {
        "expression": "@Level = 'Error' or @Level = 'Fatal'"
      }
    }
  ]
}
```

---

### 17.6 Properties (グローバルプロパティ)

**スキーマ参照**: [appsettings_schema_translated.json:813](appsettings_schema_translated.json#L813)

**説明**: グローバルプロパティをすべてのLogeventsに追加します

**type**: object (additionalProperties)

**環境変数名パターン**: `Serilog__Properties__<PropertyName>`

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "Properties": {
      "Application": "MyApp",
      "Environment": "Production",
      "Version": "1.0.0"
    }
  }
}
```

**環境変数での設定**:
```bash
Serilog__Properties__Application=MyApp
Serilog__Properties__Environment=Production
Serilog__Properties__Version=1.0.0
```

---

### 17.7 Destructure (デストラクチャリング)

**スキーマ参照**: [appsettings_schema_translated.json:825](appsettings_schema_translated.json#L825)

**説明**: セリロッグのオブジェクトデストラクチャリングメカニズムに適用される変換のリスト

**type**: array of objects

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "Destructure": [
      {
        "Name": "ToMaximumDepth",
        "Args": {
          "maximumDestructuringDepth": 4
        }
      },
      {
        "Name": "ToMaximumStringLength",
        "Args": {
          "maximumStringLength": 100
        }
      },
      {
        "Name": "ToMaximumCollectionCount",
        "Args": {
          "maximumCollectionCount": 10
        }
      }
    ]
  }
}
```

---

### 17.8 LevelSwitch (レベルスイッチ)

**スキーマ参照**: [appsettings_schema_translated.json:843](appsettings_schema_translated.json#L843)

**説明**: レベルスイッチは、ログイベントを書くかどうかのレベルを動的に切り替えることができます

**type**: object (additionalProperties)

**設定例（appsettings.json）**:
```json
{
  "Serilog": {
    "LevelSwitch": {
      "$controlSwitch": "Information"
    },
    "MinimumLevel": {
      "ControlledBy": "$controlSwitch"
    }
  }
}
```

---

### 完全なSerilog設定例

**開発環境向け設定** (appsettings.Development.json):
```json
{
  "Serilog": {
    "Using": [
      "Serilog.Sinks.Console",
      "Serilog.Sinks.File"
    ],
    "MinimumLevel": {
      "Default": "Debug",
      "Override": {
        "Microsoft": "Information",
        "Microsoft.AspNetCore": "Warning",
        "System": "Information"
      }
    },
    "Enrich": [
      "FromLogContext",
      "WithMachineName",
      "WithThreadId"
    ],
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "theme": "Serilog.Sinks.SystemConsole.Themes.AnsiConsoleTheme::Code, Serilog.Sinks.Console",
          "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}"
        }
      },
      {
        "Name": "File",
        "Args": {
          "path": "logs/log-.txt",
          "rollingInterval": "Day",
          "outputTemplate": "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] {Message:lj}{NewLine}{Exception}"
        }
      }
    ]
  }
}
```

**本番環境向け設定** (appsettings.Production.json):
```json
{
  "Serilog": {
    "Using": [
      "Serilog.Sinks.Console",
      "Serilog.Sinks.File",
      "Serilog.Sinks.Seq",
      "Serilog.Sinks.ApplicationInsights",
      "Serilog.Enrichers.Environment",
      "Serilog.Enrichers.Thread"
    ],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.AspNetCore": "Warning",
        "Microsoft.EntityFrameworkCore": "Warning",
        "System": "Warning",
        "MyApp": "Information"
      }
    },
    "Enrich": [
      "FromLogContext",
      "WithMachineName",
      "WithThreadId",
      "WithEnvironmentName",
      "WithProcessId"
    ],
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "restrictedToMinimumLevel": "Information",
          "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}"
        }
      },
      {
        "Name": "File",
        "Args": {
          "path": "logs/log-.txt",
          "rollingInterval": "Day",
          "retainedFileCountLimit": 31,
          "outputTemplate": "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] {SourceContext} {Message:lj}{NewLine}{Exception}",
          "restrictedToMinimumLevel": "Information"
        }
      },
      {
        "Name": "File",
        "Args": {
          "path": "logs/errors/error-.txt",
          "rollingInterval": "Day",
          "retainedFileCountLimit": 31,
          "restrictedToMinimumLevel": "Error"
        }
      },
      {
        "Name": "Seq",
        "Args": {
          "serverUrl": "http://seq-server:5341",
          "apiKey": "your-api-key",
          "restrictedToMinimumLevel": "Information"
        }
      },
      {
        "Name": "ApplicationInsights",
        "Args": {
          "connectionString": "InstrumentationKey=your-key",
          "restrictedToMinimumLevel": "Warning"
        }
      }
    ],
    "Filter": [
      {
        "Name": "ByExcluding",
        "Args": {
          "expression": "Contains(RequestPath, '/health')"
        }
      },
      {
        "Name": "ByExcluding",
        "Args": {
          "expression": "Contains(RequestPath, '/metrics')"
        }
      }
    ],
    "Properties": {
      "Application": "MyApp",
      "Environment": "Production"
    },
    "Destructure": [
      {
        "Name": "ToMaximumDepth",
        "Args": {
          "maximumDestructuringDepth": 4
        }
      },
      {
        "Name": "ToMaximumStringLength",
        "Args": {
          "maximumStringLength": 100
        }
      }
    ]
  }
}
```

### Program.cs での Serilog 設定

```csharp
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Serilogの設定を読み込み
builder.Host.UseSerilog((context, services, configuration) => configuration
    .ReadFrom.Configuration(context.Configuration)
    .ReadFrom.Services(services)
    .Enrich.FromLogContext()
    .WriteTo.Console());

var app = builder.Build();

// ログ出力例
app.MapGet("/", (ILogger<Program> logger) =>
{
    logger.LogInformation("Hello World!");
    return "Hello World!";
});

try
{
    Log.Information("Starting web application");
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}
```

### Serilogの使用例

```csharp
public class UserService
{
    private readonly ILogger<UserService> _logger;

    public UserService(ILogger<UserService> logger)
    {
        _logger = logger;
    }

    public async Task<User> GetUserAsync(int userId)
    {
        _logger.LogInformation("Getting user {UserId}", userId);

        try
        {
            var user = await _repository.GetUserAsync(userId);

            if (user == null)
            {
                _logger.LogWarning("User {UserId} not found", userId);
                return null;
            }

            _logger.LogDebug("User details: {@User}", user);
            return user;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting user {UserId}", userId);
            throw;
        }
    }
}
```

### 構造化ロギングの例

```csharp
// シンプルなログ
_logger.LogInformation("User logged in");

// プロパティ付きログ
_logger.LogInformation("User {UserId} logged in at {LoginTime}", userId, DateTime.UtcNow);

// オブジェクトの構造化ログ（@を使用）
_logger.LogInformation("User logged in: {@User}", user);

// 複数のプロパティ
_logger.LogInformation(
    "Order {OrderId} placed by {UserId} for {Amount:C}",
    orderId, userId, amount);
```

### 注意事項

- ? 本番環境では適切なログレベルを設定（`Information`以上）
- ? ログファイルのローテーションを設定（ディスク容量管理）
- ? 機密情報をログに出力しない
- ? 構造化ロギングを活用（`{Property}` 形式）
- ? エラー時は例外オブジェクトも記録
- ? 本番環境で `Debug` や `Verbose` レベルを使用しない
- ? ループ内で大量のログを出力しない

---

これでSerilogの設定は完了です。
