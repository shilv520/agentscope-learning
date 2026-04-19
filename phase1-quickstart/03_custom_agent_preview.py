# -*- coding: utf-8 -*-
"""
阶段1补充：自定义 Agent 预览

本文件展示如何自定义 Agent，为阶段2做准备。

AgentScope Agent 架构：
- AgentBase：基类，定义核心接口
- ReActAgent：官方实现（推理+行动）
- 自定义 Agent：继承 AgentBase 或 ReActAgent

核心概念：
- reply() 方法：Agent 的核心响应逻辑
- __call__() 方法：AgentBase 提供，调用 reply()
"""

import asyncio
import os
from typing import Sequence

from agentscope.agent import AgentBase
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import DashScopeChatModel
from agentscope.message import Msg, ContentBlock


# ========== 方式1：继承 AgentBase 创建最简单的 Agent ==========
class SimpleChatAgent(AgentBase):
    """
    最简单的自定义 Agent：直接调用模型回复
    没有工具调用，没有复杂推理
    """

    def __init__(
        self,
        name: str,
        sys_prompt: str,
        model: DashScopeChatModel,
        **kwargs,
    ) -> None:
        super().__init__(name=name, **kwargs)
        self.sys_prompt = sys_prompt
        self.model = model
        self.memory = InMemoryMemory()

    async def reply(self, x: Msg | None = None) -> Msg:
        """核心方法：处理消息并返回回复"""

        # 1. 如果有输入消息，添加到记忆
        if x is not None:
            self.memory.add(x)

        # 2. 构建对话历史（系统提示 + 用户消息）
        messages = [
            {"role": "system", "content": self.sys_prompt},
        ]
        # 从记忆中获取历史消息
        for msg in self.memory.get_memory():
            messages.append({
                "role": msg.role,
                "content": msg.content if isinstance(msg.content, str)
                          else str(msg.content),
            })

        # 3. 调用模型
        response = await self.model(messages)

        # 4. 创建回复消息并添加到记忆
        reply_msg = Msg(
            name=self.name,
            content=response.content,
            role="assistant",
        )
        self.memory.add(reply_msg)

        return reply_msg


# ========== 方式2：继承 ReActAgent 扩展功能 ==========
from agentscope.agent import ReActAgent
from agentscope.tool import Toolkit, execute_python_code


class CodeReviewAgent(ReActAgent):
    """
    扩展 ReActAgent：专门用于代码审查
    在原有 ReActAgent 基础上添加：
    - 固定的代码审查 sys_prompt
    - 预置的代码执行工具
    - 特殊的回复格式化
    """

    def __init__(self, name: str = "CodeReviewer", **kwargs) -> None:
        # 设置代码审查专用提示词
        code_review_prompt = """你是一个专业的代码审查助手。

你的职责：
1. 检查代码质量和潜在 bug
2. 提出改进建议
3. 解释最佳实践
4. 运行代码验证你的建议

审查步骤：
- 首先分析代码结构
- 检查潜在问题
- 使用 execute_python_code 验证修复方案
- 给出详细审查报告

请用中文回复，格式清晰。"""

        # 创建代码审查专用工具集
        toolkit = Toolkit()
        toolkit.register_tool_function(execute_python_code)

        # 调用父类初始化（复用 ReActAgent 的全部能力）
        super().__init__(
            name=name,
            sys_prompt=code_review_prompt,
            toolkit=toolkit,
            memory=InMemoryMemory(),
            formatter=DashScopeChatFormatter(),
            **kwargs,
        )

    # 可以覆盖 reply 方法添加特殊逻辑
    async def reply(self, x: Msg | None = None) -> Msg:
        """代码审查 Agent 的特殊回复处理"""

        # 调用父类的 reply（完整的 ReAct 流程）
        response = await super().reply(x)

        # 可以在这里添加额外的后处理
        # 例如：格式化输出、添加审查标签等

        return response


# ========== 演示运行 ==========
async def demo_simple_agent() -> None:
    """演示最简单的自定义 Agent"""

    agent = SimpleChatAgent(
        name="SimpleBot",
        sys_prompt="你是一个友好的聊天助手。请简洁回复。",
        model=DashScopeChatModel(
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model_name="qwen-max",
            stream=False,  # 简单模式下不需要流式
        ),
    )

    test_msg = Msg(
        name="user",
        content="你好，请简单介绍一下你自己。",
        role="user",
    )

    print("\n" + "=" * 50)
    print("演示：SimpleChatAgent（继承 AgentBase）")
    print("=" * 50)
    print(f"用户: {test_msg.content}")

    response = await agent(test_msg)
    print(f"Agent: {response.content}")


async def demo_code_review_agent() -> None:
    """演示扩展的 ReActAgent"""

    agent = CodeReviewAgent(
        model=DashScopeChatModel(
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model_name="qwen-max",
            stream=True,
        ),
    )

    test_msg = Msg(
        name="user",
        content="请审查这段代码：\ndef add(a, b):\n    return a + b",
        role="user",
    )

    print("\n" + "=" * 50)
    print("演示：CodeReviewAgent（继承 ReActAgent）")
    print("=" * 50)
    print(f"用户: {test_msg.content}")

    response = await agent(test_msg)
    print("-" * 50)
    print("审查结果:")
    for block in response.content:
        if hasattr(block, "text"):
            print(block.text)


async def main() -> None:
    """运行所有演示"""

    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("请设置环境变量 DASHSCOPE_API_KEY")
        exit(1)

    print("\n自定义 Agent 学习预览")
    print("=" * 50)
    print("方式1: 继承 AgentBase - 创建最简单的 Agent")
    print("方式2: 继承 ReActAgent - 扩展官方 Agent")
    print("=" * 50)

    await demo_simple_agent()
    await demo_code_review_agent()

    print("\n" + "=" * 50)
    print("阶段2将深入学习 Agent 自定义")
    print("源码位置：src/agentscope/agent/_agent_base.py")
    print("         src/agentscope/agent/_react_agent.py")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())