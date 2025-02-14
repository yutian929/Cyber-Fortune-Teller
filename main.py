from lib.bazi import calc_bazi
from lib.llm import chat
from lib.qr import generate_qr_code


def hello():
    print(f"{'*'*10}\t欢迎使用Cyber算命程序\t{'*'*10}")
    print(f"\nAuthor: yutian, huangshan\n")


if __name__ == "__main__":
    hello()
    # 1. 用户输入sex, birth_city, year, month, day, hour
    sex = input("请输入性别(男/女):")
    year = input("请输入出生年份(如1990):")
    month = input("请输入出生月份(如1):")
    day = input("请输入出生日期(如1):")
    hour = input("请输入出生时间(如15):")
    birth_city = input("请输入出生城市(如北京):")
    birth_city, year, month, day, hour = (
        birth_city,
        int(year),
        int(month),
        int(day),
        int(hour),
    )
    print("正在计算八字，请稍等...")
    bazi_str = calc_bazi(birth_city, year, month, day, hour)
    print(f"您的八字为：{bazi_str}")
    # 2. 与llm聊天，传入八字字符串，获取回答
    aspect = input("请问您想了解什么方面的事情？")
    llm_content = f"请问八字为{bazi_str}的{sex}人在{aspect}方面的运势如何？回答可以简短一些。"
    chat_generator = chat(
        messages=[
            {
                "role": "user",
                "content": llm_content,
            }
        ],
        model="deepseek-ai/DeepSeek-R1",
        max_tokens=4096,
        base_url="https://api.siliconflow.cn/v1/",
        api_key=None,
        stream=True,
    )
    print("正在为您计算，请稍等...")
    # 3. 输出结果, UI显示
    # 使用 for 循环来获取每次返回的内容
    full_content = f""
    full_reason = f""
    chunk_flag = "think"
    for content in chat_generator:
        if "<think>" in content:
            chunk_flag = "think"
        elif "<ans>" in content:
            chunk_flag = "ans"
        print(content, end="", flush=True)  # 每次打印一个字符
        if chunk_flag == "think":
            full_reason += content
        elif chunk_flag == "ans":
            full_content += content
    print("\n")
    # 4. 保存为二维码
    combined_content = f"Q:\n{llm_content}\n\nA:\n{full_content}"
    generate_qr_code(combined_content, filename="bazi_qrcode.png", show=True)
