{
  "title": "bpipe_and_emsx",
  "language": "zh-CN",
  "description": "一套面向 Bloomberg B-PIPE 与 EMSX 的体系化技术教材大纲。以 Bloomberg 实时市场数据分发与订单执行工作流为主线，分别讲解 B-PIPE 的市场数据接入、订阅、解码、字段语义、时间戳、数据质量、吞吐与延迟治理，以及 EMSX 的订单生命周期、交易路由、执行状态、成交回报、API 集成与交易系统架构；进一步覆盖两者在交易平台中的协同方式、与内部 OMS/EMS/算法交易系统的集成、故障恢复、监控、安全、测试和端到端案例。教材区分公开可验证的产品概念、依赖 Bloomberg 许可/版本/具体接口的实现细节，以及需要通过企业 Bloomberg 文档或实际环境确认的内容。",
  "navigation": {
    "mode": "hierarchical_arbitrary_depth",
    "description": "所有级别的节均建立独立物理子目录与 index.md，导航链接支持兄弟节点流转及跨层级父级兄弟智能回溯。"
  },
  "parts": [
    {
      "title": "Bloomberg 交易与市场数据平台全景",
      "slug": "01_Bloomberg交易与市场数据平台全景_BloombergPlatformOverview",
      "intro": "建立 B-PIPE 与 EMSX 的系统级认知，明确市场数据分发、交易订单管理、执行连接及企业交易架构之间的边界。",
      "sections": [
        {
          "title": "Bloomberg 产品生态与系统角色",
          "slug": "01.01_Bloomberg产品生态与系统角色_BloombergProductEcosystem",
          "intro": "从机构交易技术架构理解 Bloomberg Terminal、B-PIPE、EMSX、数据许可、交易场所及内部交易系统的关系。",
          "subsections": [
            {
              "title": "B-PIPE 与 EMSX 的定位",
              "slug": "01.01.1_BPIPE与EMSX的定位_BPIPEAndEMSXRoles",
              "intro": "区分 B-PIPE 的实时市场数据分发职责与 EMSX 的订单管理和执行工作流职责。",
              "subsections": [
                {
                  "title": "B-PIPE：实时市场数据分发",
                  "slug": "01.01.1.1_BPIPE实时市场数据分发_BPIPEMarketDataDistribution",
                  "intro": "理解 B-PIPE 作为企业级 Bloomberg 市场数据分发服务的角色、数据源、订阅方和典型使用场景。"
                },
                {
                  "title": "EMSX：订单管理与执行工作流",
                  "slug": "01.01.1.2_EMSX订单管理与执行工作流_EMSXOrderAndExecutionWorkflow",
                  "intro": "理解 EMSX 在订单创建、路由、执行监控、成交回报及交易工作流中的角色。"
                },
                {
                  "title": "市场数据平面与交易执行平面",
                  "slug": "01.01.1.3_市场数据平面与交易执行平面_MarketDataAndExecutionPlanes",
                  "intro": "比较行情分发与订单执行链路的接口模型、时效要求、故障模式和一致性边界。"
                }
              ]
            },
            {
              "title": "典型机构交易系统架构",
              "slug": "01.01.2_典型机构交易系统架构_InstitutionalTradingArchitecture",
              "intro": "梳理交易员工作站、内部 OMS/EMS、算法交易服务、市场数据平台、经纪商和交易所之间的关系。",
              "subsections": [
                {
                  "title": "买方与卖方系统角色",
                  "slug": "01.01.2.1_买方与卖方系统角色_BuySideAndSellSideRoles",
                  "intro": "比较资产管理公司、对冲基金、券商和做市商在市场数据消费与订单执行中的系统职责。"
                },
                {
                  "title": "OMS、EMS 与算法交易系统",
                  "slug": "01.01.2.2_OMS_EMS与算法交易系统_OMSAndEMSAndAlgoTrading",
                  "intro": "区分订单管理、执行管理、算法执行和交易后处理，并定位 EMSX 的集成边界。"
                },
                {
                  "title": "端到端数据流与控制流",
                  "slug": "01.01.2.3_端到端数据流与控制流_EndToEndDataAndControlFlow",
                  "intro": "描述行情从 Bloomberg 到策略、订单从内部系统到执行场所的路径。"
                }
              ]
            }
          ]
        },
        {
          "title": "接入前置条件与环境模型",
          "slug": "01.02_接入前置条件与环境模型_ConnectivityAndEnvironment",
          "intro": "理解产品许可、服务开通、网络连通、身份认证、软件组件和测试环境等前置条件。",
          "subsections": [
            {
              "title": "产品许可与数据使用权",
              "slug": "01.02.1_产品许可与数据使用权_LicensingAndEntitlements",
              "intro": "理解市场数据许可、用户/应用权限、再分发限制及合规审计；具体权利以机构合同和 Bloomberg 确认结果为准。"
            },
            {
              "title": "网络、主机与服务部署",
              "slug": "01.02.2_网络主机与服务部署_NetworkAndHostDeployment",
              "intro": "梳理网络区域、主机、端口、防火墙、冗余链路、地址配置和环境隔离等部署事项。"
            },
            {
              "title": "开发、认证与生产环境",
              "slug": "01.02.3_开发认证与生产环境_DevelopmentCertificationProduction",
              "intro": "区分开发测试、认证/验收和生产环境，建立配置、版本和变更控制流程。"
            }
          ]
        }
      ]
    },
    {
      "title": "B-PIPE 市场数据基础与接入",
      "slug": "02_BPIPE市场数据基础与接入_BPIPEFundamentalsAndConnectivity",
      "intro": "从市场数据模型出发，掌握 B-PIPE 的接入架构、订阅模型、数据标识和基础运行机制。",
      "sections": [
        {
          "title": "市场数据模型与标识体系",
          "slug": "02.01_市场数据模型与标识体系_MarketDataModelAndIdentifiers",
          "intro": "理解证券标识、Bloomberg 标识、数据字段、市场中心、交易时段和报价类型之间的关系。",
          "subsections": [
            {
              "title": "证券与金融工具标识",
              "slug": "02.01.1_证券与金融工具标识_SecurityIdentifiers",
              "intro": "比较 Bloomberg Yellow Key、Ticker、ISIN、CUSIP、SEDOL、FIGI 等标识概念及其适用边界。",
              "subsections": [
                {
                  "title": "Bloomberg Ticker 与 Yellow Key",
                  "slug": "02.01.1.1_BloombergTicker与YellowKey_BloombergTickerAndYellowKey",
                  "intro": "理解 Bloomberg 证券标识的组成思路、资产类别后缀及标识解析中的歧义。"
                },
                {
                  "title": "跨系统标识映射",
                  "slug": "02.01.1.2_跨系统标识映射_CrossSystemIdentifierMapping",
                  "intro": "设计 Bloomberg 标识与内部 Security Master、交易所代码和标准标识之间的映射及校验。"
                }
              ]
            },
            {
              "title": "市场数据字段与数据类型",
              "slug": "02.01.2_市场数据字段与数据类型_MarketDataFieldsAndTypes",
              "intro": "理解字段名称、定义、数值类型、枚举、缺失值、单位、精度和字段版本管理。",
              "subsections": [
                {
                  "title": "静态参考数据与实时行情",
                  "slug": "02.01.2.1_静态参考数据与实时行情_ReferenceDataAndRealTimeData",
                  "intro": "区分静态证券属性、参考数据、实时 Bid/Ask/Last、成交量及市场状态等数据类别。"
                },
                {
                  "title": "报价、成交与市场状态字段",
                  "slug": "02.01.2.2_报价成交与市场状态字段_QuoteTradeAndMarketStatusFields",
                  "intro": "分析 Bid、Ask、Last、Size、Volume、条件码、交易状态和交易时段等字段语义。"
                },
                {
                  "title": "缺失值、无效值与字段质量",
                  "slug": "02.01.2.3_缺失值无效值与字段质量_MissingValuesAndFieldQuality",
                  "intro": "识别空值、未定义值、无效更新、异常值和字段暂不可用，避免将其解释为零。"
                }
              ]
            }
          ]
        },
        {
          "title": "B-PIPE 接入架构与订阅生命周期",
          "slug": "02.02_BPIPE接入架构与订阅生命周期_BPIPEConnectivityAndSubscription",
          "intro": "掌握消费者与数据分发服务之间的连接、订阅、更新接收、取消订阅和资源管理。",
          "subsections": [
            {
              "title": "B-PIPE 服务与消费者架构",
              "slug": "02.02.1_BPIPE服务与消费者架构_BPIPEServiceAndConsumerArchitecture",
              "intro": "理解数据分发服务、网络连接、客户端接口、消费者应用和下游缓存之间的逻辑关系。",
              "subsections": [
                {
                  "title": "部署拓扑与冗余设计",
                  "slug": "02.02.1.1_部署拓扑与冗余设计_DeploymentTopologyAndRedundancy",
                  "intro": "分析单实例、多实例、主备、双活及跨机房部署的可用性与数据连续性取舍。"
                },
                {
                  "title": "连接建立与会话管理",
                  "slug": "02.02.1.2_连接建立与会话管理_ConnectionAndSessionManagement",
                  "intro": "梳理连接建立、会话状态、断线检测、重连和应用生命周期管理。"
                }
              ]
            },
            {
              "title": "订阅与更新处理",
              "slug": "02.02.2_订阅与更新处理_SubscriptionAndUpdateProcessing",
              "intro": "理解按证券和字段订阅数据、接收初始状态与后续更新，以及管理订阅规模。",
              "subsections": [
                {
                  "title": "订阅请求与取消订阅",
                  "slug": "02.02.2.1_订阅请求与取消订阅_SubscribeAndUnsubscribe",
                  "intro": "设计订阅注册表、订阅去重、生命周期管理和资源释放策略。"
                },
                {
                  "title": "初始快照与增量更新",
                  "slug": "02.02.2.2_初始快照与增量更新_SnapshotAndIncrementalUpdates",
                  "intro": "区分初始数据状态与后续字段更新，理解应用如何构建当前证券状态。"
                },
                {
                  "title": "批量订阅与订阅规模治理",
                  "slug": "02.02.2.3_批量订阅与订阅规模治理_BulkSubscriptionManagement",
                  "intro": "处理大规模证券订阅、字段裁剪、分批启动、限流和消费者资源预算。"
                }
              ]
            },
            {
              "title": "接口与消息解码",
              "slug": "02.02.3_接口与消息解码_APIAndMessageDecoding",
              "intro": "根据机构实际采用的 Bloomberg 接口和 SDK，理解消息类型、字段容器、类型转换及版本兼容。",
              "subsections": [
                {
                  "title": "API 消息模型与事件循环",
                  "slug": "02.02.3.1_API消息模型与事件循环_APIMessageModelAndEventLoop",
                  "intro": "理解事件驱动消息处理、回调/轮询模型、事件分派和消费者线程模型；具体行为以所用 SDK 文档为准。"
                },
                {
                  "title": "字段容器与类型安全解码",
                  "slug": "02.02.3.2_字段容器与类型安全解码_FieldContainerAndTypedDecoding",
                  "intro": "设计字段访问、类型检查、枚举解码、错误处理和内部规范化数据模型。"
                },
                {
                  "title": "SDK 版本与接口兼容性",
                  "slug": "02.02.3.3_SDK版本与接口兼容性_SDKVersionAndCompatibility",
                  "intro": "管理头文件、运行时库、编译器、操作系统、ABI 和 Bloomberg SDK 版本兼容性。"
                }
              ]
            }
          ]
        },
        {
          "title": "B-PIPE 数据语义与正确性",
          "slug": "02.03_BPIPE数据语义与正确性_BPIPEDataSemanticsAndCorrectness",
          "intro": "从金融数据语义和流式系统正确性出发，处理乱序、重复、缺口、时间戳和状态重建。",
          "subsections": [
            {
              "title": "时间戳与事件顺序",
              "slug": "02.03.1_时间戳与事件顺序_TimestampsAndEventOrdering",
              "intro": "区分事件时间、接收时间、处理时间和本地单调时钟，理解跨主机时钟同步与顺序判断。",
              "subsections": [
                {
                  "title": "交易所时间与本地接收时间",
                  "slug": "02.03.1.1_交易所时间与本地接收时间_ExchangeTimeAndReceiveTime",
                  "intro": "分析源端时间戳与本地网络接收时间的差异。"
                },
                {
                  "title": "乱序、重复与更新合并",
                  "slug": "02.03.1.2_乱序重复与更新合并_OutOfOrderDuplicateAndCoalescing",
                  "intro": "设计序列检查、重复检测、字段级合并和状态一致性策略；保证取决于具体数据产品与接口。"
                },
                {
                  "title": "时钟同步与延迟测量",
                  "slug": "02.03.1.3_时钟同步与延迟测量_ClockSynchronizationAndLatencyMeasurement",
                  "intro": "理解 NTP/PTP、时钟漂移、时间戳精度和端到端延迟测量误差。"
                }
              ]
            },
            {
              "title": "数据缺口与状态恢复",
              "slug": "02.03.2_数据缺口与状态恢复_DataGapsAndStateRecovery",
              "intro": "识别连接中断、消费者过载、服务切换和数据缺口，并设计状态恢复流程。",
              "subsections": [
                {
                  "title": "断线期间的数据完整性",
                  "slug": "02.03.2.1_断线期间的数据完整性_DataIntegrityDuringDisconnect",
                  "intro": "判断断线期间是否存在可恢复数据、是否需要重新获取快照，以及如何标记数据不确定状态。"
                },
                {
                  "title": "重连与重新订阅",
                  "slug": "02.03.2.2_重连与重新订阅_ReconnectAndResubscribe",
                  "intro": "设计退避重连、订阅恢复、状态重建和重复消息防护。"
                },
                {
                  "title": "行情状态有效性",
                  "slug": "02.03.2.3_行情状态有效性_MarketDataValidity",
                  "intro": "定义行情 stale、halted、delayed、invalid 等内部状态及策略消费门禁。"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "title": "EMSX 订单与执行管理",
      "slug": "03_EMSX订单与执行管理_EMSXOrderAndExecutionManagement",
      "intro": "从订单生命周期出发，理解 EMSX 的交易工作流、订单路由、执行状态、成交回报和程序化集成。",
      "sections": [
        {
          "title": "EMSX 业务模型与订单生命周期",
          "slug": "03.01_EMSX业务模型与订单生命周期_EMSXBusinessModelAndOrderLifecycle",
          "intro": "建立订单、子订单、执行、成交、分配和交易场所之间的业务对象模型。",
          "subsections": [
            {
              "title": "订单核心对象",
              "slug": "03.01.1_订单核心对象_OrderCoreEntities",
              "intro": "理解订单标识、证券、买卖方向、数量、价格、账户、策略和路由属性。",
              "subsections": [
                {
                  "title": "Parent Order 与 Child Order",
                  "slug": "03.01.1.1_母订单与子订单_ParentAndChildOrders",
                  "intro": "理解母订单拆分、子订单执行、数量汇总和订单层级关系。"
                },
                {
                  "title": "订单状态与状态迁移",
                  "slug": "03.01.1.2_订单状态与状态迁移_OrderStatesAndTransitions",
                  "intro": "建立通用订单状态模型，并与 EMSX 实际状态字段逐项映射。"
                },
                {
                  "title": "订单属性与执行约束",
                  "slug": "03.01.1.3_订单属性与执行约束_OrderAttributesAndExecutionConstraints",
                  "intro": "理解数量、限价、有效期、交易时段、账户、经纪商、交易场所和执行指令。"
                }
              ]
            },
            {
              "title": "订单生命周期事件",
              "slug": "03.01.2_订单生命周期事件_OrderLifecycleEvents",
              "intro": "理解订单提交、确认、路由、修改、撤销、拒绝、部分成交和完全成交等事件。",
              "subsections": [
                {
                  "title": "订单提交与确认",
                  "slug": "03.01.2.1_订单提交与确认_OrderSubmissionAndAcknowledgment",
                  "intro": "梳理内部订单创建、EMSX 接收、校验、确认及外部路由之间的边界。"
                },
                {
                  "title": "修改与撤销",
                  "slug": "03.01.2.2_修改与撤销_OrderAmendmentAndCancellation",
                  "intro": "分析修改/撤销请求、在途状态、竞态条件和最终状态确认。"
                },
                {
                  "title": "部分成交与完全成交",
                  "slug": "03.01.2.3_部分成交与完全成交_PartialAndFullFills",
                  "intro": "处理累计成交量、剩余量、平均成交价、多笔成交和终态判断。"
                }
              ]
            }
          ]
        },
        {
          "title": "EMSX 路由与市场连接",
          "slug": "03.02_EMSX路由与市场连接_EMSXRoutingAndMarketConnectivity",
          "intro": "理解订单如何从 EMSX 工作流进入经纪商、算法策略和交易场所，以及路由选择的业务约束。",
          "subsections": [
            {
              "title": "经纪商与交易场所路由",
              "slug": "03.02.1_经纪商与交易场所路由_BrokerAndVenueRouting",
              "intro": "梳理经纪商、交易场所、路由目的地和可用交易通道之间的关系。",
              "subsections": [
                {
                  "title": "Broker 与 Destination",
                  "slug": "03.02.1.1_Broker与Destination_BrokerAndDestination",
                  "intro": "理解经纪商和路由目的地的区别、可用性及机构配置依赖。"
                },
                {
                  "title": "算法路由与执行策略",
                  "slug": "03.02.1.2_算法路由与执行策略_AlgoRoutingAndExecutionStrategies",
                  "intro": "介绍 VWAP、TWAP、POV、Implementation Shortfall 等通用执行策略，并区分通用术语与 EMSX 可用功能。"
                },
                {
                  "title": "路由失败与拒单处理",
                  "slug": "03.02.1.3_路由失败与拒单处理_RoutingFailureAndRejectHandling",
                  "intro": "处理目的地不可用、权限不足、参数无效、市场关闭和经纪商拒绝等故障。"
                }
              ]
            },
            {
              "title": "交易协议与执行回报",
              "slug": "03.02.2_交易协议与执行回报_TradingProtocolsAndExecutionReports",
              "intro": "理解 EMSX 与外部经纪商/交易场所之间常见交易协议的角色；具体链路由经纪商和部署配置决定。",
              "subsections": [
                {
                  "title": "FIX 协议基础",
                  "slug": "03.02.2.1_FIX协议基础_FIXProtocolFundamentals",
                  "intro": "理解 FIX 会话、序列号、心跳、订单消息和执行报告的基本结构。"
                },
                {
                  "title": "ITCH 与 OUCH 的接口角色",
                  "slug": "03.02.2.2_ITCH与OUCH的接口角色_ITCHAndOUCHRoles",
                  "intro": "区分 ITCH 行情协议与 OUCH 订单输入协议，并理解它们并不等同于 EMSX API。"
                },
                {
                  "title": "成交回报与执行状态对账",
                  "slug": "03.02.2.3_成交回报与执行状态对账_ExecutionReportsAndReconciliation",
                  "intro": "处理执行报告、成交明细、累计数量和内部订单状态之间的对账。"
                }
              ]
            }
          ]
        },
        {
          "title": "EMSX 程序化接口与系统集成",
          "slug": "03.03_EMSX程序化接口与系统集成_EMSXAPIAndIntegration",
          "intro": "从软件工程角度理解 EMSX API 的接口能力、消息交互、订单事件订阅和内部系统集成。",
          "subsections": [
            {
              "title": "EMSX API 概览",
              "slug": "03.03.1_EMSXAPI概览_EMSXAPIOverview",
              "intro": "区分 EMSX 工作流产品、程序化 API、会话/服务模型和具体 SDK 版本；接口能力以 Bloomberg 授权文档为准。",
              "subsections": [
                {
                  "title": "API 能力边界与接入方式",
                  "slug": "03.03.1.1_API能力边界与接入方式_APICapabilitiesAndConnectivity",
                  "intro": "梳理订单提交、修改、撤销、状态查询和事件接收等能力，并标注不同 API/版本是否支持。"
                },
                {
                  "title": "请求、响应与异步事件",
                  "slug": "03.03.1.2_请求响应与异步事件_RequestResponseAndAsyncEvents",
                  "intro": "设计请求关联标识、异步回报、超时、重试和事件分派。"
                },
                {
                  "title": "API 权限与字段配置",
                  "slug": "03.03.1.3_API权限与字段配置_APIEntitlementsAndFieldConfiguration",
                  "intro": "理解用户/应用权限、账户和经纪商配置、可见字段及环境差异。"
                }
              ]
            },
            {
              "title": "内部 OMS/EMS 集成模式",
              "slug": "03.03.2_内部OMS_EMS集成模式_InternalOMSAndEMSIntegration",
              "intro": "设计内部订单系统与 EMSX 之间的适配层、状态映射、幂等处理和故障隔离。",
              "subsections": [
                {
                  "title": "订单适配器与领域模型",
                  "slug": "03.03.2.1_订单适配器与领域模型_OrderAdapterAndDomainModel",
                  "intro": "建立内部规范化订单模型，将内部订单状态和 EMSX 字段/状态映射隔离在适配层。"
                },
                {
                  "title": "幂等、重试与重复提交防护",
                  "slug": "03.03.2.2_幂等重试与重复提交防护_IdempotencyAndRetry",
                  "intro": "通过业务键、请求关联、状态检查和持久化意图防止重试导致重复订单。"
                },
                {
                  "title": "事件驱动与状态同步",
                  "slug": "03.03.2.3_事件驱动与状态同步_EventDrivenStateSynchronization",
                  "intro": "设计事件消费、状态投影、顺序处理、重复事件防护和周期性对账。"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "title": "B-PIPE 与 EMSX 的协同集成",
      "slug": "04_BPIPE与EMSX的协同集成_BPIPEAndEMSXIntegration",
      "intro": "把市场数据输入与订单执行输出连接起来，构建从行情观察、策略决策、订单生成到执行反馈的闭环。",
      "sections": [
        {
          "title": "交易系统端到端架构",
          "slug": "04.01_交易系统端到端架构_EndToEndTradingArchitecture",
          "intro": "建立行情接入、标准化、策略计算、风控、订单管理、EMSX 执行和成交回报的完整链路。",
          "subsections": [
            {
              "title": "市场数据到策略输入",
              "slug": "04.01.1_市场数据到策略输入_MarketDataToStrategy",
              "intro": "设计 B-PIPE 消费者、内部行情总线、缓存/状态库和策略订阅接口。",
              "subsections": [
                {
                  "title": "行情规范化与内部事件模型",
                  "slug": "04.01.1.1_行情规范化与内部事件模型_MarketDataNormalization",
                  "intro": "将外部字段转换为内部稳定模型，处理标识映射、精度、单位、时间戳和数据质量标记。"
                },
                {
                  "title": "行情缓存与最新状态维护",
                  "slug": "04.01.1.2_行情缓存与最新状态维护_MarketDataCacheAndState",
                  "intro": "设计按证券维护最新状态、字段更新时间、版本和 stale 标记的缓存结构。"
                },
                {
                  "title": "策略消费与数据有效性门禁",
                  "slug": "04.01.1.3_策略消费与数据有效性门禁_StrategyDataQualityGate",
                  "intro": "在策略使用行情前验证数据新鲜度、完整性、交易状态和字段有效性。"
                }
              ]
            },
            {
              "title": "策略决策到 EMSX 订单执行",
              "slug": "04.01.2_策略决策到EMSX订单执行_StrategyToEMSXExecution",
              "intro": "把策略意图转换为订单请求，经风控和订单管理后提交至 EMSX，并接收执行结果。",
              "subsections": [
                {
                  "title": "订单意图与风控检查",
                  "slug": "04.01.2.1_订单意图与风控检查_OrderIntentAndPreTradeRisk",
                  "intro": "定义订单意图、价格/数量约束、账户权限、持仓限额和重复订单检查。"
                },
                {
                  "title": "订单状态投影与执行反馈",
                  "slug": "04.01.2.2_订单状态投影与执行反馈_OrderStateProjection",
                  "intro": "将 EMSX 执行事件映射为内部订单状态，并驱动策略调整和剩余量管理。"
                },
                {
                  "title": "成交驱动的持仓与风险更新",
                  "slug": "04.01.2.3_成交驱动的持仓与风险更新_FillDrivenPositionAndRisk",
                  "intro": "根据成交回报更新持仓、现金、风险敞口和订单剩余量，处理延迟与对账差异。"
                }
              ]
            }
          ]
        },
        {
          "title": "一致性、恢复与故障隔离",
          "slug": "04.02_一致性恢复与故障隔离_ConsistencyRecoveryAndFaultIsolation",
          "intro": "处理市场数据链路和订单执行链路之间的时序差异、部分故障和状态不一致。",
          "subsections": [
            {
              "title": "行情与订单的时间一致性",
              "slug": "04.02.1_行情与订单的时间一致性_MarketDataAndOrderTemporalConsistency",
              "intro": "分析策略决策所用行情版本、订单提交时间和成交发生时间之间的因果关系。",
              "subsections": [
                {
                  "title": "决策时行情快照记录",
                  "slug": "04.02.1.1_决策时行情快照记录_DecisionTimeMarketSnapshot",
                  "intro": "记录策略决策时使用的行情版本和时间戳，以支持回放、审计和执行分析。"
                },
                {
                  "title": "行情过期与订单提交保护",
                  "slug": "04.02.1.2_行情过期与订单提交保护_StaleMarketDataOrderGuard",
                  "intro": "定义行情过期阈值、市场状态门禁和订单提交前的最后检查。"
                }
              ]
            },
            {
              "title": "故障场景与恢复策略",
              "slug": "04.02.2_故障场景与恢复策略_FailureScenariosAndRecovery",
              "intro": "建立行情中断、订单 API 断连、回报延迟、服务不可用和内部消费者崩溃时的恢复策略。",
              "subsections": [
                {
                  "title": "B-PIPE 故障对策略的影响",
                  "slug": "04.02.2.1_BPIPE故障对策略的影响_BPIPEFailureImpact",
                  "intro": "定义行情不可用时策略暂停、降级、切换数据源或只允许风险降低操作的策略。"
                },
                {
                  "title": "EMSX 故障期间的订单保护",
                  "slug": "04.02.2.2_EMSX故障期间的订单保护_EMSXFailureOrderProtection",
                  "intro": "处理执行通道不可用时的订单状态不确定性，防止盲目重发或错误认定订单终态。"
                },
                {
                  "title": "恢复后的状态对账",
                  "slug": "04.02.2.3_恢复后的状态对账_PostRecoveryReconciliation",
                  "intro": "通过查询、事件补偿、成交对账和人工确认恢复内部状态可信度。"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "title": "低延迟与高吞吐工程实践",
      "slug": "05_低延迟与高吞吐工程实践_LowLatencyAndThroughputEngineering",
      "intro": "围绕 B-PIPE 行情消费与 EMSX 订单处理链路，分析性能瓶颈、队列、内存、并发和端到端延迟。",
      "sections": [
        {
          "title": "延迟模型与性能预算",
          "slug": "05.01_延迟模型与性能预算_LatencyModelAndBudget",
          "intro": "定义行情接收、解码、分发、策略计算、风控、订单提交和回报处理各阶段的延迟指标。",
          "subsections": [
            {
              "title": "端到端延迟分解",
              "slug": "05.01.1_端到端延迟分解_EndToEndLatencyBreakdown",
              "intro": "拆分网络传输、内核处理、用户态解码、排队、调度、策略计算和外部执行时间。",
              "subsections": [
                {
                  "title": "Market Data Tick-to-Strategy",
                  "slug": "05.01.1.1_行情Tick到策略延迟_TickToStrategyLatency",
                  "intro": "度量行情到达应用、解码、状态更新和策略可见之间的时间。"
                },
                {
                  "title": "Strategy-to-Order 与执行回报延迟",
                  "slug": "05.01.1.2_策略到订单及执行回报延迟_StrategyToOrderAndExecutionLatency",
                  "intro": "度量策略决策到订单提交、确认、成交及回报处理的各阶段耗时。"
                }
              ]
            },
            {
              "title": "吞吐、突发流量与背压",
              "slug": "05.01.2_吞吐突发流量与背压_ThroughputBurstsAndBackpressure",
              "intro": "分析行情突发、消息堆积、消费者处理能力和端到端背压机制。",
              "subsections": [
                {
                  "title": "消息速率与突发特征",
                  "slug": "05.01.2.1_消息速率与突发特征_MessageRateAndBursts",
                  "intro": "测量平均消息率、峰值消息率、突发长度和不同市场时段的负载分布。"
                },
                {
                  "title": "队列深度与过载保护",
                  "slug": "05.01.2.2_队列深度与过载保护_QueueDepthAndOverloadProtection",
                  "intro": "设计有界队列、合并策略、优先级和过载告警，明确不能随意丢弃的交易事件。"
                }
              ]
            }
          ]
        },
        {
          "title": "C++ 消费者与事件处理优化",
          "slug": "05.02_Cpp消费者与事件处理优化_CppConsumerOptimization",
          "intro": "以 C++17/20 为主要示例，优化消息解码、内存分配、数据布局、线程模型和缓存局部性。",
          "subsections": [
            {
              "title": "内存与对象生命周期",
              "slug": "05.02.1_内存与对象生命周期_MemoryAndObjectLifetime",
              "intro": "降低热路径动态分配、复制和不可预测的析构成本。",
              "subsections": [
                {
                  "title": "对象复用与内存池",
                  "slug": "05.02.1.1_对象复用与内存池_ObjectReuseAndMemoryPools",
                  "intro": "比较对象池、固定容量缓冲区、arena 和常规分配器的适用场景与生命周期约束。"
                },
                {
                  "title": "数据布局与 Cache Locality",
                  "slug": "05.02.1.2_数据布局与缓存局部性_DataLayoutAndCacheLocality",
                  "intro": "比较 AoS/SoA、紧凑结构、缓存行对齐和热点字段分离对行情处理性能的影响。"
                }
              ]
            },
            {
              "title": "并发模型与线程调度",
              "slug": "05.02.2_并发模型与线程调度_ConcurrencyAndThreadScheduling",
              "intro": "分析单线程事件循环、多线程分区、SPSC 队列和线程亲和性之间的取舍。",
              "subsections": [
                {
                  "title": "事件循环与线程分区",
                  "slug": "05.02.2.1_事件循环与线程分区_EventLoopAndThreadPartitioning",
                  "intro": "按证券、数据源或功能分区处理事件，避免共享状态和锁竞争。"
                },
                {
                  "title": "无锁队列与内存序",
                  "slug": "05.02.2.2_无锁队列与内存序_LockFreeQueuesAndMemoryOrdering",
                  "intro": "使用 acquire/release 等内存序实现生产者消费者队列，并分析伪共享、ABA 和进度保证。"
                },
                {
                  "title": "CPU 亲和性与 NUMA",
                  "slug": "05.02.2.3_CPU亲和性与NUMA_CPUAffinityAndNUMA",
                  "intro": "理解绑核、NUMA 内存分配、跨节点访问和线程迁移对尾延迟的影响。"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "title": "可观测性、测试与生产运维",
      "slug": "06_可观测性测试与生产运维_ObservabilityTestingAndOperations",
      "intro": "建立从开发验证到生产运行的完整质量体系，覆盖数据正确性、订单安全、延迟监控、故障排查和发布控制。",
      "sections": [
        {
          "title": "日志、指标与链路追踪",
          "slug": "06.01_日志指标与链路追踪_LogsMetricsAndTracing",
          "intro": "为行情事件和订单事件建立可关联的可观测性体系。",
          "subsections": [
            {
              "title": "关键指标设计",
              "slug": "06.01.1_关键指标设计_KeyMetrics",
              "intro": "定义消息速率、订阅数、队列深度、数据新鲜度、订单状态分布、拒单率和执行延迟等指标。",
              "subsections": [
                {
                  "title": "延迟分位数与尾延迟",
                  "slug": "06.01.1.1_延迟分位数与尾延迟_LatencyPercentilesAndTailLatency",
                  "intro": "使用 p50、p90、p99、p99.9 和最大值描述性能分布，避免平均值掩盖尾部问题。"
                },
                {
                  "title": "数据新鲜度与订单健康度",
                  "slug": "06.01.1.2_数据新鲜度与订单健康度_DataFreshnessAndOrderHealth",
                  "intro": "监控行情 stale、订阅异常、订单悬挂、回报延迟和状态对账差异。"
                }
              ]
            },
            {
              "title": "日志关联与生产排障",
              "slug": "06.01.2_日志关联与生产排障_LogCorrelationAndTroubleshooting",
              "intro": "通过证券标识、内部订单 ID、外部订单 ID、请求 ID 和时间戳关联跨组件事件。",
              "subsections": [
                {
                  "title": "行情事件追踪",
                  "slug": "06.01.2.1_行情事件追踪_MarketDataEventTracing",
                  "intro": "追踪单条行情从接收、解码、规范化、缓存到策略消费的完整路径。"
                },
                {
                  "title": "订单事件追踪",
                  "slug": "06.01.2.2_订单事件追踪_OrderEventTracing",
                  "intro": "追踪订单创建、提交、路由、确认、成交、撤销和对账的事件链。"
                }
              ]
            }
          ]
        },
        {
          "title": "测试策略与故障演练",
          "slug": "06.02_测试策略与故障演练_TestingAndFaultInjection",
          "intro": "构建单元测试、集成测试、回放测试、压力测试和生产故障演练。",
          "subsections": [
            {
              "title": "测试环境与模拟器",
              "slug": "06.02.1_测试环境与模拟器_TestEnvironmentsAndSimulators",
              "intro": "通过接口隔离和模拟组件验证应用逻辑；模拟结果不能替代 Bloomberg 认证或真实环境验证。",
              "subsections": [
                {
                  "title": "行情回放与确定性测试",
                  "slug": "06.02.1.1_行情回放与确定性测试_MarketDataReplayAndDeterministicTesting",
                  "intro": "使用录制数据重放行情，验证字段解码、状态重建、乱序处理和策略输入一致性。"
                },
                {
                  "title": "订单状态机测试",
                  "slug": "06.02.1.2_订单状态机测试_OrderStateMachineTesting",
                  "intro": "覆盖部分成交、重复回报、乱序事件、撤单竞态、拒单和断线恢复等状态迁移。"
                }
              ]
            },
            {
              "title": "压力测试与故障注入",
              "slug": "06.02.2_压力测试与故障注入_LoadTestingAndFaultInjection",
              "intro": "模拟消息突发、网络抖动、断连、进程崩溃、消费者变慢和外部服务不可用。",
              "subsections": [
                {
                  "title": "峰值行情负载测试",
                  "slug": "06.02.2.1_峰值行情负载测试_PeakMarketDataLoadTesting",
                  "intro": "测量峰值消息率下的吞吐、CPU、内存、队列积压和尾延迟。"
                },
                {
                  "title": "订单执行故障演练",
                  "slug": "06.02.2.2_订单执行故障演练_OrderExecutionFailureDrills",
                  "intro": "验证执行通道断开、回报延迟和订单状态不确定时的保护、恢复和人工介入流程。"
                }
              ]
            }
          ]
        },
        {
          "title": "安全、权限与合规运维",
          "slug": "06.03_安全权限与合规运维_SecurityEntitlementsAndCompliance",
          "intro": "确保行情数据使用、交易操作、审计记录和生产变更满足机构控制要求。",
          "subsections": [
            {
              "title": "身份、权限与最小授权",
              "slug": "06.03.1_身份权限与最小授权_IdentityAndLeastPrivilege",
              "intro": "管理服务身份、用户权限、账户权限、密钥和环境访问控制。"
            },
            {
              "title": "审计、数据许可与交易控制",
              "slug": "06.03.2_审计数据许可与交易控制_AuditLicensingAndTradingControls",
              "intro": "保留数据访问和订单操作审计，落实市场数据许可、交易限额、权限审批及紧急停止机制。"
            },
            {
              "title": "发布、回滚与变更管理",
              "slug": "06.03.3_发布回滚与变更管理_ReleaseRollbackAndChangeManagement",
              "intro": "设计灰度发布、版本兼容、配置回滚、交易时段变更窗口和生产变更审批。"
            }
          ]
        }
      ]
    },
    {
      "title": "综合案例与工程实践项目",
      "slug": "07_综合案例与工程实践项目_CapstoneProjects",
      "intro": "通过端到端项目把 B-PIPE 数据接入、EMSX 订单执行、C++ 性能工程和生产可靠性串联起来。",
      "sections": [
        {
          "title": "案例一：B-PIPE 行情消费服务",
          "slug": "07.01_BPIPE行情消费服务案例_BPIPEMarketDataConsumerProject",
          "intro": "构建可测试、可观测、支持重连和数据质量检测的 C++ 行情消费者；接口实现以获授权的 Bloomberg SDK 文档为准。",
          "subsections": [
            {
              "title": "需求分析与架构设计",
              "slug": "07.01.1_需求分析与架构设计_RequirementsAndArchitecture",
              "intro": "定义证券订阅、字段配置、事件模型、数据质量、延迟目标和故障恢复需求。"
            },
            {
              "title": "C++ 实现与性能验证",
              "slug": "07.01.2_Cpp实现与性能验证_CppImplementationAndBenchmarking",
              "intro": "实现订阅管理、消息解码适配层、内部事件队列、行情缓存和性能基准。"
            },
            {
              "title": "故障恢复与运行手册",
              "slug": "07.01.3_故障恢复与运行手册_RecoveryAndRunbook",
              "intro": "实现断线检测、重连、重新订阅、数据有效性标记和运维诊断。"
            }
          ]
        },
        {
          "title": "案例二：EMSX 订单适配器",
          "slug": "07.02_EMSX订单适配器案例_EMSXOrderAdapterProject",
          "intro": "构建内部订单模型与 EMSX 接口之间的适配服务，重点验证幂等、状态同步和异常处理。",
          "subsections": [
            {
              "title": "订单领域模型与状态机",
              "slug": "07.02.1_订单领域模型与状态机_OrderDomainModelAndStateMachine",
              "intro": "定义订单、执行、成交和路由对象，并建立显式状态迁移规则。"
            },
            {
              "title": "接口适配与异步事件处理",
              "slug": "07.02.2_接口适配与异步事件处理_APIAdapterAndAsyncEvents",
              "intro": "隔离 Bloomberg API 细节，处理请求关联、异步事件、超时、重试和错误分类。"
            },
            {
              "title": "幂等与对账验证",
              "slug": "07.02.3_幂等与对账验证_IdempotencyAndReconciliation",
              "intro": "验证重复请求、断线重连、成交回报重放和内部外部状态对账。"
            }
          ]
        },
        {
          "title": "案例三：行情驱动的执行闭环",
          "slug": "07.03_行情驱动的执行闭环案例_MarketDataDrivenExecution",
          "intro": "把行情消费、策略决策、风控、订单提交和执行反馈整合为完整的交易工作流。",
          "subsections": [
            {
              "title": "端到端系统设计",
              "slug": "07.03.1_端到端系统设计_EndToEndSystemDesign",
              "intro": "定义组件边界、数据契约、订单状态、故障域和延迟预算。"
            },
            {
              "title": "回放、仿真与执行分析",
              "slug": "07.03.2_回放仿真与执行分析_ReplaySimulationAndExecutionAnalysis",
              "intro": "使用历史/录制行情和模拟执行环境评估策略输入、订单行为和执行质量。"
            },
            {
              "title": "生产就绪评审",
              "slug": "07.03.3_生产就绪评审_ProductionReadinessReview",
              "intro": "从权限、风控、监控、故障恢复、容量、审计和回滚能力评估上线条件。"
            }
          ]
        }
      ]
    },
    {
      "title": "术语、接口与参考资料附录",
      "slug": "08_术语接口与参考资料附录_GlossaryAndReferences",
      "intro": "汇总 B-PIPE、EMSX、市场数据、交易执行和低延迟工程中的关键术语、缩写及学习资源。",
      "sections": [
        {
          "title": "核心术语与缩写",
          "slug": "08.01_核心术语与缩写_CoreGlossary",
          "intro": "建立中英文对照术语表，明确容易混淆的产品名、业务概念和技术概念。",
          "subsections": [
            {
              "title": "Bloomberg 产品与接口术语",
              "slug": "08.01.1_Bloomberg产品与接口术语_BloombergProductAndAPI",
              "intro": "整理 B-PIPE、EMSX、Terminal、API、SDK、服务、会话、订阅、订单和执行等术语。"
            },
            {
              "title": "市场数据与交易术语",
              "slug": "08.01.2_市场数据与交易术语_MarketDataAndTrading",
              "intro": "整理 Quote、Trade、NBBO、Order Book、Parent Order、Child Order、Fill、Slippage、Market Impact 等术语。"
            },
            {
              "title": "低延迟与系统术语",
              "slug": "08.01.3_低延迟与系统术语_LowLatencyAndSystems",
              "intro": "整理 Tick-to-Trade、Tail Latency、Jitter、NUMA、Kernel Bypass、Backpressure、Idempotency 等术语。"
            }
          ]
        },
        {
          "title": "接口文档与学习路径",
          "slug": "08.02_接口文档与学习路径_APIReferencesAndLearningPath",
          "intro": "建立官方文档、机构内部文档、SDK 示例和实操验证的资料索引。",
          "subsections": [
            {
              "title": "Bloomberg 授权文档与开发者资源",
              "slug": "08.02.1_Bloomberg授权文档与开发者资源_BloombergAuthorizedDocumentation",
              "intro": "以机构可访问的 Bloomberg Enterprise 产品文档、SDK 发布说明、接口示例和支持渠道为准；公开网页不一定包含完整接口规范。"
            },
            {
              "title": "内部系统契约与运行手册",
              "slug": "08.02.2_内部系统契约与运行手册_InternalContractsAndRunbooks",
              "intro": "记录机构内部 Security Master、OMS、EMS、风控、监控、部署和应急流程的权威定义。"
            },
            {
              "title": "学习顺序与能力检查",
              "slug": "08.02.3_学习顺序与能力检查_LearningPathAndCompetencyChecklist",
              "intro": "按照产品定位、B-PIPE 数据消费、EMSX 订单生命周期、系统集成、低延迟优化和生产运维建立渐进式学习路径。"
            }
          ]
        }
      ]
    }
  ]
}
