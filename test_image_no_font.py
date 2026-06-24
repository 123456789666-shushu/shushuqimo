import sys, json, math, random, io
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont

with open("questions.json", encoding="utf-8") as f:
    CONFIG = json.load(f)
ELEMENTS = CONFIG["elements"]
ELEMENT_ORDER = ["水", "火", "风", "土"]

width, height = 800, 600
img = Image.new("RGBA", (width, height), color=(20, 18, 38, 255))
draw = ImageDraw.Draw(img)

# Simulate server: use only default font
font_default = ImageFont.load_default()

try:
    draw.text((width//2, 42), "测试用户 的元素人格", fill=(255,215,0), anchor="mt", font=font_default)
    print("OK: draw.text with default font and anchor")
except Exception as e:
    print(f"ERROR draw.text: {type(e).__name__}: {e}")

try:
    draw.rounded_rectangle([(width//2-160, 82), (width//2+160, 140)], radius=20, fill=(40,40,80), outline=(100,100,180), width=2)
    print("OK: rounded_rectangle")
except Exception as e:
    print(f"ERROR rounded_rectangle: {type(e).__name__}: {e}")

# Test with emoji
try:
    draw.text((30, 200), "💧 水: 79%", fill=(100,100,255), font=font_default)
    print("OK: draw emoji text")
except Exception as e:
    print(f"ERROR emoji text: {type(e).__name__}: {e}")

buf = io.BytesIO()
try:
    img.save(buf, format="PNG")
    print(f"OK: saved PNG, size={len(buf.getvalue())} bytes")
except Exception as e:
    print(f"ERROR save: {type(e).__name__}: {e}")
