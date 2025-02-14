import qrcode


def generate_qr_code(content, filename="bazi_qrcode.png", show=True):
    # 生成二维码
    qr = qrcode.QRCode(
        version=None,  # 改为自动检测版本（原先是强制指定40）
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 提高容错率到30%
        box_size=8,  # 减小单个单元格的像素尺寸
        border=2,  # 缩小边框宽度
    )

    qr.add_data(content)
    try:
        qr.make(fit=True)
    except qrcode.exceptions.DataOverflowError:
        print("内容过长，无法生成二维码！建议缩短分析结果")
        exit()

    # 创建图像并保存
    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)  # 保存为二维码图片

    if show:
        # 展示二维码
        img.show()


if __name__ == "__main__":
    generate_qr_code("Hello, World!")
