from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route('/add_watermark', methods=['POST'])
def add_watermark():
    file = request.files['image']
    image = Image.open(file.stream).convert('RGBA')
    width, height = image.size

    watermark_text = "@JAMALOZH"
    font_path = "Roboto-Regular.ttf"
    font_size = int(width / 4)

    # Проверяем, есть ли шрифт
    if not os.path.isfile(font_path):
        return f"❌ Font file not found: {font_path}", 500

    # Загружаем шрифт
    font = ImageFont.truetype(font_path, font_size)

    # Создаём прозрачный слой
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)

    text_width, text_height = draw.textsize(watermark_text, font)
    x_spacing = text_width + 50
    y_spacing = text_height + 50

    for y in range(0, height, y_spacing):
        for x in range(0, width, x_spacing):
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 100))

    watermarked = Image.alpha_composite(image, txt)

    img_byte_arr = io.BytesIO()
    watermarked.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(port=5001)
