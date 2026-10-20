# Console variables (ConVars)

> Generated from the Steam Linux client, bootstrap manifest version **1791918634**, by static analysis of the
> 64-bit binaries in `steamrt64/` and `ubuntu12_64/`. See [../README.md](../README.md) for method and caveats.

Every ConVar registered in the client binaries, recovered from the arguments of the static ConVar
constructors. You can set these in the Steam console (`steam://open/console`, or run with `-console`/`-dev`)
as `name value`, or on the command line as `+name value`.

**Name prefixes (Valve naming convention):** `b` = bool, `n` = int, `fl`/`f` = float, `s` = string.
A leading `@` marks a client-config convar. Steam can override these from the server-side client
configuration it downloads at login (inferred from usage). Many are internal tuning knobs that never
appear in any UI. **Flags** is the raw flags bitmask passed to the constructor.

Total: **464**.

| Name | Default | Flags | Description (Valve help text) | Binaries |
|---|---|---|---|---|
| `AlwaysCustomizeOnBadExit` | `0` | 0x4 |  | steamclient.so |
| `app_force_preload` | `0` | 0x4 | force this app into preload mode | steamclient.so |
| `app_info_http_min` | `0` | 0x4 |  | steamclient.so |
| `app_info_http_num_sockets` | `8` | 0x4 |  | steamclient.so |
| `appcloudsessions` | `all` | 0x10 |  | steamclient.so |
| `@AppMRUSize` | `20` | 0x0 |  | steamui.so |
| `apps_per_overview_chunk` | `5000` | 0x0 |  | steamui.so |
| `AsyncFileIOAlternateReadWrite` | `1` | 0x4 |  | steamclient.so |
| `AsyncFileIODisableWrite` | `0` | 0x4 |  | steamclient.so |
| `AsyncFileIOExpectOutstandingIO` | `6` | 0x4 |  | steamclient.so |
| `AsyncFileIOMaxPendingWin32` | `256` | 0x4 |  | steamclient.so |
| `AsyncFileIOReadHandleCache` | `64` | 0x4 |  | steamclient.so |
| `AsyncFileIOWriteHandleCache` | `64` | 0x4 |  | steamclient.so |
| `@bAssertOnProtoBufBodyMismatch` | `1` | 0x400000004 | Assert when a body parsed ahead of the main thread is not the type the handler builds.  See\n'protobuf_parse_stats' for the running count and which messages it happened to. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `batterycharging` | `0` | 0x0 |  | steamclient.so |
| `batterypercent` | `-1` | 0x0 |  | steamclient.so |
| `batterytime` | `-1` | 0x0 |  | steamclient.so |
| `bBroadcastAlwaysUploadThumbnails` | `1` | 0x4 |  | steamclient.so |
| `@bCallerDeadlineAbortJobDisableWhenHTTPReqStart` | `1` | 0x400000004 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `bCheckUGCIntegrity` | `1` | 0x4 |  | steamclient.so |
| `bClientConvar601DEACE` | `1` | 0x4 |  | steamclient.so, steamservice.so, steamui.so |
| `@bClientDownloadUseHTTPS` | `0` | 0x4 | Set this to use HTTPS on supported download servers | steamclient.so |
| `@bClientOpenCacheStickyRedirects` | `1` | 0x4 |  | steamclient.so |
| `bClientPingCSesForCellID` | `0` | 0x4 |  | steamclient.so |
| `@bClientTryRequestManifestWithoutCode` | `0` | 0x4 | If set, client will try to get a manifest even without a manifest request code | steamclient.so |
| `bCloudAcceptUnexpectedAutoCloudFileChanges` | `1` | 0x4 |  | steamclient.so |
| `@bCloudSyncFailDownloadIfGameOutOfDate` | `0` | 0x4 |  | steamclient.so |
| `@bCSForceNoCache` | `0` | 0x4 |  | steamclient.so |
| `bDelayGameUpdatesOnBeta` | `0` | 0x4 | Should we do scheduling of updates on Steam Beta? If not, they'll all be ASAP | steamclient.so |
| `@bDepotBuilderReadBufferSizeKB` | `8192` | 0x4 |  | steamclient.so |
| `@bDepotBuilderUnbufferedReads` | `1` | 0x4 |  | steamclient.so |
| `bDepotDeltaPatchUseAPI` | `1` | 0x4 |  | steamclient.so |
| `bDepotUseSparseFiles` | `1` | 0x0 |  | steamclient.so |
| `@bDisableDualStackDownloads` | `0` | 0x4 |  | steamclient.so |
| `bDisableTenFootOverlay` | `0` | 0x4 |  | steamclient.so |
| `@bDownloadThrottleDuringCloudSync` | `0` | 0x4 |  | steamclient.so |
| `@bEnableFrameFuncOverageWarnings` | `0` | 0x4 | This turns on the spew in SPEW_MISC at level 4, still need to adjust spew levels to see it. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bEnableHTTP2OnAllCHTTPClients` | `0` | 0x400000000 | Enable HTTP/2 on all CHTTPClients automatically for SSL connections | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `bEnableLoginUsersErrorUpload` | `0` | 0x10 | Set to enable uploading log files if there is an error loading login user info | steamui.so |
| `@bEnableLogTearOff` | `1` | 0x0 |  | friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper |
| `bEnableMHRCAsyncFileReadLog` | `0` | 0x4 |  | steamclient.so |
| `@bEnableNetworkJobsOwnStartList` | `1` | 0x400000004 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bEnableOfflineLogonTicket` | `1` | 0x4 | If true, an offline logon ticket will be requested during logon if none is cached | steamclient.so |
| `@bEnableSiteLicenseConnect` | `1` | 0x0 |  | steamclient.so |
| `@bEnableSiteLicenseConsoleLogging` | `0` | 0x0 |  | steamclient.so |
| `@bEnableSpewThrottle` | `1` | 0x4 |  | friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper |
| `bEnableSubscribedFileListCache` | `1` | 0x4 |  | steamclient.so |
| `@bEnforceValidEmailDomains` | `1` | 0x4 | Enable valid email domains in BIsValidEmailAddress | steamclient.so |
| `betaalwaysrebuild` | `0` | 0x0 |  | steamui.so |
| `bExternalProcessForVOD` | `0` | 0x0 |  | steamui.so |
| `bFinishStagedDepotVersions` | `1` | 0x4 |  | steamclient.so |
| `@bForceAbsoluteMouseCoordinates` | `0` | 0x0 |  | steamui.so |
| `@bForceLaunchEula` | `0` | 0x0 |  | steamui.so |
| `@bForceOverlayAudioRecorder` | `0` | 0x4 | force overlay based audio capture (disable MF based audio capture path) | steamui.so |
| `@bForceStreamUnsupportedApp` | `0` | 0x0 |  | steamclient.so |
| `@bHttpClientRecordHostnameDimension` | `0` | 0x400000000 | Group HTTP metrics by hostname.  Careful, the cardinality of your in-memory map might be large. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bHTTPServerHTTP2Enabled` | `0` | 0x400000004 | Global default for whether CHTTPServer advertises/accepts HTTP/2 (over TLS via ALPN). A server that calls SetHTTP2Enabled() explicitly overrides this value. | steamclient.so, steamui.so |
| `bInstallscriptReports` | `1` | 0x4 | send reports about broken install scripts | steamclient.so |
| `@bLANPeerConnectionTimeoutSec` | `5` | 0x4 |  | steamclient.so |
| `@bLogMessageToProtobufClass` | `1` | 0x400000004 | We we first discover the protobuf class used for a particular EMsg, log it | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bMeasureSSLLatencyStats` | `1` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bMetricsEnabled` | `1` | 0x4 | Enabling allows jobs to collect and report metrics through IMetricsReporters. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bMsgErrorDump` | `0` | 0x4 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `bPrefetchDownloadDetails` | `1` | 0x4 | Prefetch download size before actual update happens | steamclient.so |
| `@bProfileYieldsInTestSuiteJobs` | `0` | 0x400000000 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bProtoBufNetPacketDropRawBytes` | `1` | 0x400000004 | Release the raw packet bytes of an inbound message whose header and body were both parsed for us, rebuilding them on demand for the few callers that want them.  Also read by the SSL work thread, which then never copies those bytes out of its read buffer in the first place.  Watch 'protobuf_parse_stats' for how often that happens. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bProtobufParseSizeProfile` | `1` | 0x400000004 | Track a histogram of protobuf message body sizes as they are parsed.  See the protobuf_parse_stats console command. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bProtobufParseTimeProfile` | `0` | 0x400000004 | Also time each protobuf body parse, so protobuf_parse_stats can report time per size bucket and how much parse time actually moved off the job thread.  Off by default - it adds two clock samples per parse. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bRefreshDownloadSourcesFrequently` | `0` | 0x4 |  | steamclient.so |
| `@bRequireOfflineLogonTicket` | `1` | 0x4 | If true, a valid offline logon ticket is required when logging in in offline or no connection mode | steamclient.so |
| `broadcast_adjust_bitrate` | `200` | 0x4 |  | steamui.so |
| `broadcast_upload_drop_sec` | `6` | 0x4 |  | steamclient.so |
| `broadcast_upload_update_sec` | `3` | 0x4 |  | steamclient.so |
| `@bScreenshotsLegacyCloudUpload` | `0` | 0x4 | If set, use the legacy Steam Cloud upload path for screenshot uploads | steamclient.so |
| `bShaderAllowReplay` | `1` | 0x4 |  | steamclient.so |
| `bShaderAllowReplayOnNVIDIA` | `1` | 0x4 |  | steamclient.so |
| `bShaderAlwaysProcessWhenRunningGame` | `0` | 0x4 |  | steamclient.so |
| `bShaderCacheDownloads` | `1` | 0x4 | Allow to download shader cache depots | steamclient.so |
| `@bShaderClientGetBucketManifestUseWebAPI` | `1` | 0x4 |  | steamclient.so |
| `bShaderDepotNative` | `1` | 0x4 |  | steamclient.so |
| `bShaderEnableCacheManagement` | `1` | 0x4 |  | steamclient.so |
| `bShaderEnableFossilizeLayer` | `1` | 0x4 |  | steamclient.so |
| `bShaderEnableUpload` | `1` | 0x4 |  | steamclient.so |
| `bShaderFossilizeFastMerge` | `1` | 0x4 |  | steamclient.so |
| `bShaderPrecompiledCache` | `1` | 0x4 |  | steamclient.so |
| `bShaderVerboseLogs` | `0` | 0x4 |  | steamclient.so |
| `@bShowUninstalledDemosInLibrary` | `0` | 0x4 |  | steamui.so |
| `bSingleFileUpdateMode` | `1` | 0x4 |  | steamclient.so |
| `@bSiteLicenseAllowCachedClientCredentials` | `0` | 0x0 | Allow Steam clients that associate to this site to save username and auth credentials locally | steamclient.so |
| `@bSiteLicenseProxyCacheIsExternalProcess` | `0` | 0x0 | If set, the caching content proxy will be handled by some process other than steamcmd. You probably also should set @sSiteLicenseProxyExplicitIP. | steamclient.so |
| `@bSiteLicenseProxyEnableIPv6` | `0` | 0x0 | If set, we will enable ipv6 communications to the Steam servers | steamclient.so |
| `@bSiteLicenseServer` | `0` | 0x0 |  | steamclient.so |
| `@bSSLThreadedMsgParse` | `1` | 0x400000004 | Parse framed Steam3 message headers and bodies on the SSL work thread, as well as framing them there.  Read per message, so it takes effect live. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bSSLThreadedMsgParseRelayedBodies` | `0` | 0x400000004 | Pre-parse the bodies of service methods that execute on the client.  Off by default: the only\nservers those pass through - CM and UDS - relay them by header and never look at the body, so\nparsing it here is work nobody on this side consumes.  Watch 'protobuf_parse_stats'. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@bSSLThreadedSendDelivery` | `1` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `bSteam3LimitedUserEnable` | `1` | 0x0 |  | steamclient.so |
| `bSteamLoaderEnable` | `1` | 0x0 |  | steamclient.so |
| `bUseSystemBrowserFor2DVOD` | `1` | 0x0 |  | steamui.so |
| `bVerifyAllDownloads` | `0` | 0x4 | Verify all files after downloading an update | steamclient.so |
| `bVerifyAllInstalled` | `0` | 0x4 | Verify all installed files before installing an update | steamclient.so |
| `cAppUpdateWorkingSetMB` | `256` | 0x4 |  | steamclient.so |
| `@cbPartnerUploadChunkSize` | `1000000` | 0x4 | Chunk size to use for POSTing partner uploads | steamclient.so |
| `cChunkValidationMaxLog` | `100` | 0x4 |  | steamclient.so |
| `@cCSClientMaxNumSocketsPerHost` | `4` | 0x4 |  | steamclient.so |
| `@cCSClientMaxNumSocketsPerHostForCachingProxy` | `32` | 0x4 |  | steamclient.so |
| `@cDefaultInitialDownloadSources` | `4` | 0x4 |  | steamclient.so |
| `@cDepotBuilderFileChunkingThreads` | `0` | 0x4 |  | steamclient.so |
| `@cFileChunkingCRCFalseAlarmBytesToSkip` | `128` | 0x4 |  | steamclient.so |
| `@cFileChunkingCRCFalseAlarmThreshold` | `0` | 0x4 |  | steamclient.so |
| `@cFileChunkingSupersectionSizeMB` | `1024` | 0x4 |  | steamclient.so |
| `cFileValidationMaxLog` | `100` | 0x4 |  | steamclient.so |
| `ClickPanel` | `index` |  | code | friendsui.so, gameoverlayui.so, steamui.so |
| `ClientConnectTokenBucketEnable` | `1` | 0x0 |  | steamclient.so |
| `clientui_overlay_fps` | `60` | 0x0 |  | steamui.so |
| `clientuistats_batchsize` | `0` | 0x0 | Control how many events can be queued up for ClientUI stats before the batch is committed. 0 will commit every row. | steamui.so |
| `@cloud_testdynamicsyncapp` | `0` | 0x10 |  | steamclient.so |
| `@cMaxContentServersToRequest` | `20` | 0x4 |  | steamclient.so |
| `cMaxDecryptThreadsOverride` | `0` | 0x4 |  | steamclient.so |
| `@cMaxInitialDownloadSources` | `-1` | 0x0 |  | steamclient.so |
| `@cMinimumJobTimeoutsToCheckPerFrame` | `100` | 0x400000004 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@cNetEncryptionHandshakeWorkMax_HighPri` | `8000` | 0x4 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@cNetEncryptionHandshakeWorkMax_LowPri` | `2000` | 0x4 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@cNetEncryptionHandshakeWorkMax_MedPri` | `4000` | 0x4 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `com.steampowered.Atomupd1` | `/com/steampowered/Atomupd1` |  | DisableHttpProxy / EnableHttpProxy | steamui.so |
| `controller_base_rotation_angle` | `0` | 0x0 |  | steamclient.so |
| `controller_debug_triton_wireless` | `0` | 0x0 |  | steamclient.so |
| `controller_edge_cutoff` | `0` | 0x0 |  | steamclient.so |
| `controller_gyro_x_scale` | `16000` | 0x0 |  | steamclient.so |
| `controller_idle_poll_interval` | `50000` | 0x0 | SteamInput Idle Polling interval in microseconds. Default 50,000us = 20hz | steamclient.so |
| `controller_jerk_low_pass_filter_rate` | `4` | 0x0 | How quickly the low pass filter chases the raw gyro jerk value. | steamclient.so |
| `controller_jerk_threshold` | `500` | 0x0 | The amount of Gyro Jerk (gyro change per second) required to create a Controller Jerk count. Note, only available on SteamDeck/Neptune/Galileo | steamclient.so |
| `controller_jerk_threshold_debug` | `0` | 0x0 | Debug spew to tell us the current "Jerk" value coming from the accelerometer | steamclient.so |
| `controller_jerk_throttle` | `2` | 0x0 | (Hz) The maximum callback rate for Controller Jerk Events. | steamclient.so |
| `controller_min_activation_time` | `0.0333` | 0x0 |  | steamclient.so |
| `controller_momentum_min_vel` | `0` | 0x0 |  | steamclient.so |
| `controller_momentum_num_excluded_samples` | `1` | 0x0 |  | steamclient.so |
| `controller_momentum_num_included_samples` | `5` | 0x0 |  | steamclient.so |
| `controller_poll_state` | `-1` | 0x0 |  | steamclient.so |
| `controller_rate` | `2000` | 0x0 | SteamInput Active Polling interval in microseconds. Default 2000us = 500hz | steamclient.so |
| `controller_simulate_trackpad` | `0` | 0x0 | Simulate a trackpad swipe on the right trackpad when the left pad is touched | steamclient.so |
| `controller_spew_level` | `3` | 0x0 |  | steamclient.so, steamui.so |
| `countrycode` |  | 0x0 |  | steamclient.so |
| `cPreallocateMinimumSizeKB` | `256` | 0x4 |  | steamclient.so |
| `@csecAudioSignalLevelInterval` | `60.0` | 0x4 | Log audio capture signal levels every this many seconds | steamui.so |
| `@csecCSJobSuccessfulRequestTimeWindow` | `60` | 0x4 |  | steamclient.so |
| `@csecCSRequestProcessorTimeOut` | `300` | 0x4 |  | steamclient.so |
| `@csecDurationControlPeriod` |  | 0x4 | Override default duration-control / anti-indulgence time period. If nonzero, initial playtime threshold is this value in seconds | steamclient.so |
| `@csecDurationControlPeriodToday` |  | 0x4 | Override default duration-control / anti-indulgence time period. If nonzero, per-day playtime threshold is this value in seconds | steamclient.so |
| `@csecDurationControlSimulated` |  | 0x4 | Simulate having already played this many seconds of playtime. | steamclient.so |
| `@csecDurationControlSimulatedNonRecent` |  | 0x4 | Simulate having already played this many seconds of playtime today, but not recently. | steamclient.so |
| `@csecFavoriteGameAccountCacheTime` | `86400` | 0x4 | Control how often we refresh the account IDs in the game server favorites list | steamclient.so |
| `@csecIncomingDataRatePeriod` | `1` | 0x4 |  | steamclient.so |
| `csecManifestDownloadTimeout` | `120` | 0x4 |  | steamclient.so |
| `@csecSiteLicenseProxyStatsLog` | `60` | 0x0 | Log proxy stats this often | steamclient.so |
| `@csecSiteLicenseProxyStatsUpdate` | `1` | 0x0 | update proxy stats internally this often | steamclient.so |
| `@csecUpdateTargetNumConnectionsEpoch` | `10` | 0x4 |  | steamclient.so |
| `@cSecUploadDownloadRates` | `300` | 0x4 |  | steamclient.so |
| `@CSInterfaceProxyPassword` |  | 0x0 |  | steamclient.so |
| `@CSInterfaceProxyUsername` |  | 0x0 |  | steamclient.so |
| `@cUDPSendRetries` | `8` | 0x400000000 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `CursorMoved` | `xpos` |  | ypos | friendsui.so, gameoverlayui.so, steamui.so |
| `@CustomBinaryRequestRetryTimes` | `20` | 0x0 |  | steamclient.so |
| `debugLaunchAppDelaySecs` | `0` | 0x0 |  | steamui.so |
| `deck_mouse_haptic_tick_dist` | `9000` | 0x0 |  | steamclient.so |
| `deck_mouse_leftside_filter` | `30500` | 0x0 |  | steamclient.so |
| `@DepotBuilderDeltaMaxChunks` | `20000` | 0x4 |  | steamclient.so |
| `@DepotBuilderEnableVZd` | `1` | 0x4 |  | steamclient.so |
| `@DepotBuilderMaxParallelUploadChunks` | `24` | 0x4 |  | steamclient.so |
| `@DepotBuilderNumHTTPSocketsToMDS` | `12` | 0x4 |  | steamclient.so |
| `@DepotBuilderParallelUploadChunks` | `6` | 0x4 |  | steamclient.so |
| `@DepotBuilderProgressTimeout` | `1000` | 0x4 |  | steamclient.so |
| `@DepotBuilderVZdMinRatio` | `0.4` | 0x4 |  | steamclient.so |
| `@DepotBuilderXORMatchPercent` | `95` | 0x4 |  | steamclient.so |
| `DepotDeltaPatches` | `1` | 0x4 |  | steamclient.so |
| `DepotDownloadProgressTimeout` | `120` | 0x4 |  | steamclient.so |
| `DepotMinWriteGapSizeMB` | `64` | 0x0 |  | steamclient.so |
| `DepotReconstructionBadChunk` | `0` | 0x0 |  | steamclient.so |
| `DepotReconstructionForceGenericIO` |  | 0x4 |  | steamclient.so |
| `DepotReconstructionLowPrio` | `1` | 0x4 |  | steamclient.so |
| `DepotReconstructionNumIOThreads` | `32` | 0x4 |  | steamclient.so |
| `DepotUseAlternatingReadWrite` | `1` | 0x4 |  | steamclient.so |
| `developer` | `0` | 0x0 |  | friendsui.so, gameoverlayui.so, steamclient.so, steamui.so |
| `@durationControlNightCheck` | `1` | 0x4 | Time of day check for duration-control feature. 1 = normal. 2 = force night-time. 0 = disable checks, only enabled for age verified accounts | steamclient.so |
| `@EnableUDPHistory` | `0` | 0x400000000 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@fDownloadRateImprovementToAddAnotherConnection` | `1.2` | 0x4 |  | steamclient.so |
| `@fMinDataRateToAttemptTwoConnectionsMbps` | `1.5` | 0x4 |  | steamclient.so |
| `force_software_gyro_drift_correction` | `0` | 0x0 | 0: Only use software drift calibration based on controller capabilities. 1: Any controllers with IMUs will be forced to use the standard software drift calibration. | steamclient.so |
| `@ForceContentServer` |  | 0x0 |  | steamclient.so |
| `@ForceContentServerHTTPS` | `0` | 0x0 |  | steamclient.so |
| `@ForceContentServerType` |  | 0x0 |  | steamclient.so |
| `g_RumbleRepeatAfterDelaySeconds` | `0.050` | 0x0 |  | steamclient.so |
| `g_RumbleSustainTimeSeconds` | `10` | 0x0 |  | steamclient.so |
| `@GCNameOverride` |  | 0x10 |  | steamclient.so |
| `grip_sense_haptic_test` | `0` | 0x0 |  | steamclient.so |
| `grip_sense_haptic_test_repeats` | `1` | 0x0 |  | steamclient.so |
| `grip_sense_haptic_test_strength` | `125` | 0x0 |  | steamclient.so |
| `gyro_auto_detect_polling_rate` | `1` | 0x0 | Wired Connections only. 0: Legacy Mode. Known to be buggy with Blitz 2 and other controllers set to 1000hz+. 1: If SDL3 sensor delta time is zero, or unexpected sensor timings are detected, fall back on packet-rate based estimation of polling rate (if outside a margin of error: gyro_sensor_margin_of_error_pct). 2: Exclusively use packet-rate based estimation of polling rate. | steamclient.so |
| `gyro_calibration_duration_automatic` | `5.0` | 0x0 | Duration in seconds required to calibrate gyro drift outside of manual calibration. Warning: Short calibration times are more likely to result in false positive anti-drift solutions. | steamclient.so |
| `gyro_calibration_duration_manual` | `5.0` | 0x0 | Duration in second of manual gyro drift calibration. Longer durations make for more accurate drift corrections. | steamclient.so |
| `gyro_calibration_duration_manual_timeout` | `30.0` | 0x0 | Duration before manual gyro drift calibration times out, and returns to calibrating the noise tolerance. | steamclient.so |
| `gyro_calibration_duration_stationary` | `5.0` | 0x0 | Duration in second of gyro noise tolerance calibration. | steamclient.so |
| `gyro_debug_gyro_speed_vs_quaternion_speed` | `0` | 0x0 | 0: Off. 1: Spew the gyro speed and the extracted quaternion rotation speed | steamclient.so |
| `gyro_debug_hardware_vs_mode_time` | `0` | 0x0 | 0: Off. 1: Spew the hardware delta time vs. the platform delta time. | steamclient.so |
| `gyro_debug_sensor_timings` | `0` | 0x0 |  | steamclient.so |
| `gyro_drift_calibration_debug` | `0` | 0x0 | Display which sensor readings (accelerometer or gyroscope) are restarting the drift calibration due to their noise being bigger than noise tolerance. | steamclient.so |
| `gyro_drift_correction_enabled` | `1` | 0x0 | Turn on/off software gyro anti-drift correction. | steamclient.so |
| `gyro_drift_detection_debug` | `0` | 0x0 | Spew information about how far the gyro has deflected over time. | steamclient.so |
| `gyro_drift_detection_duration` | `30.0` | 0x0 | How long we sample for before triggering a calibration warning. Seconds. | steamclient.so |
| `gyro_drift_detection_min_deflection` | `270.0` | 0x0 | The minimum degrees of deflection we must have turned through to detect a drift event. This intentionally higher than rotations we'd expect from regular use. | steamclient.so |
| `gyro_drift_detection_min_drift_rate` | `0.1` | 0x0 | The minimum degrees per second we consider to be gyro drift. i.e. if we notice the gyroscope has drifted at higher than this rate, it could be drifting noticeably. | steamclient.so |
| `gyro_filter_enabled` | `1` | 0x0 | Enable (Pseudo) One Euro Filter to internal gyro quaternion. This reduces low level sensor noise and hand shake.  | steamclient.so |
| `gyro_filter_max_speed` | `16.0` | 0x0 | Above this gyro rotation speed (degrees/second) we apply min (zero) smoothing. | steamclient.so |
| `gyro_filter_min_speed` | `2` | 0x0 | Below this gyro rotation speed (degrees/second) we apply max smoothing (low pass filter). | steamclient.so |
| `gyro_filter_smoothness` | `75` | 0x0 | Smoothing amount for low pass filter. 1 is TOO smoothed (barely responding). 100 is barely smoothed. | steamclient.so |
| `gyro_force_handheld_orientation` | `0` | 0x0 | 0: Auto. 1: Force Controller to be "HandHeld" orientation, like SteamDeck (tilt in pitch by 90 degrees so that "Yaw" is "Through the Screen". 2: Force Controller to be "Standalone" controller like Steam Controller, where "Yaw" is "Through Sticks".  | steamclient.so |
| `gyro_force_sensor_rate` | `0` | 0x0 | If zero, cull suspected bad sensor data (can result in a loss of natural sensitivity). If not zero, ignore IMU sensor timing and use fixed rate instead. Measured in HZ. Common values: 250hz (PS5), 250hz (PS4), 200hz (Nintendo Switch) | steamclient.so |
| `gyro_handheld_pitch_offset` | `90` | 0x0 | When in handheld mode, how far we tilt the gyro quaternion before processing. This affects only the "Gyro to Mouse" and "Gyro to JoystickCamera" modes. And only affects Yaw, Roll, Yaw + Roll, and Laser Pointer 3DOF to 2D conversion styles within those modes. Player Space and World Space are controller affordance agnostic. | steamclient.so |
| `gyro_haptic_probe_enabled` | `0` | 0x0 | 0: Off. 1: Try new gyro mode. Config must have haptic level set to something other than "off\n | steamclient.so |
| `gyro_haptic_probe_max_pulse` | `100` | 0x0 | How loud the grip effect gets at max speed | steamclient.so |
| `gyro_haptic_probe_max_speed` | `360.0` | 0x0 | Highest speed for haptic probe movement. Degrees per second. | steamclient.so |
| `gyro_haptic_probe_min_pulse` | `20` | 0x0 | How loud the grip effect gets at max speed | steamclient.so |
| `gyro_haptic_probe_min_speed` | `0.125` | 0x0 | Lowest speed for haptic probe movement. Degrees per second. | steamclient.so |
| `gyro_haptic_probe_offset_scale` | `0.65` | 0x0 | How far to spread the haptic probe set is spread out. 0 = ontop of each other. 1 = 1 degree separation. | steamclient.so |
| `gyro_haptic_probe_types` | `3` | 0x0 | 0: None. 1: Trackpad Only. 2: Rumble Only. 3: Both | steamclient.so |
| `gyro_precision_speed` | `0.75` | 0x8 |  | steamclient.so |
| `gyro_precision_speed_enabled` | `1` | 0x0 | Enable linear response multiplier to speeds below the value set in the "Gyro To..." modes. This applies itself to the remaining speed after the gyro speed deadzone has been applied. | steamclient.so |
| `gyro_prediction_correction_speed_max` | `180.0` | 0x0 | Above this speed (degrees per second) there is full correction of the predicted quaternion toward the  "ground truth" quaternion. Note this will still be gradual correction, and only in the shared direction of user rotation and the correction required. | steamclient.so |
| `gyro_prediction_correction_speed_min` | `30.0` | 0x0 | Below this speed (degrees per second) there is no correction of the predicted quaternion toward the  "ground truth" quaternion. | steamclient.so |
| `gyro_prediction_enabled` | `1` | 0x0 | Enable extrapolation of rotation using the last known gyro speed. This is important to avoid staggered signals over blue tooth, but generally upgrades gyros that run lower than 500hz. The extrapolated quaternion will correct back toward the "ground truth" quaternion when the speed exceeds. | steamclient.so |
| `gyro_raw_deadzone` | `6.0` | 0x0 | Legacy deadzoning for gyro signal. Only affects "As Mouse" and its derivative modes. | steamclient.so |
| `gyro_sensor_margin_of_error_pct` | `25` | 0x0 | If gyro_auto_detect_polling_rate is set to mode 2, use this +/- X% value as the acceptable margin of error before falling back on packet-rate based estimation of polling rate. | steamclient.so |
| `gyro_speed_deadzone` | `0.5` | 0x8 |  | steamclient.so |
| `gyro_speed_deadzone_enabled` | `1` | 0x0 | Enable the minimum speed required to update the gyroscope response. | steamclient.so |
| `gyro_stationary_calibration_debug` | `0` | 0x0 | Display which sensor readings (accelerometer or gyroscope) are restarting the tolerance calibration due to their noise being too large. | steamclient.so |
| `gyro_to_joystick_camera_raw` | `1` | 0x0 | Used to test old Gyro to joystick Camera processing pipeline (1) against old (0). | steamclient.so |
| `gyro_to_joystick_camera_relax` | `0` | 0x0 | Low pass filter on the output to help lower FPS games. Needs more thought. | steamclient.so |
| `gyro_use_polling_time_for_prediction` | `1` | 0x0 | Use the main loop's cached time as opposed to a fresh sample. Just for A/B testing. | steamclient.so |
| `haptic_click_gain_modifier` | `0` | 0x0 |  | steamclient.so |
| `haptic_intensity` | `8000` | 0x0 |  | steamclient.so |
| `haptic_intensity_old` | `2500` | 0x0 |  | steamclient.so |
| `haptic_new` | `0` | 0x0 |  | steamclient.so |
| `haptic_off_divisor` | `5.0f` | 0x0 |  | steamclient.so |
| `haptic_tick_gain_modifier` | `0` | 0x0 |  | steamclient.so |
| `ibex_mouse_leftside_filter` | `32500` | 0x0 |  | steamclient.so |
| `ibex_rumble_deadzone` | `635` | 0x0 |  | steamclient.so |
| `installmanagertimeout` | `15` | 0x0 |  | steamui.so |
| `ItemsChecked` | `count` |  | itemid | friendsui.so, gameoverlayui.so, steamui.so |
| `KeyCodeTyped` | `code` |  | modifiers | friendsui.so, gameoverlayui.so, steamui.so |
| `lenovo_hook_filter` | `31500` | 0x0 |  | steamclient.so |
| `library_asset_cache_asset_file_min_sec` | `120` | 0x0 |  | steamui.so |
| `library_asset_cache_conversion_rtime` | `1724792014` | 0x0 |  | steamui.so |
| `library_asset_cache_full_check_threshold` | `25` | 0x0 |  | steamui.so |
| `library_asset_cache_full_recheck_min_hours` | `1` | 0x0 |  | steamui.so |
| `library_asset_cache_kvfile_name` | `assetcache.vdf` | 0x0 |  | steamui.so |
| `library_asset_cache_kvfile_version` | `2` | 0x0 |  | steamui.so |
| `library_asset_cache_max_notify` | `200` | 0x0 |  | steamui.so |
| `library_asset_cache_max_requests` | `20` | 0x0 |  | steamui.so |
| `library_asset_cache_notify_debounce_sec` | `60` | 0x0 |  | steamui.so |
| `library_asset_cache_version` | `3` | 0x0 |  | steamui.so |
| `library_sharing_account_max` | `5` | 0x4 |  | steamui.so |
| `@LocalContentServer` |  | 0x0 |  | steamclient.so |
| `log_files_always_flush` | `0` | 0x4 |  | gamelauncher, gameoverlayui.so, steam, steamclient.so, steamsysinfo, steamui.so, steamwebhelper |
| `log_matchmaking_callbacks` | `0` | 0x0 |  | steamclient.so |
| `@MatchmakingCreatePingWaitTime` | `0` | 0x4 |  | steamclient.so |
| `@MatchmakingJoinPingWaitTime` | `0` | 0x4 |  | steamclient.so |
| `@MatchmakingSearchPingWaitTime` | `0` | 0x4 |  | steamclient.so |
| `@MatchmakingTotalPingWaitTime` | `0` | 0x4 |  | steamclient.so |
| `@MaxOutstandingSendThreadItemFatalAssert` | `30000` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@MaxOutstandingSendThreadItemFatalAssertSecondsAtLimit` | `30` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@MaxOutstandingSendThreadItemSleep` | `10000` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `MergeCapReprocess_minutes` | `480` | 0x4 |  | steamclient.so |
| `@metricsDisabledCatalogs` |  | 0x4 | Comma separated list of metrics catalogs to disable.  This is the last check. | steamclient.so |
| `@metricsDisabledOperations` |  | 0x4 | Comma separated list of metrics operations that are disabled.  This setting has highest priority | steamclient.so |
| `@metricsEnabledOperations` |  | 0x4 | Comma separated list of metrics operations.  Overrides disabled catalogs | steamclient.so |
| `mic_autogain` | `16000` | 0x0 | automatic gain control level for microphone input | steamclient.so |
| `mic_inputfile` |  | 0x0 | causes voice data to be read from the specified file instead of from the microphone | steamclient.so |
| `mic_outputfile` |  | 0x0 | causes microphone data to be written out to the specified file | steamclient.so |
| `MouseDoublePressed` | `code` |  | modifiers | friendsui.so, gameoverlayui.so, steamui.so |
| `MousePressed` | `code` |  | modifiers | friendsui.so, gameoverlayui.so, steamui.so |
| `musiclogging` | `0` | 0x0 |  | steamclient.so |
| `@nBootReserveRetryPeriodSec` | `30` | 0x4 | Number of seconds to wait before retrying after failing to create a boot reserve file. Should be a multiple of 10. | steamclient.so |
| `nBroadcastSessionMaxDropFrames` | `100` | 0x4 |  | steamclient.so |
| `@nCallerDeadlineHopLatencyMS` | `10` | 0x400000004 | When we send a message expecting a reply from a job with a deadline, set the timeout on the message to [current time remaining in this job] - N ms.  A negative value prevents propagating caller deadlines down the chain | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `nClientBackgroundAutoUpdateLessRecentlyPlayedThresholdHours` | `168` | 0x4 | If you've played the game more recently than this, we'll schedule the background update sooner. | steamclient.so |
| `nClientBackgroundAutoUpdateNotPlayedTimeSpreadDays` | `14` | 0x4 | If the user hasn't played this game in a while, pick a morning up to this many days out to update. | steamclient.so |
| `nClientBackgroundAutoUpdateRecentlyPlayedThresholdHours` | `72` | 0x4 | If you've played the game more recently than this, we'll schedule the background update sooner. | steamclient.so |
| `nClientBackgroundAutoUpdateTargetHour` | `6` | 0x4 | Target hour, in local time, for auto-scheduled app updates. Will be spread around this point via the convar below. | steamclient.so |
| `nClientBackgroundAutoUpdateTimeSpreadMinutes` | `360` | 0x4 | Spread of time around the above target hour - this is the +/- 2-sigma window, so half this on either side. | steamclient.so |
| `@nClientCloudMaxMBParallelDownloads` | `64` | 0x4 |  | steamclient.so |
| `@nClientCloudMaxMBParallelUploads` | `64` | 0x4 |  | steamclient.so |
| `@nClientCloudMaxNumParallelDeletes` | `10` | 0x4 |  | steamclient.so |
| `@nClientCloudMaxNumParallelDownloads` | `10` | 0x4 |  | steamclient.so |
| `@nClientCloudMaxNumParallelUploads` | `10` | 0x4 |  | steamclient.so |
| `@nClientCloudMaxNumUploadsPerBatch` | `100` | 0x4 |  | steamclient.so |
| `@nClientCMDirectoryResultLoadPercentDither` | `10` | 0x8800000004 | Dither to apply to CM server loads received by CMDirectory query | steamclient.so |
| `@nClientCMUDPPingTimeGoodEnoughThresholdMS` | `50` | 0x4 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nClientCMUDPPingTimeoutUseGoodEnoughMS` | `250` | 0x4 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nClientDownloadEnableHTTP2PlatformLinux` | `1` | 0x4 | Enable HTTP/2 connections on Linux clients | steamclient.so |
| `@nClientDownloadEnableHTTP2PlatformWindows` | `1` | 0x4 | Enable HTTP/2 connections on Windows clients | steamclient.so |
| `@nClientDownloadEnableHTTP2RelBranch` | `0` | 0x4 | Only enable HTTP/2 on enabled platforms on rel branch client if this is set | steamclient.so |
| `@nClientDownloadInitWindowSizeHTTP2Connection` | `10000000` | 0x2700000004 | Init per-connection window size for HTTP/2. | steamclient.so |
| `@nClientDownloadInitWindowSizeHTTP2Stream` | `2000000` | 0x2700000004 | Init per-stream window size for HTTP/2. | steamclient.so |
| `@nClientDownloadProbUseHTTP2IfAvailable` | `50` | 0x4 | If http/2 is available for a given download source, use it w/ this probability [0,100] | steamclient.so |
| `@nClientEnableHTTP2PlatformLinux` | `1` | 0x4 | Enable HTTP/2 connections on Linux clients | steamclient.so |
| `@nClientEnableHTTP2PlatformWindows` | `1` | 0x4 | Enable HTTP/2 connections on Windows clients | steamclient.so |
| `@nClientEnableIPv6ForHTTPPlatformLinux` | `0` | 0x4 | Enable IPv6 HTTP connections by default on Linux clients | steamclient.so |
| `@nClientEnableIPv6ForHTTPPlatformWindows` | `0` | 0x4 | Enable IPv6 HTTP connections by default on Windows clients | steamclient.so |
| `@nClientFrameRateReportBatchSize` | `60` | 0x4 | Number of frame rate reports to collect locally before sending to the server | steamclient.so |
| `@nClientFrameRateReportSecs` | `60` | 0x4 | Number of seconds between individual frame rate reports | steamclient.so |
| `@nClientInitWindowSizeHTTP2Connection` | `10000000` | 0x2700000004 | Init per-connection window size for HTTP/2. | steamclient.so |
| `@nClientInitWindowSizeHTTP2Stream` | `2000000` | 0x2700000004 | Init per-stream window size for HTTP/2. | steamclient.so |
| `@nClientQueryCMDirectoryBeforeConnect` | `1` | 0x4 | Use CMDirectory webapi to get fresh CM list on connect - 0=disabled, 1=enabled, 2=main/dev/beta clients only | steamclient.so |
| `@nClientServiceMethodForDownloadListPercent` | `100` | 0x4 |  | steamclient.so |
| `nCloudFileCompressionMinFileSizeKB` | `16` | 0x4 |  | steamclient.so |
| `nCloudFileCompressionMinFileSizeKBSharedFile` | `128` | 0x4 |  | steamclient.so |
| `nCloudFileCompressionPercentageMin` | `10` | 0x4 |  | steamclient.so |
| `nCloudFileCompressionPercentageMinSharedFile` | `50` | 0x4 |  | steamclient.so |
| `nCloudUploadMinIntervalSec` | `1800` | 0x4 |  | steamclient.so |
| `nCloudUploadNetworkTimeoutSeconds` | `400` | 0x4 |  | steamclient.so |
| `@nContentDeltaChunkAppendChunksAfterProtobufSizeThresholdMB` | `33` | 0x4 |  | steamclient.so |
| `nContentDownloadsToOtherDrive` | `1` | 0x4 | Allow to download updates to other drives then install folder is on | steamclient.so |
| `nContentStatsReportInterval` | `72` | 0x4 | In Hours | steamclient.so |
| `@nContentUpdateAutoVerifyCleanBytesThresholdMB` | `2048` | 0x4 | How many clean MB must we verify before backing off on auto-verifies | steamclient.so |
| `@nContentUpdateAutoVerifyEnable` | `1` | 0x4 | 0 = disabled; 1 = enabled all clients | steamclient.so |
| `@nContentUpdateAutoVerifyIntervalDays` | `15` | 0x4 | Auto-verify game updates ever N days | steamclient.so |
| `@nCSClientRateLimitKbps` | `0` | 0x4 |  | steamclient.so |
| `@nCSJob404ResponseLimit` | `25` | 0x4 |  | steamclient.so |
| `@nCSJob5xyResponseLimit` | `10` | 0x4 |  | steamclient.so |
| `nDepotSaveCorruptChunks` | `0` | 0x4 |  | steamclient.so |
| `@nDownloadLANChunkCacheSizeMB` | `128` | 0x4 |  | steamclient.so |
| `@nDownloadLANPeerGroup` | `0` | 0x4 |  | steamclient.so |
| `@net_backlog_bytes_allowed` | `60000000` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@net_backlog_time_allowed_sec` | `8` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `net_incomingcheck` | `1` | 0x0 |  | steamclient.so |
| `@net_loopback` | `1` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `net_maxresendsperframe` | `32` | 0x0 |  | steamclient.so |
| `@NetConnectionBufferMsgLimit` | `1000` | 0x4 | Max # of message that will be buffered into a single zipped packet | steamclient.so |
| `@NetConnectionBufferThreaded` | `1` | 0x4 |  | steamclient.so |
| `@nGameRecordingTextureGPU` | `0` | 0x0 |  | steamui.so |
| `@nHTTPServerHTTP2InitWindowSizePerConnection` | `3145728` | 0x400000004 | Default HTTP/2 per-connection flow-control initial window size in bytes for CHTTPServer connections. Overridden per-server by SetHTTP2FlowControlInitWindowSizePerConnection(). | steamclient.so, steamui.so |
| `@nHTTPServerHTTP2InitWindowSizePerStream` | `1048576` | 0x400000004 | Default HTTP/2 per-stream flow-control initial window size in bytes for CHTTPServer connections. Overridden per-server by SetHTTP2FlowControlInitWindowSizePerStream(). | steamclient.so, steamui.so |
| `@nHTTPServerHTTP2MaxConcurrentStreams` | `25` | 0x400000004 | Default maximum concurrent HTTP/2 streams advertised per CHTTPServer connection. Overridden per-server by SetHTTP2MaxConcurrentStreamsPerConnection(). | steamclient.so, steamui.so |
| `@nHTTPServerLogLevelAccessLine200` | `3` | 0x400000000 | Log level to use for one-line access-log-style for each http server request returning 200 | steamclient.so, steamui.so |
| `@nHTTPServerLogLevelAccessLineNon200` | `2` | 0x400000000 | Log level to use for one-line access-log-style for each http server request that returns != 200 | steamclient.so, steamui.so |
| `@nHTTPServerLogLevelDetails200` | `4` | 0x400000000 | Log level to use for full details of any http server request returning 200.  This will probably fill up the log if you leave it on. | steamclient.so, steamui.so |
| `@nHTTPServerLogLevelDetailsNon200` | `4` | 0x400000000 | Log level to use for full details of any http server request returning != 200 | steamclient.so, steamui.so |
| `@nHTTPServerMaxPipelinedReqsPerConnection` | `8` | 0x400000000 | Max outstanding pipelined reqs per connection | steamclient.so, steamui.so |
| `@nHTTPServerYieldOn100ContinueSendSecs` | `300` | 0x400000000 | Seconds to yield when sending a 100 continue for purposes of telling client to send body of request | steamclient.so, steamui.so |
| `@nIOCPThreadCount` | `1` | 0x0 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nJobInteryieldMillisecondsAlertThreshold` | `120` | 0x400000004 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nJobInteryieldMillisecondsLogThreshold` | `80` | 0x400000004 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nJobInteryieldMillisecondsSpewThreshold` | `500` | 0x400000004 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nJobNetSendsInsaneThreshold` | `15000` | 0x400000004 |  | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nJWTVerifiedTokenCacheSize` | `0` | 0x4 | Number of verified JWTs to memoize so that re-presenting a token doesn't re-check its signature. 0 disables the cache. | steamclient.so, steamui.so |
| `@nLANPeerGroupRateLimitKbps` | `0` | 0x4 |  | steamclient.so |
| `@nLANPeerMaxConnections` | `24` | 0x4 |  | steamclient.so |
| `@nLANPeerRateLimitKbps` | `0` | 0x4 |  | steamclient.so |
| `@nLegalDictionaryUpdateRateInSeconds` | `600` | 0x4 |  | steamclient.so |
| `@nNetConnectionBufferZipLevel` | `1` | 0x4 |  | steamclient.so |
| `@nParentalSettingsLogLevel` | `4` | 0x4 | Control the amount of spew written to the parental log file | steamclient.so |
| `@nPartnerUploadFinalizeTimeoutSecs` | `600` | 0x4 | Seconds to timeout the DRM finalize which can be slow as it involves sending to cloud storage | steamclient.so |
| `nPeerContentDefaultMode` | `1` | 0x4 | 0 = off, 1 = only me, 2 = only friends, 3 = anyone | steamclient.so |
| `nProductInfoUpdateInterval` | `900` | 0x4 |  | steamclient.so |
| `@nProtobufArenaInitialBlockSize` | `65536` | 0x400000004 | Default initial allocation size for PB arena | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nProtobufArenaMaxBlockSize` | `524288` | 0x400000004 | Max block allocation size for PB arena | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nProtobufArenaNumberOfHeadersToShare` | `128` | 0x400000004 | Number of Jobs to give a single protobuf Arena before we create a new one | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nProtobufArenaNumberOfJobsToShare` | `128` | 0x400000004 | Number of Jobs to give a single protobuf Arena before we create a new one | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `nRichPresenceUploadThrottleSecs` | `5` | 0x4 |  | steamclient.so |
| `@nRoamingConfigReconnectCloudSyncWindowSec` | `7200` | 0x4 |  | steamclient.so |
| `@nScreenshotSaveMaxWidth` | `9999` | 0x0 |  | steamclient.so |
| `@nServerRefreshRateLimitAdditional` | `1` | 0x4 | Limits the burst number of calls per appid to refresh GMS game server lists | steamclient.so |
| `@nServerRefreshRateLimitBurst` | `100` | 0x4 | Limits the burst number of calls per appid to refresh GMS game server lists | steamclient.so |
| `@nServerRefreshRateLimitInterval` | `20` | 0x4 | Limits the burst number of calls per appid to refresh GMS game server lists | steamclient.so |
| `@nSiteLicenseProxyCacheMaxGB` | `100` | 0x0 | If local content cache is enabled, use up to this much disk space | steamclient.so |
| `@nSiteLicenseProxyEnableP2P` | `0` | 0x0 | If set, will have all connected clients join the same P2P download group | steamclient.so |
| `@nSiteLicenseProxyPort` | `0` | 0x0 | Local content cache: set > 0 to enable, will listen on this port | steamclient.so |
| `@nSpewThrottleNagFrequencyMs` | `5000` | 0x4 |  | friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper |
| `@nSpewThrottlePeriodMs` | `1000` | 0x4 |  | friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper |
| `@nSpewThrottleResumeThreshold` | `3` | 0x4 |  | friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper |
| `@nSpewThrottleTriggerThreshold` | `10` | 0x4 |  | friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper |
| `@nSpewThrottleUnconditionalResumeMs` | `5000` | 0x4 |  | friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper |
| `@nSpewThrottleUnconditionalTriggerCount` | `50` | 0x4 |  | friendsui.so, gamelauncher, gameoverlayui.so, libvideo.so, steam, steamclient.so, steamservice.so, steamsysinfo, steamui.so, steamwebhelper |
| `@nThreadedProtobufParseMinBytes` | `128` | 0x400000004 | Parse protobuf message bodies of at least this many bytes on a worker thread instead of on the job thread.  0 disables threaded parsing entirely. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nThreadedProtobufParseThreads` | `2` | 0x400000004 | Max worker threads in the dedicated pool used for threaded protobuf body parses (see @nThreadedProtobufParseMinBytes).  Changes take effect live. | gamelauncher, libvideo.so, steam, steamclient.so, steamservice.so, steamui.so |
| `@nVoicePostActivityXmitMS` | `250` | 0x4 | after voice activity, continue recording for this many ms even if there is silence | steamui.so |
| `@nWatchdogSteamUIPercentReport` | `1` | 0x4 |  | steamui.so |
| `OnCursorMoved` | `x` |  | y | friendsui.so, gameoverlayui.so, steamui.so |
| `OnScreenSizeChanged` | `oldwide` |  | oldtall | friendsui.so, gameoverlayui.so, steamui.so |
| `org.freedesktop.DBus` | `/org/freedesktop/DBus` / `/org/freedeskop/DBus` |  | GetConnectionUnixProcessID / AddMatch | steamclient.so, steamui.so |
| `@OSJumpListMRUSize` | `5` | 0x0 |  | steamui.so |
| `p2p_connecttimeout` | `15` | 0x0 |  | steamclient.so |
| `p2p_unusedtimeout` | `120` | 0x0 |  | steamclient.so |
| `@PeerContentClientMaxJobs` | `1` | 0x4 | number of peer sources used at the same time | steamclient.so |
| `@PeerContentServerMaxClients` | `8` | 0x4 | limit number of peers connected | steamclient.so |
| `@PeerContentServerPort` | `27040` | 0x4 | If peer content server, will listen on this port for TCP connections from peers | steamclient.so |
| `@PeerContentServerRetryDelay` | `60` | 0x4 | seconds before retrying peer content server | steamclient.so |
| `@PyrowaveHeightFactor` | `2` | 0x0 |  | steamui.so |
| `@PyrowavePSNR` | `35` | 0x0 |  | steamui.so |
| `@sBroadcastPreset` |  | 0x0 |  | steamui.so |
| `@sBroadcastTune` | `film` | 0x0 |  | steamui.so |
| `sc_kalman_a_vel` | `1.0` | 0x0 |  | steamclient.so |
| `sc_kalman_fastq` | `0` | 0x0 |  | steamclient.so |
| `sc_kalman_h_vel` | `1.0` | 0x0 |  | steamclient.so |
| `sc_kalman_q_vel` | `2.0` | 0x0 |  | steamclient.so |
| `sc_kalman_r_vel` | `2.0` | 0x0 |  | steamclient.so |
| `sc_kalman_repeated_sample` | `0` | 0x0 |  | steamclient.so |
| `sc_kalman_slowq` | `0` | 0x0 |  | steamclient.so |
| `@sCSDSVirtualHostHeader` |  | 0x4 |  | steamclient.so |
| `sDepotDownloadFileFilter` |  | 0x4 | only download matching files, eg *.exe;*.dll | steamclient.so |
| `@sForceLocalContentCache` |  | 0x4 |  | steamclient.so |
| `@sHardwareUpdateForceRequiredPriorityTS` |  | 0x4 |  | steamui.so |
| `spew_controller_loss` | `0` | 0x0 |  | steamclient.so |
| `@sSiteLicenseProxyCacheDirectory` | `appcache/slscache` | 0x0 | If local content cache is enabled, use this path for disk cache | steamclient.so |
| `@sSiteLicenseProxyExplicitIP` |  | 0x0 | Local content cache: if not blank, will instruct clients to go to this IP for the content cache. | steamclient.so |
| `@sSteamCmdForcePlatformBitness` |  | 0x4 | Must be one of: [32 \| 64] | steamclient.so |
| `@sSteamCmdForcePlatformCPU` |  | 0x4 | Must be one of: [x86 \| arm64] | steamclient.so |
| `@sSteamCmdForcePlatformType` |  | 0x4 | Must be one of: [windows \| macos \| linux \| android] | steamclient.so |
| `steam_controller_force_oobe` | `0` | 0x0 |  | steamclient.so |
| `@strCSNoCacheHeader` | `no-cache` | 0x4 |  | steamclient.so |
| `@StreamClientArgs` |  | 0x0 |  | steamclient.so |
| `streaming_log_spikes` | `0` | 0x0 |  | steamui.so |
| `@StreamTransportICEPenalty` | `0` | 0x0 | Add penalty (ms) to ICE for streaming transport selection | steamui.so |
| `@StreamTransportSDRPenalty` | `0` | 0x0 | Add penalty (ms) to SDR for streaming transport selection | steamui.so |
| `@sTrustedLocalContentCacheName` |  | 0x4 | Set this to the machine name where a trusted local Steam download cache is hosted, and we'll use it if available. | steamclient.so |
| `@test_bCloudForceSyncConflict` | `0` | 0x0 | If @test_nCloudForceSyncFailureAppID is set, then set this so that the failure case is 'file conflict' instead of generic failure | steamclient.so |
| `@test_nCloudForceSyncFailureAppID` | `0` | 0x0 | Set this to a non-zero App ID to test cloud sync failure. The next sync request will fail. | steamclient.so |
| `testappcloudpaths` | `0` | 0x10 |  | steamclient.so |
| `triton_imu_sensortime_log` | `0` | 0x0 | Spew the triton IMU sensor timings to console. | steamclient.so |
| `@uDownloadLANPeerPort` | `27038` | 0x4 | If LAN p2p download enabled, will listen on this port for TCP connections from peers. Must be set consistently across all members of the group! | steamclient.so |
| `ugc_query_default_cache_time` | `600` | 0x4 |  | steamclient.so |
| `ugc_query_max_get_details` | `2000` | 0x4 |  | steamclient.so |
| `UGCCDNReportPct` | `100` | 0x4 |  | steamclient.so |
| `@unMinimumShaderDownloadSizeInUI` | `33554432` | 0x4 |  | steamclient.so, steamui.so |
| `unShaderBackgroundProcessingThreads` | `0` | 0x4 |  | steamclient.so |
| `unShaderHighPriorityProcessingThreads` | `0` | 0x4 |  | steamclient.so |
| `unShaderHitCacheGeneration` | `0` | 0x4 |  | steamclient.so |
| `unShaderMaxHeadersPerMessage` | `1024` | 0x4 |  | steamclient.so |
| `unShaderMaxUploadMessageSizeKb` | `256` | 0x4 |  | steamclient.so |
| `@unUserStatsTest` | `0` | 0x4 |  | steamclient.so |
| `@uRemoteDiscoveryPortOverride` | `0` | 0x4 | If non-zero, will listen on this port for broadcasts instead of k_nBroadcastPort | steamclient.so |
| `@uRemoteDiscoveryPortTransmit` | `0` | 0x4 | If non-zero, will transmit outgoing broadcasts on this port instead of on the listen port | steamclient.so |
| `verifySignaturesBeforeLaunch` | `1` | 0x0 |  | steamui.so |
| `vgui_autocomplete_new_style` | `1` | 0x0 |  | steamui.so |
| `VK_LAYER_VALVE_steam_fossilize_32` | `ubuntu12_32/libVkLayer_steam_fossilize.so` |  | VK_LAYER_VALVE_steam_fossilize_1 | steamui.so |
| `VK_LAYER_VALVE_steam_fossilize_64` | `ubuntu12_64/libVkLayer_steam_fossilize.so` |  | VK_LAYER_VALVE_steam_fossilize_1 | steamui.so |
| `VK_LAYER_VALVE_steam_overlay_32` | `ubuntu12_32/steamoverlayvulkanlayer.so` |  | VK_LAYER_VALVE_steam_overlay_1 | steamui.so |
| `VK_LAYER_VALVE_steam_overlay_64` | `ubuntu12_64/steamoverlayvulkanlayer.so` |  | VK_LAYER_VALVE_steam_overlay_1 | steamui.so |
| `voice_api_optimalrate` | `24000` | 0x10 |  | steamclient.so |
| `voice_autogain` | `0` | 0x0 |  | steamclient.so |
| `voice_fakeloss` | `0` | 0x0 |  | steamclient.so |
| `@voice_minabs` | `0.15` | 0x0 |  | libvideo.so, steamclient.so, steamui.so |
| `@voice_minavg` | `1.0` | 0x0 |  | libvideo.so, steamclient.so, steamui.so |
| `voice_outputdevice` | `0` | 0x0 | 0=>Miles 1=>XAudio2 | steamclient.so |
| `voice_outputfile` |  | 0x0 | causes output from voice system to be written out to the specified file | steamclient.so |
| `voice_preprocess` | `0` | 0x0 | enables voice cleanup on incoming microphone data | steamclient.so |
| `voice_quality` | `4` | 0x0 |  | steamclient.so |
| `voice_resample_quality` | `1` | 0x10 |  | steamclient.so |
| `voice_silk_bitrate` | `30000` | 0x10 |  | steamclient.so |
| `@voice_spew_activity_check` | `0` | 0x0 |  | libvideo.so, steamclient.so, steamui.so |
| `@WatchdogThreadPercentReport` | `5` | 0x4 |  | steamclient.so |
| `workshop_items_cache_days` | `14` | 0x4 |  | steamclient.so |
| `workshop_items_full_check_interval` | `86400` | 0x4 |  | steamclient.so |
| `workshop_items_update_interval` | `2700` | 0x4 |  | steamclient.so |
| `WrapPanelItemVisibility` | `item` |  | visible | gameoverlayui.so, steamui.so |
