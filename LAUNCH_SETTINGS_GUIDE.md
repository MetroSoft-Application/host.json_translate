# launchSettings.json 設定ガイド

Visual Studio / dotnet CLI で使う `Properties/launchSettings.json` の主要項目をまとめました。プロファイルごとの実行方法を整理し、ローカルデバッグを安全に行うための参考にしてください。

## まとめ

- プロファイル(`profiles`)単位で実行方法を切り替え、IIS Express / IIS / Docker / Console などに対応。
- 共通項目でブラウザ起動、URL、環境変数、リモートデバッグ、ホットリロード等を制御。
- `iisSettings` で IIS / IIS Express の認証やバインド設定を共通管理。
- 既定値を理解したうえで、プロジェクト特性（Web/コンソール/コンテナ）に合わせて最小限を上書き。
- シークレットは環境変数やユーザーシークレットに分離し、`launchSettings.json` は共有可能な情報のみを保持。

### 設定のポイント

1. **プロファイル名を用途別に分ける**（通常実行、Docker、IIS Express、リモートデバッグなど）。
2. **`commandName` を正しく選択**（`Project` / `Docker` / `IISExpress` など）。
3. **ブラウザ起動とURL**は Web のみ有効化し、API/コンソールでは無効化。
4. **ポート/URLの衝突に注意**（`applicationUrl`/`httpPort`/`sslPort`）。
5. **ホットリロード/ネイティブデバッグ**は必要時のみ有効化し、起動負荷を最小化。

### 設定カテゴリ別サマリー

- ルート設定: 2設定 (`profiles`, `iisSettings`)
- IIS/IIS Express 共通: 4設定
- プロファイル共通: 26設定

### 参照リンク

- [launchSettings.json スキーマ (英語)](launch_schema.json)
- [VS の launchSettings.json 解説](https://learn.microsoft.com/ja-jp/visualstudio/debugger/launch-settings-manager)
- [ASP.NET Core ローカル開発のポートと証明書](https://learn.microsoft.com/ja-jp/aspnet/core/security/enforcing-ssl)

---

## 目次

- [ルート設定](#ルート設定)
  - [profiles](#profiles)
  - [iisSettings](#iissettings)
- [IIS/IIS-Express 共通設定](#iisiis-express-共通設定)
  - [windowsAuthentication](#windowsauthentication)
  - [anonymousAuthentication](#anonymousauthentication)
  - [iisExpress / iis](#iisexpress--iis)
  - [applicationUrl (IIS バインド)](#applicationurl-iis-バインド)
  - [sslPort (IIS バインド)](#sslport-iis-バインド)
- [プロファイル共通設定](#プロファイル共通設定)
  - [commandName](#commandname)
  - [commandLineArgs](#commandlineargs)
  - [executablePath](#executablepath)
  - [workingDirectory](#workingdirectory)
  - [launchBrowser](#launchbrowser)
  - [launchUrl](#launchurl)
  - [environmentVariables](#environmentvariables)
  - [applicationUrl (プロファイル)](#applicationurl-プロファイル)
  - [nativeDebugging](#nativedebugging)
  - [externalUrlConfiguration](#externalurlconfiguration)
  - [use64Bit](#use64bit)
  - [ancmHostingModel](#ancmhostingmodel)
  - [sqlDebugging](#sqldebugging)
  - [jsWebView2Debugging](#jswebview2debugging)
  - [leaveRunningOnClose](#leaverunningonclose)
  - [remoteDebugEnabled](#remotedebugenabled)
  - [remoteDebugMachine](#remotedebugmachine)
  - [authenticationMode](#authenticationmode)
  - [hotReloadEnabled](#hotreloadenabled)
  - [publishAllPorts](#publishallports)
  - [useSSL](#usessl)
  - [sslPort (プロファイル)](#sslport-プロファイル)
  - [httpPort](#httpport)
  - [dotnetRunMessages](#dotnetrunmessages)
  - [inspectUri](#inspecturi)
  - [targetProject](#targetproject)

---

## ルート設定

### profiles

**スキーマ参照**: [launch_schema_translated.json:231](launch_schema_translated.json#L231)  
**説明**: デバッグプロファイルの一覧（任意のプロファイル名をキーに `profile` オブジェクトを格納）。  
**デフォルト値**: なし（空でも可）。

**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "MyApp": {
      "commandName": "Project"
    }
  }
}
```

**推奨設定**:
- 用途ごとにプロファイルを分けて管理（例: `Project`, `IIS Express`, `Docker`, `WSL2`）。
- CI用など不要なプロファイルは含めない。

---

### iisSettings

**スキーマ参照**: [launch_schema_translated.json:238](launch_schema_translated.json#L238)  
**説明**: IIS / IIS Express 向けの共通サイト設定。  
**デフォルト値**: なし（未指定時は既定設定）。

**設定例**:
```json
{
  "iisSettings": {
    "windowsAuthentication": false,
    "anonymousAuthentication": true,
    "iisExpress": {
      "applicationUrl": "http://localhost:5000",
      "sslPort": 5001
    }
  }
}
```

**推奨設定**:
- 認証は基本 `anonymousAuthentication: true`, `windowsAuthentication: false` とし、必要なときのみ反転。
- `applicationUrl`/`sslPort` はプロファイルと矛盾しない値に調整。

---

## IIS/IIS-Express 共通設定（`iisSettings` 配下）

### windowsAuthentication

**スキーマ参照**: [launch_schema_translated.json:26](launch_schema_translated.json#L26)  
**説明**: IIS/IIS Express で Windows 認証を有効にするか。  
**デフォルト値**: `false`  
**推奨設定**:
- 社内イントラで Windows 認証が必要な場合のみ `true`。

---

### anonymousAuthentication

**スキーマ参照**: [launch_schema_translated.json:31](launch_schema_translated.json#L31)  
**説明**: IIS/IIS Express で匿名認証を有効にするか。  
**デフォルト値**: `true`  
**推奨設定**:
- 認証を別途実装する場合は `true` のまま。

---

### iisExpress / iis

**スキーマ参照**: [launch_schema_translated.json:36](launch_schema_translated.json#L36), [launch_schema_translated.json:45](launch_schema_translated.json#L45)  
**説明**: 各ホストのバインド設定（`applicationUrl`, `sslPort` を指定）。  
**デフォルト値**: なし。  
**設定例**:
```json
{
  "iisSettings": {
    "iisExpress": {
      "applicationUrl": "http://localhost:5000",
      "sslPort": 5001
    }
  }
}
```

**推奨設定**:
- HTTP/HTTPS ポートは他アプリと重複しない値にする。
- SSLが不要なら `sslPort: 0` で無効化。

---

### applicationUrl (IIS バインド)

**スキーマ参照**: [launch_schema_translated.json:58](launch_schema_translated.json#L58)  
**説明**: サイトのURL。`iis`/`iisExpress` で使用。  
**デフォルト値**: `""`  
**設定例 (launchSettings.json 内)**:
```json
{
  "iisSettings": {
    "iisExpress": {
      "applicationUrl": "http://localhost:5000"
    }
  }
}
```
**推奨設定**: ループバック (例: `http://localhost:5000`) を指定。

---

### sslPort (IIS バインド)

**スキーマ参照**: [launch_schema_translated.json:64](launch_schema_translated.json#L64)  
**説明**: サイトのSSLポート。`0` で無効。  
**デフォルト値**: `0`  
**設定例 (launchSettings.json 内)**:
```json
{
  "iisSettings": {
    "iisExpress": {
      "sslPort": 5001
    }
  }
}
```
**推奨設定**: HTTPSを使う場合は空きポートを指定し、証明書を信頼済みにする。

---

## プロファイル共通設定（`profiles.<name>` 配下）

### commandName

**スキーマ参照**: [launch_schema_translated.json:75](launch_schema_translated.json#L75)  
**説明**: 実行するターゲット種別。`Project`/`Executable`/`IISExpress`/`Docker` など。  
**デフォルト値**: `""` (必須)  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "MyApp": {
      "commandName": "Project"
    }
  }
}
```
**推奨設定**:
- 通常の .NET プロジェクト: `Project`
- IIS Express: `IISExpress`
- Docker: `Docker` または `DockerCompose`

---

### commandLineArgs

**スキーマ参照**: [launch_schema_translated.json:93](launch_schema_translated.json#L93)  
**説明**: 起動時に渡す引数。  
**デフォルト値**: `""`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "MyApp": {
      "commandLineArgs": "--urls http://*:5000 --environment Development"
    }
  }
}
```
**推奨設定**: 必要なときのみ明示し、長大な引数はスクリプトに切り出す。

---

### executablePath

**スキーマ参照**: [launch_schema_translated.json:98](launch_schema_translated.json#L98)  
**説明**: 実行可能ファイルへの絶対/相対パス（`commandName: Executable` 用）。  
**デフォルト値**: `""`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "MyTool": {
      "commandName": "Executable",
      "executablePath": ".\\tools\\myapp.exe"
    }
  }
}
```
**推奨設定**: リポジトリ内の相対パスを使用し、環境差分を減らす。

---

### workingDirectory

**スキーマ参照**: [launch_schema_translated.json:103](launch_schema_translated.json#L103)  
**説明**: 実行時の作業ディレクトリ。  
**デフォルト値**: なし  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "MyApp": {
      "workingDirectory": "."
    }
  }
}
```
**推奨設定**: `$(ProjectDir)` 相当のプロジェクトルートを指定する。

---

### launchBrowser

**スキーマ参照**: [launch_schema_translated.json:107](launch_schema_translated.json#L107)  
**説明**: 起動時にブラウザを開くか。  
**デフォルト値**: `false`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "launchBrowser": true
    }
  }
}
```
**推奨設定**: Web アプリのみ `true`。API/コンソールでは `false`。

---

### launchUrl

**スキーマ参照**: [launch_schema_translated.json:112](launch_schema_translated.json#L112)  
**説明**: ブラウザで開く相対URL。  
**デフォルト値**: なし  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "launchUrl": "swagger"
    }
  }
}
```
**推奨設定**: `swagger` など開発開始ページを指定。

---

### environmentVariables

**スキーマ参照**: [launch_schema_translated.json:116](launch_schema_translated.json#L116)  
**説明**: 環境変数 (key/value)。  
**デフォルト値**: なし  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}
```
**推奨設定**: シークレットは含めず、ローカル用の非機密値のみ記載。

---

### applicationUrl (プロファイル)

**スキーマ参照**: [launch_schema_translated.json:123](launch_schema_translated.json#L123)  
**説明**: Web サーバーの URL 一覧（`;` 区切り）。  
**デフォルト値**: なし  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "applicationUrl": "http://localhost:5000;https://localhost:5001"
    }
  }
}
```
**推奨設定**: HTTP/HTTPS のセットを指定し、`iisSettings` と整合させる。

---

### nativeDebugging

**スキーマ参照**: [launch_schema_translated.json:127](launch_schema_translated.json#L127)  
**説明**: ネイティブコードのデバッグを有効化。  
**デフォルト値**: `false`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "NativeApp": {
      "nativeDebugging": true
    }
  }
}
```
**推奨設定**: ネイティブ連携が必要な場合のみ `true`（起動が重くなる）。

---

### externalUrlConfiguration

**スキーマ参照**: [launch_schema_translated.json:132](launch_schema_translated.json#L132)  
**説明**: ASP.NET Core プロファイル実行時にサイト構成の自動設定を無効化。  
**デフォルト値**: `false`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "externalUrlConfiguration": true
    }
  }
}
```
**推奨設定**: 外部でURL管理している場合のみ `true`。

---

### use64Bit

**スキーマ参照**: [launch_schema_translated.json:137](launch_schema_translated.json#L137)  
**説明**: IIS Express を64bitで起動するか。`false`ならx86。  
**デフォルト値**: `true`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "IIS Express": {
      "use64Bit": true
    }
  }
}
```
**推奨設定**: 64bitのみ必要がない場合以外は `true` のまま。

---

### ancmHostingModel

**スキーマ参照**: [launch_schema_translated.json:142](launch_schema_translated.json#L142)  
**説明**: IIS/IIS Express での ASP.NET Core ホスティングモデル (`InProcess`/`OutOfProcess`)。  
**デフォルト値**: `false`（スキーマ既定。未指定扱い）  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "IIS Express": {
      "ancmHostingModel": "InProcess"
    }
  }
}
```
**推奨設定**: .NET 6+ 既定の `InProcess` を明示する場合に指定。

---

### sqlDebugging

**スキーマ参照**: [launch_schema_translated.json:150](launch_schema_translated.json#L150)  
**説明**: SQL スクリプト/ストアドのデバッグを有効化。  
**デフォルト値**: `false`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "DbApp": {
      "sqlDebugging": true
    }
  }
}
```
**推奨設定**: DB ステップ実行が必要な場合のみ `true`。

---

### jsWebView2Debugging

**スキーマ参照**: [launch_schema_translated.json:155](launch_schema_translated.json#L155)  
**説明**: WebView2 (Edge Chromium) の JS デバッガーを有効化。  
**デフォルト値**: `false`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "HybridApp": {
      "jsWebView2Debugging": true
    }
  }
}
```
**推奨設定**: ハイブリッドアプリ検証時のみ `true`。

---

### leaveRunningOnClose

**スキーマ参照**: [launch_schema_translated.json:160](launch_schema_translated.json#L160)  
**説明**: プロジェクト終了時に IIS アプリプールを停止せず残す。  
**デフォルト値**: `false`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "IIS Express": {
      "leaveRunningOnClose": true
    }
  }
}
```
**推奨設定**: セッションを維持したい長時間デバッグ時のみ `true`。

---

### remoteDebugEnabled

**スキーマ参照**: [launch_schema_translated.json:165](launch_schema_translated.json#L165)  
**説明**: リモートコンピューターのプロセスへ接続するか。  
**デフォルト値**: `false`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "Remote": {
      "remoteDebugEnabled": true
    }
  }
}
```
**推奨設定**: リモート検証時のみ `true`。

---

### remoteDebugMachine

**スキーマ参照**: [launch_schema_translated.json:170](launch_schema_translated.json#L170)  
**説明**: リモートマシン名とポート (`name:port`)。  
**デフォルト値**: なし  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "Remote": {
      "remoteDebugMachine": "machine01:4026"
    }
  }
}
```
**推奨設定**: `remoteDebugEnabled: true` の場合のみ設定。

---

### authenticationMode

**スキーマ参照**: [launch_schema_translated.json:174](launch_schema_translated.json#L174)  
**説明**: リモート接続時の認証方式 (`None`/`Windows`)。  
**デフォルト値**: `None`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "Remote": {
      "authenticationMode": "Windows"
    }
  }
}
```
**推奨設定**: ドメイン参加マシンでは `Windows` を検討。

---

### hotReloadEnabled

**スキーマ参照**: [launch_schema_translated.json:182](launch_schema_translated.json#L182)  
**説明**: 実行中アプリへのホットリロードを有効化。  
**デフォルト値**: `true`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "hotReloadEnabled": true
    }
  }
}
```
**推奨設定**: パフォーマンス問題がある場合のみ `false` にする。

---

### publishAllPorts

**スキーマ参照**: [launch_schema_translated.json:187](launch_schema_translated.json#L187)  
**説明**: Docker で公開ポートをランダムに割り当てる (-P)。  
**デフォルト値**: `true`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "Docker": {
      "commandName": "Docker",
      "publishAllPorts": false
    }
  }
}
```
**推奨設定**: 固定ポートが必要なら `false` にして `ports` を明示。

---

### useSSL

**スキーマ参照**: [launch_schema_translated.json:192](launch_schema_translated.json#L192)  
**説明**: SSL ポートをバインドするか。  
**デフォルト値**: `true`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "useSSL": true
    }
  }
}
```
**推奨設定**: HTTPS 検証が不要な場合のみ `false`。

---

### sslPort (プロファイル)

**スキーマ参照**: [launch_schema_translated.json:197](launch_schema_translated.json#L197)  
**説明**: プロファイルで使用する SSL ポート。  
**デフォルト値**: `0`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "sslPort": 5001
    }
  }
}
```
**推奨設定**: HTTPS を使うときのみ空きポートを設定。

---

### httpPort

**スキーマ参照**: [launch_schema_translated.json:204](launch_schema_translated.json#L204)  
**説明**: プロファイルで使用する HTTP ポート。  
**デフォルト値**: `0`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "WebApp": {
      "httpPort": 5000
    }
  }
}
```
**推奨設定**: 複数プロジェクト併用時は衝突しない値に変更。

---

### dotnetRunMessages

**スキーマ参照**: [launch_schema_translated.json:211](launch_schema_translated.json#L211)  
**説明**: ビルド時の `dotnet run` メッセージ表示を有効化。  
**デフォルト値**: `true`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "ConsoleApp": {
      "dotnetRunMessages": false
    }
  }
}
```
**推奨設定**: 冗長出力を避けたい場合のみ `false`。

---

### inspectUri

**スキーマ参照**: [launch_schema_translated.json:216](launch_schema_translated.json#L216)  
**説明**: Blazor WASM 用のデバッグ URI。  
**デフォルト値**: `{wsProtocol}://{url.hostname}:{url.port}/_framework/debug/ws-proxy?browser={browserInspectUri}`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "BlazorWasm": {
      "inspectUri": "ws://localhost:5000/_framework/debug/ws-proxy?browser=ws://127.0.0.1:9222/devtools/browser"
    }
  }
}
```
**推奨設定**: 既定のまま利用し、ポートカスタム時のみ合わせる。

---

### targetProject

**スキーマ参照**: [launch_schema_translated.json:221](launch_schema_translated.json#L221)  
**説明**: Roslyn コンポーネントを実行する対象 .NET プロジェクトへの相対/絶対パス。  
**デフォルト値**: `""`  
**設定例 (launchSettings.json 内)**:
```json
{
  "profiles": {
    "Roslyn": {
      "targetProject": "..\\src\\MyAnalyzer\\MyAnalyzer.csproj"
    }
  }
}
```
**推奨設定**: Roslyn 拡張やソースジェネレーター検証時のみ指定。
