#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Author  : rusi_

import os
import argparse

from PIL import Image

# 参数flag
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help="请输入要转换的图片文件路径，通过参数-i 或者 -input：")
parser.add_argument('-o', '--output', help="请输入字符画的路径，参数为-0 或者 -output：")
parser.add_argument('-w', '--width', type=int, default=80, help="可通过-w或者--width指定输出字符画的宽度，默认为80")
parser.add_argument('-hi', '--height', type=int, default=80, help="可通过-hi或者--height指定输出字符画的高度，默认为80")

# 获取参数
args = parser.parse_args()
IMG = args.input
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output


class TxTDraw(object):
    """
    项目原理：
    1、将所有像素都转换为字符
    2、为了保证所有像素转换为字符，所以要将图片由三通道转换为单通道。
    """

    def __init__(self):
        # 用于映射的字符集
        self.STR_MAP = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

    def get_char(self, r, g, b, alpha=256):
        """
        将256灰度映射到70个字符上
        :param r: r通道
        :param g: g通道
        :param b: b通道
        :param alpha: 标记透明度的alpha通道
        :return: 要写在文本中的字符
        """
        if alpha == 0:  # 透明的
            return ' '
        # 灰度值公式将像素的 RGB 值映射到灰度值，灰度值范围为 0-255。
        # 整型慢计算比浮点数块（其数值代表权重值，意为人眼对rgb的敏感强度）
        # gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        gray = int(2126 * r + 7152 * g + 722 * b) / 10000

        # 字符集只有,70的映射操作。
        tmp_gray = 256 + 1  # 灰度值范围为 0-255即最大为256，又因为int的退一法操作，所以再加1，
        unit = tmp_gray / len(self.STR_MAP)  # 4
        return self.STR_MAP[int(gray / unit)]

    def draw_pic(self):
        """
        将字符画画出
        :return:字符画字符串
        """
        img = Image.open(IMG)
        img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)

        txt = ""

        for i in range(HEIGHT):
            for j in range(WIDTH):
                txt += self.get_char(*img.getpixel((j, i)))
            # 一行画完，加个换行符。
            txt += '\n'
        return txt

    def write_output(self):
        """
        将字符画字符串写入文件
        :return:字符画字符串
        """
        txt = self.draw_pic()
        # 用于输出文件的命名
        txt_name = os.path.basename(IMG)
        with open(f"./obj_fie/{txt_name.replace('.', '')}.txt", 'w') as f:
            f.write(txt)
        return txt


if __name__ == '__main__':
    obj = TxTDraw()
    print(obj.write_output())

# im.getpixel()以元祖的形式返回32位4通道对应的数值。
# im.resize()重设图片大小，Image.ANTIALIAS ：图片质量（此处为最高质量）
