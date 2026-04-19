# 阶段 1 学习笔记

## 核心概念理解

### 1. AgentScope 架构总览

AgentScope 采用"乐高积木"式的设计，核心组件包括：

```
┌─────────────────────────────────────────────────────┐
│                     Agent                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Model  │  │ Memory  │  │  Tool   │  │Formatter│ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
└─────────────────────────────────────────────────────┘
```

### 2. 各组件职责

| 组件 | 职责 | 示例类 |
|-----|------|-------|
| **Model** | 与 LLM API 交互 | `DashScopeChatModel`, `OpenAIChatModel` |
| **Agent** | 智能体核心逻辑 | `ReActAgent`, `UserAgent`, `RealtimeAgent` |
| **Memory** | 存储对话历史 | `InMemoryMemory`, 长期记忆 |
| **Tool** | 工具调用能力 | `Toolkit`, `@tool_function` |
| **Formatter** | Prompt 模板管理 | `DashScopeChatFormatter` |

### 3. ReActAgent 工作流程

```
用户输入 → Agent.reason() → LLM.think() → 决策
                                    ↓
                            需要工具调用？
                                    ↓
                    是 → tool.execute() → 结果 → 继续 think
                    否 → 直接回复用户
```

### 4. 关键代码解析

#### 创建 ReActAgent
```python
agent = ReActAgent(
    name="Friday",              # Agent 名称（用于识别）
    sys_prompt="...",           # 系统提示词（定义 Agent 角色）
    model=DashScopeChatModel(), # 模型配置
    formatter=...,              # Prompt 格式化
    toolkit=toolkit,            # 工具集
    memory=InMemoryMemory(),    # 记忆
)
```

#### 注册工具
```python
# 方式1：使用内置工具
toolkit.register_tool_function(execute_python_code)

# 方式2：自定义工具
@tool_function
def my_tool(...) -> Annotated[str, "返回说明"]:
    """工具描述"""
    return result
```

### 5. 异步编程模式

AgentScope 使用 `asyncio` 实现异步：
- `async def main()` - 异步主函数
- `await agent(msg)` - 异步调用 Agent
- `asyncio.run(main())` - 启动异步运行

## 实践总结

### 练习1：创建翻译助手
修改 `sys_prompt`，让 Agent 成为专业翻译。

### 练习2：创建代码助手
添加 `execute_python_code` 工具，让 Agent 能运行代码。

### 练习3：添加自定义工具
使用 `@tool_function` 装饰器定义新工具。

## 下一步

完成阶段1后，进入阶段2学习：
- Model 配置细节
- Tool 自定义进阶
- Memory 系统（短期/长期）
- RAG 集成

## 通用概念迁移（适用于其他框架）

### Agent 核心公式（所有框架通用）

```
Agent = LLM + Memory + Tools + Planning
```

这个公式适用于：
- AgentScope
- LangChain
- AutoGen
- Dify
- 自研系统

### 概念对照表

| AgentScope | LangChain | AutoGen | 通用概念 |
|-----------|-----------|---------|---------|
| ReActAgent | AgentExecutor | ConversableAgent | Agent 基础类 |
| InMemoryMemory | ConversationBufferMemory | - | 对话历史 |
| Toolkit | Tools | - | 工具调用 |
| MsgHub | - | GroupChat | 多 Agent 通信 |
| Workflow | LCEL | GroupChat Manager | 流程编排 |

### 学习 AgentScope 的通用价值

1. **ReAct 模式**：推理+行动，所有 Agent 核心模式
2. **工具调用**：Function Calling，LLM 通用能力
3. **记忆管理**：短期/长期记忆，所有对话系统需要
4. **多 Agent 协作**：团队工作模式，复杂系统必备
5. **规划能力**：任务分解与执行，高级 Agent 能力

### 迁移到其他框架的技巧

理解本质 → 学习 API → 快速上手

示例：
```python
# AgentScope
agent = ReActAgent(sys_prompt="...", model=..., toolkit=...)

# LangChain（概念相同，API 不同）
agent = AgentExecutor.from_agent_and_tools(
    agent=..., tools=..., memory=...
)

# AutoGen
agent = ConversableAgent(
    name="...", system_message="...", llm_config=...
)
```