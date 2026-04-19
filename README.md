# AgentScope Learning

系统化学习 AgentScope 框架的项目，包含 6 个阶段的学习代码和笔记。

## 项目结构

```
agentscope-learning/
├── phase1-quickstart/     # 阶段1：环境准备与快速上手
├── phase2-components/     # 阶段2：核心组件掌握
├── phase3-workflows/      # 阶段3：多代理工作流与协作
├── phase4-voice/          # 阶段4：语音智能体
├── phase5-rl-tuning/      # 阶段5：Agentic RL 与微调
├── phase6-advanced/       # 阶段6：高级特性、部署与实战
└── LEARNING_PLAN.md       # 详细学习计划
```

## 学习进度

| 阶段 | 状态 | 描述 |
|-----|------|-----|
| Phase 1 | ✅ 完成 | ReActAgent 基础、核心组件理解 |
| Phase 2 | ⬜ 待开始 | Tool、Memory、RAG 深入学习 |
| Phase 3 | ⬜ 待开始 | 多 Agent 协作、MsgHub |
| Phase 4 | ⬜ 待开始 | Realtime Voice Agent |
| Phase 5 | ⬜ 待开始 | Agentic RL、模型微调 |
| Phase 6 | ⬜ 待开始 | MCP、部署、实战项目 |

## 阶段 1 学习内容

详见 [phase1-quickstart/README.md](phase1-quickstart/README.md)

### 核心收获
- ReActAgent 创建与使用
- Model、Agent、Memory、Tool、Formatter 五大组件
- 自定义工具 `@tool_function`
- 异步编程 `asyncio`

## 运行环境

- Python 3.10+
- AgentScope 1.0.18
- DashScope API Key（或 OpenAI API Key）

## 参考资源

- [AgentScope GitHub](https://github.com/modelscope/agentscope)
- [官方文档](https://doc.agentscope.io/)
- [中文教程](https://doc.agentscope.io/zh_CN/)