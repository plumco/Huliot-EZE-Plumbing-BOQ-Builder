# ═══════════════════════════════════════════════════════════════
#  Huliot EZE Plumbing BOQ Builder  |  Streamlit App
#  Huliot Pipes & Fittings Pvt. Ltd. | Price List W.E.F April 2026
# ═══════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

# ─── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="Huliot EZE BOQ Builder",
    page_icon="⚙️",
    layout="wide",
    menu_items={"About": "Huliot EZE BOQ Builder | W.E.F April 2026"}
)

# ─── CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background:#EEF2F7; }
.block-container { padding-top:1.2rem; padding-bottom:1rem; max-width:1440px; }
.stTabs [data-baseweb="tab"] { font-weight:700; font-size:14px; }
div[data-testid="metric-container"] {
    background:white; border:1px solid #E2E8F0;
    border-radius:12px; padding:1rem; box-shadow:0 1px 4px rgba(0,0,0,.06);
}
.huliot-header {
    background:linear-gradient(135deg,#0F172A 0%,#1E3A5F 100%);
    border-radius:14px; padding:18px 24px; margin-bottom:16px; color:white;
}
.huliot-header h1 { color:#FBBF24; margin:0; font-size:26px; font-weight:900; }
.huliot-header p  { color:rgba(255,255,255,.65); margin:4px 0 0; font-size:12px; }
.stDownloadButton > button { background:#10B981 !important; color:white !important; font-weight:700 !important; }
</style>
""", unsafe_allow_html=True)

# ─── PRODUCT DATA ───────────────────────────────────────────────
# Columns: line, code, desc, type, sub, dn, price
RAW = [
    # ══ HT PRO ─ PIPES (Single Socket) ══
    ("HT Pro","54040300-i","S/S Pipe L=3000mm","Pipe","S/S 3000mm",40,567),
    ("HT Pro","54050300-i","S/S Pipe L=3000mm","Pipe","S/S 3000mm",50,739),
    ("HT Pro","54075300-i","S/S Pipe L=3000mm","Pipe","S/S 3000mm",75,1304),
    ("HT Pro","540110300-i","S/S Pipe L=3000mm","Pipe","S/S 3000mm",110,1751),
    ("HT Pro","540125300-i","S/S Pipe L=3000mm","Pipe","S/S 3000mm",125,3400),
    ("HT Pro","540160300-i","S/S Pipe L=3000mm","Pipe","S/S 3000mm",160,4116),
    ("HT Pro","540200300-i","S/S Pipe L=3000mm","Pipe","S/S 3000mm",200,8303),
    # Double Socket 3000mm
    ("HT Pro","5404040300-i","D/S Pipe L=3000mm","Pipe","D/S 3000mm",40,588),
    ("HT Pro","5405050300-i","D/S Pipe L=3000mm","Pipe","D/S 3000mm",50,768),
    ("HT Pro","5407575300-i","D/S Pipe L=3000mm","Pipe","D/S 3000mm",75,1344),
    ("HT Pro","5401111300-i","D/S Pipe L=3000mm","Pipe","D/S 3000mm",110,2063),
    ("HT Pro","5401212300-i","D/S Pipe L=3000mm","Pipe","D/S 3000mm",125,3518),
    ("HT Pro","5401616300-i","D/S Pipe L=3000mm","Pipe","D/S 3000mm",160,4268),
    # S/S Special Lengths
    ("HT Pro","5404000025-i","S/S Pipe L=250mm","Pipe","S/S 250mm",40,77),
    ("HT Pro","5405000025-i","S/S Pipe L=250mm","Pipe","S/S 250mm",50,88),
    ("HT Pro","5407500025-i","S/S Pipe L=250mm","Pipe","S/S 250mm",75,147),
    ("HT Pro","5401100025-i","S/S Pipe L=250mm","Pipe","S/S 250mm",110,243),
    ("HT Pro","5401200025-i","S/S Pipe L=250mm","Pipe","S/S 250mm",125,392),
    ("HT Pro","5401600025-i","S/S Pipe L=250mm","Pipe","S/S 250mm",160,483),
    ("HT Pro","54040050-i","S/S Pipe L=500mm","Pipe","S/S 500mm",40,113),
    ("HT Pro","54050050-i","S/S Pipe L=500mm","Pipe","S/S 500mm",50,147),
    ("HT Pro","54075050-i","S/S Pipe L=500mm","Pipe","S/S 500mm",75,252),
    ("HT Pro","540110050-i","S/S Pipe L=500mm","Pipe","S/S 500mm",110,411),
    ("HT Pro","540125050-i","S/S Pipe L=500mm","Pipe","S/S 500mm",125,664),
    ("HT Pro","540160050-i","S/S Pipe L=500mm","Pipe","S/S 500mm",160,812),
    ("HT Pro","54040100-i","S/S Pipe L=1000mm","Pipe","S/S 1000mm",40,204),
    ("HT Pro","54050100-i","S/S Pipe L=1000mm","Pipe","S/S 1000mm",50,266),
    ("HT Pro","54075100-i","S/S Pipe L=1000mm","Pipe","S/S 1000mm",75,462),
    ("HT Pro","540110100-i","S/S Pipe L=1000mm","Pipe","S/S 1000mm",110,747),
    ("HT Pro","540125100-i","S/S Pipe L=1000mm","Pipe","S/S 1000mm",125,1212),
    ("HT Pro","540160100-i","S/S Pipe L=1000mm","Pipe","S/S 1000mm",160,1474),
    ("HT Pro","54040150-i","S/S Pipe L=1500mm","Pipe","S/S 1500mm",40,294),
    ("HT Pro","54050150-i","S/S Pipe L=1500mm","Pipe","S/S 1500mm",50,384),
    ("HT Pro","54075150-i","S/S Pipe L=1500mm","Pipe","S/S 1500mm",75,672),
    ("HT Pro","540110150-i","S/S Pipe L=1500mm","Pipe","S/S 1500mm",110,1085),
    ("HT Pro","540125150-i","S/S Pipe L=1500mm","Pipe","S/S 1500mm",125,1759),
    ("HT Pro","540160150-i","S/S Pipe L=1500mm","Pipe","S/S 1500mm",160,2134),
    ("HT Pro","54040200-i","S/S Pipe L=2000mm","Pipe","S/S 2000mm",40,385),
    ("HT Pro","54050200-i","S/S Pipe L=2000mm","Pipe","S/S 2000mm",50,503),
    ("HT Pro","54075200-i","S/S Pipe L=2000mm","Pipe","S/S 2000mm",75,882),
    ("HT Pro","540110200-i","S/S Pipe L=2000mm","Pipe","S/S 2000mm",110,1421),
    ("HT Pro","540125200-i","S/S Pipe L=2000mm","Pipe","S/S 2000mm",125,2307),
    ("HT Pro","540160200-i","S/S Pipe L=2000mm","Pipe","S/S 2000mm",160,2796),
    # D/S Special Lengths
    ("HT Pro","5404040050-i","D/S Pipe L=500mm","Pipe","D/S 500mm",40,134),
    ("HT Pro","540505050-i","D/S Pipe L=500mm","Pipe","D/S 500mm",50,175),
    ("HT Pro","5407575050-i","D/S Pipe L=500mm","Pipe","D/S 500mm",75,292),
    ("HT Pro","5401111050-i","D/S Pipe L=500mm","Pipe","D/S 500mm",110,484),
    ("HT Pro","5401212050-i","D/S Pipe L=500mm","Pipe","D/S 500mm",125,782),
    ("HT Pro","5401616050-i","D/S Pipe L=500mm","Pipe","D/S 500mm",160,964),
    ("HT Pro","5404040100-i","D/S Pipe L=1000mm","Pipe","D/S 1000mm",40,224),
    ("HT Pro","5405050100-i","D/S Pipe L=1000mm","Pipe","D/S 1000mm",50,293),
    ("HT Pro","5407575100-i","D/S Pipe L=1000mm","Pipe","D/S 1000mm",75,502),
    ("HT Pro","5401111100-i","D/S Pipe L=1000mm","Pipe","D/S 1000mm",110,821),
    ("HT Pro","5401212100-i","D/S Pipe L=1000mm","Pipe","D/S 1000mm",125,1328),
    ("HT Pro","5401616100-i","D/S Pipe L=1000mm","Pipe","D/S 1000mm",160,1624),
    ("HT Pro","5404040150-i","D/S Pipe L=1500mm","Pipe","D/S 1500mm",40,315),
    ("HT Pro","5405050150-i","D/S Pipe L=1500mm","Pipe","D/S 1500mm",50,413),
    ("HT Pro","5407575150-i","D/S Pipe L=1500mm","Pipe","D/S 1500mm",75,712),
    ("HT Pro","5401111150-i","D/S Pipe L=1500mm","Pipe","D/S 1500mm",110,1157),
    ("HT Pro","5401212150-i","D/S Pipe L=1500mm","Pipe","D/S 1500mm",125,1876),
    ("HT Pro","5401616150-i","D/S Pipe L=1500mm","Pipe","D/S 1500mm",160,2286),
    ("HT Pro","5404040200-i","D/S Pipe L=2000mm","Pipe","D/S 2000mm",40,406),
    ("HT Pro","5405050200-i","D/S Pipe L=2000mm","Pipe","D/S 2000mm",50,531),
    ("HT Pro","5407575200-i","D/S Pipe L=2000mm","Pipe","D/S 2000mm",75,924),
    ("HT Pro","5401111200-i","D/S Pipe L=2000mm","Pipe","D/S 2000mm",110,1494),
    ("HT Pro","5401212200-i","D/S Pipe L=2000mm","Pipe","D/S 2000mm",125,2423),
    ("HT Pro","5401616200-i","D/S Pipe L=2000mm","Pipe","D/S 2000mm",160,2946),
    # ══ HT PRO ─ BENDS ══
    ("HT Pro","40040150","Bend 15°","Bend","15° Bend",110,234),
    ("HT Pro","40040350","Bend 30°","Bend","30° Bend",110,239),
    ("HT Pro","40010460-i","Bend 45°","Bend","45° Bend",40,66),
    ("HT Pro","40020460-i","Bend 45°","Bend","45° Bend",50,82),
    ("HT Pro","40030460-i","Bend 45°","Bend","45° Bend",75,128),
    ("HT Pro","40040460-i","Bend 45°","Bend","45° Bend",110,186),
    ("HT Pro","40050460","Bend 45°","Bend","45° Bend",125,768),
    ("HT Pro","40060460","Bend 45°","Bend","45° Bend",160,1013),
    ("HT Pro","40020467","Door Bend 45°","Bend","Door 45°",50,149),
    ("HT Pro","40040467","Door Bend 45°","Bend","Door 45°",110,456),
    ("HT Pro","40040468","Door Bend 45° Right","Bend","Door 45° R",110,386),
    ("HT Pro","40040469","Door Bend 45° Left","Bend","Door 45° L",110,382),
    ("HT Pro","40060457","Door Bend 45°","Bend","Door 45°",160,1751),
    ("HT Pro","40060458","Door Bend 45° Right","Bend","Door 45° R",160,1504),
    ("HT Pro","40060459","Door Bend 45° Left","Bend","Door 45° L",160,1626),
    ("HT Pro","40010860-i","Bend 87.5°","Bend","87.5° Bend",40,72),
    ("HT Pro","40020860-i","Bend 87.5°","Bend","87.5° Bend",50,77),
    ("HT Pro","40030860","Bend 87.5°","Bend","87.5° Bend",75,155),
    ("HT Pro","40040860-i","Bend 87.5°","Bend","87.5° Bend",110,270),
    ("HT Pro","40050860","Bend 87.5°","Bend","87.5° Bend",125,700),
    ("HT Pro","40060860","Bend 87.5°","Bend","87.5° Bend",160,722),
    ("HT Pro","40020867-i","Door Bend 87.5°","Bend","Door 87.5°",50,221),
    ("HT Pro","40030867","Door Bend 87.5°","Bend","Door 87.5°",75,209),
    ("HT Pro","40040867-i","Door Bend 87.5°","Bend","Door 87.5°",110,517),
    ("HT Pro","40060857","Door Bend 87.5°","Bend","Door 87.5°",160,2429),
    ("HT Pro","40040868-i","Door Bend 87.5° Right","Bend","Door 87.5° R",110,553),
    ("HT Pro","40040869","Door Bend 87.5° Left","Bend","Door 87.5° L",110,565),
    ("HT Pro","40060858","Door Bend 87.5° Right","Bend","Door 87.5° R",160,1907),
    ("HT Pro","40060859","Door Bend 87.5° Left","Bend","Door 87.5° L",160,1927),
    # ══ HT PRO ─ BRANCHES ══
    ("HT Pro","40611440","Single Y 45° 40×40","Branch","Y 40×40",40,96),
    ("HT Pro","40622460","Single Y 45° 50×50","Branch","Y 50×50",50,139),
    ("HT Pro","40633460-i","Single Y 45° 75×75","Branch","Y 75×75",75,262),
    ("HT Pro","40644460-i","Single Y 45° 110×110","Branch","Y 110×110",110,575),
    ("HT Pro","40655460","Single Y 45° 125×125","Branch","Y 125×125",125,1475),
    ("HT Pro","40666450","Single Y 45° 160×160","Branch","Y 160×160",160,1942),
    ("HT Pro","40621440","Reducing Y 45° 50×40","Branch","Red.Y 50×40",50,143),
    ("HT Pro","40632460","Reducing Y 45° 75×50","Branch","Red.Y 75×50",75,350),
    ("HT Pro","40642460","Reducing Y 45° 110×50","Branch","Red.Y 110×50",110,361),
    ("HT Pro","40643460","Reducing Y 45° 110×75","Branch","Red.Y 110×75",110,578),
    ("HT Pro","40654460","Reducing Y 45° 125×110","Branch","Red.Y 125×110",125,1270),
    ("HT Pro","40664450","Reducing Y 45° 160×110","Branch","Red.Y 160×110",160,1744),
    ("HT Pro","40611860","Single Tee 90° 40×40","Branch","Tee 40×40",40,110),
    ("HT Pro","40622860","Single Tee 90° 50×50","Branch","Tee 50×50",50,121),
    ("HT Pro","40633860-i","Single Tee 90° 75×75","Branch","Tee 75×75",75,197),
    ("HT Pro","40655860","Single Tee 90° 125×125","Branch","Tee 125×125",125,607),
    ("HT Pro","40666860","Single Tee 90° 160×160","Branch","Tee 160×160",160,947),
    ("HT Pro","40621860","Reducing Tee 90° 50×40","Branch","Red.Tee 50×40",50,166),
    ("HT Pro","40632860","Reducing Tee 90° 75×50","Branch","Red.Tee 75×50",75,185),
    ("HT Pro","40642860","Reducing Tee Short 110×50","Branch","Red.Tee 110×50",110,392),
    ("HT Pro","40652860","Reducing Tee 90° 125×50","Branch","Red.Tee 125×50",125,614),
    ("HT Pro","40662860","Reducing Tee 90° 160×50","Branch","Red.Tee 160×50",160,1093),
    ("HT Pro","40664860","Reducing Tee 90° 160×110","Branch","Red.Tee 160×110",160,877),
    ("HT Pro","40733860-i","Swept Tee 87.5° 75×75","Branch","Swept 75×75",75,260),
    ("HT Pro","40742860-i","Reducing Swept Tee 110×50","Branch","Swept 110×50",110,436),
    ("HT Pro","40743860-i","Reducing Swept Tee 110×75","Branch","Swept 110×75",110,550),
    ("HT Pro","40744860-i","Swept Tee 87.5° 110×110","Branch","Swept 110×110",110,510),
    ("HT Pro","40754860","Reducing Swept Tee 125×110","Branch","Swept 125×110",125,1080),
    ("HT Pro","14040764860-i","Reducing Swept Tee 160×110","Branch","Swept 160×110",160,2086),
    ("HT Pro","41044860","Double Swept Tee 110×110×110","Branch","Dbl Swept 110",110,2023),
    ("HT Pro","41054850-i","Double Branch 87.5/90° 125×110×110","Branch","Dbl Branch 125",125,2241),
    ("HT Pro","41064850","Double Branch 87.5/90° 160×110×110","Branch","Dbl Branch 160",160,2754),
    ("HT Pro","40733867-i","Door Tee Swept 75×75","Branch","Door Swept 75×75",75,460),
    ("HT Pro","40742867-i","Door Swept Tee 110×50","Branch","Door Swept 110×50",110,616),
    ("HT Pro","40743867-i","Door Swept Tee 110×75","Branch","Door Swept 110×75",110,732),
    ("HT Pro","40744867-i","Door Swept Tee 110×110","Branch","Door Swept 110×110",110,754),
    ("HT Pro","40754867-HM","Door Swept Tee 125×110","Branch","Door Swept 125×110",125,2016),
    ("HT Pro","40664857-i","Door Swept Tee 160×110","Branch","Door Swept 160×110",160,2766),
    ("HT Pro","41044857-HM","Double Swept Door Tee 110×110×110","Branch","Dbl Door 110",110,2232),
    ("HT Pro","41042450","Reducing Double Y 110×50×50","Branch","Dbl Y 110×50×50",110,1560),
    ("HT Pro","41044450","Double Y 110×110×110","Branch","Dbl Y 110×110×110",110,1463),
    ("HT Pro","41062450","Reducing Double Y 160×50×50","Branch","Dbl Y 160×50×50",160,1225),
    ("HT Pro","41044457","Double Y Door 110×110×110","Branch","Dbl Y Door",110,3106),
    ("HT Pro","41244850","Corner Branch 87° 110×110×110","Branch","Corner 110×110×110",110,1346),
    ("HT Pro","4041254850","Corner Branch 87° 125×110×110","Branch","Corner 125×110×110",125,1968),
    ("HT Pro","41264850-i","Reducing Corner Branch 160×110×110","Branch","Corner 160×110×110",160,2382),
    # ══ HT PRO ─ TRAPS ══
    ("HT Pro","49540750G-i","P Trap 50mm Water Seal 110×110","Trap","P Trap",110,1132),
    ("HT Pro","41840051-i","S Trap Siphon Type 110×110","Trap","S Trap",110,2262),
    ("HT Pro","69111750G-i","Nahani Trap NT 110×75","Trap","Nahani Trap",110,649),
    ("HT Pro","60117051","Multi Floor Trap 7\" 110×75×50","Trap","MFT",110,1256),
    ("HT Pro","14048111060G-i","Multi Floor Trap with Socket 110×75×50","Trap","MFT Socketed",110,1680),
    ("HT Pro","41242850-i","Ht. Riser 2-Inlet 90° 110×50×50","Trap","Riser 2-Inlet 90°",110,1061),
    ("HT Pro","41042860","Ht. Riser 2-Inlet 180° 110×50×50","Trap","Riser 2-Inlet 180°",110,1265),
    ("HT Pro","4102042860","Hopper 3-Inlet 110×50×50×50","Trap","Hopper 3-Inlet",110,1380),
    ("HT Pro","4041043280","Riser 50+75mm Inlet 110×75×50","Trap","Riser 75+50",110,1038),
    ("HT Pro","69201551G-i","Height Riser L=150 for MFT","Trap","Riser L150 MFT",110,497),
    ("HT Pro","69203551G-i","Height Riser L=350 for MFT","Trap","Riser L350 MFT",110,737),
    ("HT Pro","60203651-i","Height Riser Thread Lock Trap","Trap","Riser Thread Lock",110,109),
    ("HT Pro","4049911100G-i","H.A.F.F Stack Single Stack 110×110×75","Trap","HAFF Stack",110,6600),
    # ══ HT PRO ─ INSPECTION ══
    ("HT Pro","49130060-i","Inspection Pipe (Cleaning Pipe)","Inspection","Cleaning Pipe",75,460),
    ("HT Pro","49140060-i","Inspection Pipe (Cleaning Pipe)","Inspection","Cleaning Pipe",110,566),
    ("HT Pro","49150060","Inspection Pipe (Cleaning Pipe)","Inspection","Cleaning Pipe",125,1061),
    ("HT Pro","49160060","Inspection Pipe (Cleaning Pipe)","Inspection","Cleaning Pipe",160,1199),
    # ══ HT PRO ─ COUPLERS / SLEEVES ══
    ("HT Pro","41710055-i","Double Socket / Coupler","Coupler","Coupler",40,73),
    ("HT Pro","41720055-i","One Way Socket / Coupler","Coupler","Coupler",50,85),
    ("HT Pro","41730050-i","Double Socket / Coupler","Coupler","Coupler",75,115),
    ("HT Pro","41740055-i","Double Socket / Coupler","Coupler","Coupler",110,210),
    ("HT Pro","41750065","One Way Socket / Coupler","Coupler","Coupler",125,494),
    ("HT Pro","41760055","One Way Socket / Coupler","Coupler","Coupler",160,1054),
    ("HT Pro","41720053","Sleeve Repairing Coupler","Coupler","Sleeve",50,115),
    ("HT Pro","41730053","Sleeve Repairing Coupler","Coupler","Sleeve",75,128),
    ("HT Pro","41740053","Sleeve Repairing Coupler","Coupler","Sleeve",110,215),
    # ══ HT PRO ─ REDUCERS ══
    ("HT Pro","42121060","Eccentric Reducer 50×40","Reducer","Ecc.Red 50×40",50,66),
    ("HT Pro","42132050","Eccentric Reducer 75×50","Reducer","Ecc.Red 75×50",75,83),
    ("HT Pro","42142050","Eccentric Reducer 110×50","Reducer","Ecc.Red 110×50",110,182),
    ("HT Pro","42143050-i","Eccentric Reducer 110×75","Reducer","Ecc.Red 110×75",110,215),
    ("HT Pro","42154060","Eccentric Reducer 125×110","Reducer","Ecc.Red 125×110",125,421),
    ("HT Pro","42164050","Eccentric Reducer 160×110","Reducer","Ecc.Red 160×110",160,653),
    ("HT Pro","42134050-i","Eccentric Reverse Reducer 110×75","Reducer","Rev.Red 110×75",110,510),
    ("HT Pro","P0500000000040K","Concentric Reducer Bushing 50×40","Reducer","Con.Red 50×40",50,192),
    ("HT Pro","P07500000050K","Concentric Reducer Bushing 75×50","Reducer","Con.Red 75×50",75,253),
    ("HT Pro","P1100000000050V","Concentric Reducer Bushing 110×50","Reducer","Con.Red 110×50",110,328),
    ("HT Pro","P1100000000075V","Concentric Reducer Bushing 110×75","Reducer","Con.Red 110×75",110,401),
    # ══ HT PRO ─ ACCESSORIES ══
    ("HT Pro","41610040","End Cap","Accessory","End Cap",40,35),
    ("HT Pro","41620050-i","End Cap","Accessory","End Cap",50,66),
    ("HT Pro","41630050-i","End Cap","Accessory","End Cap",75,70),
    ("HT Pro","41640050-i","End Cap","Accessory","End Cap",110,115),
    ("HT Pro","41650060","End Cap","Accessory","End Cap",125,251),
    ("HT Pro","41660060","End Cap","Accessory","End Cap",160,344),
    ("HT Pro","4042320040","Vent Cowl","Accessory","Vent Cowl",50,239),
    ("HT Pro","4042330040","Vent Cowl","Accessory","Vent Cowl",75,185),
    ("HT Pro","4042340060","Vent Cowl","Accessory","Vent Cowl",110,194),
    ("HT Pro","4042360040","Vent Cowl","Accessory","Vent Cowl",160,413),
    ("HT Pro","5401106650-i","Boss Connector 1-Inlet L660mm 110×50","Accessory","Boss Pipe 1-Inlet",110,1004),
    ("HT Pro","540110502-i","Boss Connector Double Branch L660mm 110×50×50","Accessory","Boss Pipe Double",110,1404),
    ("HT Pro","5401105102-i","Boss Connector Corner Branch L660mm 110×50×50","Accessory","Boss Pipe Corner",110,1404),
    ("HT Pro","540110503-i","Boss Connector Triple Branch L660mm 110×50×50×50","Accessory","Boss Pipe Triple",110,1604),
    ("HT Pro","41540020","WC Connector Straight White","Accessory","WC Connector",110,1558),
    ("HT Pro","41540027","WC Connector Straight Door White","Accessory","WC Door Connector",110,1776),
    ("HT Pro","41542866","WC Bend + Back Inspection White","Accessory","WC Bend Door",110,1559),
    ("HT Pro","41540615","Flange for WC Bend White","Accessory","WC Flange",110,66),
    ("HT Pro","60150331","Aquaslim S.Steel L=330mm","Accessory","Shower Channel",0,1288),
    ("HT Pro","60150339","Aquaslim Full S.Steel 330 Tiles","Accessory","Shower Channel",0,1333),
    ("HT Pro","60150701","Aquaslim S.Steel L=700mm","Accessory","Shower Channel",0,1790),
    ("HT Pro","60150709","Aquaslim Full S.Steel 700 Tiles","Accessory","Shower Channel",0,1939),
    ("HT Pro","60200260","Extension for Square Grating","Accessory","Grating Ext",0,82),
    ("HT Pro","60200263","Extension for Square Grating","Accessory","Grating Ext",0,78),
    ("HT Pro","47700012","Lubricant 250ml Tin Pack","Accessory","Lubricant",0,198),
    # ══ HT PRO ─ CLAMPS ══
    ("HT Pro","48100040-S","Split Clamp DN40","Clamp","Clamp DN40",40,126),
    ("HT Pro","48100050-S","Split Clamp DN50","Clamp","Clamp DN50",50,138),
    ("HT Pro","48100075-S","Split Clamp DN75","Clamp","Clamp DN75",75,174),
    ("HT Pro","48100011-S","Split Clamp DN110","Clamp","Clamp DN110",110,210),
    ("HT Pro","48100012-S","Split Clamp DN125","Clamp","Clamp DN125",125,246),
    ("HT Pro","48100016-S","Split Clamp DN160","Clamp","Clamp DN160",160,300),
    ("HT Pro","48100020-S","Split Clamp DN200","Clamp","Clamp DN200",200,354),
    # ══════════════════════════════════════════════
    # ══ ULTRA SILENT ─ PIPES ══
    # ══════════════════════════════════════════════
    ("Ultra Silent","5753200300-i","US S/S Pipe L=3000mm","Pipe","S/S 3000mm",32,948),
    ("Ultra Silent","5754000300-i","US S/S Pipe L=3000mm","Pipe","S/S 3000mm",40,1027),
    ("Ultra Silent","5755000300-i","US S/S Pipe L=3000mm","Pipe","S/S 3000mm",50,1313),
    ("Ultra Silent","5757500300-i","US S/S Pipe L=3000mm","Pipe","S/S 3000mm",75,2521),
    ("Ultra Silent","5751100300-i","US S/S Pipe L=3000mm","Pipe","S/S 3000mm",110,2953),
    ("Ultra Silent","5751200300-i","US S/S Pipe L=3000mm","Pipe","S/S 3000mm",125,4165),
    ("Ultra Silent","5751600300-i","US S/S Pipe L=3000mm","Pipe","S/S 3000mm",160,6060),
    ("Ultra Silent","5752000300-i","US S/S Pipe L=3000mm","Pipe","S/S 3000mm",200,8520),
    ("Ultra Silent","5754040300-i","US D/S Pipe L=3000mm","Pipe","D/S 3000mm",40,1061),
    ("Ultra Silent","5755050300-i","US D/S Pipe L=3000mm","Pipe","D/S 3000mm",50,1358),
    ("Ultra Silent","5757575300-i","US D/S Pipe L=3000mm","Pipe","D/S 3000mm",75,2593),
    ("Ultra Silent","5751111300-i","US D/S Pipe L=3000mm","Pipe","D/S 3000mm",110,3110),
    ("Ultra Silent","5751212300-i","US D/S Pipe L=3000mm","Pipe","D/S 3000mm",125,4300),
    ("Ultra Silent","5751616300-i","US D/S Pipe L=3000mm","Pipe","D/S 3000mm",160,6812),
    ("Ultra Silent","5752020300-i","US D/S Pipe L=3000mm","Pipe","D/S 3000mm",200,8653),
    # US S/S Special Lengths
    ("Ultra Silent","5754000025-i","US S/S Pipe L=250mm","Pipe","S/S 250mm",40,117),
    ("Ultra Silent","5755000025-i","US S/S Pipe L=250mm","Pipe","S/S 250mm",50,152),
    ("Ultra Silent","5757500025-i","US S/S Pipe L=250mm","Pipe","S/S 250mm",75,278),
    ("Ultra Silent","5751100025-i","US S/S Pipe L=250mm","Pipe","S/S 250mm",110,376),
    ("Ultra Silent","5751200025-i","US S/S Pipe L=250mm","Pipe","S/S 250mm",125,470),
    ("Ultra Silent","5751600025-i","US S/S Pipe L=250mm","Pipe","S/S 250mm",160,741),
    ("Ultra Silent","5754000050-i","US S/S Pipe L=500mm","Pipe","S/S 500mm",40,200),
    ("Ultra Silent","5755000050-i","US S/S Pipe L=500mm","Pipe","S/S 500mm",50,257),
    ("Ultra Silent","5757500050-i","US S/S Pipe L=500mm","Pipe","S/S 500mm",75,483),
    ("Ultra Silent","5751100050-i","US S/S Pipe L=500mm","Pipe","S/S 500mm",110,650),
    ("Ultra Silent","5751200050-i","US S/S Pipe L=500mm","Pipe","S/S 500mm",125,806),
    ("Ultra Silent","5751600050-i","US S/S Pipe L=500mm","Pipe","S/S 500mm",160,1274),
    ("Ultra Silent","5754000100-i","US S/S Pipe L=1000mm","Pipe","S/S 1000mm",40,366),
    ("Ultra Silent","5755000100-i","US S/S Pipe L=1000mm","Pipe","S/S 1000mm",50,468),
    ("Ultra Silent","5757500100-i","US S/S Pipe L=1000mm","Pipe","S/S 1000mm",75,890),
    ("Ultra Silent","5751100100-i","US S/S Pipe L=1000mm","Pipe","S/S 1000mm",110,1201),
    ("Ultra Silent","5751200100-i","US S/S Pipe L=1000mm","Pipe","S/S 1000mm",125,1478),
    ("Ultra Silent","5751600100-i","US S/S Pipe L=1000mm","Pipe","S/S 1000mm",160,2340),
    ("Ultra Silent","5752000100-i","US S/S Pipe L=1000mm","Pipe","S/S 1000mm",200,2926),
    ("Ultra Silent","5754000150-i","US S/S Pipe L=1500mm","Pipe","S/S 1500mm",40,531),
    ("Ultra Silent","5755000150-i","US S/S Pipe L=1500mm","Pipe","S/S 1500mm",50,680),
    ("Ultra Silent","5757500150-i","US S/S Pipe L=1500mm","Pipe","S/S 1500mm",75,1297),
    ("Ultra Silent","5751100150-i","US S/S Pipe L=1500mm","Pipe","S/S 1500mm",110,1751),
    ("Ultra Silent","5751200150-i","US S/S Pipe L=1500mm","Pipe","S/S 1500mm",125,2390),
    ("Ultra Silent","5751600150-i","US S/S Pipe L=1500mm","Pipe","S/S 1500mm",160,3407),
    ("Ultra Silent","5752000150-i","US S/S Pipe L=1500mm","Pipe","S/S 1500mm",200,4322),
    ("Ultra Silent","5754000200-i","US S/S Pipe L=2000mm","Pipe","S/S 2000mm",40,697),
    ("Ultra Silent","5755000200-i","US S/S Pipe L=2000mm","Pipe","S/S 2000mm",50,890),
    ("Ultra Silent","5757500200-i","US S/S Pipe L=2000mm","Pipe","S/S 2000mm",75,1705),
    ("Ultra Silent","5751100200-i","US S/S Pipe L=2000mm","Pipe","S/S 2000mm",110,2300),
    ("Ultra Silent","5751200200-i","US S/S Pipe L=2000mm","Pipe","S/S 2000mm",125,2821),
    ("Ultra Silent","5751600200-i","US S/S Pipe L=2000mm","Pipe","S/S 2000mm",160,4472),
    ("Ultra Silent","5752000200-i","US S/S Pipe L=2000mm","Pipe","S/S 2000mm",200,5718),
    # US D/S Special Lengths
    ("Ultra Silent","5754040050-i","US D/S Pipe L=500mm","Pipe","D/S 500mm",40,234),
    ("Ultra Silent","5755050050-i","US D/S Pipe L=500mm","Pipe","D/S 500mm",50,302),
    ("Ultra Silent","5757575050-i","US D/S Pipe L=500mm","Pipe","D/S 500mm",75,556),
    ("Ultra Silent","5751111050-i","US D/S Pipe L=500mm","Pipe","D/S 500mm",110,751),
    ("Ultra Silent","5751212050-i","US D/S Pipe L=500mm","Pipe","D/S 500mm",125,947),
    ("Ultra Silent","5751616050-i","US D/S Pipe L=500mm","Pipe","D/S 500mm",160,1482),
    ("Ultra Silent","5754040100-i","US D/S Pipe L=1000mm","Pipe","D/S 1000mm",40,400),
    ("Ultra Silent","5755050100-i","US D/S Pipe L=1000mm","Pipe","D/S 1000mm",50,514),
    ("Ultra Silent","5757575100-i","US D/S Pipe L=1000mm","Pipe","D/S 1000mm",75,964),
    ("Ultra Silent","5751111100-i","US D/S Pipe L=1000mm","Pipe","D/S 1000mm",110,1301),
    ("Ultra Silent","5751212100-i","US D/S Pipe L=1000mm","Pipe","D/S 1000mm",125,1613),
    ("Ultra Silent","5751616100-i","US D/S Pipe L=1000mm","Pipe","D/S 1000mm",160,2547),
    ("Ultra Silent","5752020100-i","US D/S Pipe L=1000mm","Pipe","D/S 1000mm",200,3059),
    ("Ultra Silent","5754040150-i","US D/S Pipe L=1500mm","Pipe","D/S 1500mm",40,564),
    ("Ultra Silent","5755050150-i","US D/S Pipe L=1500mm","Pipe","D/S 1500mm",50,724),
    ("Ultra Silent","5757575150-i","US D/S Pipe L=1500mm","Pipe","D/S 1500mm",75,1371),
    ("Ultra Silent","5751111150-i","US D/S Pipe L=1500mm","Pipe","D/S 1500mm",110,1850),
    ("Ultra Silent","5751212150-i","US D/S Pipe L=1500mm","Pipe","D/S 1500mm",125,2470),
    ("Ultra Silent","5751616150-i","US D/S Pipe L=1500mm","Pipe","D/S 1500mm",160,3614),
    ("Ultra Silent","5752020150-i","US D/S Pipe L=1500mm","Pipe","D/S 1500mm",200,4455),
    ("Ultra Silent","5754040200-i","US D/S Pipe L=2000mm","Pipe","D/S 2000mm",40,730),
    ("Ultra Silent","5755050200-i","US D/S Pipe L=2000mm","Pipe","D/S 2000mm",50,935),
    ("Ultra Silent","5757575200-i","US D/S Pipe L=2000mm","Pipe","D/S 2000mm",75,1779),
    ("Ultra Silent","5751111200-i","US D/S Pipe L=2000mm","Pipe","D/S 2000mm",110,2401),
    ("Ultra Silent","5751212200-i","US D/S Pipe L=2000mm","Pipe","D/S 2000mm",125,2957),
    ("Ultra Silent","5751616200-i","US D/S Pipe L=2000mm","Pipe","D/S 2000mm",160,4680),
    ("Ultra Silent","5752020200-i","US D/S Pipe L=2000mm","Pipe","D/S 2000mm",200,5851),
    # ══ ULTRA SILENT ─ BENDS ══
    ("Ultra Silent","7070000170","US Bend 15°","Bend","15°",32,61),
    ("Ultra Silent","7070010170","US Bend 15°","Bend","15°",40,82),
    ("Ultra Silent","7070020170","US Bend 15°","Bend","15°",50,102),
    ("Ultra Silent","7070030170","US Bend 15°","Bend","15°",75,184),
    ("Ultra Silent","7070040170","US Bend 15°","Bend","15°",110,698),
    ("Ultra Silent","7070050170","US Bend 15°","Bend","15°",125,694),
    ("Ultra Silent","7070060170","US Bend 15°","Bend","15°",160,1357),
    ("Ultra Silent","7070000370","US Bend 30°","Bend","30°",32,82),
    ("Ultra Silent","7070010370","US Bend 30°","Bend","30°",40,102),
    ("Ultra Silent","7070020370","US Bend 30°","Bend","30°",50,102),
    ("Ultra Silent","7070030370","US Bend 30°","Bend","30°",75,205),
    ("Ultra Silent","7070040370","US Bend 30°","Bend","30°",110,727),
    ("Ultra Silent","7070050370","US Bend 30°","Bend","30°",125,838),
    ("Ultra Silent","7070060370","US Bend 30°","Bend","30°",160,1330),
    ("Ultra Silent","7070000470","US Bend 45°","Bend","45°",32,61),
    ("Ultra Silent","7070010470","US Bend 45°","Bend","45°",40,82),
    ("Ultra Silent","7070020470","US Bend 45°","Bend","45°",50,122),
    ("Ultra Silent","7070030470-i","US Bend 45°","Bend","45°",75,205),
    ("Ultra Silent","7070040470-i","US Bend 45°","Bend","45°",110,641),
    ("Ultra Silent","7070050470","US Bend 45°","Bend","45°",125,899),
    ("Ultra Silent","7070060470","US Bend 45°","Bend","45°",160,1202),
    ("Ultra Silent","7070080470","US Bend 45°","Bend","45°",200,3493),
    ("Ultra Silent","7070000670","US Bend 67.5°","Bend","67.5°",32,61),
    ("Ultra Silent","7070010670","US Bend 67.5°","Bend","67.5°",40,61),
    ("Ultra Silent","7070020670","US Bend 67.5°","Bend","67.5°",50,82),
    ("Ultra Silent","7070030670","US Bend 67.5°","Bend","67.5°",75,122),
    ("Ultra Silent","7070040670","US Bend 67.5°","Bend","67.5°",110,632),
    ("Ultra Silent","7070050670","US Bend 67.5°","Bend","67.5°",125,643),
    ("Ultra Silent","7070000870","US Bend 87.5°","Bend","87.5°",32,61),
    ("Ultra Silent","7070010870","US Bend 87.5°","Bend","87.5°",40,102),
    ("Ultra Silent","7070020870-i","US Bend 87.5°","Bend","87.5°",50,143),
    ("Ultra Silent","7070030870","US Bend 87.5°","Bend","87.5°",75,224),
    ("Ultra Silent","7070040870","US Bend 87.5°","Bend","87.5°",110,697),
    ("Ultra Silent","7070050870","US Bend 87.5°","Bend","87.5°",125,1062),
    ("Ultra Silent","7070060870","US Bend 87.5°","Bend","87.5°",160,2122),
    ("Ultra Silent","7070040877-i","US Door Bend 87.5°","Bend","Door 87.5°",110,1054),
    # ══ ULTRA SILENT ─ BRANCHES ══
    ("Ultra Silent","7070600470","US Wye 45° 32×32","Branch","Y 32×32",32,194),
    ("Ultra Silent","7070611470","US Wye 45° 40×40","Branch","Y 40×40",40,274),
    ("Ultra Silent","7070621470","US Wye 45° 50×40","Branch","Y 50×40",50,352),
    ("Ultra Silent","7070622470","US Wye 45° 50×50","Branch","Y 50×50",50,390),
    ("Ultra Silent","7070632470","US Wye 45° 75×50","Branch","Y 75×50",75,523),
    ("Ultra Silent","7070633470","US Wye 45° 75×75","Branch","Y 75×75",75,698),
    ("Ultra Silent","7070642470","US Wye 45° 110×50","Branch","Y 110×50",110,640),
    ("Ultra Silent","7070643470-i","US Wye 45° 110×75","Branch","Y 110×75",110,959),
    ("Ultra Silent","7070644470-i","US Wye 45° 110×110","Branch","Y 110×110",110,1183),
    ("Ultra Silent","7070654470","US Wye 45° 125×110","Branch","Y 125×110",125,1489),
    ("Ultra Silent","7070655470","US Wye 45° 125×125","Branch","Y 125×125",125,1754),
    ("Ultra Silent","7070664470","US Wye 45° 160×110","Branch","Y 160×110",160,2672),
    ("Ultra Silent","7070666470","US Wye 45° 160×160","Branch","Y 160×160",160,3653),
    ("Ultra Silent","7070686470","US Wye 45° 200×160","Branch","Y 200×160",200,6776),
    ("Ultra Silent","7070688470","US Wye 45° 200×200","Branch","Y 200×200",200,7529),
    ("Ultra Silent","7070611870","US Tee 90° 40×40","Branch","Tee 40×40",40,312),
    ("Ultra Silent","7070621870","US Tee 90° 50×40","Branch","Tee 50×40",50,352),
    ("Ultra Silent","7070622870","US Tee 90° 50×50","Branch","Tee 50×50",50,352),
    ("Ultra Silent","7070632870","US Tee 90° 75×50","Branch","Tee 75×50",75,553),
    ("Ultra Silent","7070633870","US Tee 90° 75×75","Branch","Tee 75×75",75,781),
    ("Ultra Silent","7070642870","US Tee 90° 110×50","Branch","Tee 110×50",110,898),
    ("Ultra Silent","7070666870","US Tee 90° 160×160","Branch","Tee 160×160",160,3122),
    ("Ultra Silent","7070744870","US Swept Tee 87.5° 110×110","Branch","Swept 110×110",110,1081),
    ("Ultra Silent","7070743870","US Swept Tee 87.5° 110×75","Branch","Swept 110×75",110,938),
    ("Ultra Silent","7070754870","US Swept Tee 87.5° 125×110","Branch","Swept 125×110",125,1062),
    ("Ultra Silent","7070764870","US Swept Tee 87.5° 160×110","Branch","Swept 160×110",160,2366),
    ("Ultra Silent","7070744877","US Door Swept Tee 110×110","Branch","Door Swept 110×110",110,1342),
    ("Ultra Silent","7070754877-i","US Door Swept Tee 125×110","Branch","Door Swept 125×110",125,1740),
    ("Ultra Silent","7070764877-i","US Door Swept Tee 160×110","Branch","Door Swept 160×110",160,2752),
    ("Ultra Silent","7071044870","US Double Swept Tee 110×110×110","Branch","Dbl Swept 110",110,2970),
    ("Ultra Silent","7071244870","US Corner Branch 110×110×110","Branch","Corner 110×110×110",110,1285),
    ("Ultra Silent","7071254870","US Corner Branch 125×110×110","Branch","Corner 125×110×110",125,1489),
    ("Ultra Silent","7071264870-i","US Corner Branch 160×110×110","Branch","Corner 160×110×110",160,2582),
    ("Ultra Silent","7071042670","US Double Branch 67.5° 110×50×50","Branch","Dbl 110×50×50",110,1105),
    ("Ultra Silent","7071044670","US Double Branch 67.5° 110×110×110","Branch","Dbl 110×110×110",110,1518),
    ("Ultra Silent","7071054870-i","US Double Branch 87.5/90° 125×110×110","Branch","Dbl 125×110×110",125,2441),
    # ══ ULTRA SILENT ─ TRAPS ══
    ("Ultra Silent","49540750B-i","US P Trap 50mm Water Seal 110×110","Trap","P Trap",110,1435),
    ("Ultra Silent","7071840070-i","US S Trap 110mm","Trap","S Trap",110,2870),
    ("Ultra Silent","60117060","US Multi Floor Trap W/O Ring 110×75×50","Trap","MFT W/O Ring",110,1496),
    ("Ultra Silent","S11050505075-i","US Multi Floor Trap With Ring 110×75×50","Trap","MFT With Ring",110,1778),
    ("Ultra Silent","17078111070-B","US Multi Floor Trap With Socket 110×75×50","Trap","MFT With Socket",110,1835),
    ("Ultra Silent","69111750B-i","US Nahani Trap 110×75","Trap","Nahani Trap",110,781),
    ("Ultra Silent","7079911100B-i","US H.A.F.F Stack 110×110×75","Trap","HAFF Stack",110,9000),
    ("Ultra Silent","7071042877-i","US Double Branch 180° 110×50×50","Trap","Riser 180°",110,1289),
    ("Ultra Silent","7071242877-i","US Corner Branch 90° 110×50×50","Trap","Corner Riser 90°",110,1459),
    ("Ultra Silent","70712","US Hopper 3-Inlet 110×50×50×50","Trap","Hopper 3-Inlet",110,1674),
    ("Ultra Silent","70713-i","US Hopper 3-Inlet 110×75×75×75","Trap","Hopper 3-Inlet 75mm",110,1958),
    ("Ultra Silent","7071043870-i","US Double Branch 180° 110×75×75","Trap","Riser 180° 75mm",110,1778),
    ("Ultra Silent","7071243870-HM","US Corner Branch 90° 110×75×75","Trap","Corner 90° 75mm",110,1778),
    ("Ultra Silent","69201551B-i","US Height Riser L=150 for MFT","Trap","Riser L150 MFT",110,650),
    ("Ultra Silent","69203551B-i","US Height Riser L=350 for MFT","Trap","Riser L350 MFT",110,977),
    ("Ultra Silent","60203651-i","Height Riser Smart Lock Trap","Trap","Riser Smart Lock",110,109),
    ("Ultra Silent","70114500","SmartLock Trap 140/50 Single Discharge","Trap","SmartLock 140/50",50,1243),
    ("Ultra Silent","70124599","SmartLock Trap 245/50 Single Discharge","Trap","SmartLock 245/50",50,1499),
    ("Ultra Silent","70114590","SmartLock Trap 140/40/50 Multi Discharge","Trap","SmartLock Multi 140",50,1820),
    ("Ultra Silent","70124590","SmartLock Trap 245/40/50 Multi Discharge","Trap","SmartLock Multi 245",50,2047),
    ("Ultra Silent","70140760","Collector 70/40 Single Discharge W/O Trap","Trap","Collector 70/40",40,760),
    # ══ ULTRA SILENT ─ INSPECTION ══
    ("Ultra Silent","7079120070","US Inspection Pipe","Inspection","Inspection",50,349),
    ("Ultra Silent","7079130070","US Inspection Pipe","Inspection","Inspection",75,821),
    ("Ultra Silent","7079140070","US Inspection Pipe","Inspection","Inspection",110,1530),
    ("Ultra Silent","7079150070","US Inspection Pipe","Inspection","Inspection",125,1775),
    ("Ultra Silent","7079160070","US Inspection Pipe","Inspection","Inspection",160,1859),
    ("Ultra Silent","7079180070","US Inspection Pipe","Inspection","Inspection",200,5498),
    # ══ ULTRA SILENT ─ COUPLERS / SLEEVES ══
    ("Ultra Silent","7071700270","US Double Socket 32","Coupler","Coupler",32,157),
    ("Ultra Silent","7071710270","US Double Socket 40","Coupler","Coupler",40,193),
    ("Ultra Silent","7071720275","US One Way Socket 50","Coupler","Coupler",50,194),
    ("Ultra Silent","7071730275-i","US One Way Socket 75","Coupler","Coupler",75,352),
    ("Ultra Silent","7071740275-i","US One Way Socket 110","Coupler","Coupler",110,640),
    ("Ultra Silent","7071750275","US One Way Socket 125","Coupler","Coupler",125,878),
    ("Ultra Silent","7071760275","US One Way Socket 160","Coupler","Coupler",160,1717),
    ("Ultra Silent","7071780275","US One Way Socket 200","Coupler","Coupler",200,2594),
    ("Ultra Silent","7071710070","US Sleeve 40","Coupler","Sleeve",40,349),
    ("Ultra Silent","7071720070","US Sleeve 50","Coupler","Sleeve",50,821),
    ("Ultra Silent","7071730070","US Sleeve 75","Coupler","Sleeve",75,898),
    ("Ultra Silent","7071740070","US Sleeve 110","Coupler","Sleeve",110,1775),
    ("Ultra Silent","7071750070","US Sleeve 125","Coupler","Sleeve",125,1913),
    ("Ultra Silent","7071760070","US Sleeve 160","Coupler","Sleeve",160,5498),
    ("Ultra Silent","41740060","Double Socket Cast Iron+Seal 110","Coupler","CI Socket",110,1019),
    ("Ultra Silent","41760051","Double Socket Cast Iron+Seal 160","Coupler","CI Socket",160,1192),
    # ══ ULTRA SILENT ─ REDUCERS ══
    ("Ultra Silent","7072110070","US Reducer 40×32","Reducer","Red 40×32",40,386),
    ("Ultra Silent","7072120070","US Reducer 50×32","Reducer","Red 50×32",50,391),
    ("Ultra Silent","7072121070","US Reducer 50×40","Reducer","Red 50×40",50,398),
    ("Ultra Silent","7072132070","US Reducer 75×50","Reducer","Red 75×50",75,426),
    ("Ultra Silent","7072142070","US Reducer 110×50","Reducer","Red 110×50",110,469),
    ("Ultra Silent","7072143070","US Reducer 110×75","Reducer","Red 110×75",110,491),
    ("Ultra Silent","7072154070","US Reducer 125×110","Reducer","Red 125×110",125,613),
    ("Ultra Silent","7072164070","US Reducer 160×110","Reducer","Red 160×110",160,1021),
    ("Ultra Silent","7072165070","US Reducer 160×125","Reducer","Red 160×125",160,1163),
    ("Ultra Silent","7072186070","US Reducer 200×160","Reducer","Red 200×160",200,2327),
    ("Ultra Silent","7072134070-i","US Reverse Reducer 110×75","Reducer","Rev.Red 110×75",110,510),
    # ══ ULTRA SILENT ─ ACCESSORIES ══
    ("Ultra Silent","7071610070","US End Cap","Accessory","End Cap",40,40),
    ("Ultra Silent","7071620070-i","US End Cap","Accessory","End Cap",50,78),
    ("Ultra Silent","7071630070","US End Cap","Accessory","End Cap",75,157),
    ("Ultra Silent","7071640070-i","US End Cap","Accessory","End Cap",110,352),
    ("Ultra Silent","7071650070","US End Cap","Accessory","End Cap",125,757),
    ("Ultra Silent","7071660070","US End Cap","Accessory","End Cap",160,768),
    ("Ultra Silent","7071680070","US End Cap","Accessory","End Cap",200,1616),
    ("Ultra Silent","42320040","US Vent Cowl 50","Accessory","Vent Cowl",50,239),
    ("Ultra Silent","42330040","US Vent Cowl 75","Accessory","Vent Cowl",75,185),
    ("Ultra Silent","42340060","US Vent Cowl 110","Accessory","Vent Cowl",110,194),
    ("Ultra Silent","42360040","US Vent Cowl 160","Accessory","Vent Cowl",160,413),
    ("Ultra Silent","7072330000","US Lock Seal 75","Accessory","Lock Seal",75,434),
    ("Ultra Silent","7072340000","US Lock Seal 110","Accessory","Lock Seal",110,965),
    ("Ultra Silent","7072350000","US Lock Seal 125","Accessory","Lock Seal",125,1115),
    ("Ultra Silent","7072360000","US Lock Seal 160","Accessory","Lock Seal",160,1372),
    ("Ultra Silent","7072380000","US Lock Seal 200","Accessory","Lock Seal",200,6918),
    ("Ultra Silent","7078004000","US End Lock 110","Accessory","End Lock",110,1518),
    ("Ultra Silent","7078005000","US End Lock 125","Accessory","End Lock",125,1663),
    ("Ultra Silent","7078006000","US End Lock 160","Accessory","End Lock",160,1702),
    ("Ultra Silent","7078008000","US End Lock 200","Accessory","End Lock",200,9194),
    ("Ultra Silent","41540020","WC Connector Straight White","Accessory","WC Connector",110,1558),
    ("Ultra Silent","41540027","WC Connector Straight Door White","Accessory","WC Door Connector",110,1776),
    ("Ultra Silent","41542866","WC Bend + Back Inspection White","Accessory","WC Bend Door",110,1559),
    ("Ultra Silent","7074010970","USSW Technical Bend 46mm","Accessory","Tech Bend",46,193),
    ("Ultra Silent","7074021970","USSW Technical Bend 50mm","Accessory","Tech Bend",50,215),
    ("Ultra Silent","7074021971","Long USSW Technical Bend 50mm","Accessory","Long Tech Bend",50,302),
    ("Ultra Silent","T047T000000000","Rubber Gasket US/USSW 46mm","Accessory","Rubber Gasket",46,217),
    ("Ultra Silent","T050T000000032","Rubber Gasket US/USSW 50mm","Accessory","Rubber Gasket",50,308),
    ("Ultra Silent","47700012","Lubricant 250ml Tin Pack","Accessory","Lubricant",0,198),
    # ══ ULTRA SILENT ─ CLAMPS ══
    ("Ultra Silent","7890004070-S","US HD Split Clamp DN40","Clamp","HD Clamp DN40",40,228),
    ("Ultra Silent","7890005070-S","US HD Split Clamp DN50","Clamp","HD Clamp DN50",50,258),
    ("Ultra Silent","7890007570-S","US HD Split Clamp DN75","Clamp","HD Clamp DN75",75,312),
    ("Ultra Silent","7890011070-S","US HD Split Clamp DN110","Clamp","HD Clamp DN110",110,408),
    ("Ultra Silent","7890012570-S","US HD Split Clamp DN125","Clamp","HD Clamp DN125",125,432),
    ("Ultra Silent","7890016070-S","US HD Split Clamp DN160","Clamp","HD Clamp DN160",160,540),
    ("Ultra Silent","7890020070-S","US HD Split Clamp DN200","Clamp","HD Clamp DN200",200,630),
]

# ─── LOAD PRODUCTS ──────────────────────────────────────────────
@st.cache_data
def get_df():
    return pd.DataFrame(RAW, columns=["line","code","desc","type","sub","dn","price"])

df_all = get_df()

# ─── SESSION STATE INIT ─────────────────────────────────────────
for k, v in [("boq", []), ("project", ""), ("global_disc", 0.0)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HEADER ─────────────────────────────────────────────────────
st.markdown("""
<div class="huliot-header">
  <h1>⚙️ Huliot EZE Plumbing BOQ Builder</h1>
  <p>Huliot Pipes & Fittings Pvt. Ltd. &nbsp;|&nbsp; 714/715, Manjusar GIDC, Savli, Vadodara &nbsp;|&nbsp;
     Price List W.E.F April 2026 &nbsp;|&nbsp; Prices Ex-Factory/Depot &nbsp;|&nbsp; GST Extra as Applicable</p>
</div>
""", unsafe_allow_html=True)

hc1, hc2 = st.columns([3, 2])
with hc1:
    st.session_state.project = st.text_input(
        "🏗️ Project / Site Name",
        value=st.session_state.project,
        placeholder="e.g. Prestige Tower — Block A, Mumbai"
    )
with hc2:
    st.session_state.global_disc = st.number_input(
        "🏷️ Global Discount (%)",
        min_value=0.0, max_value=100.0,
        value=float(st.session_state.global_disc),
        step=0.5, format="%.1f",
        help="Applied to all BOQ items unless overridden per-item"
    )

st.divider()

# ─── TABS ───────────────────────────────────────────────────────
tab_cat, tab_boq = st.tabs([
    f"📦  Product Catalog  ({len(df_all)} items)",
    f"📋  Bill of Quantities  ({len(st.session_state.boq)} line items)"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 — PRODUCT CATALOG
# ═══════════════════════════════════════════════════════════════
with tab_cat:
    fc1, fc2 = st.columns([1, 3])

    with fc1:
        pl = st.radio(
            "Product Line",
            ["HT Pro 🟠", "Ultra Silent 🔵"],
            index=0, key="pl_radio"
        )
    pl_key = "HT Pro" if "HT Pro" in pl else "Ultra Silent"
    line_df = df_all[df_all["line"] == pl_key].copy()

    with fc2:
        avail_dn = sorted([d for d in line_df["dn"].unique() if d > 0])
        dn_options = ["All"] + [f"DN {d}" for d in avail_dn]
        dn_sel = st.pills("📏 Pipe Size (DN mm) — click to filter", dn_options, default="All", key="dn_pills")

    avail_cat = sorted(line_df["type"].unique())
    cat_sel = st.pills("🔩 Category", ["All"] + avail_cat, default="All", key="cat_pills")

    srch = st.text_input(
        "🔍 Search",
        placeholder="Type item code / description / size / sub-category...",
        key="search_box"
    )

    # Apply filters
    filt = line_df.copy()
    if dn_sel and dn_sel != "All":
        dn_val = int(dn_sel.replace("DN ", "").strip())
        filt = filt[filt["dn"] == dn_val]
    if cat_sel and cat_sel != "All":
        filt = filt[filt["type"] == cat_sel]
    if srch:
        q = srch.lower()
        filt = filt[
            filt["code"].str.lower().str.contains(q, na=False) |
            filt["desc"].str.lower().str.contains(q, na=False) |
            filt["sub"].str.lower().str.contains(q, na=False)  |
            filt["dn"].astype(str).str.contains(q, na=False)
        ]

    st.caption(f"**{len(filt)}** items · ✔ Tick checkbox → set Qty → click **Add to BOQ**")

    # Build display table
    filt_reset = filt.reset_index(drop=True)
    filt_reset.insert(0, "Add", False)
    filt_reset.insert(1, "Qty", 1)
    filt_reset["DN mm"] = filt_reset["dn"].apply(lambda x: int(x) if x > 0 else "-")
    filt_reset["List Price ₹"] = filt_reset["price"]

    edited = st.data_editor(
        filt_reset[["Add","Qty","code","desc","sub","DN mm","List Price ₹"]],
        column_config={
            "Add":          st.column_config.CheckboxColumn("✓ Add", default=False, width="small"),
            "Qty":          st.column_config.NumberColumn("Qty", min_value=1, max_value=9999, step=1, width="small"),
            "code":         st.column_config.TextColumn("Item Code", disabled=True, width="medium"),
            "desc":         st.column_config.TextColumn("Description", disabled=True, width="large"),
            "sub":          st.column_config.TextColumn("Category / Size", disabled=True, width="medium"),
            "DN mm":        st.column_config.TextColumn("DN mm", disabled=True, width="small"),
            "List Price ₹": st.column_config.NumberColumn("List Price ₹", disabled=True, format="₹%d", width="small"),
        },
        hide_index=True,
        use_container_width=True,
        height=420,
        key="catalog_editor",
    )

    if st.button("➕  Add Selected Items to BOQ", type="primary", use_container_width=True):
        sel_rows = edited[edited["Add"] == True]
        if len(sel_rows) == 0:
            st.warning("⚠️ Tick the **✓ Add** checkbox on the rows you want first.")
        else:
            added, updated = 0, 0
            existing_codes = {b["code"]: i for i, b in enumerate(st.session_state.boq)}
            for _, row in sel_rows.iterrows():
                code = row["code"]
                orig = filt[filt["code"] == code]
                if orig.empty:
                    continue
                prod = orig.iloc[0]
                qty = int(row["Qty"]) if row["Qty"] and row["Qty"] >= 1 else 1
                if code in existing_codes:
                    st.session_state.boq[existing_codes[code]]["qty"] += qty
                    updated += 1
                else:
                    st.session_state.boq.append({
                        "code": prod["code"],
                        "desc": prod["desc"],
                        "type": prod["type"],
                        "sub":  prod["sub"],
                        "dn":   int(prod["dn"]) if prod["dn"] > 0 else 0,
                        "price": float(prod["price"]),
                        "line": prod["line"],
                        "qty":  qty,
                        "disc": None,
                    })
                    added += 1
            msgs = []
            if added:   msgs.append(f"**{added}** new item(s) added")
            if updated: msgs.append(f"**{updated}** item(s) quantity updated")
            st.success(f"✅ BOQ updated — {', '.join(msgs)}. Switch to **Bill of Quantities** tab to review.")
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# TAB 2 — BILL OF QUANTITIES
# ═══════════════════════════════════════════════════════════════
with tab_boq:
    if not st.session_state.boq:
        st.info("📋 BOQ is empty — go to **Product Catalog** tab, tick items and click **Add to BOQ**.")
    else:
        gd = float(st.session_state.global_disc)

        # Build working DataFrame
        boq_df = pd.DataFrame(st.session_state.boq)
        boq_df["disc_pct"] = boq_df["disc"]   # may contain None

        # ── Editable BOQ table ───────────────────────────────────
        st.markdown("##### Edit quantities & per-item discounts below (leave Disc blank to use global)")
        edit_cols = ["code","desc","sub","dn","line","qty","disc_pct","price"]
        edited_boq = st.data_editor(
            boq_df[edit_cols].copy(),
            column_config={
                "code":     st.column_config.TextColumn("Item Code", disabled=True, width="medium"),
                "desc":     st.column_config.TextColumn("Description", disabled=True, width="large"),
                "sub":      st.column_config.TextColumn("Category/Size", disabled=True, width="medium"),
                "dn":       st.column_config.NumberColumn("DN mm", disabled=True, format="%d", width="small"),
                "line":     st.column_config.TextColumn("Line", disabled=True, width="small"),
                "qty":      st.column_config.NumberColumn("Qty", min_value=1, max_value=99999, step=1, width="small"),
                "disc_pct": st.column_config.NumberColumn(
                    f"Disc % (blank = {gd:.1f}% global)",
                    min_value=0.0, max_value=100.0, step=0.5, format="%.1f%%", width="medium"
                ),
                "price":    st.column_config.NumberColumn("List Price ₹", disabled=True, format="₹%d", width="small"),
            },
            hide_index=False,
            use_container_width=True,
            num_rows="dynamic",
            height=min(500, 80 + len(boq_df) * 38),
            key="boq_editor",
        )

        # Sync edits back to session state (qty + disc)
        remaining = []
        for i, row in edited_boq.iterrows():
            if i < len(st.session_state.boq):
                st.session_state.boq[i]["qty"]  = max(1, int(row["qty"]) if pd.notna(row["qty"]) else 1)
                st.session_state.boq[i]["disc"] = float(row["disc_pct"]) if pd.notna(row["disc_pct"]) else None
                remaining.append(st.session_state.boq[i])
        # handle deletions via num_rows=dynamic
        if len(edited_boq) < len(st.session_state.boq):
            st.session_state.boq = remaining

        # ── Calculations ──────────────────────────────────────────
        calc = edited_boq.copy()
        calc["eff_disc"]  = calc["disc_pct"].apply(lambda d: float(d) if pd.notna(d) else gd)
        calc["net_rate"]  = calc["price"] * (1 - calc["eff_disc"] / 100)
        calc["amount"]    = calc["qty"] * calc["net_rate"]
        calc["list_amt"]  = calc["qty"] * calc["price"]
        grand_total       = calc["amount"].sum()
        list_total        = calc["list_amt"].sum()
        savings           = list_total - grand_total

        # ── Summary Metrics ───────────────────────────────────────
        st.divider()
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Line Items",  len(calc))
        m2.metric("Total Units", int(calc["qty"].sum()))
        m3.metric("List Value",  f"₹{list_total:,.0f}")
        m4.metric("Savings",     f"₹{savings:,.0f}")
        m5.metric("Net Amount",  f"₹{grand_total:,.0f}")

        st.divider()

        # ── Action Buttons ────────────────────────────────────────
        ac1, ac2, ac3 = st.columns([2, 2, 1])

        # Excel Export
        def build_excel() -> BytesIO:
            output = BytesIO()
            proj = st.session_state.project or "Huliot"
            today = str(datetime.date.today())

            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                wb  = writer.book
                ws  = wb.add_worksheet("BOQ")
                writer.sheets["BOQ"] = ws

                # ── Formats ──
                f_title  = wb.add_format({"bold": True, "font_size": 14,
                                          "bg_color": "#0F172A", "font_color": "white",
                                          "valign": "vcenter"})
                f_sub    = wb.add_format({"font_size": 10, "italic": True,
                                          "font_color": "#4B5563", "valign": "vcenter"})
                f_warn   = wb.add_format({"font_size": 9, "italic": True,
                                          "font_color": "#B45309", "valign": "vcenter"})
                f_col    = wb.add_format({"bold": True, "bg_color": "#FBBF24",
                                          "font_color": "#0F172A", "border": 1,
                                          "font_size": 11, "align": "center",
                                          "valign": "vcenter", "text_wrap": True})
                f_norm   = wb.add_format({"border": 1, "valign": "vcenter"})
                f_num    = wb.add_format({"border": 1, "num_format": "#,##0",
                                          "valign": "vcenter"})
                f_money  = wb.add_format({"border": 1, "num_format": "₹#,##0.00",
                                          "valign": "vcenter"})
                f_pct    = wb.add_format({"border": 1, "num_format": "0.0%",
                                          "valign": "vcenter"})
                f_tot_l  = wb.add_format({"bold": True, "bg_color": "#0F172A",
                                          "font_color": "white", "border": 1,
                                          "font_size": 12, "valign": "vcenter"})
                f_tot_v  = wb.add_format({"bold": True, "bg_color": "#0F172A",
                                          "font_color": "#FBBF24", "border": 1,
                                          "font_size": 12, "num_format": "₹#,##0.00",
                                          "valign": "vcenter"})
                f_alt    = wb.add_format({"border": 1, "bg_color": "#F8FAFC",
                                          "valign": "vcenter"})
                f_alt_m  = wb.add_format({"border": 1, "bg_color": "#F8FAFC",
                                          "num_format": "₹#,##0.00", "valign": "vcenter"})
                f_alt_p  = wb.add_format({"border": 1, "bg_color": "#F8FAFC",
                                          "num_format": "0.0%", "valign": "vcenter"})

                # ── Column widths ──
                ws.set_column(0,  0, 5)    # Sr.No
                ws.set_column(1,  1, 18)   # Item Code
                ws.set_column(2,  2, 36)   # Description
                ws.set_column(3,  3, 16)   # Category
                ws.set_column(4,  4, 7)    # DN
                ws.set_column(5,  5, 13)   # Product Line
                ws.set_column(6,  6, 6)    # Unit
                ws.set_column(7,  7, 7)    # Qty
                ws.set_column(8,  8, 13)   # List Price
                ws.set_column(9,  9, 10)   # Disc %
                ws.set_column(10, 10, 14)  # Net Rate
                ws.set_column(11, 11, 14)  # Amount

                # ── Header rows ──
                ws.set_row(0, 24)
                ws.merge_range("A1:L1",
                    f"HULIOT PIPES & FITTINGS PVT. LTD.  —  BILL OF QUANTITIES", f_title)
                ws.set_row(1, 18)
                ws.merge_range("A2:L2",
                    f"Project: {proj}  |  Date: {today}  |  Price List W.E.F April 2026", f_sub)
                ws.set_row(2, 16)
                ws.merge_range("A3:L3",
                    "Prices ex-factory/depot  |  GST extra as applicable  |  "
                    "All prices provisional & subject to change without prior notice", f_warn)

                # ── Column headers (row 4) ──
                headers = ["Sr.No","Item Code","Description","Category/Size",
                           "DN (mm)","Product Line","Unit","Qty",
                           "List Price (₹)","Disc (%)","Net Rate (₹)","Amount (₹)"]
                ws.set_row(3, 30)
                for ci, h in enumerate(headers):
                    ws.write(3, ci, h, f_col)

                # ── Data rows ──
                for ri, (_, row) in enumerate(calc.iterrows(), start=4):
                    even = (ri % 2 == 0)
                    fn   = f_alt   if even else f_norm
                    fm   = f_alt_m if even else f_money
                    fp   = f_alt_p if even else f_pct
                    fn2  = f_alt   if even else f_norm

                    ws.write(ri, 0,  ri - 3,                 fn)
                    ws.write(ri, 1,  row["code"],             fn)
                    ws.write(ri, 2,  row["desc"],             fn)
                    ws.write(ri, 3,  row["sub"],              fn)
                    ws.write(ri, 4,  int(row["dn"]) if row["dn"] > 0 else "-",  fn)
                    ws.write(ri, 5,  row["line"],             fn)
                    ws.write(ri, 6,  "Nos",                   fn)
                    ws.write(ri, 7,  int(row["qty"]),         fn)
                    ws.write(ri, 8,  float(row["price"]),     fm)
                    ws.write(ri, 9,  float(row["eff_disc"]) / 100, fp)
                    ws.write(ri, 10, float(row["net_rate"]),  fm)
                    ws.write(ri, 11, float(row["amount"]),    fm)

                # ── Grand Total row ──
                tr = 4 + len(calc)
                ws.set_row(tr, 24)
                ws.merge_range(tr, 0, tr, 7,  "GRAND TOTAL",  f_tot_l)
                ws.write(tr, 8,  list_total,  f_tot_v)
                ws.write(tr, 9,  "",          f_tot_l)
                ws.write(tr, 10, "",          f_tot_l)
                ws.write(tr, 11, grand_total, f_tot_v)

                # ── Terms sheet ──
                tw = wb.add_worksheet("Terms & Conditions")
                tw.set_column(0, 0, 90)
                tf = wb.add_format({"font_size": 11, "valign": "vcenter"})
                th = wb.add_format({"bold": True, "font_size": 12,
                                    "bg_color": "#0F172A", "font_color": "white"})
                tw.write(0, 0, "Terms & Conditions — Huliot Pipes & Fittings Pvt. Ltd.", th)
                terms = [
                    "1. Prices are ex-factory / depot.",
                    "2. Payment: Advance Payment.",
                    "3. GST extra as applicable.",
                    "4. All disputes subject to Mumbai jurisdiction only.",
                    "5. All prices are provisional and subject to change without prior notice at sole discretion.",
                    "6. Prices at time of dispatch/invoicing shall be final and binding.",
                    "7. Force Majeure: Not liable for delay/non-performance due to events beyond control.",
                ]
                for i, t in enumerate(terms, 1):
                    tw.set_row(i, 18)
                    tw.write(i, 0, t, tf)

            output.seek(0)
            return output

        with ac1:
            fname = f"{(st.session_state.project or 'Huliot').replace(' ','_')}_BOQ_{datetime.date.today()}.xlsx"
            excel_bytes = build_excel()
            st.download_button(
                "⬇️  Export BOQ to Excel",
                data=excel_bytes,
                file_name=fname,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )

        with ac2:
            imp_file = st.file_uploader(
                "⬆️  Import BOQ from Excel",
                type=["xlsx", "xls"],
                key="import_uploader",
                label_visibility="visible"
            )
            if imp_file is not None:
                try:
                    imp_df = pd.read_excel(imp_file)
                    # Accept both exported format and simple format
                    col_aliases = {
                        "Item Code": "code", "item code": "code", "Code": "code",
                        "Qty": "qty", "QTY": "qty",
                        "Disc (%)": "disc_raw", "Discount (%)": "disc_raw",
                    }
                    imp_df = imp_df.rename(columns=col_aliases)
                    new_items = []
                    for _, r in imp_df.iterrows():
                        code = str(r.get("code", "")).strip()
                        if not code or code.lower() in ["nan", "grand total", ""]:
                            continue
                        prod = df_all[df_all["code"] == code]
                        if prod.empty:
                            continue
                        p = prod.iloc[0]
                        disc_raw = r.get("disc_raw", None)
                        disc_val = None
                        if pd.notna(disc_raw):
                            v = float(disc_raw)
                            disc_val = v * 100 if v < 1 else v  # handle % vs decimal
                        new_items.append({
                            "code": p["code"], "desc": p["desc"],
                            "type": p["type"], "sub": p["sub"],
                            "dn":   int(p["dn"]) if p["dn"] > 0 else 0,
                            "price": float(p["price"]), "line": p["line"],
                            "qty":  max(1, int(r.get("qty", 1)) if pd.notna(r.get("qty", 1)) else 1),
                            "disc": disc_val,
                        })
                    if new_items:
                        st.session_state.boq = new_items
                        st.success(f"✅ Imported **{len(new_items)}** items from Excel.")
                        st.rerun()
                    else:
                        st.error("No matching items found. Ensure 'Item Code' column matches Huliot codes.")
                except Exception as e:
                    st.error(f"Import failed: {e}")

        with ac3:
            if st.button("🗑️ Clear BOQ", type="secondary", use_container_width=True):
                st.session_state.boq = []
                st.rerun()

        # ── Disclaimer ────────────────────────────────────────────
        st.markdown("""
        <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;padding:10px 14px;
                    font-size:11px;color:#92400E;margin-top:8px;">
        ⚠️ <strong>Disclaimer:</strong> All prices are provisional and subject to change without prior notice.
        Prices at time of dispatch/invoicing shall be final and binding.
        GST extra as applicable. All disputes subject to Mumbai jurisdiction only.
        </div>
        """, unsafe_allow_html=True)
