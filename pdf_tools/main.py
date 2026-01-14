import logging
import sys

import PyPDF2
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from fontTools.ttLib import TTFont

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def otf_to_ttf(otf_path, ttf_path):
    try:
        # 读取 .otf 文件
        font = TTFont(otf_path)

        # 将 .otf 文件转换为 .ttf 文件
        font.saveXML("temp.xml")  # 保存为 XML 文件
        ttf_font = TTFont(recalcBBoxes=False, recalcTimestamp=False)
        ttf_font.importXML("temp.xml")
        ttf_font.save(ttf_path)

        # 删除临时文件
        import os
        os.remove("temp.xml")

        logger.info(f"Converted {otf_path} to {ttf_path}")
    except Exception as e:
        logger.error(f"Error converting {otf_path} to {ttf_path}: {e}")
        raise



def add_watermark_img(input_pdf, output_pdf, watermark_image_path, x=200, y=400, opacity=0.3):
    # 创建 PDF 读取器
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # 获取第一个页面的尺寸
    page_width = reader.pages[0].mediabox.width
    page_height = reader.pages[0].mediabox.height

    # 创建一个空白页面用于水印
    watermark_page = PageObject.create_blank_page(width=page_width, height=page_height)

    # 添加图片水印
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    img = ImageReader(watermark_image_path)
    img_width = int(img.getSize()[0] * opacity)
    img_height = int(img.getSize()[1] * opacity)
    can.drawImage(img, x, int(page_height - img_width - y), width=img_width, height=img_height, mask='auto')
    can.save()

    # 从内存中读取水印页面
    packet.seek(0)
    new_pdf = PdfReader(packet)
    watermark_page.merge_page(new_pdf.pages[0])

    # 合并每个页面
    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    # 写入输出文件
    try:
        with open(output_pdf, 'wb') as f:
            writer.write(f)
    except IOError as e:
        print(f"Error writing to file: {e}")

def add_watermark_font(input_pdf, output_pdf, watermark_text, font_path='font.ttf', font_size=30, alpha=0.3, x=200, y=400):
    # 加载自定义字体
    pdfmetrics.registerFont(TTFont('Font', font_path))

    # 创建 PDF 读取器
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # 获取第一个页面的尺寸
    page_width = reader.pages[0].mediabox.width
    page_height = reader.pages[0].mediabox.height
    print(page_width, page_height)

    # 创建一个空白页面用于水印
    watermark_page = PageObject.create_blank_page(width=page_width, height=page_height)

    # 添加水印文本
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    can.setFont('Font', font_size)
    can.setFillColorRGB(0, 0, 0, alpha)
    can.drawString(x, y, watermark_text)
    can.save()

    # 从内存中读取水印页面
    packet.seek(0)
    new_pdf = PdfReader(packet)
    watermark_page.merge_page(new_pdf.pages[0])

    # 合并每个页面
    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    # 写入输出文件
    try:
        with open(output_pdf, 'wb') as f:
            writer.write(f)
    except IOError as e:
        print(f"Error writing to file: {e}")


if __name__ == '__main__':

    # argv[0]是脚本名称，argv[1]开始才是传入的参数
    print('Script name:', sys.argv[0])
    params = sys.argv[1:]
    for i, arg in enumerate(sys.argv[1:]):
        print(f'Argument {i + 1}:', arg)

    # 使用示例
    input_pdf_path = params[0]  # 输入的PDF文件路径
    # output_pdf_path = params[2]  # 输出的PDF文件路径
    output_pdf_img_path = params[2]  # 输出的PDF文件路径
    # watermark_text = "哈哈哈"  # 水印文字
    # add_watermark_font(input_pdf_path, output_pdf_path, watermark_text)

    add_watermark_img(input_pdf_path, output_pdf_img_path, params[1], x=10, y=10, opacity=0.2)

    # otf_to_ttf('a.otf', 'a.ttf')
