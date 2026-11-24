import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('documentation/screenshots', exist_ok=True)

def draw_browser_chrome(draw, width, height, title, url):
    # Top browser header
    draw.rectangle([0, 0, width, 50], fill=(241, 245, 249))
    draw.line([(0, 50), (width, 50)], fill=(226, 232, 240), width=1)
    # Window control circles
    draw.ellipse([15, 18, 27, 30], fill=(239, 68, 68))
    draw.ellipse([35, 18, 47, 30], fill=(245, 158, 11))
    draw.ellipse([55, 18, 67, 30], fill=(16, 185, 129))
    # URL bar
    draw.rounded_rectangle([120, 10, width - 120, 40], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    try:
        font_sm = ImageFont.truetype('arial.ttf', 13)
        font_title = ImageFont.truetype('arialbd.ttf', 13)
    except Exception:
        font_sm = ImageFont.load_default()
        font_title = font_sm
    draw.text((140, 18), "🔒 https://mcbconstructions.com" + url, fill=(71, 85, 105), font=font_sm)

def create_screenshot_1_public():
    w, h = 1200, 750
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, w, h, "MCB - Home", "/")

    # Hero background
    draw.rectangle([0, 51, w, 400], fill=(15, 23, 42))
    # Overlay accent house visual
    house_path = 'static/images/portfolio_project_1.png'
    if os.path.exists(house_path):
        house_img = Image.open(house_path).resize((500, 320))
        img.paste(house_img, (650, 90))

    try:
        font_h1 = ImageFont.truetype('arialbd.ttf', 28)
        font_p = ImageFont.truetype('arial.ttf', 15)
        font_tag = ImageFont.truetype('arialbd.ttf', 12)
        font_btn = ImageFont.truetype('arialbd.ttf', 14)
    except Exception:
        font_h1 = ImageFont.load_default()
        font_p = font_h1
        font_tag = font_h1
        font_btn = font_h1

    # Hero text
    draw.rounded_rectangle([60, 85, 420, 115], radius=15, fill=(30, 41, 59), outline=(245, 158, 11), width=1)
    draw.text((80, 92), "WARANGAL'S TRUSTED RESIDENTIAL BUILDER", fill=(253, 230, 138), font=font_tag)

    draw.text((60, 135), "MAMATHA CONSTRUCTIONS & BUILDERS", fill=(255, 255, 255), font=font_h1)
    draw.text((60, 175), "Your Dream Home. Planned with Care, Built with Confidence.", fill=(245, 158, 11), font=font_p)
    draw.text((60, 205), "From plot survey to possession - engineered with genuine brand specifications:\nUltraTech cement, 16mm/12mm rebar, Godavari sand, and teakwood joinery.", fill=(203, 213, 225), font=font_p)

    draw.rounded_rectangle([60, 265, 240, 310], radius=8, fill=(217, 119, 6))
    draw.text((85, 278), "Request Consultation", fill=(255, 255, 255), font=font_btn)

    draw.rounded_rectangle([255, 265, 435, 310], radius=8, outline=(255, 255, 255), width=2)
    draw.text((280, 278), "Get Cost Estimate", fill=(255, 255, 255), font=font_btn)

    draw.text((60, 340), "PRIMARY BUILDER: SARGU SANJU | Cell: +91 7386181866", fill=(253, 230, 138), font=font_tag)
    draw.text((60, 360), "Vishwanath Colony, Near Hanuman Temple, Shambunipet, Warangal", fill=(148, 163, 184), font=font_p)

    # Trust stats bar
    draw.rectangle([0, 451, w, 520], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((100, 470), "15+ Completed Projects", fill=(15, 23, 42), font=font_tag)
    draw.text((380, 470), "UltraTech & TMT Rebar Guaranteed", fill=(217, 119, 6), font=font_tag)
    draw.text((680, 470), "IS 456:2000 Civil Standards", fill=(16, 185, 129), font=font_tag)
    draw.text((950, 470), "AI Daily Site Diary & Expenses", fill=(2, 132, 199), font=font_tag)

    # Featured Project thumbnails
    draw.text((60, 545), "FEATURED REAL PORTFOLIO PROJECTS (WARANGAL)", fill=(15, 23, 42), font=font_h1)
    for i in range(4):
        x = 60 + i * 275
        draw.rounded_rectangle([x, 585, x + 255, 720], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        sub_img_path = f'static/images/portfolio_project_{i+2}.jpg'
        if os.path.exists(sub_img_path):
            sub_p = Image.open(sub_img_path).resize((253, 90))
            img.paste(sub_p, (x + 1, 586))
        draw.text((x + 10, 685), f"MCB Residence {i+1}", fill=(15, 23, 42), font=font_tag)
        draw.text((x + 10, 702), "G+1 Contemporary Villa", fill=(100, 116, 139), font=font_tag)

    img.save('documentation/screenshots/01_public_landing_page.png')
    print("Generated: documentation/screenshots/01_public_landing_page.png")

def create_screenshot_2_dashboard():
    w, h = 1200, 750
    img = Image.new('RGB', (w, h), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, w, h, "MCB Executive Dashboard", "/dashboard")

    # Left Sidebar
    draw.rectangle([0, 51, 240, h], fill=(11, 17, 32))
    logo_path = 'static/images/mcb_logo.png'
    if os.path.exists(logo_path):
        l_img = Image.open(logo_path).resize((210, 50))
        img.paste(l_img, (15, 65))

    try:
        font_nav = ImageFont.truetype('arial.ttf', 13)
        font_h1 = ImageFont.truetype('arialbd.ttf', 20)
        font_card_val = ImageFont.truetype('arialbd.ttf', 24)
        font_card_lbl = ImageFont.truetype('arialbd.ttf', 11)
        font_sm = ImageFont.truetype('arial.ttf', 11)
    except Exception:
        font_nav = ImageFont.load_default()
        font_h1 = font_nav
        font_card_val = font_nav
        font_card_lbl = font_nav
        font_sm = font_nav

    nav_items = ["Dashboard", "Project Management", "Site Diary & Expenses", "AI Cost Estimator", "Material Forecast (ML)", "Site Progress & Vision", "Material Inventory", "Workforce & Labour", "Weather Telemetry", "AI Assistant Chatbot"]
    for idx, item in enumerate(nav_items):
        y = 135 + idx * 36
        if idx == 0:
            draw.rectangle([0, y - 5, 240, y + 25], fill=(30, 41, 59))
            draw.rectangle([0, y - 5, 4, y + 25], fill=(245, 158, 11))
        draw.text((30, y), item, fill=(255, 255, 255) if idx == 0 else (203, 213, 225), font=font_nav)

    # Topbar
    draw.rectangle([240, 51, w, 110], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((270, 68), "Executive Construction Dashboard", fill=(15, 23, 42), font=font_h1)
    draw.text((270, 92), "Builder: SARGU SANJU | Warangal Headquarters | AI-Enabled Telemetry", fill=(100, 116, 139), font=font_sm)

    # KPI Cards
    kpis = [
        ("TOTAL PROJECTS", "5 Projects", "2 Active | 1 Delayed", (245, 158, 11)),
        ("BUDGET COMMITTED", "₹2.38 Cr", "Spent: ₹1.34 Cr (56%)", (2, 132, 199)),
        ("MATERIAL INVENTORY", "23 Items", "Stock Healthy (Val: ₹17.8L)", (16, 185, 129)),
        ("WORKFORCE ON SITE", "9 / 10 Active", "Attendance Rate: 90%", (147, 51, 234))
    ]
    for i, (title, val, sub, col) in enumerate(kpis):
        x = 270 + i * 225
        draw.rounded_rectangle([x, 130, x + 210, 215], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.rectangle([x, 130, x + 4, 215], fill=col)
        draw.text((x + 16, 142), title, fill=(100, 116, 139), font=font_card_lbl)
        draw.text((x + 16, 160), val, fill=(15, 23, 42), font=font_card_val)
        draw.text((x + 16, 192), sub, fill=(71, 85, 105), font=font_sm)

    # Mid Section: Charts preview
    draw.rounded_rectangle([270, 235, 780, 480], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((290, 250), "Budget vs Actual Expenditure (Lakhs ₹)", fill=(15, 23, 42), font=font_card_lbl)
    # Draw sample chart bars
    projects = [("Sargu Villa", 68, 44), ("Vishwanath", 38, 37), ("Hanamkonda", 55, 18), ("Kazipet", 45, 32), ("Fort View", 32, 2.5)]
    for i, (pname, bgt, act) in enumerate(projects):
        bx = 310 + i * 90
        # Budget bar
        h_bgt = int(bgt * 2.2)
        draw.rectangle([bx, 440 - h_bgt, bx + 28, 440], fill=(30, 41, 59))
        # Actual bar
        h_act = int(act * 2.2)
        draw.rectangle([bx + 32, 440 - h_act, bx + 60, 440], fill=(234, 88, 12))
        draw.text((bx, 450), pname, fill=(100, 116, 139), font=font_sm)

    # Delay Risk & Weather Box
    draw.rounded_rectangle([800, 235, 1170, 480], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((820, 250), "Live Weather Telemetry & Delay Risk", fill=(15, 23, 42), font=font_card_lbl)
    draw.text((820, 275), "Warangal: 31.0°C | Humidity: 52% | Rain: 15%", fill=(217, 119, 6), font=font_sm)
    draw.rounded_rectangle([820, 298, 1150, 340], radius=6, fill=(220, 252, 231))
    draw.text((830, 310), "IS 456 Advisory: Favorable for slab pour & curing.", fill=(21, 128, 61), font=font_sm)

    draw.text((820, 355), "ML DELAY RISK CLASSIFIER (GradientBoosting):", fill=(15, 23, 42), font=font_card_lbl)
    risks = [("Sargu Sanju Villa", "78% Complete", "On Track", (16, 185, 129)),
             ("Kazipet Urban Duplex", "62% Complete", "Moderate Risk", (245, 158, 11)),
             ("Hanamkonda Elevation", "35% Complete", "On Track", (16, 185, 129))]
    for i, (p, comp, r_lbl, col) in enumerate(risks):
        y = 380 + i * 30
        draw.text((820, y), p, fill=(15, 23, 42), font=font_sm)
        draw.text((1000, y), comp, fill=(100, 116, 139), font=font_sm)
        draw.rounded_rectangle([1080, y - 2, 1150, y + 16], radius=4, fill=col)
        draw.text((1085, y), r_lbl, fill=(255, 255, 255), font=font_sm)

    # Bottom Recent Site Diary Preview
    draw.rounded_rectangle([270, 500, 1170, 720], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((290, 515), "RECENT SITE DIARY & DAILY EXPENSES (ON-SITE PETTY CASH LOGS)", fill=(15, 23, 42), font=font_card_lbl)
    logs = [
        ("2026-11-24", "Sargu Sanju Villa", "Cast 6 RCC columns with UltraTech 53 grade, M25 mix. Water curing initiated.", "₹2,850.00", "Rajesh Varma (Eng)"),
        ("2026-11-23", "Sargu Sanju Villa", "Shuttering & rebar inspection for level 2 beams. Diesel & binding wire purchased.", "₹4,750.00", "Rajesh Varma (Eng)")
    ]
    for i, (dt, prj, desc, exp, eng) in enumerate(logs):
        y = 545 + i * 75
        draw.text((290, y), f"📅 {dt} | {prj} | Engineer: {eng}", fill=(217, 119, 6), font=font_sm)
        draw.text((290, y + 20), desc, fill=(15, 23, 42), font=font_sm)
        draw.text((1040, y + 10), f"Petty Exp: {exp}", fill=(220, 38, 38), font=font_card_lbl)
        draw.line([(290, y + 55), (1150, y + 55)], fill=(241, 245, 249), width=1)

    img.save('documentation/screenshots/02_executive_admin_dashboard.png')
    print("Generated: documentation/screenshots/02_executive_admin_dashboard.png")

def create_screenshot_3_site_diary():
    w, h = 1200, 750
    img = Image.new('RGB', (w, h), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    draw_browser_chrome(draw, w, h, "MCB Site Diary Tool", "/site-diary")

    try:
        font_h1 = ImageFont.truetype('arialbd.ttf', 20)
        font_sub = ImageFont.truetype('arial.ttf', 13)
        font_bold = ImageFont.truetype('arialbd.ttf', 12)
        font_sm = ImageFont.truetype('arial.ttf', 11)
    except Exception:
        font_h1 = ImageFont.load_default()
        font_sub = font_h1
        font_bold = font_h1
        font_sm = font_h1

    # Header
    draw.rounded_rectangle([60, 75, w - 60, 140], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((80, 88), "ON-SITE CONSTRUCTION DAILY DIARY & PETTY EXPENSE TOOL", fill=(15, 23, 42), font=font_h1)
    draw.text((80, 115), "Dedicated mobile-responsive site diary to record daily progress, challenges, and track petty cash expenses.", fill=(100, 116, 139), font=font_sub)

    # Diary Log Entry Card
    draw.rounded_rectangle([60, 160, w - 60, 710], radius=12, fill=(255, 255, 255), outline=(217, 119, 6), width=2)
    draw.rectangle([60, 160, 68, 710], fill=(217, 119, 6))

    # Top metadata
    draw.text((90, 180), "Log Reference: MCB-SD-01 | Project: Sargu Sanju Villa (MCB-2026-01)", fill=(15, 23, 42), font=font_bold)
    draw.text((90, 202), "Date: 2026-11-24 | Shift: Day Shift | Weather: Clear & Sunny (31.5°C) | Workers Deployed: 9", fill=(100, 116, 139), font=font_sm)

    draw.rounded_rectangle([920, 175, 1110, 220], radius=6, fill=(254, 242, 242), outline=(239, 68, 68), width=1)
    draw.text((930, 185), "DAILY ON-SITE EXPENSE:", fill=(153, 27, 27), font=font_sm)
    draw.text((930, 200), "₹4,750.00", fill=(185, 28, 28), font=font_h1)

    # Work carried out
    draw.text((90, 245), "CONSTRUCTION WORK CARRIED OUT:", fill=(15, 23, 42), font=font_bold)
    draw.rounded_rectangle([90, 268, 680, 360], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    work_text = (
        "• Completed shuttering and rebar inspection for second floor beams.\n"
        "• Mixed and poured M25 grade concrete for 6 columns using UltraTech 53 grade and Godavari sand.\n"
        "• Initiated continuous water ponding curing on first floor slabs (14-day schedule).\n"
        "• Minor morning sand tractor delay resolved by 9:30 AM."
    )
    draw.text((105, 280), work_text, fill=(30, 41, 59), font=font_sm)

    # Petty Expense Table
    draw.text((710, 245), "ITEMIZED ON-SITE PETTY EXPENSES BREAKDOWN:", fill=(15, 23, 42), font=font_bold)
    draw.rounded_rectangle([710, 268, 1110, 520], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rectangle([710, 268, 1110, 298], fill=(241, 245, 249))
    draw.text((720, 278), "Item Description", fill=(71, 85, 105), font=font_bold)
    draw.text((920, 278), "Category", fill=(71, 85, 105), font=font_bold)
    draw.text((1040, 278), "Amount (₹)", fill=(71, 85, 105), font=font_bold)

    items = [
        ("Worker tea & snacks (9 workers)", "Food/Beverage", "₹360.00"),
        ("Binding wire 10kg & nails", "Hardware", "₹1,250.00"),
        ("Tractor unloading coolie", "Labor Help", "₹800.00"),
        ("Diesel 20L for generator", "Fuel", "₹1,940.00"),
        ("First aid cream & bandage", "Safety", "₹400.00")
    ]
    for i, (itm, cat, amt) in enumerate(items):
        y = 312 + i * 36
        draw.text((720, y), itm, fill=(15, 23, 42), font=font_sm)
        draw.text((920, y), cat, fill=(100, 116, 139), font=font_sm)
        draw.text((1040, y), amt, fill=(185, 28, 28), font=font_bold)
        draw.line([(710, y + 25), (1110, y + 25)], fill=(241, 245, 249), width=1)

    # Photos preview
    draw.text((90, 385), "SITE PHOTO EVIDENCE ATTACHED:", fill=(15, 23, 42), font=font_bold)
    for i in range(2):
        px = 90 + i * 220
        p_path = f'static/images/portfolio_project_{i+1}.png' if i == 0 else f'static/images/portfolio_project_{i+1}.jpg'
        if os.path.exists(p_path):
            p_img = Image.open(p_path).resize((200, 120))
            img.paste(p_img, (px, 410))

    # Attestation Signatures
    draw.line([(90, 560), (1110, 560)], fill=(226, 232, 240), width=1)
    draw.text((90, 580), "PREPARED & ATTESTED BY:", fill=(100, 116, 139), font=font_sm)
    draw.text((90, 600), "Rajesh Varma (B.Tech Civil - Site Engineer)", fill=(15, 23, 42), font=font_bold)

    draw.text((800, 580), "VERIFIED & APPROVED BY:", fill=(100, 116, 139), font=font_sm)
    draw.text((800, 600), "SARGU SANJU (Chief Builder & Proprietor)", fill=(217, 119, 6), font=font_bold)
    draw.text((800, 620), "Mamatha Constructions & Builders, Warangal", fill=(100, 116, 139), font=font_sm)

    img.save('documentation/screenshots/06_site_diary_daily_expenses.png')
    print("Generated: documentation/screenshots/06_site_diary_daily_expenses.png")

if __name__ == '__main__':
    create_screenshot_1_public()
    create_screenshot_2_dashboard()
    create_screenshot_3_site_diary()
