import os
from PIL import Image, ImageDraw, ImageFont

def generate_logo():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 120" width="520" height="120">
  <defs>
    <linearGradient id="gradBrand" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f59e0b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ea580c;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradDark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e293b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f172a;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Architectural Icon -->
  <g transform="translate(15, 10)">
    <rect x="0" y="0" width="95" height="95" rx="16" fill="url(#gradDark)" stroke="#f59e0b" stroke-width="2" />
    <!-- Building geometric towers -->
    <path d="M20 75 L20 45 L38 30 L56 45 L56 75 Z" fill="none" stroke="#f8fafc" stroke-width="3" stroke-linejoin="round" />
    <path d="M42 75 L42 22 L62 8 L80 22 L80 75 Z" fill="none" stroke="url(#gradBrand)" stroke-width="3.5" stroke-linejoin="round" />
    <line x1="28" y1="52" x2="32" y2="52" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" />
    <line x1="28" y1="62" x2="32" y2="62" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" />
    <line x1="66" y1="32" x2="70" y2="32" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />
    <line x1="66" y1="45" x2="70" y2="45" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />
    <line x1="66" y1="58" x2="70" y2="58" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" />
    <!-- Foundation line & beam -->
    <line x1="12" y1="75" x2="84" y2="75" stroke="#f59e0b" stroke-width="3.5" stroke-linecap="round" />
    <circle cx="62" cy="8" r="3.5" fill="#f59e0b" />
  </g>

  <!-- Typography -->
  <text x="125" y="44" font-family="'Segoe UI', Inter, Arial, sans-serif" font-size="30" font-weight="900" letter-spacing="1.5" fill="#0f172a">
    MCB <tspan fill="#ea580c">CONSTRUCTIONS</tspan>
  </text>
  <text x="127" y="70" font-family="'Segoe UI', Inter, Arial, sans-serif" font-size="13" font-weight="700" letter-spacing="2.5" fill="#475569">
    MAMATHA CONSTRUCTIONS &amp; BUILDERS
  </text>
  <text x="127" y="92" font-family="'Segoe UI', Inter, Arial, sans-serif" font-size="11" font-weight="600" letter-spacing="1.2" fill="#d97706">
    BUILDER: SARGU SANJU | WARANGAL
  </text>
</svg>"""

    os.makedirs('static/images', exist_ok=True)
    with open('static/images/mcb_logo.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)

    img = Image.new('RGBA', (520, 120), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Background icon
    draw.rounded_rectangle([15, 12, 110, 107], radius=16, fill=(15, 23, 42, 255), outline=(245, 158, 11, 255), width=2)
    # Draw buildings
    draw.line([(35, 85), (35, 55), (53, 40), (71, 55), (71, 85)], fill=(248, 250, 252, 255), width=3)
    draw.line([(57, 85), (57, 32), (77, 18), (95, 32), (95, 85)], fill=(234, 88, 12, 255), width=4)
    draw.line([(27, 85), (99, 85)], fill=(245, 158, 11, 255), width=4)

    try:
        font_bold = ImageFont.truetype('arialbd.ttf', 30)
        font_sub = ImageFont.truetype('arialbd.ttf', 13)
        font_tag = ImageFont.truetype('arial.ttf', 11)
    except Exception:
        font_bold = ImageFont.load_default()
        font_sub = font_bold
        font_tag = font_bold

    draw.text((125, 18), 'MCB ', fill=(15, 23, 42, 255), font=font_bold)
    draw.text((200, 18), 'CONSTRUCTIONS', fill=(234, 88, 12, 255), font=font_bold)
    draw.text((127, 56), 'MAMATHA CONSTRUCTIONS & BUILDERS', fill=(71, 85, 105, 255), font=font_sub)
    draw.text((127, 80), 'BUILDER: SARGU SANJU | WARANGAL', fill=(217, 119, 6, 255), font=font_tag)

    img.save('static/images/mcb_logo.png')
    print('Generated static/images/mcb_logo.svg and static/images/mcb_logo.png')

if __name__ == '__main__':
    generate_logo()
