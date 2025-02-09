from lib.bazi import calc_bazi
from lib.llm import chat
import qrcode

if __name__ == "__main__":
    # 1. 用户输入birth_city, year, month, day, hour
    print("欢迎使用八字算命系统")
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
    chat_generator = chat(
        messages=[
            {
                "role": "user",
                "content": f"请问八字为{bazi_str}的{sex}人在{aspect}方面的运势如何？简短点，思考快一点",
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
    full_content = ""
    full_reason = ""
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
    print("完整内容：")
    print(full_reason)
    print(full_content)
    # 4. 保存为二维码
    combined_content = f"{full_content}\n{full_reason}"
    # 生成二维码
    qr = qrcode.QRCode(
        version=1,  # version决定二维码的大小，从1（21x21）到40（177x177）
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 错误修正级别，L（低）- 7%容错，M（中）- 15%，H（高）- 30%
        box_size=10,  # 每个二维码单元格的像素大小
        border=4,  # 边框宽度
    )

    qr.add_data(combined_content)  # 把字符串数据加到二维码
    qr.make(fit=True)

    # 创建图像并保存
    img = qr.make_image(fill="black", back_color="white")
    img.save("bazi_qrcode.png")  # 保存为二维码图片

    # 展示二维码
    img.show()
