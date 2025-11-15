# Azure Functions host.json 設定ガイド

このドキュメントは、Azure Functions の host.json 設定項目を環境変数として Azure Portal で設定する方法を説明します。

## まとめ

このガイドでは、Azure Functions の host.json 設定を Azure Portal の環境変数として構成する方法を説明しています。全106設定について、デフォルト値、環境変数名、設定例、推奨設定を提供しています。

### 設定のポイント

1. **環境変数の命名規則**: `AzureFunctionsJobHost__` プレフィックスに続いて、階層をダブルアンダースコア (`__`) で区切ります
2. **slotSetting**: デプロイスロット固有の設定が必要な場合は `true` に設定します
3. **デフォルト値の理解**: 各設定のデフォルト値を理解し、必要な場合のみ上書きします
4. **環境別の設定**: 開発、ステージング、本番環境で異なる値を使用することを推奨します

### 設定カテゴリ別サマリー

- **拡張バンドル**: 2設定
- **集約**: 2設定
- **関数タイムアウト**: 1設定
- **シングルトン**: 4設定
- **ヘルスモニター**: 5設定
- **HTTP拡張**: 4設定
- **キュー拡張**: 4設定
- **Durable Functions**: 18設定
- **Cosmos DB**: 2設定
- **Service Bus**: 34設定
- **Event Hubs**: 16設定
- **Blobs**: 2設定
- **ロギング**: 27設定 (Application Insightsサンプリング設定含む)
- **その他**: 11設定 (マネージド依存関係、カスタムハンドラー、同時実行など)

**合計**: 106設定

### 参考リンク

- [Azure Functions の host.json リファレンス](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-host-json)
- [Azure Functions のアプリケーション設定](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-app-settings)
- [Azure Portal での環境変数設定](https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-how-to-use-azure-function-app-settings)

---

## 目次

- [Azure Functions host.json 設定ガイド](#azure-functions-hostjson-設定ガイド)
  - [まとめ](#まとめ)
    - [設定のポイント](#設定のポイント)
    - [設定カテゴリ別サマリー](#設定カテゴリ別サマリー)
    - [参考リンク](#参考リンク)
  - [目次](#目次)
  - [拡張バンドル設定](#拡張バンドル設定)
    - [extensionBundle.id](#extensionbundleid)
    - [extensionBundle.version](#extensionbundleversion)
  - [集約設定](#集約設定)
    - [aggregator.batchSize](#aggregatorbatchsize)
    - [aggregator.flushTimeout](#aggregatorflushtimeout)
  - [関数タイムアウト設定](#関数タイムアウト設定)
    - [functionTimeout](#functiontimeout)
  - [シングルトン設定](#シングルトン設定)
    - [singleton.lockPeriod](#singletonlockperiod)
    - [singleton.listenerLockPeriod](#singletonlistenerlockperiod)
    - [singleton.listenerLockRecoveryPollingInterval](#singletonlistenerlockrecoverypollinginterval)
    - [singleton.lockAcquisitionTimeout](#singletonlockacquisitiontimeout)
    - [singleton.lockAcquisitionPollingInterval](#singletonlockacquisitionpollinginterval)
  - [ヘルスモニター設定](#ヘルスモニター設定)
    - [healthMonitor.enabled](#healthmonitorenabled)
    - [healthMonitor.healthCheckInterval](#healthmonitorhealthcheckinterval)
    - [healthMonitor.healthCheckWindow](#healthmonitorhealthcheckwindow)
    - [healthMonitor.healthCheckThreshold](#healthmonitorhealthcheckthreshold)
    - [healthMonitor.counterThreshold](#healthmonitorcounterthreshold)
  - [HTTP拡張設定](#http拡張設定)
    - [extensions.http.routePrefix](#extensionshttprouteprefix)
    - [extensions.http.maxConcurrentRequests](#extensionshttpmaxconcurrentrequests)
    - [extensions.http.maxOutstandingRequests](#extensionshttpmaxoutstandingrequests)
    - [extensions.http.dynamicThrottlesEnabled](#extensionshttpdynamicthrottlesenabled)
  - [キュー拡張設定](#キュー拡張設定)
    - [extensions.queues.maxPollingInterval](#extensionsqueuesmaxpollinginterval)
    - [extensions.queues.batchSize](#extensionsqueuesbatchsize)
    - [extensions.queues.maxDequeueCount](#extensionsqueuesmaxdequeuecount)
    - [extensions.queues.visibilityTimeout](#extensionsqueuesvisibilitytimeout)
    - [extensions.queues.newBatchThreshold](#extensionsqueuesnewbatchthreshold)
    - [extensions.queues.messageEncoding](#extensionsqueuesmessageencoding)
  - [Durable Functions設定](#durable-functions設定)
    - [extensions.durableTask.hubName](#extensionsdurabletaskhubname)
    - [extensions.durableTask.storageProvider.controlQueueBatchSize](#extensionsdurabletaskstorageprovidercontrolqueuebatchsize)
    - [extensions.durableTask.storageProvider.controlQueueBufferThreshold](#extensionsdurabletaskstorageprovidercontrolqueuebufferthreshold)
    - [extensions.durableTask.storageProvider.controlQueueVisibilityTimeout](#extensionsdurabletaskstorageprovidercontrolqueuevisibilitytimeout)
    - [extensions.durableTask.storageProvider.maxQueuePollingInterval](#extensionsdurabletaskstorageprovidermaxqueuepollinginterval)
    - [extensions.durableTask.storageProvider.partitionCount](#extensionsdurabletaskstorageproviderpartitioncount)
    - [extensions.durableTask.storageProvider.useLegacyPartitionManagement](#extensionsdurabletaskstorageprovideruselegacypartitionmanagement)
    - [extensions.durableTask.storageProvider.workItemQueueVisibilityTimeout](#extensionsdurabletaskstorageproviderworkitemqueuevisibilitytimeout)
    - [extensions.durableTask.tracing.traceInputsAndOutputs](#extensionsdurabletasktracingtraceinputsandoutputs)
    - [extensions.durableTask.tracing.traceReplayEvents](#extensionsdurabletasktracingtracereplayevents)
    - [extensions.durableTask.notifications.eventGrid.topicEndpoint](#extensionsdurabletasknotificationseventgridtopicendpoint)
    - [extensions.durableTask.notifications.eventGrid.keySettingName](#extensionsdurabletasknotificationseventgridkeysettingname)
    - [extensions.durableTask.notifications.eventGrid.publishRetryCount](#extensionsdurabletasknotificationseventgridpublishretrycount)
    - [extensions.durableTask.notifications.eventGrid.publishRetryInterval](#extensionsdurabletasknotificationseventgridpublishretryinterval)
    - [extensions.durableTask.notifications.eventGrid.publishEventTypes](#extensionsdurabletasknotificationseventgridpublisheventtypes)
    - [extensions.durableTask.maxConcurrentActivityFunctions](#extensionsdurabletaskmaxconcurrentactivityfunctions)
    - [extensions.durableTask.maxConcurrentOrchestratorFunctions](#extensionsdurabletaskmaxconcurrentorchestratorfunctions)
    - [extensions.durableTask.extendedSessionsEnabled](#extensionsdurabletaskextendedsessionsenabled)
    - [extensions.durableTask.extendedSessionIdleTimeoutInSeconds](#extensionsdurabletaskextendedsessionidletimeoutinseconds)
    - [extensions.durableTask.useAppLease](#extensionsdurabletaskuseapplease)
    - [extensions.durableTask.useGracefulShutdown](#extensionsdurabletaskusegracefulshutdown)
    - [extensions.durableTask.maxEntityOperationBatchSize](#extensionsdurabletaskmaxentityoperationbatchsize)
    - [extensions.durableTask.useTablePartitionManagement](#extensionsdurabletaskusetablepartitionmanagement)
  - [Cosmos DB設定](#cosmos-db設定)
    - [extensions.cosmosDB.connectionMode](#extensionscosmosdbconnectionmode)
    - [extensions.cosmosDB.protocol](#extensionscosmosdbprotocol)
    - [extensions.cosmosDB.leaseOptions.leasePrefix](#extensionscosmosdbleaseoptionsleaseprefix)
  - [Service Bus設定](#service-bus設定)
    - [extensions.serviceBus.transportType](#extensionsservicebustransporttype)
    - [extensions.serviceBus.prefetchCount](#extensionsservicebusprefetchcount)
    - [extensions.serviceBus.autoCompleteMessages](#extensionsservicebusautocompletemessages)
    - [extensions.serviceBus.maxAutoLockRenewalDuration](#extensionsservicebusmaxautolockrenewalduration)
    - [extensions.serviceBus.maxConcurrentCalls](#extensionsservicebusmaxconcurrentcalls)
    - [extensions.serviceBus.maxConcurrentSessions](#extensionsservicebusmaxconcurrentsessions)
    - [extensions.serviceBus.maxMessageBatchSize](#extensionsservicebusmaxmessagebatchsize)
    - [extensions.serviceBus.sessionIdleTimeout](#extensionsservicebussessionidletimeout)
    - [extensions.serviceBus.clientRetryOptions.mode](#extensionsservicebusclientretryoptionsmode)
    - [extensions.serviceBus.clientRetryOptions.tryTimeout](#extensionsservicebusclientretryoptionstrytimeout)
    - [extensions.serviceBus.clientRetryOptions.delay](#extensionsservicebusclientretryoptionsdelay)
    - [extensions.serviceBus.clientRetryOptions.maxDelay](#extensionsservicebusclientretryoptionsmaxdelay)
    - [extensions.serviceBus.clientRetryOptions.maxRetries](#extensionsservicebusclientretryoptionsmaxretries)
    - [extensions.serviceBus.processorOptions.maxConcurrentCalls](#extensionsservicebusprocessoroptionsmaxconcurrentcalls)
    - [extensions.serviceBus.processorOptions.prefetchCount](#extensionsservicebusprocessoroptionsprefetchcount)
    - [extensions.serviceBus.processorOptions.autoCompleteMessages](#extensionsservicebusprocessoroptionsautocompletemessages)
    - [extensions.serviceBus.processorOptions.maxAutoLockRenewalDuration](#extensionsservicebusprocessoroptionsmaxautolockrenewalduration)
    - [extensions.serviceBus.sessionProcessorOptions.maxConcurrentSessions](#extensionsservicebussessionprocessoroptionsmaxconcurrentsessions)
    - [extensions.serviceBus.sessionProcessorOptions.maxConcurrentCallsPerSession](#extensionsservicebussessionprocessoroptionsmaxconcurrentcallspersession)
    - [extensions.serviceBus.sessionProcessorOptions.sessionIdleTimeout](#extensionsservicebussessionprocessoroptionssessionidletimeout)
    - [extensions.serviceBus.sessionProcessorOptions.autoCompleteMessages](#extensionsservicebussessionprocessoroptionsautocompletemessages)
    - [extensions.serviceBus.sessionProcessorOptions.maxAutoLockRenewalDuration](#extensionsservicebussessionprocessoroptionsmaxautolockrenewalduration)
    - [extensions.serviceBus.enableCrossEntityTransactions](#extensionsservicebusenablecrossentitytransactions)
    - [extensions.serviceBus.maxBatchWaitTime](#extensionsservicebusmaxbatchwaittime)
    - [extensions.serviceBus.batchOptions.autoComplete](#extensionsservicebusbatchoptionsautocomplete)
    - [extensions.serviceBus.batchOptions.maxMessageCount](#extensionsservicebusbatchoptionsmaxmessagecount)
    - [extensions.serviceBus.batchOptions.operationTimeout](#extensionsservicebusbatchoptionsoperationtimeout)
    - [extensions.serviceBus.messageHandlerOptions.autoComplete](#extensionsservicebusmessagehandleroptionsautocomplete)
    - [extensions.serviceBus.messageHandlerOptions.maxAutoRenewDuration](#extensionsservicebusmessagehandleroptionsmaxautorenewduration)
    - [extensions.serviceBus.messageHandlerOptions.maxConcurrentCalls](#extensionsservicebusmessagehandleroptionsmaxconcurrentcalls)
    - [extensions.serviceBus.sessionHandlerOptions.autoComplete](#extensionsservicebussessionhandleroptionsautocomplete)
    - [extensions.serviceBus.sessionHandlerOptions.maxAutoRenewDuration](#extensionsservicebussessionhandleroptionsmaxautorenewduration)
    - [extensions.serviceBus.sessionHandlerOptions.maxConcurrentSessions](#extensionsservicebussessionhandleroptionsmaxconcurrentsessions)
    - [extensions.serviceBus.sessionHandlerOptions.messageWaitTimeout](#extensionsservicebussessionhandleroptionsmessagewaittimeout)
  - [Event Hubs設定](#event-hubs設定)
    - [extensions.eventHubs.maxEventBatchSize](#extensionseventhubsmaxeventbatchsize)
    - [extensions.eventHubs.minEventBatchSize](#extensionseventhubsmineventbatchsize)
    - [extensions.eventHubs.targetUnprocessedEventThreshold](#extensionseventhubstargetunprocessedeventthreshold)
    - [extensions.eventHubs.clientRetryOptions.mode](#extensionseventhubsclientretryoptionsmode)
    - [extensions.eventHubs.clientRetryOptions.tryTimeout](#extensionseventhubsclientretryoptionstrytimeout)
    - [extensions.eventHubs.clientRetryOptions.delay](#extensionseventhubsclientretryoptionsdelay)
    - [extensions.eventHubs.clientRetryOptions.maxDelay](#extensionseventhubsclientretryoptionsmaxdelay)
    - [extensions.eventHubs.clientRetryOptions.maxRetries](#extensionseventhubsclientretryoptionsmaxretries)
    - [extensions.eventHubs.loadBalancingUpdateInterval](#extensionseventhubsloadbalancingupdateinterval)
    - [extensions.eventHubs.partitionOwnershipExpirationInterval](#extensionseventhubspartitionownershipexpirationinterval)
    - [extensions.eventHubs.batchCheckpointFrequency](#extensionseventhubsbatchcheckpointfrequency)
    - [extensions.eventHubs.initialOffsetOptions.type](#extensionseventhubsinitialoffsetoptionstype)
    - [extensions.eventHubs.prefetchCount](#extensionseventhubsprefetchcount)
    - [extensions.eventHubs.transportType](#extensionseventhubstransporttype)
  - [Blobs設定](#blobs設定)
    - [extensions.blobs.maxDegreeOfParallelism](#extensionsblobsmaxdegreeofparallelism)
    - [extensions.blobs.poisonBlobThreshold](#extensionsblobspoisonblobthreshold)
  - [ログ設定](#ログ設定)
    - [logging.logLevel.default](#logginglogleveldefault)
    - [logging.logLevel.Function](#loggingloglevelfunction)
    - [logging.logLevel.Host.Aggregator](#loggingloglevelhostaggregator)
    - [logging.logLevel.Host.Results](#loggingloglevelhostresults)
    - [logging.applicationInsights.samplingSettings.isEnabled](#loggingapplicationinsightssamplingsettingsisenabled)
    - [logging.applicationInsights.samplingSettings.maxTelemetryItemsPerSecond](#loggingapplicationinsightssamplingsettingsmaxtelemetryitemspersecond)
    - [logging.applicationInsights.samplingSettings.excludedTypes](#loggingapplicationinsightssamplingsettingsexcludedtypes)
    - [logging.applicationInsights.samplingSettings.includedTypes](#loggingapplicationinsightssamplingsettingsincludedtypes)
    - [logging.applicationInsights.snapshotConfiguration.isEnabled](#loggingapplicationinsightssnapshotconfigurationisenabled)
    - [logging.applicationInsights.enableLiveMetricsFilters](#loggingapplicationinsightsenablelivemetricsfilters)
    - [logging.applicationInsights.enableDependencyTracking](#loggingapplicationinsightsenabledependencytracking)
    - [logging.applicationInsights.enablePerformanceCountersCollection](#loggingapplicationinsightsenableperformancecounterscollection)
    - [logging.applicationInsights.httpAutoCollectionOptions.enableHttpTriggerExtendedInfoCollection](#loggingapplicationinsightshttpautocollectionoptionsenablehttptriggerextendedinfocollection)
    - [logging.applicationInsights.httpAutoCollectionOptions.enableResponseHeaderInjection](#loggingapplicationinsightshttpautocollectionoptionsenableresponseheaderinjection)
    - [logging.applicationInsights.httpAutoCollectionOptions.enableW3CDistributedTracing](#loggingapplicationinsightshttpautocollectionoptionsenablew3cdistributedtracing)
    - [logging.fileLoggingMode](#loggingfileloggingmode)
    - [logging.console.isEnabled](#loggingconsoleisenabled)
    - [extensions.applicationInsights.enableLiveMetrics](#extensionsapplicationinsightsenablelivemetrics)
    - [extensions.applicationInsights.enableW3CDistributedTracing](#extensionsapplicationinsightsenablew3cdistributedtracing)
    - [extensions.applicationInsights.samplingSettings.evaluationInterval](#extensionsapplicationinsightssamplingsettingsevaluationinterval)
    - [extensions.applicationInsights.samplingSettings.initialSamplingPercentage](#extensionsapplicationinsightssamplingsettingsinitialsamplingpercentage)
    - [extensions.applicationInsights.samplingSettings.maxSamplingPercentage](#extensionsapplicationinsightssamplingsettingsmaxsamplingpercentage)
    - [extensions.applicationInsights.samplingSettings.minSamplingPercentage](#extensionsapplicationinsightssamplingsettingsminsamplingpercentage)
    - [extensions.applicationInsights.samplingSettings.movingAverageRatio](#extensionsapplicationinsightssamplingsettingsmovingaverageratio)
    - [extensions.applicationInsights.samplingSettings.samplingPercentageDecreaseTimeout](#extensionsapplicationinsightssamplingsettingssamplingpercentagedecreasetimeout)
    - [extensions.applicationInsights.samplingSettings.samplingPercentageIncreaseTimeout](#extensionsapplicationinsightssamplingsettingssamplingpercentageincreasetimeout)
  - [その他の設定](#その他の設定)
    - [managedDependency.enabled](#manageddependencyenabled)
    - [customHandler.description.defaultExecutablePath](#customhandlerdescriptiondefaultexecutablepath)
    - [concurrency.dynamicConcurrencyEnabled](#concurrencydynamicconcurrencyenabled)
    - [concurrency.maximumFunctionConcurrency](#concurrencymaximumfunctionconcurrency)
    - [sendCanceledInvocationsToWorker](#sendcanceledinvocationstoworker)
    - [concurrency.snapshotPersistenceEnabled](#concurrencysnapshotpersistenceenabled)
    - [customHandler.enableForwardingHttpRequest](#customhandlerenableforwardinghttprequest)

---

## 拡張バンドル設定

拡張バンドルを使用すると、Functions の拡張機能を簡単に管理できます。

### extensionBundle.id

**スキーマ参照**: [host_schema_translated.json:652](host_schema_translated.json#L652)

**説明**: 拡張バンドルのID

**デフォルト値**: `Microsoft.Azure.Functions.ExtensionBundle`

**環境変数名**: `AzureFunctionsJobHost__extensionBundle__id`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensionBundle__id",
  "value": "Microsoft.Azure.Functions.ExtensionBundle",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle"
  }
}
```

---

### extensionBundle.version

**スキーマ参照**: [host_schema_translated.json:657](host_schema_translated.json#L657)

**説明**: 拡張バンドルのバージョン範囲

**デフォルト値**: `[2.*, 3.0.0)`

**環境変数名**: `AzureFunctionsJobHost__extensionBundle__version`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensionBundle__version",
  "value": "[2.*, 3.0.0)",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensionBundle": {
    "version": "[2.*, 3.0.0)"
  }
}
```

**バージョン指定の例**:
- `[3.*, 4.0.0)`: バージョン3系の最新を使用（4.0.0未満）
- `[2.*, 3.0.0)`: バージョン2系の最新を使用（3.0.0未満）
- `[1.*, 2.0.0)`: バージョン1系の最新を使用（2.0.0未満）

---

## 集約設定

関数実行結果の集約に関する設定です。

### aggregator.batchSize

**スキーマ参照**: [host_schema_translated.json:9](host_schema_translated.json#L9)

**説明**: 集約の最大バッチサイズ。この値に到達すると、フラッシュタイムアウトの前でもすべての値がフラッシュされます。

**デフォルト値**: `1000`

**環境変数名**: `AzureFunctionsJobHost__aggregator__batchSize`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__aggregator__batchSize",
  "value": "1000",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "aggregator": {
    "batchSize": 1000
  }
}
```

**推奨設定**:
- 標準: `1000`
- 高頻度実行: `500` （より頻繁にフラッシュ）
- 低頻度実行: `2000` （より効率的に集約）

---

### aggregator.flushTimeout

**スキーマ参照**: [host_schema_translated.json:14](host_schema_translated.json#L14)

**説明**: 集約期間。アグリゲーターは、この値に基づいて定期的にフラッシュします。

**デフォルト値**: `00:00:30` (30秒)

**環境変数名**: `AzureFunctionsJobHost__aggregator__flushTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__aggregator__flushTimeout",
  "value": "00:00:30",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "aggregator": {
    "flushTimeout": "00:00:30"
  }
}
```

**推奨設定**:
- リアルタイム監視: `00:00:10` (10秒)
- 標準: `00:00:30` (30秒)
- バッチ処理: `00:01:00` (1分)

---

## 関数タイムアウト設定

### functionTimeout

**スキーマ参照**: [host_schema_translated.json:30](host_schema_translated.json#L30)

**説明**: すべての関数のタイムアウト期間を示す値。

**デフォルト値**:
- Consumption プラン: `00:05:00` (5分)
- Premium/Dedicated プラン: `00:30:00` (30分)

**環境変数名**: `AzureFunctionsJobHost__functionTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__functionTimeout",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "functionTimeout": "00:05:00"
}
```

**推奨設定**:
- Consumption プラン: `00:05:00` (最大10分)
- Premium プラン: `00:30:00` (無制限も可能)
- 無制限: `-1` または `null`

**注意**: Consumption プランでは最大10分、Premium/Dedicated プランでは無制限に設定できます。

---

## シングルトン設定

シングルトンロック動作の構成設定です。複数のインスタンスで実行される関数の同時実行を制御します。

### singleton.lockPeriod

**スキーマ参照**: [host_schema_translated.json:57](host_schema_translated.json#L57)

**説明**: 関数レベルのロックが使用される期間（自動更新されます）。

**デフォルト値**: `00:00:15` (15秒)

**環境変数名**: `AzureFunctionsJobHost__singleton__lockPeriod`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__singleton__lockPeriod",
  "value": "00:00:15",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "singleton": {
    "lockPeriod": "00:00:15"
  }
}
```

**推奨設定**:
- 短時間処理: `00:00:15` (15秒)
- 標準: `00:00:30` (30秒)
- 長時間処理: `00:01:00` (1分)

---

### singleton.listenerLockPeriod

**スキーマ参照**: [host_schema_translated.json:61](host_schema_translated.json#L61)

**説明**: リスナーがロックされる期間。

**デフォルト値**: `00:01:00` (1分)

**環境変数名**: `AzureFunctionsJobHost__singleton__listenerLockPeriod`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__singleton__listenerLockPeriod",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "singleton": {
    "listenerLockPeriod": "00:01:00"
  }
}
```

---

### singleton.listenerLockRecoveryPollingInterval

**スキーマ参照**: [host_schema_translated.json:66](host_schema_translated.json#L66)

**説明**: リスナーロックが起動時に取得できなかった場合、リスナーロックリカバリに使用される時間間隔。

**デフォルト値**: `00:01:00` (1分)

**環境変数名**: `AzureFunctionsJobHost__singleton__listenerLockRecoveryPollingInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__singleton__listenerLockRecoveryPollingInterval",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "singleton": {
    "listenerLockRecoveryPollingInterval": "00:01:00"
  }
}
```

---

### singleton.lockAcquisitionTimeout

**スキーマ参照**: [host_schema_translated.json:71](host_schema_translated.json#L71)

**説明**: ランタイムがロックを取得しようとする最大時間。

**デフォルト値**: `00:01:00` (1分)

**環境変数名**: `AzureFunctionsJobHost__singleton__lockAcquisitionTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__singleton__lockAcquisitionTimeout",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "singleton": {
    "lockAcquisitionTimeout": "00:01:00"
  }
}
```

**推奨設定**:
- 高頻度実行: `00:00:30` (30秒)
- 標準: `00:01:00` (1分)
- 低頻度実行: `00:05:00` (5分)

---

### singleton.lockAcquisitionPollingInterval

**スキーマ参照**: [host_schema_translated.json:76](host_schema_translated.json#L76)

**説明**: ロック取得の試み間の間隔。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__singleton__lockAcquisitionPollingInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__singleton__lockAcquisitionPollingInterval",
  "value": "00:00:05",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "singleton": {
    "lockAcquisitionPollingInterval": "00:00:05"
  }
}
```

**推奨設定**:
- 高頻度ポーリング: `00:00:01` (1秒)
- 標準: `00:00:05` (5秒)
- 低頻度ポーリング: `00:00:10` (10秒)

---

## ヘルスモニター設定

関数ホストヘルスモニターの構成設定です。ホストの健全性を監視し、問題がある場合は自動的にリサイクルします。

### healthMonitor.enabled

**スキーマ参照**: [host_schema_translated.json:88](host_schema_translated.json#L88)

**説明**: ヘルスモニター機能が有効になっているかどうかを指定します。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__healthMonitor__enabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__healthMonitor__enabled",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "healthMonitor": {
    "enabled": true
  }
}
```

**推奨設定**:
- 本番環境: `true` (有効)
- 開発環境: `true` (有効)
- デバッグ時のみ: `false` (無効)

---

### healthMonitor.healthCheckInterval

**スキーマ参照**: [host_schema_translated.json:92](host_schema_translated.json#L92)

**説明**: 周期的なバックグラウンドヘルスチェック間の時間間隔。

**デフォルト値**: `00:00:10` (10秒)

**環境変数名**: `AzureFunctionsJobHost__healthMonitor__healthCheckInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__healthMonitor__healthCheckInterval",
  "value": "00:00:10",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "healthMonitor": {
    "healthCheckInterval": "00:00:10"
  }
}
```

**推奨設定**:
- 高頻度監視: `00:00:05` (5秒)
- 標準: `00:00:10` (10秒)
- 低頻度監視: `00:00:30` (30秒)

---

### healthMonitor.healthCheckWindow

**スキーマ参照**: [host_schema_translated.json:97](host_schema_translated.json#L97)

**説明**: healthCheckThreshold設定と組み合わせて使用されるスライドタイムウィンドウ。

**デフォルト値**: `00:02:00` (2分)

**環境変数名**: `AzureFunctionsJobHost__healthMonitor__healthCheckWindow`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__healthMonitor__healthCheckWindow",
  "value": "00:02:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "healthMonitor": {
    "healthCheckWindow": "00:02:00"
  }
}
```

**推奨設定**:
- 短期監視: `00:01:00` (1分)
- 標準: `00:02:00` (2分)
- 長期監視: `00:05:00` (5分)

---

### healthMonitor.healthCheckThreshold

**スキーマ参照**: [host_schema_translated.json:102](host_schema_translated.json#L102)

**説明**: ホストのリサイクルが開始される前に、ヘルスチェックが失敗する可能性がある最大回数。

**デフォルト値**: `6`

**環境変数名**: `AzureFunctionsJobHost__healthMonitor__healthCheckThreshold`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__healthMonitor__healthCheckThreshold",
  "value": "6",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "healthMonitor": {
    "healthCheckThreshold": 6
  }
}
```

**推奨設定**:
- 敏感: `3` (早期リサイクル)
- 標準: `6`
- 寛容: `10` (より多くの失敗を許容)

---

### healthMonitor.counterThreshold

**スキーマ参照**: [host_schema_translated.json:107](host_schema_translated.json#L107)

**説明**: パフォーマンスカウンターが不健康と見なされるしきい値。

**デフォルト値**: `0.8` (80%)

**環境変数名**: `AzureFunctionsJobHost__healthMonitor__counterThreshold`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__healthMonitor__counterThreshold",
  "value": "0.8",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "healthMonitor": {
    "counterThreshold": 0.8
  }
}
```

**推奨設定**:
- 敏感: `0.7` (70%で警告)
- 標準: `0.8` (80%で警告)
- 寛容: `0.9` (90%で警告)

---

## HTTP拡張設定

HTTPトリガーの構成設定です。

### extensions.http.routePrefix

**スキーマ参照**: [host_schema_translated.json:123](host_schema_translated.json#L123)

**説明**: すべてのルートに適用されるデフォルトのルートプレフィックスを定義します。空の文字列を使用してプレフィックスを削除します。

**デフォルト値**: `api`

**環境変数名**: `AzureFunctionsJobHost__extensions__http__routePrefix`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__http__routePrefix",
  "value": "api",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "http": {
      "routePrefix": "api"
    }
  }
}
```

**推奨設定**:
- 標準APIパス: `api` → `https://yourapp.azurewebsites.net/api/functionname`
- カスタムパス: `v1` → `https://yourapp.azurewebsites.net/v1/functionname`
- プレフィックスなし: `""` → `https://yourapp.azurewebsites.net/functionname`

---

### extensions.http.maxConcurrentRequests

**スキーマ参照**: [host_schema_translated.json:128](host_schema_translated.json#L128)

**説明**: 並行して実行されるHTTP関数の最大数を定義します。

**デフォルト値**: `-1` (無制限)

**環境変数名**: `AzureFunctionsJobHost__extensions__http__maxConcurrentRequests`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__http__maxConcurrentRequests",
  "value": "-1",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "http": {
      "maxConcurrentRequests": -1
    }
  }
}
```

**推奨設定**:
- 無制限: `-1`
- 制限あり（小規模）: `100`
- 制限あり（中規模）: `500`
- 制限あり（大規模）: `1000`

---

### extensions.http.maxOutstandingRequests

**スキーマ参照**: [host_schema_translated.json:133](host_schema_translated.json#L133)

**説明**: いつでも保持される未解決のリクエストの最大数を定義します。

**デフォルト値**: `-1` (無制限)

**環境変数名**: `AzureFunctionsJobHost__extensions__http__maxOutstandingRequests`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__http__maxOutstandingRequests",
  "value": "-1",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "http": {
      "maxOutstandingRequests": -1
    }
  }
}
```

**推奨設定**:
- 無制限: `-1`
- 制限あり: `200`

---

### extensions.http.dynamicThrottlesEnabled

**スキーマ参照**: [host_schema_translated.json:138](host_schema_translated.json#L138)

**説明**: 動的ホストカウンターチェックを有効にする必要があるかどうかを示します。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__extensions__http__dynamicThrottlesEnabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__http__dynamicThrottlesEnabled",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "http": {
      "dynamicThrottlesEnabled": false
    }
  }
}
```

**推奨設定**:
- 標準: `false` (無効)
- 自動調整が必要な場合: `true` (有効)

---

## キュー拡張設定

Azure Storage Queueトリガーの構成設定です。

### extensions.queues.maxPollingInterval

**スキーマ参照**: [host_schema_translated.json:220](host_schema_translated.json#L220)

**説明**: キューポーリング間の最大間隔。最小は00:00:00.100（100ミリ秒）です。

**デフォルト値**: `00:00:02` (2秒)

**環境変数名**: `AzureFunctionsJobHost__extensions__queues__maxPollingInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__queues__maxPollingInterval",
  "value": "00:00:02",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "queues": {
      "maxPollingInterval": "00:00:02"
    }
  }
}
```

**推奨設定**:
- リアルタイム処理: `00:00:00.100` (100ミリ秒)
- 標準: `00:00:02` (2秒)
- 低頻度: `00:00:10` (10秒)

---

### extensions.queues.batchSize

**スキーマ参照**: [host_schema_translated.json:231](host_schema_translated.json#L231)

**説明**: 関数ランタイムが同時に取得し、並行して処理するキューメッセージの数。

**デフォルト値**: `16`

**環境変数名**: `AzureFunctionsJobHost__extensions__queues__batchSize`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__queues__batchSize",
  "value": "16",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "queues": {
      "batchSize": 16
    }
  }
}
```

**推奨設定**:
- 小規模: `8`
- 標準: `16`
- 大規模: `32` (最大値)

---

### extensions.queues.maxDequeueCount

**スキーマ参照**: [host_schema_translated.json:238](host_schema_translated.json#L238)

**説明**: メッセージを毒キューに移動する前に処理を試みる回数。

**デフォルト値**: `5`

**環境変数名**: `AzureFunctionsJobHost__extensions__queues__maxDequeueCount`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__queues__maxDequeueCount",
  "value": "5",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "queues": {
      "maxDequeueCount": 5
    }
  }
}
```

**推奨設定**:
- 少ない再試行: `3`
- 標準: `5`
- 多い再試行: `10`

---

### extensions.queues.visibilityTimeout

**スキーマ参照**: [host_schema_translated.json:225](host_schema_translated.json#L225)

**説明**: メッセージの処理が失敗したときの再試行間の時間間隔。

**デフォルト値**: `00:00:00` (デフォルト動作)

**環境変数名**: `AzureFunctionsJobHost__extensions__queues__visibilityTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__queues__visibilityTimeout",
  "value": "00:00:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "queues": {
      "visibilityTimeout": "00:00:00"
    }
  }
}
```

**推奨設定**:
- デフォルト: `00:00:00`
- カスタム（短期）: `00:00:30` (30秒)
- カスタム（長期）: `00:05:00` (5分)

---

### extensions.queues.newBatchThreshold

**スキーマ参照**: [host_schema_translated.json:201](host_schema_translated.json#L201), [host_schema_translated.json:241](host_schema_translated.json#L241)

**説明**: メッセージの新しいバッチが取得されるしきい値。

**デフォルト値**: `batchSize/2` (動的に計算)

**環境変数名**: `AzureFunctionsJobHost__extensions__queues__newBatchThreshold`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__queues__newBatchThreshold",
  "value": "8",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "queues": {
      "newBatchThreshold": 8
    }
  }
}
```

**推奨設定**:
- デフォルト: 未設定 (batchSize/2が自動使用される)
- カスタム: batchSizeが16の場合は8など

---

### extensions.queues.messageEncoding

**スキーマ参照**: [host_schema_translated.json:245](host_schema_translated.json#L245)

**説明**: メッセージのエンコード形式。この設定は拡張バージョン5.0.0以上でのみ使用可能です。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__queues__messageEncoding`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__queues__messageEncoding",
  "value": "base64",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "queues": {
      "messageEncoding": "base64"
    }
  }
}
```

**推奨設定**:
- Base64エンコード: `base64` (レガシー互換性)
- エンコードなし: `none` (拡張v5.0.0以上)

---

## Durable Functions設定

Durable Functionsのオーケストレーション/アクティビティトリガーの構成設定です。

### extensions.durableTask.hubName

**スキーマ参照**: [host_schema_translated.json:1522](host_schema_translated.json#L1522)

**説明**: 代替タスクハブ名。同じストレージバックエンドを使用している場合でも、複数のDurable Functionsアプリケーションを互いに分離できます。

**デフォルト値**: `DurableFunctionsHub`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__hubName`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__hubName",
  "value": "DurableFunctionsHub",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "hubName": "DurableFunctionsHub"
    }
  }
}
```

**推奨設定**:
- 開発環境: `DurableFunctionsHub-Dev`
- ステージング環境: `DurableFunctionsHub-Staging`
- 本番環境: `DurableFunctionsHub-Prod`

---

### extensions.durableTask.storageProvider.controlQueueBatchSize

**スキーマ参照**: [host_schema_translated.json:272](host_schema_translated.json#L272)

**説明**: 一度にコントロールキューから引き出すメッセージの数。

**デフォルト値**: `32`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__storageProvider__controlQueueBatchSize`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__storageProvider__controlQueueBatchSize",
  "value": "32",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "storageProvider": {
        "controlQueueBatchSize": 32
      }
    }
  }
}
```

---

### extensions.durableTask.storageProvider.controlQueueBufferThreshold

**スキーマ参照**: [host_schema_translated.json:277](host_schema_translated.json#L277)

**説明**: 一度にメモリでバッファリングできるコントロールキューメッセージの数。

**デフォルト値**: `256`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__storageProvider__controlQueueBufferThreshold`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__storageProvider__controlQueueBufferThreshold",
  "value": "256",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "storageProvider": {
        "controlQueueBufferThreshold": 256
      }
    }
  }
}
```

---

### extensions.durableTask.storageProvider.controlQueueVisibilityTimeout

**スキーマ参照**: [host_schema_translated.json:282](host_schema_translated.json#L282)

**説明**: デキューされたコントロールキューメッセージの可視性タイムアウト。

**デフォルト値**: `00:05:00` (5分)

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__storageProvider__controlQueueVisibilityTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__storageProvider__controlQueueVisibilityTimeout",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "storageProvider": {
        "controlQueueVisibilityTimeout": "00:05:00"
      }
    }
  }
}
```

---

### extensions.durableTask.storageProvider.maxQueuePollingInterval

**スキーマ参照**: [host_schema_translated.json:287](host_schema_translated.json#L287)

**説明**: 最大制御および作業項目キューポーリング間隔。値が高いとメッセージ処理のレイテンシが高くなる可能性があります。

**デフォルト値**: `00:00:30` (30秒)

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__storageProvider__maxQueuePollingInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__storageProvider__maxQueuePollingInterval",
  "value": "00:00:30",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "storageProvider": {
        "maxQueuePollingInterval": "00:00:30"
      }
    }
  }
}
```

**推奨設定**:
- 低レイテンシ: `00:00:05` (5秒)
- 標準: `00:00:30` (30秒)
- 低コスト: `00:01:00` (1分)

---

### extensions.durableTask.storageProvider.partitionCount

**スキーマ参照**: [host_schema_translated.json:292](host_schema_translated.json#L292)

**説明**: 制御キューのパーティションカウント。1〜16の間の正の整数。

**デフォルト値**: `4`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__storageProvider__partitionCount`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__storageProvider__partitionCount",
  "value": "4",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "storageProvider": {
        "partitionCount": 4
      }
    }
  }
}
```

**推奨設定**:
- 小規模: `2`
- 標準: `4`
- 大規模: `8` または `16`

---

### extensions.durableTask.storageProvider.useLegacyPartitionManagement

**スキーマ参照**: [host_schema_translated.json:306](host_schema_translated.json#L306)

**説明**: falseに設定すると、パーティション管理アルゴリズムを使用して、スケーリング時に関数実行の重複の可能性を減らします。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__storageProvider__useLegacyPartitionManagement`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__storageProvider__useLegacyPartitionManagement",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "storageProvider": {
        "useLegacyPartitionManagement": false
      }
    }
  }
}
```

---

### extensions.durableTask.storageProvider.workItemQueueVisibilityTimeout

**スキーマ参照**: [host_schema_translated.json:311](host_schema_translated.json#L311)

**説明**: デキューされた作業項目キューメッセージの可視性タイムアウト。

**デフォルト値**: `00:05:00` (5分)

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__storageProvider__workItemQueueVisibilityTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__storageProvider__workItemQueueVisibilityTimeout",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "storageProvider": {
        "workItemQueueVisibilityTimeout": "00:05:00"
      }
    }
  }
}
```

---

### extensions.durableTask.tracing.traceInputsAndOutputs

**スキーマ参照**: [host_schema_translated.json:322](host_schema_translated.json#L322)

**説明**: オーケストレーション・アクティビティ関数呼び出しの入力と出力をトレースするかどうか。関数実行イベントをトレースする際のデフォルトの動作は、オーケストレーション・アクティビティ関数呼び出しのシリアル化された入力と出力にバイト数を含めます。この動作は、ログを膨張させたり不注意に機密情報をログに公開することなく、入力と出力がどのように見えるかについての最小限の情報を提供します。このプロパティをtrueに設定すると、関数ログのデフォルトは関数の入力と出力の内容全体をログに記録します。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__tracing__traceInputsAndOutputs`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__tracing__traceInputsAndOutputs",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "tracing": {
        "traceInputsAndOutputs": false
      }
    }
  }
}
```

**推奨設定**:
- 開発環境: `true` (デバッグ用)
- 本番環境: `false` (セキュリティとログサイズ管理)

---

### extensions.durableTask.tracing.traceReplayEvents

**スキーマ参照**: [host_schema_translated.json:327](host_schema_translated.json#L327)

**説明**: オーケストレーターリプレイイベントをApplication Insightsに書き込むかどうかを示す値。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__tracing__traceReplayEvents`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__tracing__traceReplayEvents",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "tracing": {
        "traceReplayEvents": false
      }
    }
  }
}
```

**推奨設定**:
- 通常: `false` (ログ量削減)
- トラブルシューティング時: `true`

---

### extensions.durableTask.notifications.eventGrid.topicEndpoint

**スキーマ参照**: [host_schema_translated.json:341](host_schema_translated.json#L341)

**説明**: Azure Event Gridカスタムトピックエンドポイントへの URL。このプロパティを設定すると、オーケストレーションライフサイクル通知イベントがこのエンドポイントに公開されます。このプロパティはアプリ設定解決をサポートします。

**デフォルト値**: 空

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__topicEndpoint`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__topicEndpoint",
  "value": "https://your-topic.region.eventgrid.azure.net/api/events",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "notifications": {
        "eventGrid": {
          "topicEndpoint": "https://your-topic.region.eventgrid.azure.net/api/events"
        }
      }
    }
  }
}
```

---

### extensions.durableTask.notifications.eventGrid.keySettingName

**スキーマ参照**: [host_schema_translated.json:343](host_schema_translated.json#L343)

**説明**: Azure Event Gridカスタムトピックでの認証に使用するキーを含むアプリ設定の名前。

**デフォルト値**: 空

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__keySettingName`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__keySettingName",
  "value": "EventGridKey",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "notifications": {
        "eventGrid": {
          "keySettingName": "EventGridKey"
        }
      }
    }
  }
}
```

---

### extensions.durableTask.notifications.eventGrid.publishRetryCount

**スキーマ参照**: [host_schema_translated.json:349](host_schema_translated.json#L349)

**説明**: Event Gridトピックへの公開が失敗した場合の再試行回数。

**デフォルト値**: `0`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__publishRetryCount`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__publishRetryCount",
  "value": "3",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "notifications": {
        "eventGrid": {
          "publishRetryCount": 3
        }
      }
    }
  }
}
```

**推奨設定**:
- 標準: `3`
- 高信頼性: `5`

---

### extensions.durableTask.notifications.eventGrid.publishRetryInterval

**スキーマ参照**: [host_schema_translated.json:354](host_schema_translated.json#L354)

**説明**: Event Grid公開の再試行間隔（hh:mm:ss形式）。

**デフォルト値**: `00:05:00` (5分)

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__publishRetryInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__publishRetryInterval",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "notifications": {
        "eventGrid": {
          "publishRetryInterval": "00:05:00"
        }
      }
    }
  }
}
```

---

### extensions.durableTask.notifications.eventGrid.publishEventTypes

**スキーマ参照**: [host_schema_translated.json:359](host_schema_translated.json#L359)

**説明**: このリストに含まれるEvent Gridライフサイクルイベントタイプのみが公開されます。指定しない場合は、すべてのイベントタイプが公開されます。許可される値: Started、Pending、Failed、Terminated。

**デフォルト値**: すべてのイベントタイプ

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__publishEventTypes`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__notifications__eventGrid__publishEventTypes",
  "value": "[\"Started\", \"Completed\", \"Failed\"]",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "notifications": {
        "eventGrid": {
          "publishEventTypes": ["Started", "Completed", "Failed"]
        }
      }
    }
  }
}
```

---

### extensions.durableTask.maxConcurrentActivityFunctions

**スキーマ参照**: [host_schema_translated.json:380](host_schema_translated.json#L380)

**説明**: 単一ホストインスタンスで同時に処理できるアクティビティ関数の最大数。

**デフォルト値**: `10`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__maxConcurrentActivityFunctions`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__maxConcurrentActivityFunctions",
  "value": "10",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "maxConcurrentActivityFunctions": 10
    }
  }
}
```

**推奨設定**:
- 小規模: `5`
- 標準: `10`
- 大規模（Premium/Dedicated）: `20-50`

---

### extensions.durableTask.maxConcurrentOrchestratorFunctions

**スキーマ参照**: [host_schema_translated.json:385](host_schema_translated.json#L385)

**説明**: 単一ホストインスタンスで同時に処理できるオーケストレーター関数の最大数。

**デフォルト値**: `10`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__maxConcurrentOrchestratorFunctions`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__maxConcurrentOrchestratorFunctions",
  "value": "10",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "maxConcurrentOrchestratorFunctions": 10
    }
  }
}
```

**推奨設定**:
- 小規模: `5`
- 標準: `10`
- 大規模（Premium/Dedicated）: `20-50`

---

### extensions.durableTask.extendedSessionsEnabled

**スキーマ参照**: [host_schema_translated.json:391](host_schema_translated.json#L391)

**説明**: 拡張セッションを有効にするかどうか。有効にすると、オーケストレーターインスタンスがメモリに保持され、新しいメッセージを処理できます。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__extendedSessionsEnabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__extendedSessionsEnabled",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "extendedSessionsEnabled": true
    }
  }
}
```

**推奨設定**:
- 高スループット: `true` (メモリ使用量増加)
- 標準: `false` または未設定

---

### extensions.durableTask.extendedSessionIdleTimeoutInSeconds

**スキーマ参照**: [host_schema_translated.json:394](host_schema_translated.json#L394)

**説明**: 拡張セッションのアイドルタイムアウト(秒)。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__extendedSessionIdleTimeoutInSeconds`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__extendedSessionIdleTimeoutInSeconds",
  "value": "30",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "extendedSessionIdleTimeoutInSeconds": 30
    }
  }
}
```

**推奨設定**:
- 短いタイムアウト: `10` (10秒)
- 標準: `30` (30秒)
- 長いタイムアウト: `60` (1分)

---

### extensions.durableTask.useAppLease

**スキーマ参照**: [host_schema_translated.json:396](host_schema_translated.json#L396)

**説明**: trueに設定すると、アプリは、タスクハブパーティションのみを処理するホストインスタンスのアプリレベルブロブリースを取得します。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__useAppLease`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__useAppLease",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "useAppLease": true
    }
  }
}
```

---

### extensions.durableTask.useGracefulShutdown

**スキーマ参照**: [host_schema_translated.json:401](host_schema_translated.json#L401)

**説明**: ホストシャットダウンの確率を減らすためにグレースフルシャットダウンを有効にして、インプロセス関数実行でエラーが発生しないようにします。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__useGracefulShutdown`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__useGracefulShutdown",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "useGracefulShutdown": true
    }
  }
}
```

**推奨設定**:
- 本番環境: `true` (推奨)
- 開発環境: `false`

---

### extensions.durableTask.maxEntityOperationBatchSize

**スキーマ参照**: [host_schema_translated.json:406](host_schema_translated.json#L406)

**説明**: バッチとして一緒に処理されるエンティティ操作の最大数。

**デフォルト値**: `50`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__maxEntityOperationBatchSize`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__maxEntityOperationBatchSize",
  "value": "50",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "maxEntityOperationBatchSize": 50
    }
  }
}
```

**推奨設定**:
- 標準: `50`
- 大規模: `100`

---

### extensions.durableTask.useTablePartitionManagement

**スキーマ参照**: [host_schema_translated.json:410](host_schema_translated.json#L410)

**説明**: Durable Functions v2.10.0で導入された改善されたパーティション管理ロジックを使用するかどうか。パーティション管理ロジックにより、異なるインスタンス間での作業の配分、およびスケールインとスケールアウトに対する応答性が向上します。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__extensions__durableTask__useTablePartitionManagement`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__durableTask__useTablePartitionManagement",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "durableTask": {
      "useTablePartitionManagement": true
    }
  }
}
```

**推奨設定**:
- 新規デプロイ: `true` (推奨)
- 既存デプロイ: 動作確認後に`true`へ移行

---

## Cosmos DB設定

Cosmos DBトリガーの構成設定です。

### extensions.cosmosDB.connectionMode

**スキーマ参照**: [host_schema_translated.json:421](host_schema_translated.json#L421)

**説明**: サービスへの接続に使用される接続モード。使用可能なオプションは、DirectとGatewayです。

**デフォルト値**: `Gateway`

**環境変数名**: `AzureFunctionsJobHost__extensions__cosmosDB__connectionMode`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__cosmosDB__connectionMode",
  "value": "Gateway",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "cosmosDB": {
      "connectionMode": "Gateway"
    }
  }
}
```

**推奨設定**:
- 通常: `Gateway` (ファイアウォール対応)
- 高パフォーマンス: `Direct` (低レイテンシ)

---

### extensions.cosmosDB.protocol

**スキーマ参照**: [host_schema_translated.json:429](host_schema_translated.json#L429)

**説明**: サービスへの接続に使用される接続プロトコル。使用可能なオプションは、HttpsとTcpです。

**デフォルト値**: `Https`

**環境変数名**: `AzureFunctionsJobHost__extensions__cosmosDB__protocol`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__cosmosDB__protocol",
  "value": "Https",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "cosmosDB": {
      "protocol": "Https"
    }
  }
}
```

**推奨設定**:
- 標準: `Https`
- Direct接続時: `Tcp` (パフォーマンス重視)

---

### extensions.cosmosDB.leaseOptions.leasePrefix

**スキーマ参照**: [host_schema_translated.json:466](host_schema_translated.json#L466)

**説明**: アプリ内のすべての機能で使用するリースプレフィックス。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__cosmosDB__leaseOptions__leasePrefix`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__cosmosDB__leaseOptions__leasePrefix",
  "value": "myapp",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "cosmosDB": {
      "leaseOptions": {
        "leasePrefix": "myapp"
      }
    }
  }
}
```

**推奨設定**:
- マルチアプリ環境: アプリ名やスロット名を含むプレフィックスを設定
- 単一アプリ環境: 未設定

---

## Service Bus設定

Azure Service Busトリガーの構成設定です。

### extensions.serviceBus.transportType

**スキーマ参照**: [host_schema_translated.json:1292](host_schema_translated.json#L1292)

**説明**: Service Busとの通信に使用するトランスポートの種類。

**デフォルト値**: `AmqpTcp`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__transportType`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__transportType",
  "value": "AmqpTcp",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "transportType": "AmqpTcp"
    }
  }
}
```

**推奨設定**:
- 標準: `AmqpTcp`
- Webソケット経由: `AmqpWebSockets` (ファイアウォール環境)

---

### extensions.serviceBus.prefetchCount

**スキーマ参照**: [host_schema_translated.json:1307](host_schema_translated.json#L1307)

**説明**: 基になるMessageReceiverが使用する既定のPrefetchCountを取得または設定します。

**デフォルト値**: `0`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__prefetchCount`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__prefetchCount",
  "value": "0",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "prefetchCount": 0
    }
  }
}
```

**推奨設定**:
- 無効: `0`
- 小規模プリフェッチ: `32`
- 標準: `100`
- 大規模: `300`

---

### extensions.serviceBus.autoCompleteMessages

**スキーマ参照**: [host_schema_translated.json:1305](host_schema_translated.json#L1305)

**説明**: トリガーがメッセージを自動的に完了を呼び出すか、または関数コードが完了を手動で呼び出すかどうかを決定する値を取得または設定します。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__autoCompleteMessages`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__autoCompleteMessages",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "autoCompleteMessages": true
    }
  }
}
```

**推奨設定**:
- 自動完了: `true` (推奨)
- 手動完了: `false` (細かい制御が必要な場合)

---

### extensions.serviceBus.maxAutoLockRenewalDuration

**スキーマ参照**: [host_schema_translated.json:1310](host_schema_translated.json#L1310)

**説明**: メッセージロックが自動的に更新される最大期間を取得または設定します。

**デフォルト値**: `00:05:00` (5分)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__maxAutoLockRenewalDuration`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__maxAutoLockRenewalDuration",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "maxAutoLockRenewalDuration": "00:05:00"
    }
  }
}
```

**推奨設定**:
- 短時間処理: `00:05:00` (5分)
- 標準処理: `00:10:00` (10分)
- 長時間処理: `00:30:00` (30分)

---

### extensions.serviceBus.maxConcurrentCalls

**スキーマ参照**: [host_schema_translated.json:1315](host_schema_translated.json#L1315)

**説明**: メッセージポンプが開始する必要があるコールバックへの同時呼び出しの最大数。

**デフォルト値**: `16`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__maxConcurrentCalls`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__maxConcurrentCalls",
  "value": "16",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "maxConcurrentCalls": 16
    }
  }
}
```

**推奨設定**:
- 小規模: `8`
- 標準: `16`
- 大規模: `32`

---

### extensions.serviceBus.maxConcurrentSessions

**スキーマ参照**: [host_schema_translated.json:1320](host_schema_translated.json#L1320)

**説明**: メッセージポンプが開始する必要がある同時セッションの最大数。

**デフォルト値**: `8`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__maxConcurrentSessions`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__maxConcurrentSessions",
  "value": "8",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "maxConcurrentSessions": 8
    }
  }
}
```

**推奨設定**:
- 小規模: `4`
- 標準: `8`
- 大規模: `16`

---

### extensions.serviceBus.maxMessageBatchSize

**スキーマ参照**: [host_schema_translated.json:1326](host_schema_translated.json#L1326)

**説明**: 単一の関数呼び出しで受信できるメッセージの最大数。

**デフォルト値**: `1000`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__maxMessageBatchSize`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__maxMessageBatchSize",
  "value": "1000",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "maxMessageBatchSize": 1000
    }
  }
}
```

**推奨設定**:
- 小規模バッチ: `100`
- 標準: `1000`
- 大規模バッチ: `5000`

---

### extensions.serviceBus.sessionIdleTimeout

**スキーマ参照**: [host_schema_translated.json:1337](host_schema_translated.json#L1337)

**説明**: セッションアイドルタイムアウト。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionIdleTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionIdleTimeout",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionIdleTimeout": "00:01:00"
    }
  }
}
```

**推奨設定**:
- 短いタイムアウト: `00:00:30` (30秒)
- 標準: `00:01:00` (1分)
- 長いタイムアウト: `00:05:00` (5分)

---

### extensions.serviceBus.clientRetryOptions.mode

**スキーマ参照**: [host_schema_translated.json:1252](host_schema_translated.json#L1252)

**説明**: Service Bus操作失敗時の再試行戦略。

**デフォルト値**: `Exponential`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__mode`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__mode",
  "value": "Exponential",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "clientRetryOptions": {
        "mode": "Exponential"
      }
    }
  }
}
```

**推奨設定**:
- 指数バックオフ: `Exponential` (推奨)
- 固定間隔: `Fixed`

---

### extensions.serviceBus.clientRetryOptions.tryTimeout

**スキーマ参照**: [host_schema_translated.json:1260](host_schema_translated.json#L1260)

**説明**: 個別の試行に許可される最大期間。

**デフォルト値**: `00:00:10` (10秒)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__tryTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__tryTimeout",
  "value": "00:00:10",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "clientRetryOptions": {
        "tryTimeout": "00:00:10"
      }
    }
  }
}
```

**推奨設定**:
- 短いタイムアウト: `00:00:05` (5秒)
- 標準: `00:00:10` (10秒)
- 長いタイムアウト: `00:00:30` (30秒)

---

### extensions.serviceBus.clientRetryOptions.delay

**スキーマ参照**: [host_schema_translated.json:1265](host_schema_translated.json#L1265)

**説明**: 再試行間の遅延時間。

**デフォルト値**: `00:00:00.8` (0.8秒)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__delay`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__delay",
  "value": "00:00:00.8",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "clientRetryOptions": {
        "delay": "00:00:00.8"
      }
    }
  }
}
```

**推奨設定**:
- 短い遅延: `00:00:00.5` (0.5秒)
- 標準: `00:00:00.8` (0.8秒)
- 長い遅延: `00:00:01` (1秒)

---

### extensions.serviceBus.clientRetryOptions.maxDelay

**スキーマ参照**: [host_schema_translated.json:1271](host_schema_translated.json#L1271)

**説明**: 再試行間の最大遅延時間。

**デフォルト値**: `00:01:00` (1分)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__maxDelay`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__maxDelay",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "clientRetryOptions": {
        "maxDelay": "00:01:00"
      }
    }
  }
}
```

**推奨設定**:
- 短い最大遅延: `00:00:30` (30秒)
- 標準: `00:01:00` (1分)
- 長い最大遅延: `00:02:00` (2分)

---

### extensions.serviceBus.clientRetryOptions.maxRetries

**スキーマ参照**: [host_schema_translated.json:1277](host_schema_translated.json#L1277)

**説明**: 最大再試行回数。

**デフォルト値**: `3`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__maxRetries`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__clientRetryOptions__maxRetries",
  "value": "3",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "clientRetryOptions": {
        "maxRetries": 3
      }
    }
  }
}
```

**推奨設定**:
- 少ない再試行: `2`
- 標準: `3`
- 多い再試行: `5`

---

### extensions.serviceBus.processorOptions.maxConcurrentCalls

**スキーマ参照**: [host_schema_translated.json:1315](host_schema_translated.json#L1315)

**説明**: プロセッサが開始する必要があるコールバックへの同時呼び出しの最大数。

**デフォルト値**: `8`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__processorOptions__maxConcurrentCalls`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__processorOptions__maxConcurrentCalls",
  "value": "8",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "processorOptions": {
        "maxConcurrentCalls": 8
      }
    }
  }
}
```

**推奨設定**:
- 小規模: `4`
- 標準: `8`
- 大規模: `16`

---

### extensions.serviceBus.processorOptions.prefetchCount

**スキーマ参照**: [host_schema_translated.json:1307](host_schema_translated.json#L1307)

**説明**: プロセッサが使用するプリフェッチカウント。

**デフォルト値**: `0`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__processorOptions__prefetchCount`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__processorOptions__prefetchCount",
  "value": "0",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "processorOptions": {
        "prefetchCount": 0
      }
    }
  }
}
```

**推奨設定**:
- 無効: `0`
- 標準: `32`
- 大規模: `100`

---

### extensions.serviceBus.processorOptions.autoCompleteMessages

**スキーマ参照**: [host_schema_translated.json:1305](host_schema_translated.json#L1305)

**説明**: プロセッサがメッセージを自動的に完了するかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__processorOptions__autoCompleteMessages`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__processorOptions__autoCompleteMessages",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "processorOptions": {
        "autoCompleteMessages": true
      }
    }
  }
}
```

---

### extensions.serviceBus.processorOptions.maxAutoLockRenewalDuration

**スキーマ参照**: [host_schema_translated.json:1310](host_schema_translated.json#L1310)

**説明**: メッセージロックが自動的に更新される最大期間。

**デフォルト値**: `00:05:00` (5分)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__processorOptions__maxAutoLockRenewalDuration`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__processorOptions__maxAutoLockRenewalDuration",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "processorOptions": {
        "maxAutoLockRenewalDuration": "00:05:00"
      }
    }
  }
}
```

---

### extensions.serviceBus.sessionProcessorOptions.maxConcurrentSessions

**スキーマ参照**: [host_schema_translated.json:1320](host_schema_translated.json#L1320)

**説明**: セッションプロセッサが開始する必要がある同時セッションの最大数。

**デフォルト値**: `8`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__maxConcurrentSessions`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__maxConcurrentSessions",
  "value": "8",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionProcessorOptions": {
        "maxConcurrentSessions": 8
      }
    }
  }
}
```

---

### extensions.serviceBus.sessionProcessorOptions.maxConcurrentCallsPerSession

**スキーマ参照**: [host_schema_translated.json:1320](host_schema_translated.json#L1320)

**説明**: セッションごとのコールバックへの同時呼び出しの最大数。

**デフォルト値**: `1`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__maxConcurrentCallsPerSession`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__maxConcurrentCallsPerSession",
  "value": "1",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionProcessorOptions": {
        "maxConcurrentCallsPerSession": 1
      }
    }
  }
}
```

**推奨設定**:
- 順次処理: `1` (推奨)
- 並列処理: `2-4`

---

### extensions.serviceBus.sessionProcessorOptions.sessionIdleTimeout

**スキーマ参照**: [host_schema_translated.json:1337](host_schema_translated.json#L1337)

**説明**: セッションアイドルタイムアウト。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__sessionIdleTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__sessionIdleTimeout",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionProcessorOptions": {
        "sessionIdleTimeout": "00:01:00"
      }
    }
  }
}
```

---

### extensions.serviceBus.sessionProcessorOptions.autoCompleteMessages

**スキーマ参照**: [host_schema_translated.json:1305](host_schema_translated.json#L1305)

**説明**: セッションプロセッサがメッセージを自動的に完了するかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__autoCompleteMessages`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__autoCompleteMessages",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionProcessorOptions": {
        "autoCompleteMessages": true
      }
    }
  }
}
```

---

### extensions.serviceBus.sessionProcessorOptions.maxAutoLockRenewalDuration

**スキーマ参照**: [host_schema_translated.json:1310](host_schema_translated.json#L1310)

**説明**: セッションメッセージロックが自動的に更新される最大期間。

**デフォルト値**: `00:05:00` (5分)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__maxAutoLockRenewalDuration`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionProcessorOptions__maxAutoLockRenewalDuration",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionProcessorOptions": {
        "maxAutoLockRenewalDuration": "00:05:00"
      }
    }
  }
}
```

---

### extensions.serviceBus.enableCrossEntityTransactions

**スキーマ参照**: [host_schema_translated.json:1342](host_schema_translated.json#L1342)

**説明**: エンティティ間のトランザクションを有効にするかどうか。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__enableCrossEntityTransactions`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__enableCrossEntityTransactions",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "enableCrossEntityTransactions": false
    }
  }
}
```

---

### extensions.serviceBus.maxBatchWaitTime

**スキーマ参照**: [host_schema_translated.json:1331](host_schema_translated.json#L1331)

**説明**: バッチを待機する最大時間。

**デフォルト値**: `00:00:00` (待機なし)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__maxBatchWaitTime`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__maxBatchWaitTime",
  "value": "00:00:01",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "maxBatchWaitTime": "00:00:01"
    }
  }
}
```

**推奨設定**:
- 待機なし: `00:00:00`
- 短い待機: `00:00:01` (1秒)
- 標準待機: `00:00:05` (5秒)

---

### extensions.serviceBus.batchOptions.autoComplete

**スキーマ参照**: [host_schema_translated.json:1233](host_schema_translated.json#L1233)

**説明**: バッチ処理でメッセージを自動完了するかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__batchOptions__autoComplete`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__batchOptions__autoComplete",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "batchOptions": {
        "autoComplete": true
      }
    }
  }
}
```

---

### extensions.serviceBus.batchOptions.maxMessageCount

**スキーマ参照**: [host_schema_translated.json:1224](host_schema_translated.json#L1224)

**説明**: バッチあたりの最大メッセージ数。

**デフォルト値**: `1000`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__batchOptions__maxMessageCount`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__batchOptions__maxMessageCount",
  "value": "1000",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "batchOptions": {
        "maxMessageCount": 1000
      }
    }
  }
}
```

---

### extensions.serviceBus.batchOptions.operationTimeout

**スキーマ参照**: [host_schema_translated.json:1228](host_schema_translated.json#L1228)

**説明**: バッチ操作のタイムアウト。

**デフォルト値**: `00:01:00` (1分)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__batchOptions__operationTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__batchOptions__operationTimeout",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "batchOptions": {
        "operationTimeout": "00:01:00"
      }
    }
  }
}
```

---

### extensions.serviceBus.messageHandlerOptions.autoComplete

**スキーマ参照**: [host_schema_translated.json:1188](host_schema_translated.json#L1188)

**説明**: メッセージハンドラーでメッセージを自動完了するかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__messageHandlerOptions__autoComplete`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__messageHandlerOptions__autoComplete",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "messageHandlerOptions": {
        "autoComplete": true
      }
    }
  }
}
```

---

### extensions.serviceBus.messageHandlerOptions.maxAutoRenewDuration

**スキーマ参照**: [host_schema_translated.json:1182](host_schema_translated.json#L1182)

**説明**: メッセージハンドラーでロックを自動更新する最大期間。

**デフォルト値**: `00:05:00` (5分)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__messageHandlerOptions__maxAutoRenewDuration`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__messageHandlerOptions__maxAutoRenewDuration",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "messageHandlerOptions": {
        "maxAutoRenewDuration": "00:05:00"
      }
    }
  }
}
```

---

### extensions.serviceBus.messageHandlerOptions.maxConcurrentCalls

**スキーマ参照**: [host_schema_translated.json:1176](host_schema_translated.json#L1176)

**説明**: メッセージハンドラーの最大同時呼び出し数。

**デフォルト値**: `16`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__messageHandlerOptions__maxConcurrentCalls`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__messageHandlerOptions__maxConcurrentCalls",
  "value": "16",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "messageHandlerOptions": {
        "maxConcurrentCalls": 16
      }
    }
  }
}
```

---

### extensions.serviceBus.sessionHandlerOptions.autoComplete

**スキーマ参照**: [host_schema_translated.json:1204](host_schema_translated.json#L1204)

**説明**: セッションハンドラーでメッセージを自動完了するかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionHandlerOptions__autoComplete`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionHandlerOptions__autoComplete",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionHandlerOptions": {
        "autoComplete": true
      }
    }
  }
}
```

---

### extensions.serviceBus.sessionHandlerOptions.maxAutoRenewDuration

**スキーマ参照**: [host_schema_translated.json:1198](host_schema_translated.json#L1198)

**説明**: セッションハンドラーでロックを自動更新する最大期間。

**デフォルト値**: `00:05:00` (5分)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionHandlerOptions__maxAutoRenewDuration`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionHandlerOptions__maxAutoRenewDuration",
  "value": "00:05:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionHandlerOptions": {
        "maxAutoRenewDuration": "00:05:00"
      }
    }
  }
}
```

---

### extensions.serviceBus.sessionHandlerOptions.maxConcurrentSessions

**スキーマ参照**: [host_schema_translated.json:1210](host_schema_translated.json#L1210)

**説明**: セッションハンドラーの最大同時セッション数。

**デフォルト値**: `8`

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionHandlerOptions__maxConcurrentSessions`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionHandlerOptions__maxConcurrentSessions",
  "value": "8",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionHandlerOptions": {
        "maxConcurrentSessions": 8
      }
    }
  }
}
```

---

### extensions.serviceBus.sessionHandlerOptions.messageWaitTimeout

**スキーマ参照**: [host_schema_translated.json:1215](host_schema_translated.json#L1215)

**説明**: セッションハンドラーがメッセージを待機するタイムアウト。

**デフォルト値**: `00:00:30` (30秒)

**環境変数名**: `AzureFunctionsJobHost__extensions__serviceBus__sessionHandlerOptions__messageWaitTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__serviceBus__sessionHandlerOptions__messageWaitTimeout",
  "value": "00:00:30",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "serviceBus": {
      "sessionHandlerOptions": {
        "messageWaitTimeout": "00:00:30"
      }
    }
  }
}
```

---

## Event Hubs設定

Azure Event Hubsトリガーの構成設定です。

### extensions.eventHubs.maxEventBatchSize

**スキーマ参照**: [host_schema_translated.json:1364](host_schema_translated.json#L1364)

**説明**: イベントバッチごとに受信するイベントの最大数。

**デフォルト値**: `10`

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__maxEventBatchSize`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__maxEventBatchSize",
  "value": "10",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "maxEventBatchSize": 10
    }
  }
}
```

**推奨設定**:
- 小規模バッチ: `10`
- 標準: `64`
- 大規模バッチ: `100`

---

### extensions.eventHubs.minEventBatchSize

**スキーマ参照**: [host_schema_translated.json:1364](host_schema_translated.json#L1364)

**説明**: イベントバッチごとに受信するイベントの最小数。

**デフォルト値**: `1`

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__minEventBatchSize`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__minEventBatchSize",
  "value": "1",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "minEventBatchSize": 1
    }
  }
}
```

---

### extensions.eventHubs.targetUnprocessedEventThreshold

**スキーマ参照**: [host_schema_translated.json:1358](host_schema_translated.json#L1358)

**説明**: スケーリングを制御するために使用される未処理イベントのしきい値。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__targetUnprocessedEventThreshold`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__targetUnprocessedEventThreshold",
  "value": "100",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "targetUnprocessedEventThreshold": 100
    }
  }
}
```

**推奨設定**:
- 敏感なスケール: `50`
- 標準: `100`
- 緩やかなスケール: `200`

---

### extensions.eventHubs.clientRetryOptions.mode

**スキーマ参照**: [host_schema_translated.json:1420](host_schema_translated.json#L1420)

**説明**: Event Hubs操作失敗時の再試行戦略。

**デフォルト値**: `Exponential`

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__mode`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__mode",
  "value": "Exponential",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "clientRetryOptions": {
        "mode": "Exponential"
      }
    }
  }
}
```

---

### extensions.eventHubs.clientRetryOptions.tryTimeout

**スキーマ参照**: [host_schema_translated.json:1428](host_schema_translated.json#L1428)

**説明**: 個別の試行に許可される最大期間。

**デフォルト値**: `00:01:00` (1分)

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__tryTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__tryTimeout",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "clientRetryOptions": {
        "tryTimeout": "00:01:00"
      }
    }
  }
}
```

---

### extensions.eventHubs.clientRetryOptions.delay

**スキーマ参照**: [host_schema_translated.json:1434](host_schema_translated.json#L1434)

**説明**: 再試行間の遅延時間。

**デフォルト値**: `00:00:00.8` (0.8秒)

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__delay`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__delay",
  "value": "00:00:00.8",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "clientRetryOptions": {
        "delay": "00:00:00.8"
      }
    }
  }
}
```

---

### extensions.eventHubs.clientRetryOptions.maxDelay

**スキーマ参照**: [host_schema_translated.json:1440](host_schema_translated.json#L1440)

**説明**: 再試行間の最大遅延時間。

**デフォルト値**: `00:01:00` (1分)

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__maxDelay`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__maxDelay",
  "value": "00:01:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "clientRetryOptions": {
        "maxDelay": "00:01:00"
      }
    }
  }
}
```

---

### extensions.eventHubs.clientRetryOptions.maxRetries

**スキーマ参照**: [host_schema_translated.json:1446](host_schema_translated.json#L1446)

**説明**: 最大再試行回数。

**デフォルト値**: `3`

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__maxRetries`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__clientRetryOptions__maxRetries",
  "value": "3",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "clientRetryOptions": {
        "maxRetries": 3
      }
    }
  }
}
```

---

### extensions.eventHubs.loadBalancingUpdateInterval

**スキーマ参照**: [host_schema_translated.json:1458](host_schema_translated.json#L1458)

**説明**: 負荷分散の更新間隔。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__loadBalancingUpdateInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__loadBalancingUpdateInterval",
  "value": "00:00:10",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "loadBalancingUpdateInterval": "00:00:10"
    }
  }
}
```

**推奨設定**:
- 高頻度更新: `00:00:05` (5秒)
- 標準: `00:00:10` (10秒)
- 低頻度更新: `00:00:30` (30秒)

---

### extensions.eventHubs.partitionOwnershipExpirationInterval

**スキーマ参照**: [host_schema_translated.json:1464](host_schema_translated.json#L1464)

**説明**: パーティション所有権の有効期限間隔。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__partitionOwnershipExpirationInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__partitionOwnershipExpirationInterval",
  "value": "00:00:30",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "partitionOwnershipExpirationInterval": "00:00:30"
    }
  }
}
```

---

### extensions.eventHubs.batchCheckpointFrequency

**スキーマ参照**: [host_schema_translated.json:1370](host_schema_translated.json#L1370)

**説明**: バッチ処理でチェックポイントを作成する頻度。

**デフォルト値**: `1`

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__batchCheckpointFrequency`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__batchCheckpointFrequency",
  "value": "1",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "batchCheckpointFrequency": 1
    }
  }
}
```

---

### extensions.eventHubs.initialOffsetOptions.type

**スキーマ参照**: [host_schema_translated.json:1401](host_schema_translated.json#L1401)

**説明**: イベント処理の初期オフセットタイプ。

**デフォルト値**: `fromStart`

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__initialOffsetOptions__type`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__initialOffsetOptions__type",
  "value": "fromStart",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "initialOffsetOptions": {
        "type": "fromStart"
      }
    }
  }
}
```

**推奨設定**:
- 最初から: `fromStart`
- 最新のみ: `fromEnd`
- 特定時刻から: `fromEnqueuedTime`

---

### extensions.eventHubs.prefetchCount

**スキーマ参照**: [host_schema_translated.json:1375](host_schema_translated.json#L1375)

**説明**: プリフェッチするイベントの数。

**デフォルト値**: `300`

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__prefetchCount`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__prefetchCount",
  "value": "300",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "prefetchCount": 300
    }
  }
}
```

**推奨設定**:
- 小規模: `100`
- 標準: `300`
- 大規模: `500`

---

### extensions.eventHubs.transportType

**スキーマ参照**: [host_schema_translated.json:1380](host_schema_translated.json#L1380)

**説明**: Event Hubsとの通信に使用するトランスポートの種類。

**デフォルト値**: `AmqpTcp`

**環境変数名**: `AzureFunctionsJobHost__extensions__eventHubs__transportType`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__eventHubs__transportType",
  "value": "AmqpTcp",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "eventHubs": {
      "transportType": "AmqpTcp"
    }
  }
}
```

**推奨設定**:
- 標準: `AmqpTcp`
- Webソケット経由: `AmqpWebSockets` (ファイアウォール環境)

---

## Blobs設定

Azure Blobsトリガーの構成設定です。

### extensions.blobs.maxDegreeOfParallelism

**スキーマ参照**: [host_schema_translated.json:1532](host_schema_translated.json#L1532)

**説明**: 各関数呼び出しに対する同時アップロードの数。

**デフォルト値**: `8 * コア数`

**環境変数名**: `AzureFunctionsJobHost__extensions__blobs__maxDegreeOfParallelism`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__blobs__maxDegreeOfParallelism",
  "value": "32",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "blobs": {
      "maxDegreeOfParallelism": 32
    }
  }
}
```

**推奨設定**:
- 小規模: `16`
- 標準: `32`
- 大規模: `64`

---

### extensions.blobs.poisonBlobThreshold

**スキーマ参照**: [host_schema_translated.json:1537](host_schema_translated.json#L1537)

**説明**: Blob処理が失敗した場合に毒メッセージとして扱うまでの試行回数。

**デフォルト値**: `5`

**環境変数名**: `AzureFunctionsJobHost__extensions__blobs__poisonBlobThreshold`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__blobs__poisonBlobThreshold",
  "value": "5",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "blobs": {
      "poisonBlobThreshold": 5
    }
  }
}
```

**推奨設定**:
- 少ない再試行: `3`
- 標準: `5`
- 多い再試行: `10`

---

## ログ設定

Azure Functionsのログ記録とApplication Insightsの構成設定です。

### logging.logLevel.default

**スキーマ参照**: [host_schema_translated.json:707](host_schema_translated.json#L707)

**説明**: デフォルトのログレベル。

**デフォルト値**: `Information`

**環境変数名**: `AzureFunctionsJobHost__logging__logLevel__default`

**設定例(Azure Portal)**:
```json
{
  "name": "AzureFunctionsJobHost__logging__logLevel__default",
  "value": "Information",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "logLevel": {
      "default": "Information"
    }
  }
}
```

**推奨設定**:
- 開発環境: `Debug`
- ステージング: `Information`
- 本番環境: `Warning`

---

### logging.logLevel.Function

**スキーマ参照**: [host_schema_translated.json:720](host_schema_translated.json#L720)

**説明**: Function カテゴリのログレベル。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__logging__logLevel__Function`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__logLevel__Function",
  "value": "Information",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "logLevel": {
      "Function": "Information"
    }
  }
}
```

---

### logging.logLevel.Host.Aggregator

**スキーマ参照**: [host_schema_translated.json:720](host_schema_translated.json#L720)

**説明**: Host.Aggregatorカテゴリのログレベル。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__logging__logLevel__Host.Aggregator`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__logLevel__Host.Aggregator",
  "value": "Trace",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "logLevel": {
      "Host.Aggregator": "Trace"
    }
  }
}
```

---

### logging.logLevel.Host.Results

**スキーマ参照**: [host_schema_translated.json:720](host_schema_translated.json#L720)

**説明**: Host.Resultsカテゴリのログレベル。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__logging__logLevel__Host.Results`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__logLevel__Host.Results",
  "value": "Information",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "logLevel": {
      "Host.Results": "Information"
    }
  }
}
```

---

### logging.applicationInsights.samplingSettings.isEnabled

**スキーマ参照**: [host_schema_translated.json:740](host_schema_translated.json#L740)

**説明**: Application Insightsサンプリングを有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__isEnabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__isEnabled",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true
      }
    }
  }
}
```

**推奨設定**:
- 本番環境: `true` (コスト削減)
- 開発環境: `false` (完全なログ)

---

### logging.applicationInsights.samplingSettings.maxTelemetryItemsPerSecond

**スキーマ参照**: [host_schema_translated.json:745](host_schema_translated.json#L745)

**説明**: 各サーバーホストでログに記録されるテレメトリ項目の最大数/秒。

**デフォルト値**: `20`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__maxTelemetryItemsPerSecond`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__maxTelemetryItemsPerSecond",
  "value": "20",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "maxTelemetryItemsPerSecond": 20
      }
    }
  }
}
```

**推奨設定**:
- 低コスト: `5`
- 標準: `20`
- 詳細ログ: `50`

---

### logging.applicationInsights.samplingSettings.excludedTypes

**スキーマ参照**: [host_schema_translated.json:779](host_schema_translated.json#L779)

**説明**: サンプリングから除外するテレメトリタイプのセミコロン区切りリスト。

**デフォルト値**: 空

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__excludedTypes`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__excludedTypes",
  "value": "Request;Exception",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "excludedTypes": "Request;Exception"
      }
    }
  }
}
```

**推奨設定**:
- すべてサンプリング: 空
- リクエストと例外は常に記録: `Request;Exception`

---

### logging.applicationInsights.samplingSettings.includedTypes

**スキーマ参照**: [host_schema_translated.json:784](host_schema_translated.json#L784)

**説明**: サンプリングに含めるテレメトリタイプのセミコロン区切りリスト。

**デフォルト値**: 空（すべて含める）

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__includedTypes`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__includedTypes",
  "value": "Dependency;Trace",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "includedTypes": "Dependency;Trace"
      }
    }
  }
}
```

---

### logging.applicationInsights.snapshotConfiguration.isEnabled

**スキーマ参照**: [host_schema_translated.json:857](host_schema_translated.json#L857)

**説明**: スナップショットデバッガーを有効にするかどうか。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__snapshotConfiguration__isEnabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__snapshotConfiguration__isEnabled",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "snapshotConfiguration": {
        "isEnabled": false
      }
    }
  }
}
```

**推奨設定**:
- 本番環境: `false`
- トラブルシューティング時: `true`

---

### logging.applicationInsights.enableLiveMetrics

**スキーマ参照**: [host_schema_translated.json:796](host_schema_translated.json#L796)

**説明**: Live Metricsコレクションを有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__enableLiveMetrics`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__enableLiveMetrics",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "enableLiveMetrics": true
    }
  }
}
```

**推奨設定**:
- 本番環境: `true` (リアルタイム監視)
- 開発環境: `true`

---

### logging.applicationInsights.enableLiveMetricsFilters

**スキーマ参照**: [host_schema_translated.json:796](host_schema_translated.json#L796)

**説明**: Live Metricsフィルターを有効にするかどうか。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__enableLiveMetricsFilters`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__enableLiveMetricsFilters",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "enableLiveMetricsFilters": false
    }
  }
}
```

---

### logging.applicationInsights.enableDependencyTracking

**スキーマ参照**: [host_schema_translated.json:801](host_schema_translated.json#L801)

**説明**: 依存関係の追跡を有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__enableDependencyTracking`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__enableDependencyTracking",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "enableDependencyTracking": true
    }
  }
}
```

**推奨設定**:
- 本番環境: `true` (推奨)
- 低コスト環境: `false`

---

### logging.applicationInsights.enablePerformanceCountersCollection

**スキーマ参照**: [host_schema_translated.json:806](host_schema_translated.json#L806)

**説明**: パフォーマンスカウンターの収集を有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__enablePerformanceCountersCollection`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__enablePerformanceCountersCollection",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "enablePerformanceCountersCollection": true
    }
  }
}
```

---

### logging.applicationInsights.httpAutoCollectionOptions.enableHttpTriggerExtendedInfoCollection

**スキーマ参照**: [host_schema_translated.json:813](host_schema_translated.json#L813)

**説明**: HTTPトリガーの拡張情報収集を有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__httpAutoCollectionOptions__enableHttpTriggerExtendedInfoCollection`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__httpAutoCollectionOptions__enableHttpTriggerExtendedInfoCollection",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "httpAutoCollectionOptions": {
        "enableHttpTriggerExtendedInfoCollection": true
      }
    }
  }
}
```

---

### logging.applicationInsights.httpAutoCollectionOptions.enableResponseHeaderInjection

**スキーマ参照**: [host_schema_translated.json:823](host_schema_translated.json#L823)

**説明**: HTTP応答ヘッダーへのトレース情報の挿入を有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__httpAutoCollectionOptions__enableResponseHeaderInjection`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__httpAutoCollectionOptions__enableResponseHeaderInjection",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "httpAutoCollectionOptions": {
        "enableResponseHeaderInjection": true
      }
    }
  }
}
```

---

### logging.applicationInsights.httpAutoCollectionOptions.enableW3CDistributedTracing

**スキーマ参照**: [host_schema_translated.json:824](host_schema_translated.json#L824)

**説明**: W3C分散トレースプロトコルのサポートを有効または無効にします。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__logging__applicationInsights__httpAutoCollectionOptions__enableW3CDistributedTracing`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__applicationInsights__httpAutoCollectionOptions__enableW3CDistributedTracing",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "applicationInsights": {
      "httpAutoCollectionOptions": {
        "enableW3CDistributedTracing": true
      }
    }
  }
}
```

**推奨設定**:
- 標準: `true` (W3Cトレース有効)
- レガシー: `false` (旧相関スキーマ使用)

---

### logging.fileLoggingMode

**スキーマ参照**: [host_schema_translated.json:1005](host_schema_translated.json#L1005)

**説明**: ファイルログモードを指定します。

**デフォルト値**: `debugOnly`

**環境変数名**: `AzureFunctionsJobHost__logging__fileLoggingMode`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__fileLoggingMode",
  "value": "debugOnly",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "fileLoggingMode": "debugOnly"
  }
}
```

**推奨設定**:
- デバッグのみ: `debugOnly`
- 常に有効: `always`
- 無効: `never`

---

### logging.console.isEnabled

**スキーマ参照**: [host_schema_translated.json:1018](host_schema_translated.json#L1018)

**説明**: コンソールログを有効にするかどうか。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__logging__console__isEnabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__logging__console__isEnabled",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "logging": {
    "console": {
      "isEnabled": false
    }
  }
}
```

---

### extensions.applicationInsights.enableLiveMetrics

**スキーマ参照**: [host_schema_translated.json:796](host_schema_translated.json#L796)

**説明**: Application InsightsのLive Metricsを有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__enableLiveMetrics`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__enableLiveMetrics",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "enableLiveMetrics": true
    }
  }
}
```

---

### extensions.applicationInsights.enableW3CDistributedTracing

**スキーマ参照**: [host_schema_translated.json:823](host_schema_translated.json#L823)

**説明**: W3C分散トレーシングを有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__enableW3CDistributedTracing`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__enableW3CDistributedTracing",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "enableW3CDistributedTracing": true
    }
  }
}
```

---

### extensions.applicationInsights.samplingSettings.evaluationInterval

**スキーマ参照**: [host_schema_translated.json:749](host_schema_translated.json#L749)

**説明**: サンプリング評価の間隔。

**デフォルト値**: `01:00:00` (1時間)

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__evaluationInterval`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__evaluationInterval",
  "value": "01:00:00",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "samplingSettings": {
        "evaluationInterval": "01:00:00"
      }
    }
  }
}
```

---

### extensions.applicationInsights.samplingSettings.initialSamplingPercentage

**スキーマ参照**: [host_schema_translated.json:754](host_schema_translated.json#L754)

**説明**: サンプリングの初期パーセンテージ。

**デフォルト値**: `100.0`

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__initialSamplingPercentage`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__initialSamplingPercentage",
  "value": "100.0",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "samplingSettings": {
        "initialSamplingPercentage": 100.0
      }
    }
  }
}
```

---

### extensions.applicationInsights.samplingSettings.maxSamplingPercentage

**スキーマ参照**: [host_schema_translated.json:774](host_schema_translated.json#L774)

**説明**: サンプリングの最大パーセンテージ。

**デフォルト値**: `100.0`

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__maxSamplingPercentage`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__maxSamplingPercentage",
  "value": "100.0",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "samplingSettings": {
        "maxSamplingPercentage": 100.0
      }
    }
  }
}
```

---

### extensions.applicationInsights.samplingSettings.minSamplingPercentage

**スキーマ参照**: [host_schema_translated.json:769](host_schema_translated.json#L769)

**説明**: サンプリングの最小パーセンテージ。

**デフォルト値**: `0.1`

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__minSamplingPercentage`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__minSamplingPercentage",
  "value": "0.1",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "samplingSettings": {
        "minSamplingPercentage": 0.1
      }
    }
  }
}
```

---

### extensions.applicationInsights.samplingSettings.movingAverageRatio

**スキーマ参照**: [host_schema_translated.json:779](host_schema_translated.json#L779)

**説明**: 移動平均の計算で使用する比率。

**デフォルト値**: `1`

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__movingAverageRatio`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__movingAverageRatio",
  "value": "1",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "samplingSettings": {
        "movingAverageRatio": 1
      }
    }
  }
}
```

---

### extensions.applicationInsights.samplingSettings.samplingPercentageDecreaseTimeout

**スキーマ参照**: [host_schema_translated.json:764](host_schema_translated.json#L764)

**説明**: サンプリングパーセンテージを減少させるまでのタイムアウト。

**デフォルト値**: `00:00:01` (1秒)

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__samplingPercentageDecreaseTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__samplingPercentageDecreaseTimeout",
  "value": "00:00:01",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "samplingSettings": {
        "samplingPercentageDecreaseTimeout": "00:00:01"
      }
    }
  }
}
```

---

### extensions.applicationInsights.samplingSettings.samplingPercentageIncreaseTimeout

**スキーマ参照**: [host_schema_translated.json:759](host_schema_translated.json#L759)

**説明**: サンプリングパーセンテージを増加させるまでのタイムアウト。

**デフォルト値**: `00:00:01` (1秒)

**環境変数名**: `AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__samplingPercentageIncreaseTimeout`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__extensions__applicationInsights__samplingSettings__samplingPercentageIncreaseTimeout",
  "value": "00:00:01",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "extensions": {
    "applicationInsights": {
      "samplingSettings": {
        "samplingPercentageIncreaseTimeout": "00:00:01"
      }
    }
  }
}
```

---

## その他の設定

### managedDependency.enabled

**スキーマ参照**: [host_schema_translated.json:1021](host_schema_translated.json#L1021)

**説明**: マネージド依存関係機能を有効にするかどうか。PowerShell関数で依存関係を自動管理します。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__managedDependency__enabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__managedDependency__enabled",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "managedDependency": {
    "enabled": false
  }
}
```

**推奨設定**:
- PowerShell関数: `true`
- その他: `false`

---

### customHandler.description.defaultExecutablePath

**スキーマ参照**: [host_schema_translated.json:1097](host_schema_translated.json#L1097)

**説明**: カスタムハンドラー実行ファイルのパス。

**デフォルト値**: `handler`

**環境変数名**: `AzureFunctionsJobHost__customHandler__description__defaultExecutablePath`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__customHandler__description__defaultExecutablePath",
  "value": "handler",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "customHandler": {
    "description": {
      "defaultExecutablePath": "handler"
    }
  }
}
```

**使用例**:
- Go: `handler` または `handler.exe`
- Rust: `handler` または `handler.exe`
- カスタム: 任意の実行ファイルパス

---

### concurrency.dynamicConcurrencyEnabled

**スキーマ参照**: [host_schema_translated.json:1552](host_schema_translated.json#L1552)

**説明**: 動的並行性を有効にするかどうか。有効にすると、ランタイムは各関数の並行性を動的に調整します。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__concurrency__dynamicConcurrencyEnabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__concurrency__dynamicConcurrencyEnabled",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "concurrency": {
    "dynamicConcurrencyEnabled": false
  }
}
```

**推奨設定**:
- 本番環境(Premium/Dedicated): `true` (推奨)
- Consumption: `false`
- 開発環境: `false`

---

### concurrency.maximumFunctionConcurrency

**スキーマ参照**: [host_schema_translated.json:1548](host_schema_translated.json#L1548)

> **補足**: 公式 host.json v2 スキーマには `maximumFunctionConcurrency` プロパティが記載されていません。`concurrency` オブジェクトの仕様 (L1548 以降) のみ公開されています。

**説明**: 関数の最大並行実行数。

**デフォルト値**: 未設定

**環境変数名**: `AzureFunctionsJobHost__concurrency__maximumFunctionConcurrency`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__concurrency__maximumFunctionConcurrency",
  "value": "100",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "concurrency": {
    "maximumFunctionConcurrency": 100
  }
}
```

**推奨設定**:
- 小規模: `50`
- 標準: `100`
- 大規模: `500`

---

### sendCanceledInvocationsToWorker

**スキーマ参照**: [host_schema_translated.json:1566](host_schema_translated.json#L1566)

**説明**: キャンセルされた呼び出しをワーカープロセスに送信するかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__sendCanceledInvocationsToWorker`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__sendCanceledInvocationsToWorker",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "sendCanceledInvocationsToWorker": true
}
```

**推奨設定**:
- 通常: `true` (デフォルト)
- キャンセル処理が不要: `false`

---

### concurrency.snapshotPersistenceEnabled

**スキーマ参照**: [host_schema_translated.json:1557](host_schema_translated.json#L1557)

**説明**: 同時実行のスナップショット永続化を有効にするかどうか。

**デフォルト値**: `true`

**環境変数名**: `AzureFunctionsJobHost__concurrency__snapshotPersistenceEnabled`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__concurrency__snapshotPersistenceEnabled",
  "value": "true",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "concurrency": {
    "snapshotPersistenceEnabled": true
  }
}
```

---

### customHandler.enableForwardingHttpRequest

**スキーマ参照**: [host_schema_translated.json:1115](host_schema_translated.json#L1115)

**説明**: カスタムハンドラーへのHTTPリクエスト転送を有効にするかどうか。

**デフォルト値**: `false`

**環境変数名**: `AzureFunctionsJobHost__customHandler__enableForwardingHttpRequest`

**設定例（Azure Portal）**:
```json
{
  "name": "AzureFunctionsJobHost__customHandler__enableForwardingHttpRequest",
  "value": "false",
  "slotSetting": false
}
```

**host.jsonでの設定**:
```json
{
  "customHandler": {
    "enableForwardingHttpRequest": false
  }
}
```

---