import qrcode
from PIL import Image
import numpy as np
import cv2
from MyQR import myqr
import os


# imgFile = 'transportation_and_vehicle_05.png'
imgFile = 'jia.png'


def convertPNG(img1):
    img = img1.convert('RGBA')
    r, g, b, a = img.split()
    a0 = np.array(b)  # 转换为np矩阵
    a1 = cv2.threshold(a0, 0, 255, cv2.THRESH_BINARY)  # 设定阈值
    a2 = Image.fromarray(a1[1])  # 转换为Image的tube格式，注意为a1[1]
    a3 = np.array(a2)
    a4 = Image.fromarray(a3.astype('uint8'))  # 由float16转换为uint8
    img = Image.merge("RGBA", (b, g, r, a4))
    return img


def make_bw_qrcode():
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=1
    )
    # 设置二维码的大小
    qr.add_data("https://www.guanacossj.com/")
    qr.make(fit=True)
    icon = Image.open(imgFile)
    # icon = convertPNG(icon)
    img = qr.make_image()
    img = img.convert("RGBA")
    # 获取图片的宽高
    img_w, img_h = img.size
    factor = 3
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    # 重新设置logo的尺寸
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    print(img.size, w, h)
    img.paste(icon, (w, h), icon)
    img.save("my_blog.png")


def make_col_qrcode():
    version, level, qr_name = myqr.run(
        words="https://www.baidu.com",  # 可以是字符串，也可以是网址(前面要加http(s)://)
        version=1,  # 设置容错率为最高
        level='H',  # 控制纠错水平，范围是L、M、Q、H，从左到右依次升高
        picture="123.gif",  # 将二维码和图片合成
        colorized=True,  # 彩色二维码
        contrast=1.0,  # 用以调节图片的对比度，1.0 表示原始图片，更小的值表示更低对比度，更大反之。默认为1.0
        brightness=1.0,  # 用来调节图片的亮度，其余用法和取值同上
        save_name="3.gif",  # 保存文件的名字，格式可以是jpg,png,bmp,gif
        save_dir=os.getcwd()  # 控制位置
    )


if __name__ == '__main__':
    make_bw_qrcode()