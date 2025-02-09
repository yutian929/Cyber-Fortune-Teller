from openai import OpenAI
import os


def chat(
    messages,
    model="deepseek-ai/DeepSeek-R1",
    max_tokens=4096,
    base_url="https://api.siliconflow.cn/v1/",
    api_key=None,
    stream=True,
):
    """
    流式聊天补全函数

    参数：
    messages: 对话消息列表
    model: 使用的模型，默认为DeepSeek-R1
    max_tokens: 最大生成token数
    base_url: API基础地址
    api_key: 可选API密钥，默认从环境变量读取

    返回：
    (完整内容, 推理内容) 元组
    """
    # 获取API密钥
    api_key = api_key or os.environ.get("SILICONFOLW_API_KEY")
    if not api_key:
        raise ValueError("未找到API密钥, 请设置SILICONFOLW_API_KEY环境变量或直接传递密钥")

    # 初始化客户端
    client = OpenAI(base_url=base_url, api_key=api_key)

    try:
        # 创建流式请求
        response = client.chat.completions.create(
            model=model, messages=messages, stream=True, max_tokens=max_tokens
        )
    except Exception as e:
        raise RuntimeError(f"API请求失败: {str(e)}") from e

    first_content = True
    first_reason = True
    # 处理流式响应
    for chunk in response:
        delta = chunk.choices[0].delta

        # 处理普通内容
        if delta.content:
            new_content = delta.content
            if stream:
                if first_content:
                    yield "\n<ans>\n"
                    first_content = False
                for char in new_content:
                    yield char

        # 处理推理内容（如果存在）
        if hasattr(delta, "reasoning_content") and delta.reasoning_content:
            new_reasoning = delta.reasoning_content
            if stream:
                if first_reason:
                    yield "\n<think>\n"
                    first_reason = False
                for char in new_reasoning:
                    yield char


# 使用示例
if __name__ == "__main__":
    # 调用 chat 函数，它会返回一个生成器对象
    messages = [{"role": "user", "content": "请问我的事业运势如何？"}]
    response_generator = chat(messages)

    # 使用 for 循环来获取每次返回的内容
    for content in response_generator:
        # 这里你可以将每次输出的 content 进行显示或处理
        # 比如：更新UI，打印到屏幕，或者追加到文本框等
        print(content, end="", flush=True)  # 每次打印一个字符
