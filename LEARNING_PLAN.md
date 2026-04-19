# AgentScope 详细学习计划

基于项目仓库结构分析，为你制定的系统化学习路线。

---

## 阶段 1：环境准备与快速上手（1-2 天）

### 学习目标
- 成功运行第一个 Agent，建立信心
- 理解 AgentScope 核心架构

### 具体步骤

#### 1.1 安装环境
```bash
pip install agentscope
# 或使用 uv
uv pip install agentscope
```

#### 1.2 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [README_zh.md](README_zh.md) | 项目整体介绍、核心特性 |
| [README_zh.md:58-69](README_zh.md#L58-L69) | 核心架构概念 |
| [docs/tutorial/zh_CN/src/quickstart_installation.py](docs/tutorial/zh_CN/src/quickstart_installation.py) | 安装配置 |
| [docs/tutorial/zh_CN/src/quickstart_message.py](docs/tutorial/zh_CN/src/quickstart_message.py) | 消息机制基础 |
| [docs/tutorial/zh_CN/src/quickstart_agent.py](docs/tutorial/zh_CN/src/quickstart_agent.py) | Agent 创建流程 |
| [docs/tutorial/zh_CN/src/quickstart_key_concept.py](docs/tutorial/zh_CN/src/quickstart_key_concept.py) | 核心概念理解 |

#### 1.3 运行第一个示例
运行 [examples/agent/react_agent/main.py](examples/agent/react_agent/main.py)

关键代码解析：
```python
# 第 26-38 行：ReActAgent 创建流程
agent = ReActAgent(
    name="Friday",
    sys_prompt="You are a helpful assistant named Friday.",
    model=DashScopeChatModel(...),  # 模型配置
    formatter=DashScopeChatFormatter(),  # Prompt 格式化
    toolkit=toolkit,  # 工具集
    memory=InMemoryMemory(),  # 内存
)
```

### 核心概念清单

| 概念 | 源码位置 | 用途说明 |
|-----|---------|---------|
| **Model** | [src/agentscope/model/](src/agentscope/model/) | 负责与 LLM API 交互 |
| **Agent** | [src/agentscope/agent/](src/agentscope/agent/) | 智能体核心逻辑 |
| **Memory** | [src/agentscope/memory/](src/agentscope/memory/) | 存储对话历史 |
| **Tool** | [src/agentscope/tool/](src/agentscope/tool/) | 工具调用能力 |
| **Formatter** | [src/agentscope/formatter/](src/agentscope/formatter/) | Prompt 模板管理 |
| **Message** | [src/agentscope/message/](src/agentscope/message/) | 消息数据结构 |

### 实践练习
1. 修改 ReActAgent 的 sys_prompt，让 Agent 具有不同的角色（如翻译助手、代码助手）
2. 尝试添加一个新的 tool_function 到 toolkit
3. 观察异步编程模式 `asyncio.run(main())`

---

## 阶段 2：核心组件掌握（3-5 天）

### 学习目标
- 深入理解每个核心组件的实现细节
- 能够自定义 Tool、Memory、Formatter

### 2.1 Model & Prompt Formatter

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_model.py](docs/tutorial/zh_CN/src/task_model.py) | 模型配置与使用 |
| [docs/tutorial/zh_CN/src/task_prompt.py](docs/tutorial/zh_CN/src/task_prompt.py) | Prompt 构建技巧 |
| [src/agentscope/model/__init__.py](src/agentscope/model/__init__.py) | 支持的模型列表 |

#### 源码深入
- [src/agentscope/model/](src/agentscope/model/) - 查看不同 Model 实现
- [src/agentscope/formatter/](src/agentscope/formatter/) - Formatter 继承体系

### 2.2 Tool（工具调用）

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_tool.py](docs/tutorial/zh_CN/src/task_tool.py) | 工具系统详解 |
| [src/agentscope/tool/__init__.py](src/agentscope/tool/__init__.py) | 工具接口定义 |
| [examples/functionality/](examples/functionality/) | 功能示例 |

#### 运行示例
- [examples/functionality/structured_output/](examples/functionality/structured_output/) - 结构化输出

#### 自定义 Tool 学习
源码位置：[src/agentscope/tool/](src/agentscope/tool/)
学习如何使用 `@tool_function` 装饰器定义工具

### 2.3 Memory（短期 + 长期）

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_memory.py](docs/tutorial/zh_CN/src/task_memory.py) | Memory 系统完整教程 |
| [docs/tutorial/zh_CN/src/task_long_term_memory.py](docs/tutorial/zh_CN/src/task_long_term_memory.py) | 长期记忆与 ReMe |
| [src/agentscope/memory/](src/agentscope/memory/) | Memory 源码 |

#### 运行示例
- [examples/functionality/short_term_memory/](examples/functionality/short_term_memory/) - 短期记忆
- [examples/functionality/long_term_memory/](examples/functionality/long_term_memory/) - 长期记忆（含 ReMe）
- [examples/functionality/session_with_sqlite/](examples/functionality/session_with_sqlite/) - SQLite 持久化

### 2.4 Agent Skill

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_agent_skill.py](docs/tutorial/zh_CN/src/task_agent_skill.py) | Agent Skill 教程 |
| [examples/functionality/agent_skill/](examples/functionality/agent_skill/) | Anthropic Agent Skill 示例 |

### 2.5 RAG 集成

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_rag.py](docs/tutorial/zh_CN/src/task_rag.py) | RAG 教程 |
| [src/agentscope/rag/](src/agentscope/rag/) | RAG 模块源码 |
| [src/agentscope/embedding/](src/agentscope/embedding/) | Embedding 模块 |

#### 运行示例
- [examples/functionality/rag/](examples/functionality/rag/)
- [examples/functionality/vector_store/](examples/functionality/vector_store/)

### 实践练习
构建一个"带记忆的个人助手"：
1. 添加 2-3 个自定义工具（天气查询、日历提醒等）
2. 配置 SQLite 持久化记忆
3. 实现记忆压缩功能

---

## 阶段 3：多代理工作流与协作（5-7 天）

### 学习目标
- 掌握多 Agent 协作的多种模式
- 理解 MsgHub 通信机制

### 3.1 Workflow 模式

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/workflow_conversation.py](docs/tutorial/zh_CN/src/workflow_conversation.py) | 基础对话模式 |
| [docs/tutorial/zh_CN/src/workflow_multiagent_debate.py](docs/tutorial/zh_CN/src/workflow_multiagent_debate.py) | 多 Agent 辩论 |
| [docs/tutorial/zh_CN/src/workflow_concurrent_agents.py](docs/tutorial/zh_CN/src/workflow_concurrent_agents.py) | 并发 Agent |
| [docs/tutorial/zh_CN/src/workflow_handoffs.py](docs/tutorial/zh_CN/src/workflow_handoffs.py) | Handoffs 交接 |
| [docs/tutorial/zh_CN/src/workflow_routing.py](docs/tutorial/zh_CN/src/workflow_routing.py) | 路由分发 |
| [docs/tutorial/zh_CN/src/task_pipeline.py](docs/tutorial/zh_CN/src/task_pipeline.py) | Pipeline 流程 |

#### 运行示例
| 示例路径 | 学习内容 |
|---------|---------|
| [examples/workflows/multiagent_conversation/](examples/workflows/multiagent_conversation/) | 多 Agent 对话 |
| [examples/workflows/multiagent_debate/](examples/workflows/multiagent_debate/) | 辩论模式 |
| [examples/workflows/multiagent_concurrent/](examples/workflows/multiagent_concurrent/) | 并发执行 |
| [examples/game/werewolves/](examples/game/werewolves/) | 狼人杀游戏（多 Agent 复杂协作） |

### 3.2 A2A 协议

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_a2a.py](docs/tutorial/zh_CN/src/task_a2a.py) | A2A 协议详解 |
| [src/agentscope/a2a/](src/agentscope/a2a/) | A2A 源码实现 |
| [examples/agent/a2a_agent/](examples/agent/a2a_agent/) | A2A Agent 示例 |

### 3.3 State & Session

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_state.py](docs/tutorial/zh_CN/src/task_state.py) | 状态管理 |
| [src/agentscope/session/](src/agentscope/session/) | Session 模块 |

### 核心概念
| 概念 | 说明 | 源码位置 |
|-----|------|---------|
| **MsgHub** | 多 Agent 消息中心 | [src/agentscope/message/](src/agentscope/message/) |
| **Pipeline** | 流程编排 | [src/agentscope/pipeline/](src/agentscope/pipeline/) |
| **Handoffs** | Agent 交接机制 | workflow 文档 |

### 实践练习
构建一个"研究团队"：
- 研究员 Agent：搜索并收集信息
- 批判者 Agent：分析和质疑
- 总结者 Agent：整合并输出结论

---

## 阶段 4：语音智能体（Realtime Voice Agent）（4-6 天）

### 学习目标
- 掌握实时语音 Agent 的完整实现
- 理解多 Agent 实时语音协作

### 4.1 Realtime Agent

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_realtime.py](docs/tutorial/zh_CN/src/task_realtime.py) | 实时语音教程 |
| [src/agentscope/realtime/](src/agentscope/realtime/) | Realtime 模块源码 |
| [src/agentscope/agent/_realtime_agent.py](src/agentscope/agent/_realtime_agent.py) | RealtimeAgent 实现 |

#### 关键源码分析
```
src/agentscope/realtime/
├── _base.py                    # 基类定义
├── _dashscope_realtime_model.py # 阿里 DashScope 实时模型
├── _openai_realtime_model.py   # OpenAI 实时模型
├── _gemini_realtime_model.py   # Gemini 实时模型
└── _events/                    # 事件处理
```

#### 运行示例
| 示例路径 | 学习内容 |
|---------|---------|
| [examples/agent/realtime_voice_agent/](examples/agent/realtime_voice_agent/) | 实时语音 Agent |
| [examples/agent/voice_agent/](examples/agent/voice_agent/) | 语音 Agent |
| [examples/workflows/multiagent_realtime/](examples/workflows/multiagent_realtime/) | 多 Agent 实时语音 |

### 4.2 TTS（文本转语音）

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_tts.py](docs/tutorial/zh_CN/src/task_tts.py) | TTS 教程 |
| [src/agentscope/tts/](src/agentscope/tts/) | TTS 模块源码 |
| [examples/functionality/tts/](examples/functionality/tts/) | TTS 示例 |

### 核心概念
| 概念 | 说明 |
|-----|------|
| **流式输出** | 实时音频流处理 |
| **延迟优化** | 低延迟交互技巧 |
| **Web 部署** | 前端集成方案 |

### 实践练习
制作一个语音个人助理：
1. 实现语音输入 → LLM → TTS → 实时输出
2. 集成工具调用能力
3. 配置记忆持久化

---

## 阅段 5：Agentic RL 与微调（5-7 天）

### 学习目标
- 掌握完整的 Agent 微调流程
- 理解 Agentic RL 的原理与实践

### 5.1 Tuner 模块

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_tuner.py](docs/tutorial/zh_CN/src/task_tuner.py) | 微调教程 |
| [src/agentscope/tuner/](src/agentscope/tuner/) | Tuner 模块源码 |
| [src/agentscope/tune/](src/agentscope/tune/) | Tune 相关模块 |

#### 运行示例
| 示例路径 | 学习内容 |
|---------|---------|
| [examples/tuner/model_tuning/](examples/tuner/model_tuning/) | 模型微调 |
| [examples/tuner/model_selection/](examples/tuner/model_selection/) | 模型选择 |
| [examples/tuner/prompt_tuning/](examples/tuner/prompt_tuning/) | Prompt 微调 |

### 5.2 Tuner 源码结构
```
src/agentscope/tuner/
├── _config.py      # 微调配置
├── _dataset.py     # 数据集处理
├── _algorithm.py   # 算法实现
├── _model.py       # 模型接口
├── _workflow.py    # 工作流程
├── _judge.py       # 评判器
└── _tune.py        # 微调执行
```

### 5.3 Trinity-RFT 集成
官方 Trinity-RFT 仓库提供了更多 Agentic RL 示例：
- Math Agent
- Frozen Lake
- Learn to Ask
- Email Search
- Werewolf Game

### 核心概念
| 概念 | 说明 | 源码位置 |
|-----|------|---------|
| **SFT** | 监督微调 | _algorithm.py |
| **RLHF** | 人类反馈强化学习 | _algorithm.py |
| **Reward Model** | 奖励模型 | _judge.py |
| **数据收集** | Agent 交互数据 | _dataset.py |

### 实践练习
选择一个任务进行微调实验：
1. 收集 Agent 交互数据
2. 设计 reward 函数
3. 执行 SFT + RL 流程
4. 对比前后性能

---

## 阶段 6：高级特性、部署与实战项目（7-10 天）

### 学习目标
- 掌握 MCP、Evaluation 等高级功能
- 实现生产级部署

### 6.1 MCP（Model Context Protocol）

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_mcp.py](docs/tutorial/zh_CN/src/task_mcp.py) | MCP 教程 |
| [src/agentscope/mcp/](src/agentscope/mcp/) | MCP 模块源码 |
| [examples/functionality/mcp/](examples/functionality/mcp/) | MCP 示例 |

#### MCP 源码结构
```
src/agentscope/mcp/
├── _client_base.py            # 客户端基类
├── _stdio_stateful_client.py  # 标准输入输出客户端
├── _http_stateful_client.py   # HTTP 客户端
├── _http_stateless_client.py  # 无状态 HTTP 客户端
├── _mcp_function.py           # MCP 函数封装
└── _stateful_client_base.py   # 有状态客户端基类
```

### 6.2 Evaluation（评估）

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_eval.py](docs/tutorial/zh_CN/src/task_eval.py) | 评估教程 |
| [docs/tutorial/zh_CN/src/task_eval_openjudge.py](docs/tutorial/zh_CN/src/task_eval_openjudge.py) | OpenJudge 评估 |
| [src/agentscope/evaluate/](src/agentscope/evaluate/) | Evaluate 模块 |

#### 运行示例
- [examples/evaluation/](examples/evaluation/) - ACEBench 评估示例

### 6.3 Tracing & Middleware

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [docs/tutorial/zh_CN/src/task_tracing.py](docs/tutorial/zh_CN/src/task_tracing.py) | Tracing 教程 |
| [docs/tutorial/zh_CN/src/task_middleware.py](docs/tutorial/zh_CN/src/task_middleware.py) | Middleware 教程 |
| [docs/tutorial/zh_CN/src/task_hook.py](docs/tutorial/zh_CN/src/task_hook.py) | Hook 教程 |
| [src/agentscope/tracing/](src/agentscope/tracing/) | Tracing 模块 |

### 6.4 部署

#### 需要阅读的文件
| 文件路径 | 学习重点 |
|---------|---------|
| [examples/deployment/](examples/deployment/) | 部署示例 |
| [docs/tutorial/zh_CN/src/task_studio.py](docs/tutorial/zh_CN/src/task_studio.py) | Studio 可视化调试 |

### 6.5 其他高级 Agent

#### 需要阅读的文件
| 示例路径 | 学习内容 |
|---------|---------|
| [examples/agent/deep_research_agent/](examples/agent/deep_research_agent/) | 深度研究 Agent |
| [examples/agent/meta_planner_agent/](examples/agent/meta_planner_agent/) | 元规划 Agent |
| [examples/agent/browser_agent/](examples/agent/browser_agent/) | 浏览器 Agent |
| [examples/agent/a2ui_agent/](examples/agent/a2ui_agent/) | A2UI Agent |

### 实践练习
完成一个完整的实战项目：
- 语音多 Agent 研究助手
- RL 优化 + MCP Skill + Realtime Voice
- GitHub 开源发布

---

## 项目结构速查表

### 核心源码目录
```
src/agentscope/
├── agent/          # Agent 实现（ReAct, Realtime, User 等）
├── model/          # 模型接口（OpenAI, DashScope, Gemini 等）
├── memory/         # 记忆系统（短期、长期）
├── tool/           # 工具系统
├── formatter/      # Prompt 格式化
├── message/        # 消息数据结构
├── realtime/       # 实时语音模块
├── tts/            # TTS 模块
├── rag/            # RAG 模块
├── mcp/            # MCP 协议
├── tuner/          # 微调模块
├── a2a/            # A2A 协议
├── pipeline/       # 流程编排
├── session/        # Session 管理
├── tracing/        # 可观察性
├── embedding/      # Embedding 模块
├── evaluate/       # 评估模块
└── hooks/          # 钩子机制
```

### 示例目录
```
examples/
├── agent/          # Agent 示例（ReAct, Voice, Realtime 等）
├── functionality/  # 功能示例（Memory, RAG, MCP, TTS 等）
├── workflows/      # 工作流示例（对话、辩论、并发等）
├── game/           # 游戏示例（狼人杀）
├── tuner/          # 微调示例
├── deployment/     # 部署示例
├── evaluation/     # 评估示例
└── integration/    # 集成示例
```

### 教程源码
```
docs/tutorial/zh_CN/src/
├── quickstart_*.py   # 快速开始教程
├── task_*.py         # 任务教程
├── workflow_*.py     # 工作流教程
└── faq.py            # FAQ
```

---

## 学习进度追踪

建议使用以下表格追踪学习进度：

| 阶段 | 完成状态 | 关键收获 | 下一步 |
|-----|---------|---------|-------|
| 阶段 1 | ⬜ 未开始 | - | - |
| 阶段 2 | ⬜ 未开始 | - | - |
| 阶段 3 | ⬜ 未开始 | - | - |
| 阶段 4 | ⬜ 未开始 | - | - |
| 阶段 5 | ⬜ 未开始 | - | - |
| 阶段 6 | ⬜ 未开始 | - | - |

---

## 官方资源链接

- **GitHub 主仓库**: https://github.com/modelscope/agentscope
- **官方文档**: https://doc.agentscope.io/
- **中文文档**: https://doc.agentscope.io/zh_CN/
- **FAQ**: https://doc.agentscope.io/zh_CN/tutorial/faq.html
- **Roadmap**: docs/roadmap.md