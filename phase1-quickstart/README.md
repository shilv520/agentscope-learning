# 阶段 1：环境准备与快速上手

AgentScope 学习第一阶段代码和笔记。

## 文件说明

| 文件 | 说明 |
|-----|------|
| `01_hello_agentscope.py` | 第一个 Agent 示例（基础版） |
| `02_practice_agents.py` | 实践练习（翻译助手、代码助手、通用助手） |
| `LEARNING NOTES.md` | 学习笔记和核心概念总结 |

## 运行方法

### 1. 设置 API Key
```bash
# Windows CMD
set DASHSCOPE_API_KEY=your_api_key

# Windows PowerShell / Linux / Mac
export DASHSCOPE_API_KEY=your_api_key
```

### 2. 运行示例
```bash
# 基础示例
python 01_hello_agentscope.py

# 实践练习（可选择不同 Agent）
python 02_practice_agents.py
```

## 学习目标

1. ✅ 理解 AgentScope 核心架构（Model、Agent、Memory、Tool、Formatter）
2. ✅ 运行第一个 ReAct Agent
3. ✅ 掌握 sys_prompt 的作用
4. ✅ 学会使用 `@tool_function` 定义自定义工具
5. ✅ 理解异步编程模式

## 核心概念

- **ReActAgent**: 采用 Reasoning + Acting 模式的智能体
- **Toolkit**: 工具容器，Agent 可调用其中的工具
- **InMemoryMemory**: 短期记忆，存储对话历史
- **Formatter**: Prompt 格式化，适配不同模型

## 学习收获

完成本阶段后，你将能够：
- 创建具有不同角色的 Agent
- 添加自定义工具扩展 Agent 能力
- 理解 AgentScope 的核心设计理念