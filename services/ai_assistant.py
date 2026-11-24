import re
import json
from datetime import datetime
from database.db import get_db_connection

# Comprehensive Construction Knowledge Base (Bilingual EN + TE)
KNOWLEDGE_BASE = {
    "mcb_profile": {
        "keywords": ["builder", "sanju", "sargu sanju", "mcb", "mamatha", "contact", "address", "phone", "నాయకుడు", "సంప్రదించండి", "వరంగల్"],
        "response_en": (
            "**MAMATHA CONSTRUCTIONS & BUILDERS (MCB)** is a premier residential construction firm based in Warangal, Telangana.\n"
            "• **Primary Builder:** SARGU SANJU\n"
            "• **Office Address:** Vishwanath Colony, Near Hanuman Temple, Shambunipet, Warangal, Telangana\n"
            "• **Direct Phone:** +91 7386181866\n"
            "• **Service Coverage:** Warangal, Hanamkonda, Kazipet and nearby regions.\n"
            "We handle complete house construction from plot survey, architectural planning, RCC frame, premium finishing, to final handover with documented quality control."
        ),
        "response_te": (
            "**మమత కన్‌స్ట్రక్షన్స్ అండ్ బిల్డర్స్ (MCB)** — వరంగల్:\n"
            "• **ప్రధాన బిల్డర్:** సర్గూ సంజు (SARGU SANJU)\n"
            "• **చిరునామా:** విశ్వనాథ్ కాలనీ, హనుమాన్ టెంపుల్ దగ్గర, శంభునిపేట, వరంగల్, తెలంగాణ.\n"
            "• **ఫోన్ నంబర్:** 7386181866\n"
            "స్థలం ఎంపిక నుంచి ప్లానింగ్, పిల్లర్లు, స్లాబ్, టైల్స్, రంగులు వేసి ఇంటి తాళాలు ఇచ్చే వరకు నాణ్యతతో నిర్మిస్తాము."
        )
    },
    "cement_specs": {
        "keywords": ["cement", "ultratech", "grade", "opc", "ppc", "సిమెంట్", "ఆల్ట్రా టెక్", "అల్ట్రాటెక్"],
        "response_en": (
            "**MCB Approved Cement Specifications:**\n"
            "• **Brand:** UltraTech Cement (Official specification from MCB Agreement Sheet).\n"
            "• **Grade:** UltraTech OPC 53 Grade for RCC footings, columns, beams, and 5-inch slabs.\n"
            "• **PPC:** UltraTech Super / Weather Plus for brick masonry and external plastering.\n"
            "• **Rule of Thumb:** Approx. 0.40 to 0.45 bags per sq.ft of built-up area.\n"
            "• **Curing Requirement:** Minimum 14 days continuous water curing for RCC slabs (IS 456 standard)."
        ),
        "response_te": (
            "**సిమెంట్ వివరాలు (MCB అగ్రిమెంట్ ప్రకారం):**\n"
            "• **బ్రాండ్:** ఆల్ట్రా టెక్ సిమెంట్ (UltraTech Cement).\n"
            "• పిల్లర్లు, బీమ్స్ మరియు 5 అంగుళాల స్లాబ్ కోసం OPC 53 గ్రేడ్ లేదా RMC మిల్లర్ మిక్స్ వాడతాము.\n"
            "• ఇటుక గోడల కట్టుబడి మరియు ప్లాస్టరింగ్ కోసం PPC వాడబడుతుంది.\n"
            "• సగటున చదరపు అడుగుకి 0.42 సిమెంట్ బస్తాలు అవసరం."
        )
    },
    "steel_specs": {
        "keywords": ["steel", "tmt", "rebar", "16mm", "12mm", "pillar", "స్టీల్", "సలాక", "పిల్లర్", "కడ్డీలు"],
        "response_en": (
            "**MCB Approved Steel & Rebar Specifications:**\n"
            "• **Pillar Dimensions:** 9 inches × 14 inches standard RCC columns.\n"
            "• **Main Rebar:** 16mm TMT (4 vertical bars per pillar) combined with 12mm TMT (4 bars) Fe550D grade as detailed in the builder agreement.\n"
            "• **Slab Thickness:** 5 Inches (cast using RMC Miller / Machine Mix).\n"
            "• **Standard Quantity:** Approx. 3.5 to 4.2 kg of steel per sq.ft of built-up area.\n"
            "• **Brands:** TATA Tiscon, Jindal Panther, Vizag Steel (all with Mill Test Certificates)."
        ),
        "response_te": (
            "**స్టీల్ వివరాలు (MCB అగ్రిమెంట్ షీట్ ప్రకారం):**\n"
            "• **పిల్లర్స్ కొలత:** 9/14 అంగుళాలు.\n"
            "• **సలాక పేర్లు:** 16mm TMT (పిల్లర్‌కి 4 బార్లు) మరియు 12mm TMT (4 బార్లు).\n"
            "• **స్లాబ్ మందం:** 5 అంగుళాలు (మిల్లర్/మెషిన్ మిక్స్).\n"
            "• నాణ్యమైన TATA Tiscon / Jindal Panther స్టీల్ మాత్రమే ఉపయోగిస్తాము."
        )
    },
    "plumbing_specs": {
        "keywords": ["plumbing", "pipe", "sudhakar", "ashirvad", "tap", "drainage", "ప్లంబింగ్", "పైపులు", "సుధాకర్", "ఆశీర్వాద్"],
        "response_en": (
            "**MCB Plumbing & Sanitary Specifications:**\n"
            "• **Pipes:** Ashirvad CPVC for hot/cold internal water supply; Sudhakar PVC for SWR drainage and rainwater downpipes.\n"
            "• **Fittings:** Cera / Western commodes and Indian taps, brass wall mixer in all master bathrooms.\n"
            "• **Overhead Tank:** 1,000 Litres triple-layer UV-stabilized tank (Sintex / Supreme).\n"
            "• **Quality Checks:** 100 psi hydraulic pressure leak testing before concealing plumbing chases."
        ),
        "response_te": (
            "**ప్లంబింగ్ సామగ్రి:**\n"
            "• **పైపులు:** ఆశీర్వాద్ పైపులు (Ashirvad Pipes) మరియు సుధాకర్ పైపులు (Sudhakar Pipes).\n"
            "• **ఫిట్టింగ్స్:** వెస్ట్రన్ / ఇండియన్ ట్యాప్స్, వాల్ మిక్సర్ (Wall Mixer).\n"
            "• **ఓవర్‌హెడ్ ట్యాంక్:** 1000 లీటర్ల ట్రిపుల్ లేయర్ ట్యాంక్."
        )
    },
    "electrical_specs": {
        "keywords": ["electrical", "current", "wire", "switch", "finolex", "goldmedal", "కరెంట్", "వైరింగ్", "స్విచ్", "ఫినోలెక్స్"],
        "response_en": (
            "**MCB Electrical Specifications:**\n"
            "• **Wires:** Finolex Flame Retardant (FR) multi-strand copper wires (1.5 sq mm for lighting, 2.5 sq mm for power points, 4.0 sq mm for AC/Geyser).\n"
            "• **Switches & Plates:** Goldmedal modular switches with safety child-shutter sockets.\n"
            "• **Distribution:** Dedicated MCB/ELCB distribution board with proper copper plate earthing pit."
        ),
        "response_te": (
            "**కరెంట్ & వైరింగ్ వివరాలు:**\n"
            "• **వైరింగ్:** ఫినోలెక్స్ వైర్ (Finolex Flame Retardant Wires).\n"
            "• **స్విచ్‌లు:** గోల్డ్ మెడల్ మాడ్యులర్ స్విచ్‌లు (Goldmedal Switches).\n"
            "• ప్రతి బెడ్‌రూమ్, హాల్‌లో తగినన్ని పాయింట్లు, AC లైన్లు మరియు అర్తింగ్ సౌకర్యం."
        )
    },
    "doors_windows_flooring": {
        "keywords": ["wood", "door", "window", "marble", "granite", "tile", "upvc", "వుడ్", "తలుపులు", "కిటికీలు", "మార్బుల్", "టైల్స్", "గ్రానైట్"],
        "response_en": (
            "**Wood, Openings & Flooring Specifications (From MCB Agreement):**\n"
            "• **Frames:** 2nd Quality wood frames; **Main Door:** 1st Quality solid Teakwood (చెక్క).\n"
            "• **Bedroom Doors:** 1st quality Lamination PVC flush doors.\n"
            "• **Bathroom Doors:** WPVC 100% waterproof doors.\n"
            "• **Windows:** UPVC sliding frames with insect mesh.\n"
            "• **Flooring:** Parking tiles at ₹70/sqft, Kitchen Granite at ₹100/sqft, and Wall tiles (Bathroom/Kitchen/Puja room) at ₹250/box."
        ),
        "response_te": (
            "**వుడ్, కిటికీలు & ఫ్లోరింగ్ (అగ్రిమెంట్ ప్రకారం):**\n"
            "• **మెయిన్ డోర్:** ఫస్ట్ క్వాలిటీ చెక్క (Teakwood), ఫ్రేమ్ సెకండ్ క్వాలిటీ.\n"
            "• **బెడ్‌రూమ్ డోర్స్:** లామినేషన్ డోర్స్ (PVC).\n"
            "• **బాత్‌రూమ్ డోర్స్:** WPVC వాటర్‌ప్రూఫ్ డోర్స్.\n"
            "• **కిటికీలు:** UPVC స్లైడింగ్ విండోస్.\n"
            "• **టైల్స్/గ్రానైట్:** పార్కింగ్ టైల్స్ ₹70/sqft, కిచెన్ గ్రానైట్ ₹100/sqft, బాత్‌రూమ్/పూజ గది టైల్స్ ₹250/బాక్స్."
        )
    },
    "finishing_specs": {
        "keywords": ["paint", "putty", "pop", "ceiling", "grill", "railing", "రంగులు", "పుట్టీ", "సీలింగ్", "గ్రిల్స్", "రైలింగ్"],
        "response_en": (
            "**Finishing, Ceiling & Painting Specifications:**\n"
            "• **Ceiling:** POP (Plaster of Paris) designer false ceiling in living & dining halls.\n"
            "• **Wall Putty:** J.K. / Birla White Wall Putty (2 smooth leveling coats).\n"
            "• **Paints:** Asian Paints (Apex Ultima exterior weather-proof & Royale luxury interior).\n"
            "• **Grills & Gate:** Mild steel iron safety grills and modern architectural entrance gate.\n"
            "• **Staircase:** Stainless Steel (SS 304) designer handrail."
        ),
        "response_te": (
            "**ఫినిషింగ్, పెయింట్ & సీలింగ్:**\n"
            "• **సీలింగ్:** POP ఫాల్స్ సీలింగ్.\n"
            "• **పుట్టీ:** J.K. / బిర్లా వైట్ పుట్టీ.\n"
            "• **రంగులు:** ఏషియన్ పెయింట్స్ (Asian Paints).\n"
            "• **గ్రిల్స్ & గేట్:** ఐరన్ గ్రిల్స్ మరియు మెయిన్ గేట్.\n"
            "• **మెట్ల రైలింగ్:** స్టెయిన్‌లెస్ స్టీల్ రైలింగ్."
        )
    },
    "cost_estimation": {
        "keywords": ["cost", "estimate", "budget", "price", "rate", "sqft", "ఎంత", "ధర", "ఖర్చు", "బడ్జెట్"],
        "response_en": (
            "**Construction Cost Structure (Warangal 2026 Rates):**\n"
            "• **Standard Quality:** ₹1,750 – ₹1,900 / sq.ft (Class-1 brick, UltraTech cement, Fe550D rebar, standard ceramic tiles).\n"
            "• **Premium Quality (MCB Standard):** ₹2,100 – ₹2,400 / sq.ft (Teakwood main door, Granite counter, UPVC windows, Asian Paints Apex, POP ceiling).\n"
            "• **Luxury Quality:** ₹2,600 – ₹3,200 / sq.ft (Double elevation styling, imported marble, solar power, smart home provisions).\n"
            "Try our interactive **Cost Estimator** tool in the menu for an instant breakdown based on your plot and built-up area!"
        ),
        "response_te": (
            "**ఇంటి నిర్మాణ ఖర్చు అంచనా (వరంగల్ 2026):**\n"
            "• **ప్రీమియం నిర్మాణం (MCB స్టాండర్డ్):** చదరపు అడుగుకి సుమారు ₹2,100 నుండి ₹2,400 వరకు ఉంటుంది.\n"
            "• ఇందులో పిల్లర్లు, 5 అంగుళాల స్లాబ్, టేకు మెయిన్ డోర్, UPVC కిటికీలు, కిచెన్ గ్రానైట్, POP సీలింగ్, ఏషియన్ పెయింట్స్ అన్నీ చేర్చబడి ఉంటాయి.\n"
            "ఖచ్చితమైన అంచనా కోసం మన సైట్‌లోని 'Cost Estimator' ఉపయోగించండి."
        )
    },
    "safety_and_standards": {
        "keywords": ["safety", "is code", "curing", "soil", "vastu", "భద్రత", "వాస్తు", "క్యూరింగ్"],
        "response_en": (
            "**Civil Engineering Quality & Safety Standards:**\n"
            "• **Concrete Mix:** Minimum M20/M25 grade design mix as per IS 456:2000.\n"
            "• **Curing Period:** Continuous water curing for at least 14 days for slabs and columns to achieve 99% design compressive strength.\n"
            "• **Vastu Integration:** East/North entry alignment, Northeast (Ishan) water sump/pooja room, and Southeast (Agneya) kitchen orientation.\n"
            "• **On-Site Safety:** Compulsory PPE helmets, steel-toe boots, and safety netting during upper-floor shuttering."
        ),
        "response_te": (
            "**నాణ్యత మరియు భద్రతా ప్రమాణాలు:**\n"
            "• స్లాబ్ పోసిన తర్వాత కనీసం 14 రోజుల పాటు వాటర్ పాండింగ్ (క్యూరింగ్) చేయాలి.\n"
            "• ఈశాన్యంలో సంప్/దేవుని గది, ఆగ్నేయంలో వంటగది ఉండేలా వాస్తు సూచనలు పాటిస్తాము.\n"
            "• నిర్మాణ సమయంలో కార్మికులకు పూర్తి భద్రతా పరికరాలు (హెల్మెట్లు, సేఫ్టీ బెల్టులు) నిర్ధారిస్తాము."
        )
    }
}

def is_telugu_text(text):
    """Detects whether user query contains Telugu Unicode range characters."""
    return any(0x0C00 <= ord(c) <= 0x0C7F for c in text)

def process_chat_message(user_message, session_id="guest", user_id=None):
    """
    Intelligent chatbot engine that matches construction inquiries against the MCB knowledge base,
    detects English vs Telugu language, extracts intent, and records the interaction in SQLite.
    """
    msg_clean = user_message.strip().lower()
    in_telugu = is_telugu_text(user_message)
    
    matched_topic = None
    max_matches = 0
    
    for topic_key, topic_data in KNOWLEDGE_BASE.items():
        matches = sum(1 for kw in topic_data["keywords"] if kw.lower() in msg_clean)
        if matches > max_matches:
            max_matches = matches
            matched_topic = topic_key
            
    if matched_topic:
        data = KNOWLEDGE_BASE[matched_topic]
        response = data["response_te"] if in_telugu else data["response_en"]
        intent = matched_topic
    else:
        intent = "general_query"
        if in_telugu:
            response = (
                "నమస్కారం! నేను **MCB స్మార్ట్ కన్‌స్ట్రక్షన్ అసిస్టెంట్‌ని**. "
                "మీరు ఇల్లు కట్టే విధానం, బడ్జెట్ అంచనా, ఆల్ట్రాటెక్ సిమెంట్, 16mm/12mm TMT స్టీల్, "
                "టేకు తలుపులు, UPVC కిటికీలు, టైల్స్, లేదా బిల్డర్ **సర్గూ సంజు (SARGU SANJU)** గురించి నన్ను అడగవచ్చు. "
                "మీ అవసరాన్ని వివరంగా తెలియజేయండి!"
            )
        else:
            response = (
                "Hello! I am the **MCB Smart AI Construction Assistant**. "
                "You can ask me about our construction processes, estimated costs per square foot, "
                "authentic materials (UltraTech cement, 16mm/12mm TMT steel, Godavari sand, Finolex wiring, Asian Paints), "
                "site safety protocols, or directly contact our builder **SARGU SANJU** at +91 7386181866. "
                "How can I assist your construction planning today?"
            )

    # Save to chat_messages table
    try:
        conn = get_db_connection()
        conn.execute("""
        INSERT INTO chat_messages (user_id, session_id, role, message, intent)
        VALUES (?, ?, 'user', ?, ?);
        """, (user_id, session_id, user_message, intent))
        
        conn.execute("""
        INSERT INTO chat_messages (user_id, session_id, role, message, intent)
        VALUES (?, ?, 'assistant', ?, ?);
        """, (user_id, session_id, response, intent))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Chat logging error: {e}")

    return {
        "reply": response,
        "intent": intent,
        "language": "telugu" if in_telugu else "english",
        "timestamp": datetime.now().strftime('%I:%M %p')
    }
