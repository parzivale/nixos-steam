# steam_dev.cfg overridable convars (`@`-prefixed)

Steam Linux client, manifest `1791918634`.

## Method

I pulled every string matching `^@[A-Za-z][A-Za-z0-9_]{5,}$` out of `strs/steamrt64__steamclient.so.txt`. A few matches were protobuf or enum noise (`@CMarketing…`, `@k_…`, random bytes) and are excluded. That leaves **210 names**.

In the first ~100k lines of `steamclient.so` the strings are still in source order. In that region, each convar's registration places its help text, then its default value (when it isn't 0 or empty), then its name. **56** names fall in that region and have a description adjacent, and some of them also have a default. For those, the description and default are read straight off the neighbouring strings. The rest come from the hash-ordered part of the string table, so for them only the name is known.

Usage (community-documented): put one `@name value` per line in `<steam root>/steam_dev.cfg`. Note that `steam_dev.cfg` also puts the install in development mode: no `~/.steam/steam` symlink, `--reset` refuses to run, and no bootstrap reinstall (see [steam-cfg-and-magic-files.md](steam-cfg-and-magic-files.md)).

Name prefixes follow Valve's Hungarian notation:

| Prefix | Type |
|---|---|
| `b` | bool |
| `n`, `c`, `u`, `un` | integer |
| `f` | float |
| `s` | string |
| `csec` | seconds |
| `cb` | bytes |

Some names are not client options:

* `DepotBuilder*`, `HTTPServer*`, `SiteLicense*` and `SteamCmd*` belong to steamcmd, depot tooling, or site-license (cafe) servers that share `steamclient.so`.
* `test_*` are test hooks.

Non-`@` settings registered next to these are documented with the client binary, not here. Examples: `unShaderBackgroundProcessingThreads`, `bShaderAllowReplay`, `bVerifyAllDownloads`, `nClientBackgroundAutoUpdateTargetHour`.

| Convar | Default (if adjacent) | Description (if adjacent in ordered strings) |
|---|---|---|
| `@bAssertOnProtoBufBodyMismatch` |  |  |
| `@bCallerDeadlineAbortJobDisableWhenHTTPReqStart` |  |  |
| `@bClientDownloadUseHTTPS` |  | Set this to use HTTPS on supported download servers |
| `@bClientOpenCacheStickyRedirects` |  |  |
| `@bClientTryRequestManifestWithoutCode` |  | If set, client will try to get a manifest even without a manifest request code |
| `@bCloudSyncFailDownloadIfGameOutOfDate` |  |  |
| `@bCSForceNoCache` |  |  |
| `@bDepotBuilderReadBufferSizeKB` |  |  |
| `@bDepotBuilderUnbufferedReads` |  |  |
| `@bDisableDualStackDownloads` |  |  |
| `@bDownloadThrottleDuringCloudSync` |  |  |
| `@bEnableFrameFuncOverageWarnings` |  |  |
| `@bEnableHTTP2OnAllCHTTPClients` |  |  |
| `@bEnableLogTearOff` |  |  |
| `@bEnableNetworkJobsOwnStartList` |  |  |
| `@bEnableOfflineLogonTicket` |  | If true, an offline logon ticket will be requested during logon if none is cached |
| `@bEnableSiteLicenseConnect` |  |  |
| `@bEnableSiteLicenseConsoleLogging` |  |  |
| `@bEnableSpewThrottle` |  |  |
| `@bEnforceValidEmailDomains` |  |  |
| `@bForceStreamUnsupportedApp` |  |  |
| `@bHttpClientRecordHostnameDimension` |  |  |
| `@bHTTPServerHTTP2Enabled` |  |  |
| `@bLANPeerConnectionTimeoutSec` |  |  |
| `@bLogMessageToProtobufClass` |  |  |
| `@bMeasureSSLLatencyStats` |  |  |
| `@bMetricsEnabled` |  |  |
| `@bMsgErrorDump` |  |  |
| `@bProfileYieldsInTestSuiteJobs` |  |  |
| `@bProtoBufNetPacketDropRawBytes` |  |  |
| `@bProtobufParseSizeProfile` |  |  |
| `@bProtobufParseTimeProfile` |  |  |
| `@bRefreshDownloadSourcesFrequently` |  |  |
| `@bRequireOfflineLogonTicket` |  | If true, a valid offline logon ticket is required when logging in in offline or no connection mode |
| `@bScreenshotsLegacyCloudUpload` |  | If set, use the legacy Steam Cloud upload path for screenshot uploads |
| `@bShaderClientGetBucketManifestUseWebAPI` |  |  |
| `@bSiteLicenseAllowCachedClientCredentials` |  | Allow Steam clients that associate to this site to save username and auth credentials locally |
| `@bSiteLicenseProxyCacheIsExternalProcess` |  | If set, the caching content proxy will be handled by some process other than steamcmd. You probably also should set @sSiteLicenseProxyExplicitIP. |
| `@bSiteLicenseProxyEnableIPv6` |  | If set, we will enable ipv6 communications to the Steam servers |
| `@bSiteLicenseServer` |  |  |
| `@bSSLThreadedMsgParse` |  |  |
| `@bSSLThreadedMsgParseRelayedBodies` |  |  |
| `@bSSLThreadedSendDelivery` |  |  |
| `@cbPartnerUploadChunkSize` | 1000000 | Chunk size to use for POSTing partner uploads |
| `@cCSClientMaxNumSocketsPerHost` |  |  |
| `@cCSClientMaxNumSocketsPerHostForCachingProxy` |  |  |
| `@cDefaultInitialDownloadSources` |  |  |
| `@cDepotBuilderFileChunkingThreads` |  |  |
| `@cFileChunkingCRCFalseAlarmBytesToSkip` |  |  |
| `@cFileChunkingCRCFalseAlarmThreshold` |  |  |
| `@cFileChunkingSupersectionSizeMB` |  |  |
| `@cloud_testdynamicsyncapp` |  |  |
| `@cMaxContentServersToRequest` |  |  |
| `@cMaxInitialDownloadSources` |  |  |
| `@cMinimumJobTimeoutsToCheckPerFrame` |  |  |
| `@cNetEncryptionHandshakeWorkMax_HighPri` |  |  |
| `@cNetEncryptionHandshakeWorkMax_LowPri` |  |  |
| `@cNetEncryptionHandshakeWorkMax_MedPri` |  |  |
| `@csecCSJobSuccessfulRequestTimeWindow` |  |  |
| `@csecCSRequestProcessorTimeOut` | 300 |  |
| `@csecDurationControlPeriod` |  | Override default duration-control / anti-indulgence time period. If nonzero, initial playtime threshold is this value in seconds |
| `@csecDurationControlPeriodToday` |  | Override default duration-control / anti-indulgence time period. If nonzero, per-day playtime threshold is this value in seconds |
| `@csecDurationControlSimulated` |  | Simulate having already played this many seconds of playtime. |
| `@csecDurationControlSimulatedNonRecent` |  | Simulate having already played this many seconds of playtime today, but not recently. |
| `@csecFavoriteGameAccountCacheTime` | 86400 | Control how often we refresh the account IDs in the game server favorites list |
| `@csecIncomingDataRatePeriod` |  |  |
| `@csecSiteLicenseProxyStatsLog` |  | Log proxy stats this often |
| `@csecSiteLicenseProxyStatsUpdate` |  | update proxy stats internally this often |
| `@csecUpdateTargetNumConnectionsEpoch` |  |  |
| `@cSecUploadDownloadRates` | 300 |  |
| `@CSInterfaceProxyPassword` |  |  |
| `@CSInterfaceProxyUsername` |  |  |
| `@cUDPSendRetries` |  |  |
| `@CustomBinaryRequestRetryTimes` |  |  |
| `@DepotBuilderDeltaMaxChunks` | 20000 |  |
| `@DepotBuilderEnableVZd` |  |  |
| `@DepotBuilderMaxParallelUploadChunks` |  |  |
| `@DepotBuilderNumHTTPSocketsToMDS` |  |  |
| `@DepotBuilderParallelUploadChunks` |  |  |
| `@DepotBuilderProgressTimeout` |  |  |
| `@DepotBuilderVZdMinRatio` | 0.4 |  |
| `@DepotBuilderXORMatchPercent` |  |  |
| `@durationControlNightCheck` |  | Time of day check for duration-control feature. 1 = normal. 2 = force night-time. 0 = disable checks, only enabled for age verified accounts |
| `@EnableUDPHistory` |  |  |
| `@fDownloadRateImprovementToAddAnotherConnection` | 1.2 |  |
| `@fMinDataRateToAttemptTwoConnectionsMbps` | 1.5 |  |
| `@ForceContentServer` |  |  |
| `@ForceContentServerHTTPS` |  |  |
| `@ForceContentServerType` |  |  |
| `@GCNameOverride` |  |  |
| `@LocalContentServer` |  |  |
| `@MatchmakingCreatePingWaitTime` |  |  |
| `@MatchmakingJoinPingWaitTime` |  |  |
| `@MatchmakingSearchPingWaitTime` |  |  |
| `@MatchmakingTotalPingWaitTime` |  |  |
| `@MaxOutstandingSendThreadItemFatalAssert` |  |  |
| `@MaxOutstandingSendThreadItemFatalAssertSecondsAtLimit` |  |  |
| `@MaxOutstandingSendThreadItemSleep` |  |  |
| `@metricsDisabledCatalogs` |  |  |
| `@metricsDisabledOperations` |  |  |
| `@metricsEnabledOperations` |  |  |
| `@nBootReserveRetryPeriodSec` |  | Number of seconds to wait before retrying after failing to create a boot reserve file. Should be a multiple of 10. |
| `@nCallerDeadlineHopLatencyMS` |  |  |
| `@nClientCloudMaxMBParallelDownloads` |  |  |
| `@nClientCloudMaxMBParallelUploads` |  |  |
| `@nClientCloudMaxNumParallelDeletes` |  |  |
| `@nClientCloudMaxNumParallelDownloads` |  |  |
| `@nClientCloudMaxNumParallelUploads` |  |  |
| `@nClientCloudMaxNumUploadsPerBatch` | 100 |  |
| `@nClientCMDirectoryResultLoadPercentDither` |  | Dither to apply to CM server loads received by CMDirectory query |
| `@nClientCMUDPPingTimeGoodEnoughThresholdMS` |  |  |
| `@nClientCMUDPPingTimeoutUseGoodEnoughMS` |  |  |
| `@nClientDownloadEnableHTTP2PlatformLinux` |  | Enable HTTP/2 connections on Linux clients |
| `@nClientDownloadEnableHTTP2PlatformWindows` |  | Enable HTTP/2 connections on Windows clients |
| `@nClientDownloadEnableHTTP2RelBranch` |  | Only enable HTTP/2 on enabled platforms on rel branch client if this is set |
| `@nClientDownloadInitWindowSizeHTTP2Connection` | 10000000 | Init per-connection window size for HTTP/2. |
| `@nClientDownloadInitWindowSizeHTTP2Stream` | 2000000 | Init per-stream window size for HTTP/2. |
| `@nClientDownloadProbUseHTTP2IfAvailable` |  | If http/2 is available for a given download source, use it w/ this probability [0,100] |
| `@nClientEnableHTTP2PlatformLinux` |  | Enable HTTP/2 connections on Linux clients |
| `@nClientEnableHTTP2PlatformWindows` |  | Enable HTTP/2 connections on Windows clients |
| `@nClientEnableIPv6ForHTTPPlatformLinux` |  | Enable IPv6 HTTP connections by default on Linux clients |
| `@nClientEnableIPv6ForHTTPPlatformWindows` |  | Enable IPv6 HTTP connections by default on Windows clients |
| `@nClientFrameRateReportBatchSize` |  | Number of frame rate reports to collect locally before sending to the server |
| `@nClientFrameRateReportSecs` |  | Number of seconds between individual frame rate reports |
| `@nClientInitWindowSizeHTTP2Connection` | 10000000 | Init per-connection window size for HTTP/2. |
| `@nClientInitWindowSizeHTTP2Stream` | 2000000 | Init per-stream window size for HTTP/2. |
| `@nClientQueryCMDirectoryBeforeConnect` |  | Use CMDirectory webapi to get fresh CM list on connect - 0=disabled, 1=enabled, 2=main/dev/beta clients only |
| `@nClientServiceMethodForDownloadListPercent` | 100 |  |
| `@nContentDeltaChunkAppendChunksAfterProtobufSizeThresholdMB` |  |  |
| `@nContentUpdateAutoVerifyCleanBytesThresholdMB` | 2048 | How many clean MB must we verify before backing off on auto-verifies |
| `@nContentUpdateAutoVerifyEnable` |  | 0 = disabled; 1 = enabled all clients |
| `@nContentUpdateAutoVerifyIntervalDays` |  | Auto-verify game updates ever N days |
| `@nCSClientRateLimitKbps` |  |  |
| `@nCSJob404ResponseLimit` |  |  |
| `@nCSJob5xyResponseLimit` |  |  |
| `@nDownloadLANChunkCacheSizeMB` | 128 |  |
| `@nDownloadLANPeerGroup` |  |  |
| `@net_backlog_bytes_allowed` |  |  |
| `@net_backlog_time_allowed_sec` |  |  |
| `@net_loopback` |  |  |
| `@NetConnectionBufferMsgLimit` |  |  |
| `@NetConnectionBufferThreaded` |  |  |
| `@nHTTPServerHTTP2InitWindowSizePerConnection` |  |  |
| `@nHTTPServerHTTP2InitWindowSizePerStream` |  |  |
| `@nHTTPServerHTTP2MaxConcurrentStreams` |  |  |
| `@nHTTPServerLogLevelAccessLine200` |  |  |
| `@nHTTPServerLogLevelAccessLineNon200` |  |  |
| `@nHTTPServerLogLevelDetails200` |  |  |
| `@nHTTPServerLogLevelDetailsNon200` |  |  |
| `@nHTTPServerMaxPipelinedReqsPerConnection` |  |  |
| `@nHTTPServerYieldOn100ContinueSendSecs` |  |  |
| `@nIOCPThreadCount` |  |  |
| `@nJobInteryieldMillisecondsAlertThreshold` |  |  |
| `@nJobInteryieldMillisecondsLogThreshold` |  |  |
| `@nJobInteryieldMillisecondsSpewThreshold` |  |  |
| `@nJobNetSendsInsaneThreshold` |  |  |
| `@nJWTVerifiedTokenCacheSize` |  |  |
| `@nLANPeerGroupRateLimitKbps` |  |  |
| `@nLANPeerMaxConnections` |  |  |
| `@nLANPeerRateLimitKbps` |  |  |
| `@nLegalDictionaryUpdateRateInSeconds` | 600 |  |
| `@nNetConnectionBufferZipLevel` |  |  |
| `@nParentalSettingsLogLevel` |  | Control the amount of spew written to the parental log file |
| `@nPartnerUploadFinalizeTimeoutSecs` | 600 | Seconds to timeout the DRM finalize which can be slow as it involves sending to cloud storage |
| `@nProtobufArenaInitialBlockSize` |  |  |
| `@nProtobufArenaMaxBlockSize` |  |  |
| `@nProtobufArenaNumberOfHeadersToShare` |  |  |
| `@nProtobufArenaNumberOfJobsToShare` |  |  |
| `@nRoamingConfigReconnectCloudSyncWindowSec` | 7200 |  |
| `@nScreenshotSaveMaxWidth` | 9999 |  |
| `@nServerRefreshRateLimitAdditional` |  |  |
| `@nServerRefreshRateLimitBurst` | 100 | Limits the burst number of calls per appid to refresh GMS game server lists |
| `@nServerRefreshRateLimitInterval` |  |  |
| `@nSiteLicenseProxyCacheMaxGB` | 100 | If local content cache is enabled, use up to this much disk space |
| `@nSiteLicenseProxyEnableP2P` |  | If set, will have all connected clients join the same P2P download group |
| `@nSiteLicenseProxyPort` |  | Local content cache: set > 0 to enable, will listen on this port |
| `@nSpewThrottleNagFrequencyMs` |  |  |
| `@nSpewThrottlePeriodMs` |  |  |
| `@nSpewThrottleResumeThreshold` |  |  |
| `@nSpewThrottleTriggerThreshold` |  |  |
| `@nSpewThrottleUnconditionalResumeMs` |  |  |
| `@nSpewThrottleUnconditionalTriggerCount` |  |  |
| `@nThreadedProtobufParseMinBytes` |  |  |
| `@nThreadedProtobufParseThreads` |  |  |
| `@PeerContentClientMaxJobs` |  | number of peer sources used at the same time |
| `@PeerContentServerMaxClients` |  | limit number of peers connected |
| `@PeerContentServerPort` | 27040 | If peer content server, will listen on this port for TCP connections from peers |
| `@PeerContentServerRetryDelay` |  | seconds before retrying peer content server |
| `@sCSDSVirtualHostHeader` |  |  |
| `@sForceLocalContentCache` |  |  |
| `@sSiteLicenseProxyCacheDirectory` |  |  |
| `@sSiteLicenseProxyExplicitIP` |  | Local content cache: if not blank, will instruct clients to go to this IP for the content cache. |
| `@sSteamCmdForcePlatformBitness` |  | Must be one of: [32 / 64] |
| `@sSteamCmdForcePlatformCPU` |  | Must be one of: [x86 / arm64] |
| `@sSteamCmdForcePlatformType` |  | Must be one of: [windows / macos / linux / android] |
| `@strCSNoCacheHeader` |  |  |
| `@StreamClientArgs` |  |  |
| `@sTrustedLocalContentCacheName` |  | Set this to the machine name where a trusted local Steam download cache is hosted, and we'll use it if available. |
| `@test_bCloudForceSyncConflict` |  | If @test_nCloudForceSyncFailureAppID is set, then set this so that the failure case is 'file conflict' instead of generic failure |
| `@test_nCloudForceSyncFailureAppID` |  | Set this to a non-zero App ID to test cloud sync failure. The next sync request will fail. |
| `@uDownloadLANPeerPort` | 27038 | If LAN p2p download enabled, will listen on this port for TCP connections from peers. Must be set consistently across all members of the group! |
| `@unMinimumShaderDownloadSizeInUI` | 33554432 |  |
| `@unUserStatsTest` |  |  |
| `@uRemoteDiscoveryPortOverride` |  | If non-zero, will listen on this port for broadcasts instead of k_nBroadcastPort |
| `@uRemoteDiscoveryPortTransmit` |  | If non-zero, will transmit outgoing broadcasts on this port instead of on the listen port |
| `@UUUUUU` |  |  |
| `@voice_minabs` | 0.15 |  |
| `@voice_minavg` | 1.0 |  |
| `@voice_spew_activity_check` |  |  |
| `@WatchdogThreadPercentReport` |  |  |
