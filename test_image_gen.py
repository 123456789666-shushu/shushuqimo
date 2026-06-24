import sys, json, math, random, io
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont

with open("questions.json", encoding="utf-8") as f:
    CONFIG = json.load(f)
ELEMENTS = CONFIG["elements"]
ELEMENT_ORDER = ["水", "火", "风", "土"]

def generate_result_image(nickname, element, scores_vec, compound_name=None):
    width, height = 800, 600
    img = Image.new("RGBA", (width, height), color=(20, 18, 38, 255))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(20 + (40 - 20) * y / height)
        g = int(18 + (20 - 18) * y / height)
        b = int(38 + (80 - 38) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    elem_short = element.split()[-1] if " " in element else element
    elem_color = ELEMENTS[elem_short]["color"]
    ec = tuple(int(elem_color.lstrip("#")[j:j+2], 16) for j in (0, 2, 4))
    for r in range(200, 0, -8):
        alpha = max(0, 8 - (200 - r) // 30)
        draw.ellipse([width//2 - r, 60 - r, width//2 + r, 60 + r], fill=(ec[0], ec[1], ec[2], alpha))
    for _ in range(80):
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        s = random.choice([2, 3, 4])
        a = random.randint(15, 50)
        draw.ellipse([cx, cy, cx + s, cy + s], fill=(255, 255, 255, a))
    try:
        font_title = ImageFont.truetype("simhei.ttf", 36)
        font_subtitle = ImageFont.truetype("simhei.ttf", 24)
        font_text = ImageFont.truetype("simhei.ttf", 20)
        font_small = ImageFont.truetype("simhei.ttf", 16)
        font_badge = ImageFont.truetype("simhei.ttf", 14)
    except BaseException:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_badge = ImageFont.load_default()
    for i in range(width):
        c = int(255 - 200 * abs(i - width/2) / (width/2))
        draw.point((i, 0), fill=(c, 215, 0))
        if 5 < i < width - 5:
            draw.point((i, 1), fill=(c//2, 215//2, 0))
    draw.text((width//2, 42), f"{nickname} 的元素人格", fill=(255,215,0), anchor="mt", font=font_title)
    ec_dark = (ec[0]//6, ec[1]//6, ec[2]//6)
    draw.rounded_rectangle([(width//2-160, 82), (width//2+160, 140)], radius=20, fill=ec_dark, outline=ec, width=2)
    draw.text((width//2, 111), f"✨ 主导元素：{element}", fill=(255,255,255), anchor="mt", font=font_subtitle)
    bar_x, bar_y, bar_w, bar_h = 130, 180, 540, 30
    for i, elem in enumerate(ELEMENT_ORDER):
        info = ELEMENTS[elem]
        pct = int(scores_vec[i] / info["max_score"] * 100)
        y = bar_y + i * 52
        color_hex = info["color"].lstrip("#")
        c_rgb = tuple(int(color_hex[j:j+2], 16) for j in (0, 2, 4))
        draw.text((30, y+5), f"{info['emoji']} {elem}", fill=c_rgb, font=font_text)
        draw.rounded_rectangle([(bar_x, y+4), (bar_x+bar_w+4, y+bar_h+4)], radius=16, fill=(c_rgb[0]//8, c_rgb[1]//8, c_rgb[2]//8))
        draw.rounded_rectangle([(bar_x, y), (bar_x+bar_w, y+bar_h)], radius=14, fill=(c_rgb[0]//5, c_rgb[1]//5, c_rgb[2]//5))
        fill_w = int(bar_w * pct / 100)
        if fill_w > 4:
            for x in range(bar_x, bar_x + fill_w):
                ratio = (x - bar_x) / fill_w
                r2 = int(c_rgb[0] * (0.7 + 0.3 * ratio))
                g2 = int(c_rgb[1] * (0.7 + 0.3 * ratio))
                b2 = int(c_rgb[2] * (0.7 + 0.3 * ratio))
                draw.line([(x, y+2), (x, y+bar_h-2)], fill=(min(r2,255), min(g2,255), min(b2,255)))
            draw.rounded_rectangle([(bar_x, y), (bar_x+fill_w, y+bar_h)], radius=14, fill=None, outline=(255,255,255,40), width=1)
        draw.rounded_rectangle([(bar_x+bar_w+10, y-2), (bar_x+bar_w+60, y+bar_h+2)], radius=12, fill=(c_rgb[0]//3, c_rgb[1]//3, c_rgb[2]//3))
        draw.text((bar_x+bar_w+35, y+bar_h//2), f"{pct}%", fill=c_rgb, anchor="mm", font=font_badge)
    if compound_name:
        draw.rounded_rectangle([(width//2-150, 410), (width//2+150, 455)], radius=16, fill=(40,40,80), outline=(100,100,180), width=1)
        draw.text((width//2, 432), f"🧬 {compound_name}", fill=(200,200,255), anchor="mt", font=font_text)
    for i in range(width):
        c = int(100 - 80 * abs(i - width/2) / (width/2))
        draw.point((i, height-3), fill=(c, c, c+40))
    draw.text((width//2, height-16), "生成于 元素人格测试仪", fill=(100,100,140), anchor="mb", font=font_small)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

data = generate_result_image("测试用户", "💧 水", [55, 30, 25, 40], "蒸汽")
print(f"Image generated: {len(data)} bytes")
with open("test_image.png", "wb") as f:
    f.write(data)
print("Saved to test_image.png")
