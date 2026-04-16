import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import uuid

# ── PAGE CONFIG ──
st.set_page_config(page_title="Huliot EZE BOQ", page_icon="⚙", layout="wide")

# ── GLOBAL CSS ──
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 0.6rem; padding-bottom: 1rem;}
.stButton > button {font-weight: 700; border-radius: 8px; font-size: 12px;}
.stTextInput > div > div > input {font-size: 13px;}
.stSelectbox > div > div {font-size: 13px;}
div[data-testid="column"] > div {gap: 0.2rem;}
.stTabs [data-baseweb="tab"] {font-weight: 700; font-size: 13px;}
.stTabs [data-baseweb="tab-list"] {gap: 6px; border-bottom: 2px solid #E2E8F0;}
.huliot-hdr {background:linear-gradient(135deg,#0F172A 0%,#1E3A5F 100%);padding:12px 18px;border-radius:12px;color:white;display:flex;align-items:center;gap:12px;margin-bottom:4px;}
.huliot-logo {font-size:20px;font-weight:900;color:#FBBF24;letter-spacing:-1px;}
.sh-bar {border-radius:12px;padding:10px 16px;margin:6px 0 4px 0;display:flex;align-items:center;gap:10px;}
.boq-row {border-bottom:1px solid #F1F5F9;padding:4px 0;}
.summary-card {border-radius:12px;padding:14px;margin-bottom:8px;}
.badge {display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700;}
.dn-badge {padding:2px 8px;border-radius:10px;font-size:12px;font-weight:800;}
table.boq-tbl {width:100%;border-collapse:collapse;font-size:12px;}
table.boq-tbl th {background:#F8FAFC;padding:7px 8px;font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;border-bottom:2px solid #E2E8F0;}
table.boq-tbl td {padding:6px 8px;border-bottom:1px solid #F8FAFC;}
table.boq-tbl tr:nth-child(even) {background:#FAFBFD;}
.total-row {background:linear-gradient(90deg,#0F172A,#1E3A5F);color:white;padding:10px 14px;border-radius:0 0 10px 10px;font-weight:900;}
.sh-group-hdr {padding:10px 14px;border-radius:10px 10px 0 0;display:flex;justify-content:space-between;align-items:center;margin-top:10px;}
.footer-note {background:#FFFBEB;border-top:1px solid #FDE68A;padding:6px 14px;font-size:10px;color:#92400E;border-radius:0 0 10px 10px;}
</style>
""", unsafe_allow_html=True)

# ── PRODUCT DATA ──
def _p(code, desc, ptype, dn, price, line, sub=""):
    return {"code": code, "desc": desc, "type": ptype, "sub": sub, "dn": dn, "price": price, "line": line}

PRODUCTS = [
    # ── HT PRO PIPES ──
    _p("54040300-i","S/S Pipe L=3000mm","Pipe",40,567,"HT Pro","S/S 3000mm"),
    _p("54050300-i","S/S Pipe L=3000mm","Pipe",50,739,"HT Pro","S/S 3000mm"),
    _p("54075300-i","S/S Pipe L=3000mm","Pipe",75,1304,"HT Pro","S/S 3000mm"),
    _p("540110300-i","S/S Pipe L=3000mm","Pipe",110,1751,"HT Pro","S/S 3000mm"),
    _p("540125300-i","S/S Pipe L=3000mm","Pipe",125,3400,"HT Pro","S/S 3000mm"),
    _p("540160300-i","S/S Pipe L=3000mm","Pipe",160,4116,"HT Pro","S/S 3000mm"),
    _p("540200300-i","S/S Pipe L=3000mm","Pipe",200,8303,"HT Pro","S/S 3000mm"),
    _p("5404040300-i","D/S Pipe L=3000mm","Pipe",40,588,"HT Pro","D/S 3000mm"),
    _p("5405050300-i","D/S Pipe L=3000mm","Pipe",50,768,"HT Pro","D/S 3000mm"),
    _p("5407575300-i","D/S Pipe L=3000mm","Pipe",75,1344,"HT Pro","D/S 3000mm"),
    _p("5401111300-i","D/S Pipe L=3000mm","Pipe",110,2063,"HT Pro","D/S 3000mm"),
    _p("5401212300-i","D/S Pipe L=3000mm","Pipe",125,3518,"HT Pro","D/S 3000mm"),
    _p("5401616300-i","D/S Pipe L=3000mm","Pipe",160,4268,"HT Pro","D/S 3000mm"),
    _p("54040050-i","S/S Pipe L=500mm","Pipe",40,113,"HT Pro","S/S 500mm"),
    _p("54050050-i","S/S Pipe L=500mm","Pipe",50,147,"HT Pro","S/S 500mm"),
    _p("54075050-i","S/S Pipe L=500mm","Pipe",75,252,"HT Pro","S/S 500mm"),
    _p("540110050-i","S/S Pipe L=500mm","Pipe",110,411,"HT Pro","S/S 500mm"),
    _p("540125050-i","S/S Pipe L=500mm","Pipe",125,664,"HT Pro","S/S 500mm"),
    _p("540160050-i","S/S Pipe L=500mm","Pipe",160,812,"HT Pro","S/S 500mm"),
    _p("54040100-i","S/S Pipe L=1000mm","Pipe",40,204,"HT Pro","S/S 1000mm"),
    _p("54050100-i","S/S Pipe L=1000mm","Pipe",50,266,"HT Pro","S/S 1000mm"),
    _p("54075100-i","S/S Pipe L=1000mm","Pipe",75,462,"HT Pro","S/S 1000mm"),
    _p("540110100-i","S/S Pipe L=1000mm","Pipe",110,747,"HT Pro","S/S 1000mm"),
    _p("540125100-i","S/S Pipe L=1000mm","Pipe",125,1212,"HT Pro","S/S 1000mm"),
    _p("540160100-i","S/S Pipe L=1000mm","Pipe",160,1474,"HT Pro","S/S 1000mm"),
    _p("54040150-i","S/S Pipe L=1500mm","Pipe",40,294,"HT Pro","S/S 1500mm"),
    _p("54050150-i","S/S Pipe L=1500mm","Pipe",50,384,"HT Pro","S/S 1500mm"),
    _p("54075150-i","S/S Pipe L=1500mm","Pipe",75,672,"HT Pro","S/S 1500mm"),
    _p("540110150-i","S/S Pipe L=1500mm","Pipe",110,1085,"HT Pro","S/S 1500mm"),
    _p("540125150-i","S/S Pipe L=1500mm","Pipe",125,1759,"HT Pro","S/S 1500mm"),
    _p("540160150-i","S/S Pipe L=1500mm","Pipe",160,2134,"HT Pro","S/S 1500mm"),
    _p("54040200-i","S/S Pipe L=2000mm","Pipe",40,385,"HT Pro","S/S 2000mm"),
    _p("54050200-i","S/S Pipe L=2000mm","Pipe",50,503,"HT Pro","S/S 2000mm"),
    _p("54075200-i","S/S Pipe L=2000mm","Pipe",75,882,"HT Pro","S/S 2000mm"),
    _p("540110200-i","S/S Pipe L=2000mm","Pipe",110,1421,"HT Pro","S/S 2000mm"),
    _p("540125200-i","S/S Pipe L=2000mm","Pipe",125,2307,"HT Pro","S/S 2000mm"),
    _p("540160200-i","S/S Pipe L=2000mm","Pipe",160,2796,"HT Pro","S/S 2000mm"),
    _p("5404040100-i","D/S Pipe L=1000mm","Pipe",40,224,"HT Pro","D/S 1000mm"),
    _p("5405050100-i","D/S Pipe L=1000mm","Pipe",50,293,"HT Pro","D/S 1000mm"),
    _p("5407575100-i","D/S Pipe L=1000mm","Pipe",75,502,"HT Pro","D/S 1000mm"),
    _p("5401111100-i","D/S Pipe L=1000mm","Pipe",110,821,"HT Pro","D/S 1000mm"),
    _p("5401212100-i","D/S Pipe L=1000mm","Pipe",125,1328,"HT Pro","D/S 1000mm"),
    _p("5401616100-i","D/S Pipe L=1000mm","Pipe",160,1624,"HT Pro","D/S 1000mm"),
    _p("5404040150-i","D/S Pipe L=1500mm","Pipe",40,315,"HT Pro","D/S 1500mm"),
    _p("5405050150-i","D/S Pipe L=1500mm","Pipe",50,413,"HT Pro","D/S 1500mm"),
    _p("5407575150-i","D/S Pipe L=1500mm","Pipe",75,712,"HT Pro","D/S 1500mm"),
    _p("5401111150-i","D/S Pipe L=1500mm","Pipe",110,1157,"HT Pro","D/S 1500mm"),
    _p("5401212150-i","D/S Pipe L=1500mm","Pipe",125,1876,"HT Pro","D/S 1500mm"),
    _p("5401616150-i","D/S Pipe L=1500mm","Pipe",160,2286,"HT Pro","D/S 1500mm"),
    _p("5404040200-i","D/S Pipe L=2000mm","Pipe",40,406,"HT Pro","D/S 2000mm"),
    _p("5405050200-i","D/S Pipe L=2000mm","Pipe",50,531,"HT Pro","D/S 2000mm"),
    _p("5407575200-i","D/S Pipe L=2000mm","Pipe",75,924,"HT Pro","D/S 2000mm"),
    _p("5401111200-i","D/S Pipe L=2000mm","Pipe",110,1494,"HT Pro","D/S 2000mm"),
    _p("5401212200-i","D/S Pipe L=2000mm","Pipe",125,2423,"HT Pro","D/S 2000mm"),
    _p("5401616200-i","D/S Pipe L=2000mm","Pipe",160,2946,"HT Pro","D/S 2000mm"),
    # ── HT PRO BENDS ──
    _p("40040150","Bend 15° DN110","Bend",110,234,"HT Pro","15°"),
    _p("40040350","Bend 30° DN110","Bend",110,239,"HT Pro","30°"),
    _p("40010460-i","Bend 45° DN40","Bend",40,66,"HT Pro","45°"),
    _p("40020460-i","Bend 45° DN50","Bend",50,82,"HT Pro","45°"),
    _p("40030460-i","Bend 45° DN75","Bend",75,128,"HT Pro","45°"),
    _p("40040460-i","Bend 45° DN110","Bend",110,186,"HT Pro","45°"),
    _p("40050460","Bend 45° DN125","Bend",125,768,"HT Pro","45°"),
    _p("40060460","Bend 45° DN160","Bend",160,1013,"HT Pro","45°"),
    _p("40020467","Door Bend 45° DN50","Bend",50,149,"HT Pro","Door 45°"),
    _p("40040467","Door Bend 45° DN110","Bend",110,456,"HT Pro","Door 45°"),
    _p("40040468","Door Bend 45° Right DN110","Bend",110,386,"HT Pro","Door 45° R"),
    _p("40040469","Door Bend 45° Left DN110","Bend",110,382,"HT Pro","Door 45° L"),
    _p("40060457","Door Bend 45° DN160","Bend",160,1751,"HT Pro","Door 45°"),
    _p("40010860-i","Bend 87.5° DN40","Bend",40,72,"HT Pro","87.5°"),
    _p("40020860-i","Bend 87.5° DN50","Bend",50,77,"HT Pro","87.5°"),
    _p("40030860","Bend 87.5° DN75","Bend",75,155,"HT Pro","87.5°"),
    _p("40040860-i","Bend 87.5° DN110","Bend",110,270,"HT Pro","87.5°"),
    _p("40050860","Bend 87.5° DN125","Bend",125,700,"HT Pro","87.5°"),
    _p("40060860","Bend 87.5° DN160","Bend",160,722,"HT Pro","87.5°"),
    _p("40020867-i","Door Bend 87.5° DN50","Bend",50,221,"HT Pro","Door 87.5°"),
    _p("40040867-i","Door Bend 87.5° DN110","Bend",110,517,"HT Pro","Door 87.5°"),
    _p("40060857","Door Bend 87.5° DN160","Bend",160,2429,"HT Pro","Door 87.5°"),
    _p("40040868-i","Door Bend 87.5° Right DN110","Bend",110,553,"HT Pro","Door 87.5° R"),
    _p("40040869","Door Bend 87.5° Left DN110","Bend",110,565,"HT Pro","Door 87.5° L"),
    # ── HT PRO BRANCHES ──
    _p("40611440","Single Y 45° 40×40","Branch",40,96,"HT Pro","Y 40×40"),
    _p("40622460","Single Y 45° 50×50","Branch",50,139,"HT Pro","Y 50×50"),
    _p("40633460-i","Single Y 45° 75×75","Branch",75,262,"HT Pro","Y 75×75"),
    _p("40644460-i","Single Y 45° 110×110","Branch",110,575,"HT Pro","Y 110×110"),
    _p("40655460","Single Y 45° 125×125","Branch",125,1475,"HT Pro","Y 125×125"),
    _p("40666450","Single Y 45° 160×160","Branch",160,1942,"HT Pro","Y 160×160"),
    _p("40621440","Reducing Y 45° 50×40","Branch",50,143,"HT Pro","Red.Y 50×40"),
    _p("40632460","Reducing Y 45° 75×50","Branch",75,350,"HT Pro","Red.Y 75×50"),
    _p("40642460","Reducing Y 45° 110×50","Branch",110,361,"HT Pro","Red.Y 110×50"),
    _p("40643460","Reducing Y 45° 110×75","Branch",110,578,"HT Pro","Red.Y 110×75"),
    _p("40654460","Reducing Y 45° 125×110","Branch",125,1270,"HT Pro","Red.Y 125×110"),
    _p("40664450","Reducing Y 45° 160×110","Branch",160,1744,"HT Pro","Red.Y 160×110"),
    _p("40611860","Single Tee 90° 40×40","Branch",40,110,"HT Pro","Tee 40×40"),
    _p("40622860","Single Tee 90° 50×50","Branch",50,121,"HT Pro","Tee 50×50"),
    _p("40633860-i","Single Tee 90° 75×75","Branch",75,197,"HT Pro","Tee 75×75"),
    _p("40655860","Single Tee 90° 125×125","Branch",125,607,"HT Pro","Tee 125×125"),
    _p("40666860","Single Tee 90° 160×160","Branch",160,947,"HT Pro","Tee 160×160"),
    _p("40621860","Reducing Tee 90° 50×40","Branch",50,166,"HT Pro","Red.Tee 50×40"),
    _p("40632860","Reducing Tee 90° 75×50","Branch",75,185,"HT Pro","Red.Tee 75×50"),
    _p("40642860","Reducing Tee Short 110×50","Branch",110,392,"HT Pro","Red.Tee 110×50"),
    _p("40664860","Reducing Tee 90° 160×110","Branch",160,877,"HT Pro","Red.Tee 160×110"),
    _p("40733860-i","Swept Tee 87.5° 75×75","Branch",75,260,"HT Pro","Swept 75×75"),
    _p("40742860-i","Reducing Swept Tee 110×50","Branch",110,436,"HT Pro","Swept 110×50"),
    _p("40743860-i","Reducing Swept Tee 110×75","Branch",110,550,"HT Pro","Swept 110×75"),
    _p("40744860-i","Swept Tee 87.5° 110×110","Branch",110,510,"HT Pro","Swept 110×110"),
    _p("40754860","Reducing Swept Tee 125×110","Branch",125,1080,"HT Pro","Swept 125×110"),
    _p("14040764860-i","Reducing Swept Tee 160×110","Branch",160,2086,"HT Pro","Swept 160×110"),
    _p("41044860","Double Swept Tee 110×110×110","Branch",110,2023,"HT Pro","Dbl Swept"),
    _p("40733867-i","Door Swept Tee 75×75","Branch",75,460,"HT Pro","Door Swept 75×75"),
    _p("40742867-i","Door Swept Tee 110×50","Branch",110,616,"HT Pro","Door Swept 110×50"),
    _p("40743867-i","Door Swept Tee 110×75","Branch",110,732,"HT Pro","Door Swept 110×75"),
    _p("40744867-i","Door Swept Tee 110×110","Branch",110,754,"HT Pro","Door Swept 110×110"),
    _p("41244850","Corner Branch 87° 110×110×110","Branch",110,1346,"HT Pro","Corner 110"),
    _p("4041254850","Corner Branch 87° 125×110×110","Branch",125,1968,"HT Pro","Corner 125"),
    _p("41264850-i","Red. Corner Branch 160×110×110","Branch",160,2382,"HT Pro","Corner 160"),
    _p("41044450","Double Y 110×110×110","Branch",110,1463,"HT Pro","Dbl Y 110"),
    _p("41044457","Double Y Door 110×110×110","Branch",110,3106,"HT Pro","Dbl Y Door"),
    # ── HT PRO TRAPS ──
    _p("49540750G-i","P Trap 50mm Water Seal","Trap",110,1132,"HT Pro","P Trap"),
    _p("41840051-i","S Trap Siphon Type","Trap",110,2262,"HT Pro","S Trap"),
    _p("69111750G-i","Nahani Trap 110×75","Trap",110,649,"HT Pro","Nahani Trap"),
    _p("60117051","Multi Floor Trap MFT","Trap",110,1256,"HT Pro","MFT"),
    _p("14048111060G-i","Multi Floor Trap with Socket","Trap",110,1680,"HT Pro","MFT Socketed"),
    _p("41242850-i","Ht. Riser 2-Inlet 90°","Trap",110,1061,"HT Pro","Riser 2-Inlet"),
    _p("4102042860","Hopper 3-Inlet","Trap",110,1380,"HT Pro","Hopper 3-Inlet"),
    _p("69201551G-i","Height Riser L150 MFT","Trap",110,497,"HT Pro","Riser L150"),
    _p("69203551G-i","Height Riser L350 MFT","Trap",110,737,"HT Pro","Riser L350"),
    _p("4049911100G-i","H.A.F.F Stack Single Stack","Trap",110,6600,"HT Pro","HAFF Stack"),
    # ── HT PRO INSPECTION ──
    _p("49130060-i","Inspection Pipe DN75","Inspection",75,460,"HT Pro","Cleaning Pipe"),
    _p("49140060-i","Inspection Pipe DN110","Inspection",110,566,"HT Pro","Cleaning Pipe"),
    _p("49150060","Inspection Pipe DN125","Inspection",125,1061,"HT Pro","Cleaning Pipe"),
    _p("49160060","Inspection Pipe DN160","Inspection",160,1199,"HT Pro","Cleaning Pipe"),
    # ── HT PRO COUPLERS ──
    _p("41710055-i","Coupler DN40","Coupler",40,73,"HT Pro","Coupler"),
    _p("41720055-i","Coupler DN50","Coupler",50,85,"HT Pro","Coupler"),
    _p("41730050-i","Coupler DN75","Coupler",75,115,"HT Pro","Coupler"),
    _p("41740055-i","Coupler DN110","Coupler",110,210,"HT Pro","Coupler"),
    _p("41750065","Coupler DN125","Coupler",125,494,"HT Pro","Coupler"),
    _p("41760055","Coupler DN160","Coupler",160,1054,"HT Pro","Coupler"),
    _p("41720053","Sleeve DN50","Coupler",50,115,"HT Pro","Sleeve"),
    _p("41730053","Sleeve DN75","Coupler",75,128,"HT Pro","Sleeve"),
    _p("41740053","Sleeve DN110","Coupler",110,215,"HT Pro","Sleeve"),
    # ── HT PRO REDUCERS ──
    _p("42121060","Eccentric Reducer 50×40","Reducer",50,66,"HT Pro","Ecc.Red"),
    _p("42132050","Eccentric Reducer 75×50","Reducer",75,83,"HT Pro","Ecc.Red"),
    _p("42142050","Eccentric Reducer 110×50","Reducer",110,182,"HT Pro","Ecc.Red"),
    _p("42143050-i","Eccentric Reducer 110×75","Reducer",110,215,"HT Pro","Ecc.Red"),
    _p("42154060","Eccentric Reducer 125×110","Reducer",125,421,"HT Pro","Ecc.Red"),
    _p("42164050","Eccentric Reducer 160×110","Reducer",160,653,"HT Pro","Ecc.Red"),
    _p("42134050-i","Eccentric Reverse Reducer 110×75","Reducer",110,510,"HT Pro","Rev.Red"),
    _p("P0500000000040K","Concentric Reducer Bushing 50×40","Reducer",50,192,"HT Pro","Con.Red"),
    _p("P07500000050K","Concentric Reducer Bushing 75×50","Reducer",75,253,"HT Pro","Con.Red"),
    _p("P1100000000050V","Concentric Reducer Bushing 110×50","Reducer",110,328,"HT Pro","Con.Red"),
    _p("P1100000000075V","Concentric Reducer Bushing 110×75","Reducer",110,401,"HT Pro","Con.Red"),
    # ── HT PRO ACCESSORIES ──
    _p("41610040","End Cap DN40","Accessory",40,35,"HT Pro","End Cap"),
    _p("41620050-i","End Cap DN50","Accessory",50,66,"HT Pro","End Cap"),
    _p("41630050-i","End Cap DN75","Accessory",75,70,"HT Pro","End Cap"),
    _p("41640050-i","End Cap DN110","Accessory",110,115,"HT Pro","End Cap"),
    _p("41650060","End Cap DN125","Accessory",125,251,"HT Pro","End Cap"),
    _p("41660060","End Cap DN160","Accessory",160,344,"HT Pro","End Cap"),
    _p("4042320040","Vent Cowl DN50","Accessory",50,239,"HT Pro","Vent Cowl"),
    _p("4042330040","Vent Cowl DN75","Accessory",75,185,"HT Pro","Vent Cowl"),
    _p("4042340060","Vent Cowl DN110","Accessory",110,194,"HT Pro","Vent Cowl"),
    _p("4042360040","Vent Cowl DN160","Accessory",160,413,"HT Pro","Vent Cowl"),
    _p("5401106650-i","Boss Connector 1-Inlet 110×L660","Accessory",110,1004,"HT Pro","Boss Pipe"),
    _p("540110502-i","Boss Connector Double Branch","Accessory",110,1404,"HT Pro","Boss Pipe"),
    _p("540110503-i","Boss Connector Triple Branch","Accessory",110,1604,"HT Pro","Boss Pipe"),
    _p("41540020","WC Connector Straight White","Accessory",110,1558,"HT Pro","WC Connector"),
    _p("41540027","WC Connector with Inspection","Accessory",110,1776,"HT Pro","WC Door"),
    _p("41542866","WC Bend Back Inspection","Accessory",110,1559,"HT Pro","WC Bend"),
    _p("41540615","Flange for WC Bend","Accessory",110,66,"HT Pro","WC Flange"),
    _p("60150331","Aquaslim S.Steel L=330mm","Accessory",0,1288,"HT Pro","Shower Channel"),
    _p("60150701","Aquaslim S.Steel L=700mm","Accessory",0,1790,"HT Pro","Shower Channel"),
    _p("47700012","Lubricant 250ml","Accessory",0,198,"HT Pro","Lubricant"),
    # ── HT PRO CLAMPS ──
    _p("48100040-S","Split Clamp DN40","Clamp",40,126,"HT Pro","Clamp"),
    _p("48100050-S","Split Clamp DN50","Clamp",50,138,"HT Pro","Clamp"),
    _p("48100075-S","Split Clamp DN75","Clamp",75,174,"HT Pro","Clamp"),
    _p("48100011-S","Split Clamp DN110","Clamp",110,210,"HT Pro","Clamp"),
    _p("48100012-S","Split Clamp DN125","Clamp",125,246,"HT Pro","Clamp"),
    _p("48100016-S","Split Clamp DN160","Clamp",160,300,"HT Pro","Clamp"),
    _p("48100020-S","Split Clamp DN200","Clamp",200,354,"HT Pro","Clamp"),
    # ── ULTRA SILENT PIPES ──
    _p("5753200300-i","US S/S Pipe L=3000mm","Pipe",32,948,"Ultra Silent","S/S 3000mm"),
    _p("5754000300-i","US S/S Pipe L=3000mm","Pipe",40,1027,"Ultra Silent","S/S 3000mm"),
    _p("5755000300-i","US S/S Pipe L=3000mm","Pipe",50,1313,"Ultra Silent","S/S 3000mm"),
    _p("5757500300-i","US S/S Pipe L=3000mm","Pipe",75,2521,"Ultra Silent","S/S 3000mm"),
    _p("5751100300-i","US S/S Pipe L=3000mm","Pipe",110,2953,"Ultra Silent","S/S 3000mm"),
    _p("5751200300-i","US S/S Pipe L=3000mm","Pipe",125,4165,"Ultra Silent","S/S 3000mm"),
    _p("5751600300-i","US S/S Pipe L=3000mm","Pipe",160,6060,"Ultra Silent","S/S 3000mm"),
    _p("5752000300-i","US S/S Pipe L=3000mm","Pipe",200,8520,"Ultra Silent","S/S 3000mm"),
    _p("5754040300-i","US D/S Pipe L=3000mm","Pipe",40,1061,"Ultra Silent","D/S 3000mm"),
    _p("5755050300-i","US D/S Pipe L=3000mm","Pipe",50,1358,"Ultra Silent","D/S 3000mm"),
    _p("5757575300-i","US D/S Pipe L=3000mm","Pipe",75,2593,"Ultra Silent","D/S 3000mm"),
    _p("5751111300-i","US D/S Pipe L=3000mm","Pipe",110,3110,"Ultra Silent","D/S 3000mm"),
    _p("5751212300-i","US D/S Pipe L=3000mm","Pipe",125,4300,"Ultra Silent","D/S 3000mm"),
    _p("5751616300-i","US D/S Pipe L=3000mm","Pipe",160,6812,"Ultra Silent","D/S 3000mm"),
    _p("5754000100-i","US S/S Pipe L=1000mm","Pipe",40,366,"Ultra Silent","S/S 1000mm"),
    _p("5755000100-i","US S/S Pipe L=1000mm","Pipe",50,468,"Ultra Silent","S/S 1000mm"),
    _p("5757500100-i","US S/S Pipe L=1000mm","Pipe",75,890,"Ultra Silent","S/S 1000mm"),
    _p("5751100100-i","US S/S Pipe L=1000mm","Pipe",110,1201,"Ultra Silent","S/S 1000mm"),
    _p("5751600100-i","US S/S Pipe L=1000mm","Pipe",160,2340,"Ultra Silent","S/S 1000mm"),
    _p("5754000150-i","US S/S Pipe L=1500mm","Pipe",40,531,"Ultra Silent","S/S 1500mm"),
    _p("5755000150-i","US S/S Pipe L=1500mm","Pipe",50,680,"Ultra Silent","S/S 1500mm"),
    _p("5757500150-i","US S/S Pipe L=1500mm","Pipe",75,1297,"Ultra Silent","S/S 1500mm"),
    _p("5751100150-i","US S/S Pipe L=1500mm","Pipe",110,1751,"Ultra Silent","S/S 1500mm"),
    _p("5751600150-i","US S/S Pipe L=1500mm","Pipe",160,3407,"Ultra Silent","S/S 1500mm"),
    _p("5754000200-i","US S/S Pipe L=2000mm","Pipe",40,697,"Ultra Silent","S/S 2000mm"),
    _p("5755000200-i","US S/S Pipe L=2000mm","Pipe",50,890,"Ultra Silent","S/S 2000mm"),
    _p("5757500200-i","US S/S Pipe L=2000mm","Pipe",75,1705,"Ultra Silent","S/S 2000mm"),
    _p("5751100200-i","US S/S Pipe L=2000mm","Pipe",110,2300,"Ultra Silent","S/S 2000mm"),
    _p("5751600200-i","US S/S Pipe L=2000mm","Pipe",160,4472,"Ultra Silent","S/S 2000mm"),
    # ── ULTRA SILENT BENDS ──
    _p("7070010170","US Bend 15° DN40","Bend",40,82,"Ultra Silent","15°"),
    _p("7070020170","US Bend 15° DN50","Bend",50,102,"Ultra Silent","15°"),
    _p("7070030170","US Bend 15° DN75","Bend",75,184,"Ultra Silent","15°"),
    _p("7070040170","US Bend 15° DN110","Bend",110,698,"Ultra Silent","15°"),
    _p("7070060170","US Bend 15° DN160","Bend",160,1357,"Ultra Silent","15°"),
    _p("7070010370","US Bend 30° DN40","Bend",40,102,"Ultra Silent","30°"),
    _p("7070020370","US Bend 30° DN50","Bend",50,102,"Ultra Silent","30°"),
    _p("7070030370","US Bend 30° DN75","Bend",75,205,"Ultra Silent","30°"),
    _p("7070040370","US Bend 30° DN110","Bend",110,727,"Ultra Silent","30°"),
    _p("7070060370","US Bend 30° DN160","Bend",160,1330,"Ultra Silent","30°"),
    _p("7070010470","US Bend 45° DN40","Bend",40,82,"Ultra Silent","45°"),
    _p("7070020470","US Bend 45° DN50","Bend",50,122,"Ultra Silent","45°"),
    _p("7070030470-i","US Bend 45° DN75","Bend",75,205,"Ultra Silent","45°"),
    _p("7070040470-i","US Bend 45° DN110","Bend",110,641,"Ultra Silent","45°"),
    _p("7070050470","US Bend 45° DN125","Bend",125,899,"Ultra Silent","45°"),
    _p("7070060470","US Bend 45° DN160","Bend",160,1202,"Ultra Silent","45°"),
    _p("7070080470","US Bend 45° DN200","Bend",200,3493,"Ultra Silent","45°"),
    _p("7070010870","US Bend 87.5° DN40","Bend",40,102,"Ultra Silent","87.5°"),
    _p("7070020870-i","US Bend 87.5° DN50","Bend",50,143,"Ultra Silent","87.5°"),
    _p("7070030870","US Bend 87.5° DN75","Bend",75,224,"Ultra Silent","87.5°"),
    _p("7070040870","US Bend 87.5° DN110","Bend",110,697,"Ultra Silent","87.5°"),
    _p("7070050870","US Bend 87.5° DN125","Bend",125,1062,"Ultra Silent","87.5°"),
    _p("7070060870","US Bend 87.5° DN160","Bend",160,2122,"Ultra Silent","87.5°"),
    _p("7070040877-i","US Door Bend 87.5° DN110","Bend",110,1054,"Ultra Silent","Door 87.5°"),
    # ── ULTRA SILENT BRANCHES ──
    _p("7070611470","US Wye 45° 40×40","Branch",40,274,"Ultra Silent","Y 40×40"),
    _p("7070622470","US Wye 45° 50×50","Branch",50,390,"Ultra Silent","Y 50×50"),
    _p("7070632470","US Wye 45° 75×50","Branch",75,523,"Ultra Silent","Y 75×50"),
    _p("7070633470","US Wye 45° 75×75","Branch",75,698,"Ultra Silent","Y 75×75"),
    _p("7070642470","US Wye 45° 110×50","Branch",110,640,"Ultra Silent","Y 110×50"),
    _p("7070643470-i","US Wye 45° 110×75","Branch",110,959,"Ultra Silent","Y 110×75"),
    _p("7070644470-i","US Wye 45° 110×110","Branch",110,1183,"Ultra Silent","Y 110×110"),
    _p("7070654470","US Wye 45° 125×110","Branch",125,1489,"Ultra Silent","Y 125×110"),
    _p("7070664470","US Wye 45° 160×110","Branch",160,2672,"Ultra Silent","Y 160×110"),
    _p("7070744870","US Swept Tee 87.5° 110×110","Branch",110,1081,"Ultra Silent","Swept 110×110"),
    _p("7070743870","US Swept Tee 87.5° 110×75","Branch",110,938,"Ultra Silent","Swept 110×75"),
    _p("7070754870","US Swept Tee 87.5° 125×110","Branch",125,1062,"Ultra Silent","Swept 125×110"),
    _p("7070764870","US Swept Tee 87.5° 160×110","Branch",160,2366,"Ultra Silent","Swept 160×110"),
    _p("7070744877","US Door Swept Tee 110×110","Branch",110,1342,"Ultra Silent","Door Swept 110×110"),
    _p("7071244870","US Corner Branch 110×110×110","Branch",110,1285,"Ultra Silent","Corner 110"),
    _p("7071264870-i","US Corner Branch 160×110×110","Branch",160,2582,"Ultra Silent","Corner 160"),
    # ── ULTRA SILENT TRAPS ──
    _p("49540750B-i","US P Trap 50mm Water Seal","Trap",110,1435,"Ultra Silent","P Trap"),
    _p("7071840070-i","US S Trap 110mm","Trap",110,2870,"Ultra Silent","S Trap"),
    _p("60117060","US Multi Floor Trap W/O Ring","Trap",110,1496,"Ultra Silent","MFT"),
    _p("S11050505075-i","US Multi Floor Trap With Ring","Trap",110,1778,"Ultra Silent","MFT With Ring"),
    _p("69111750B-i","US Nahani Trap","Trap",110,781,"Ultra Silent","Nahani Trap"),
    _p("7079911100B-i","US H.A.F.F Stack","Trap",110,9000,"Ultra Silent","HAFF Stack"),
    _p("70114500","SmartLock Trap 140/50 Single","Trap",50,1243,"Ultra Silent","SmartLock"),
    _p("70124590","SmartLock Trap 245/40/50 Multi","Trap",50,2047,"Ultra Silent","SmartLock Multi"),
    # ── ULTRA SILENT INSPECTION ──
    _p("7079120070","US Inspection Pipe DN50","Inspection",50,349,"Ultra Silent","Inspection"),
    _p("7079130070","US Inspection Pipe DN75","Inspection",75,821,"Ultra Silent","Inspection"),
    _p("7079140070","US Inspection Pipe DN110","Inspection",110,1530,"Ultra Silent","Inspection"),
    _p("7079160070","US Inspection Pipe DN160","Inspection",160,1859,"Ultra Silent","Inspection"),
    # ── ULTRA SILENT COUPLERS ──
    _p("7071720275","US One Way Socket DN50","Coupler",50,194,"Ultra Silent","Coupler"),
    _p("7071730275-i","US One Way Socket DN75","Coupler",75,352,"Ultra Silent","Coupler"),
    _p("7071740275-i","US One Way Socket DN110","Coupler",110,640,"Ultra Silent","Coupler"),
    _p("7071760275","US One Way Socket DN160","Coupler",160,1717,"Ultra Silent","Coupler"),
    # ── ULTRA SILENT REDUCERS ──
    _p("7072121070","US Reducer 50×40","Reducer",50,398,"Ultra Silent","Reducer"),
    _p("7072132070","US Reducer 75×50","Reducer",75,426,"Ultra Silent","Reducer"),
    _p("7072142070","US Reducer 110×50","Reducer",110,469,"Ultra Silent","Reducer"),
    _p("7072143070","US Reducer 110×75","Reducer",110,491,"Ultra Silent","Reducer"),
    _p("7072154070","US Reducer 125×110","Reducer",125,613,"Ultra Silent","Reducer"),
    _p("7072164070","US Reducer 160×110","Reducer",160,1021,"Ultra Silent","Reducer"),
    # ── ULTRA SILENT ACCESSORIES ──
    _p("7071620070-i","US End Cap DN50","Accessory",50,78,"Ultra Silent","End Cap"),
    _p("7071630070","US End Cap DN75","Accessory",75,157,"Ultra Silent","End Cap"),
    _p("7071640070-i","US End Cap DN110","Accessory",110,352,"Ultra Silent","End Cap"),
    _p("7071660070","US End Cap DN160","Accessory",160,768,"Ultra Silent","End Cap"),
    _p("7072340000","US Lock Seal DN110","Accessory",110,965,"Ultra Silent","Lock Seal"),
    _p("7078004000","US End Lock DN110","Accessory",110,1518,"Ultra Silent","End Lock"),
    # ── ULTRA SILENT CLAMPS ──
    _p("7890004070-S","US HD Clamp DN40","Clamp",40,228,"Ultra Silent","HD Clamp"),
    _p("7890005070-S","US HD Clamp DN50","Clamp",50,258,"Ultra Silent","HD Clamp"),
    _p("7890007570-S","US HD Clamp DN75","Clamp",75,312,"Ultra Silent","HD Clamp"),
    _p("7890011070-S","US HD Clamp DN110","Clamp",110,408,"Ultra Silent","HD Clamp"),
    _p("7890012570-S","US HD Clamp DN125","Clamp",125,432,"Ultra Silent","HD Clamp"),
    _p("7890016070-S","US HD Clamp DN160","Clamp",160,540,"Ultra Silent","HD Clamp"),
    _p("7890020070-S","US HD Clamp DN200","Clamp",200,630,"Ultra Silent","HD Clamp"),
]

# ── CONSTANTS ──
SH_CODES = ["NA"] + [f"SH{i:02d}" for i in range(1, 51)] + [f"K{i:02d}" for i in range(1, 51)]
QUICK_SH  = ["NA"] + [f"SH{i:02d}" for i in range(1, 11)] + [f"K{i:02d}" for i in range(1, 6)]
CATS = ["Pipe","Bend","Branch","Trap","Coupler","Reducer","Inspection","Clamp","Accessory"]
CAT_ICONS = {"Pipe":"▭","Bend":"↩","Branch":"⑂","Trap":"⊔","Coupler":"○","Reducer":"◁","Inspection":"◎","Clamp":"⊓","Accessory":"⚙"}
CAT_COLORS = {"Pipe":"#1D4ED8","Bend":"#B45309","Branch":"#065F46","Trap":"#6D28D9","Coupler":"#0E7490","Reducer":"#3730A3","Inspection":"#92400E","Clamp":"#991B1B","Accessory":"#374151"}
DN_LIST = [32, 40, 50, 75, 110, 125, 160, 200]
DN_COLORS = {32:"#7C3AED",40:"#1D4ED8",50:"#0E7490",75:"#065F46",110:"#B45309",125:"#B91C1C",160:"#9D174D",200:"#3730A3"}

# ── SESSION STATE INIT ──
_defaults = {
    "boq": [], "global_sh": "NA", "line": "HT Pro",
    "dn_f": None, "cat_f": None, "srch": "",
    "proj": "", "g_disc": 0,
    "boq_fsh": "ALL",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── HELPERS ──
def sh_colors(c):
    if c == "NA":
        return "#64748B", "#F1F5F9", "#94A3B8"
    if c.startswith("SH"):
        return "#1D4ED8", "#DBEAFE", "#3B82F6"
    return "#065F46", "#D1FAE5", "#10B981"

def fmt(n):
    return f"₹{int(round(n)):,}"

def eff_disc(b):
    return b["disc"] if b["disc"] is not None else st.session_state.g_disc

def net_rate(b):
    return b["price"] * (1 - eff_disc(b) / 100)

def amt(b):
    return b["qty"] * net_rate(b)

def grand():
    return sum(amt(b) for b in st.session_state.boq)

def add_to_boq(prod, qty):
    sh = st.session_state.global_sh
    for item in st.session_state.boq:
        if item["code"] == prod["code"] and item["shaft"] == sh:
            item["qty"] += qty
            return
    st.session_state.boq.append({
        **prod, "qty": qty, "disc": None,
        "shaft": sh, "_id": str(uuid.uuid4())[:8]
    })

def get_filtered():
    ps = [p for p in PRODUCTS if p["line"] == st.session_state.line]
    if st.session_state.dn_f:
        ps = [p for p in ps if p["dn"] == st.session_state.dn_f]
    if st.session_state.cat_f:
        ps = [p for p in ps if p["type"] == st.session_state.cat_f]
    if st.session_state.srch:
        q = st.session_state.srch.lower()
        ps = [p for p in ps if q in p["desc"].lower() or q in p["code"].lower() or q in p.get("sub","").lower()]
    return ps

def get_dn_counts():
    m = {}
    for p in PRODUCTS:
        if p["line"] == st.session_state.line and p["dn"] > 0:
            m[p["dn"]] = m.get(p["dn"], 0) + 1
    return m

def boq_sh_counts():
    m = {}
    for b in st.session_state.boq:
        sh = b.get("shaft", "NA")
        m[sh] = m.get(sh, 0) + 1
    return m

def sh_label(c):
    if c == "NA": return "NA — Unassigned"
    if c.startswith("SH"): return f"{c} — Shaft {int(c[2:])}"
    return f"{c} — Kitchen/Flat {int(c[1:])}"

# ── EXCEL EXPORT ──
def export_excel():
    wb = openpyxl.Workbook()
    boq = st.session_state.boq
    proj = st.session_state.proj or "Huliot"

    # ── Shared styles ──
    hdr_fill  = PatternFill("solid", fgColor="0F172A")
    hdr_font  = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
    hdr_align = Alignment(horizontal="center", vertical="center", wrap_text=False)
    alt_fill  = PatternFill("solid", fgColor="F8FAFC")
    tot_fill  = PatternFill("solid", fgColor="1E3A5F")
    tot_font  = Font(bold=True, color="FBBF24", name="Calibri", size=12)
    sub_font  = Font(bold=True, name="Calibri", size=11)
    thin      = Side(style="thin", color="E2E8F0")
    border    = Border(bottom=Side(style="thin", color="E2E8F0"))

    def write_header(ws, headers, widths, fill=hdr_fill):
        for c, (h, w) in enumerate(zip(headers, widths), 1):
            cell = ws.cell(1, c, h)
            cell.font = hdr_font; cell.fill = fill
            cell.alignment = hdr_align
            ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width = w
        ws.row_dimensions[1].height = 22
        ws.freeze_panes = "A2"

    def align(ws, row, rights=(), centers=()):
        for c in range(1, ws.max_column + 1):
            cell = ws.cell(row, c)
            if c in rights:   cell.alignment = Alignment(horizontal="right",  vertical="center")
            elif c in centers: cell.alignment = Alignment(horizontal="center", vertical="center")
            else:              cell.alignment = Alignment(horizontal="left",   vertical="center")

    # ══════════════════════════════════════════
    # SHEET 1 — Full BOQ (Aggregated, All Shafts Combined)
    # Same as the "All" tab in the app
    # ══════════════════════════════════════════
    ws = wb.active
    ws.title = "Full BOQ"
    ws.sheet_view.showGridLines = False

    agg_headers = ["Sr.No","Item Code","Description","Type","DN","Unit",
                   "Total Qty","List Price (₹)","Disc%","Net Rate (₹)","Amount (₹)","Shafts / Location","Line"]
    agg_widths  = [6, 22, 42, 14, 6, 5, 9, 14, 7, 14, 14, 28, 12]
    write_header(ws, agg_headers, agg_widths)

    # Aggregate by item code (same logic as app "All" view)
    agg = {}
    for b in boq:
        key = b["code"]
        if key not in agg:
            agg[key] = {**b, "qty": b["qty"], "shafts": [b.get("shaft","NA")]}
        else:
            agg[key]["qty"] += b["qty"]
            sh = b.get("shaft","NA")
            if sh not in agg[key]["shafts"]:
                agg[key]["shafts"].append(sh)

    agg_rows = list(agg.values())
    grand_total = sum(r["qty"] * net_rate(r) for r in agg_rows)

    for i, r in enumerate(agg_rows, 2):
        nr = net_rate(r)
        a  = round(r["qty"] * nr, 2)
        shafts_str = ", ".join(sorted(r["shafts"]))
        row_data = [
            i-1, r["code"], r["desc"], r["sub"],
            r["dn"] if r["dn"] else "-", "Nos",
            r["qty"], r["price"], eff_disc(r),
            round(nr,2), a, shafts_str, r["line"]
        ]
        for c, v in enumerate(row_data, 1):
            cell = ws.cell(i, c, v)
            cell.border = border
        align(ws, i, rights=(8,10,11), centers=(1,5,6,7,9))
        # Highlight total qty column
        qty_cell = ws.cell(i, 7)
        qty_cell.font = Font(bold=True, color="1D4ED8", name="Calibri", size=11)
        # Shade shafts column light blue
        sh_cell = ws.cell(i, 12)
        sh_cell.fill = PatternFill("solid", fgColor="DBEAFE")
        sh_cell.font = Font(color="1D4ED8", name="Calibri", size=9)
        if i % 2 == 0:
            for c in range(1, len(row_data)+1):
                if c not in (7, 12):  # keep highlights on qty/shaft cols
                    ws.cell(i, c).fill = alt_fill

    # Grand total row
    gt_row = len(agg_rows) + 2
    ws.cell(gt_row, 3, "GRAND TOTAL — ALL SHAFTS COMBINED").font = Font(bold=True, name="Calibri", size=11, color="0F172A")
    ws.cell(gt_row, 7, sum(r["qty"] for r in agg_rows)).font = Font(bold=True, color="1D4ED8", name="Calibri", size=12)
    ws.cell(gt_row, 7).alignment = Alignment(horizontal="center")
    gt_cell = ws.cell(gt_row, 11, round(grand_total, 2))
    gt_cell.font = tot_font; gt_cell.fill = tot_fill
    gt_cell.alignment = Alignment(horizontal="right")
    ws.cell(gt_row, 12, f"{len(boq)} entries across {len(set(b.get('shaft','NA') for b in boq))} locations").font = Font(italic=True, color="64748B", name="Calibri", size=9)

    # ══════════════════════════════════════════
    # SHEET 2 — Detail BOQ (every entry, with shaft per row)
    # ══════════════════════════════════════════
    ws_det = wb.create_sheet("Detail BOQ")
    ws_det.sheet_view.showGridLines = False
    det_headers = ["Sr.No","Location","Item Code","Description","Type","DN","Unit",
                   "Qty","List Price (₹)","Disc%","Net Rate (₹)","Amount (₹)","Line"]
    det_widths   = [6, 10, 22, 42, 14, 6, 5, 6, 14, 7, 14, 14, 12]
    write_header(ws_det, det_headers, det_widths)

    detail_total = 0
    for i, b in enumerate(boq, 2):
        nd = eff_disc(b); nr = net_rate(b); a = round(amt(b), 2); detail_total += a
        fg_loc = "DBEAFE" if b.get("shaft","NA").startswith("SH") else "D1FAE5" if b.get("shaft","NA").startswith("K") else "F1F5F9"
        row_data = [i-1, b.get("shaft","NA"), b["code"], b["desc"], b["sub"],
                    b["dn"] if b["dn"] else "-", "Nos", b["qty"],
                    b["price"], nd, round(nr,2), a, b["line"]]
        for c, v in enumerate(row_data, 1):
            cell = ws_det.cell(i, c, v)
            cell.border = border
        align(ws_det, i, rights=(9,11,12), centers=(1,6,7,8,10))
        ws_det.cell(i, 2).fill = PatternFill("solid", fgColor=fg_loc)
        ws_det.cell(i, 2).font = Font(bold=True, name="Calibri", size=10,
                                       color="1D4ED8" if b.get("shaft","NA").startswith("SH") else "065F46" if b.get("shaft","NA").startswith("K") else "64748B")
        if i % 2 == 0:
            for c in range(1, len(row_data)+1):
                if c != 2: ws_det.cell(i, c).fill = alt_fill

    dt_row = len(boq) + 2
    ws_det.cell(dt_row, 4, "GRAND TOTAL").font = Font(bold=True, name="Calibri", size=11)
    gt2 = ws_det.cell(dt_row, 12, round(detail_total, 2))
    gt2.font = tot_font; gt2.fill = tot_fill; gt2.alignment = Alignment(horizontal="right")

    # ══════════════════════════════════════════
    # Per-shaft sheets (unchanged logic, cleaner style)
    # ══════════════════════════════════════════
    shaft_groups = {}
    for b in boq:
        sh = b.get("shaft", "NA")
        shaft_groups.setdefault(sh, []).append(b)

    for sh, items in sorted(shaft_groups.items()):
        ws2 = wb.create_sheet(sh[:31])
        ws2.sheet_view.showGridLines = False
        fg_hex = "1D4ED8" if sh.startswith("SH") else "065F46" if sh.startswith("K") else "475569"
        sh_fill = PatternFill("solid", fgColor=fg_hex)
        sh_hdrs = ["Sr.No","Item Code","Description","Type","DN","Unit",
                   "Qty","List Price (₹)","Disc%","Net Rate (₹)","Amount (₹)"]
        sh_widths = [6,22,42,14,6,5,6,14,7,14,14]
        write_header(ws2, sh_hdrs, sh_widths, fill=sh_fill)

        subtotal = 0
        for i, b in enumerate(items, 2):
            nd = eff_disc(b); nr = net_rate(b); a = round(amt(b),2); subtotal += a
            row_data = [i-1, b["code"], b["desc"], b["sub"],
                        b["dn"] if b["dn"] else "-", "Nos",
                        b["qty"], b["price"], nd, round(nr,2), a]
            for c, v in enumerate(row_data, 1):
                cell = ws2.cell(i, c, v); cell.border = border
            align(ws2, i, rights=(8,10,11), centers=(1,5,6,7,9))
            if i % 2 == 0:
                for c in range(1, len(row_data)+1):
                    ws2.cell(i, c).fill = alt_fill

        # Subtotal row
        sub_row = len(items) + 2
        ws2.cell(sub_row, 3, f"SUBTOTAL — {sh}").font = sub_font
        st_cell = ws2.cell(sub_row, 11, round(subtotal, 2))
        st_cell.font = Font(bold=True, color=fg_hex, name="Calibri", size=12)
        st_cell.fill  = PatternFill("solid", fgColor="F8FAFC")
        st_cell.alignment = Alignment(horizontal="right")
        ws2.cell(sub_row, 7, sum(b["qty"] for b in items)).font = Font(bold=True, color=fg_hex, name="Calibri", size=11)
        ws2.cell(sub_row, 7).alignment = Alignment(horizontal="center")

    buf = BytesIO()
    wb.save(buf); buf.seek(0)
    return buf

# ── EXCEL IMPORT ──
def import_excel(uploaded):
    wb = openpyxl.load_workbook(uploaded)
    ws = wb["Full BOQ"] if "Full BOQ" in wb.sheetnames else wb.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    added = 0
    for row in rows:
        if not row[2] or str(row[3]).startswith("───"):
            continue
        code = str(row[2]).strip()
        prod = next((p for p in PRODUCTS if p["code"] == code), None)
        shaft = str(row[1] or "NA").strip()
        qty = int(row[7] or 1)
        disc = float(row[9]) if row[9] is not None else None
        if prod:
            item = {**prod, "qty": qty, "disc": disc, "shaft": shaft, "_id": str(uuid.uuid4())[:8]}
        else:
            item = {"code": code, "desc": str(row[3] or ""), "type": "Imported",
                    "sub": str(row[4] or ""), "dn": int(row[5]) if row[5] and str(row[5]).isdigit() else 0,
                    "price": float(row[8] or 0), "line": str(row[12] or "HT Pro"),
                    "qty": qty, "disc": disc, "shaft": shaft, "_id": str(uuid.uuid4())[:8]}
        st.session_state.boq.append(item)
        added += 1
    return added

# ══════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════
hc1, hc2, hc3 = st.columns([2, 5, 3])
with hc1:
    st.markdown("""<div class="huliot-hdr">
    <span class="huliot-logo">⚙ Huliot BOQ</span>
    </div>""", unsafe_allow_html=True)

with hc2:
    proj_val = st.text_input("proj", placeholder="Project / Site name...", label_visibility="collapsed",
                              value=st.session_state.proj, key="proj_inp")
    st.session_state.proj = proj_val

with hc3:
    col_ht, col_us = st.columns(2)
    with col_ht:
        if st.button("🔶 HT Pro", use_container_width=True,
                     type="primary" if st.session_state.line=="HT Pro" else "secondary"):
            st.session_state.line = "HT Pro"; st.session_state.dn_f = None; st.session_state.cat_f = None; st.rerun()
    with col_us:
        if st.button("🔷 Ultra Silent", use_container_width=True,
                     type="primary" if st.session_state.line=="Ultra Silent" else "secondary"):
            st.session_state.line = "Ultra Silent"; st.session_state.dn_f = None; st.session_state.cat_f = None; st.rerun()

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  GLOBAL SHAFT SELECTOR BAR
# ══════════════════════════════════════════════
tc, bc, _ = sh_colors(st.session_state.global_sh)
sh_counts = boq_sh_counts()

st.markdown(f"""<div style="background:{bc};border:2px solid {tc}44;border-radius:12px;padding:10px 16px;margin:4px 0;">
<span style="font-size:13px;font-weight:800;color:{tc};">📍 ADDING TO LOCATION — All items will be tagged to selected location</span>
</div>""", unsafe_allow_html=True)

bar1, bar2 = st.columns([2, 6])
with bar1:
    new_sh = st.selectbox(
        "loc", SH_CODES,
        index=SH_CODES.index(st.session_state.global_sh),
        format_func=sh_label,
        label_visibility="collapsed",
        key="sh_select"
    )
    if new_sh != st.session_state.global_sh:
        st.session_state.global_sh = new_sh; st.rerun()

with bar2:
    st.markdown("<div style='padding-top:4px;font-size:11px;color:#64748B;font-weight:600;margin-bottom:2px;'>Quick select:</div>", unsafe_allow_html=True)
    qcols = st.columns(len(QUICK_SH))
    for i, code in enumerate(QUICK_SH):
        with qcols[i]:
            cnt = sh_counts.get(code, 0)
            label = f"{code}\n({cnt})" if cnt else code
            active = st.session_state.global_sh == code
            if st.button(label, key=f"qsh_{code}",
                         type="primary" if active else "secondary",
                         use_container_width=True):
                st.session_state.global_sh = code; st.rerun()

st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════════
filtered = get_filtered()
boq_len  = len(st.session_state.boq)
gt       = grand()

tab_catalog, tab_boq, tab_summary = st.tabs([
    f"📦 Catalog ({len(filtered)})",
    f"📋 BOQ ({boq_len} items)" + (f"  ·  {fmt(gt)}" if gt else ""),
    f"📊 Shaft Summary ({len(set(b['shaft'] for b in st.session_state.boq))} locations)" if boq_len else "📊 Shaft Summary"
])

# ══════════════════════════════════════════════
#  TAB 1 — CATALOG
# ══════════════════════════════════════════════
with tab_catalog:
    # DN Filter
    st.markdown("<div style='font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;margin:4px 0 6px 0;letter-spacing:.5px;'>Select Size (DN)</div>", unsafe_allow_html=True)
    dn_counts = get_dn_counts()
    dn_cols = st.columns(len(DN_LIST) + 1)
    with dn_cols[0]:
        if st.button(f"ALL\n{len([p for p in PRODUCTS if p['line']==st.session_state.line])}",
                     use_container_width=True,
                     type="primary" if st.session_state.dn_f is None else "secondary"):
            st.session_state.dn_f = None; st.rerun()
    for i, d in enumerate(DN_LIST):
        cnt = dn_counts.get(d, 0)
        if not cnt: continue
        with dn_cols[i+1]:
            if st.button(f"DN{d}\n{cnt} items", use_container_width=True,
                         type="primary" if st.session_state.dn_f == d else "secondary",
                         key=f"dn_{d}"):
                st.session_state.dn_f = None if st.session_state.dn_f == d else d; st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Category Filter
    cat_cols = st.columns(len(CATS) + 1)
    with cat_cols[0]:
        if st.button("All Types", use_container_width=True,
                     type="primary" if not st.session_state.cat_f else "secondary"):
            st.session_state.cat_f = None; st.rerun()
    for i, c in enumerate(CATS):
        with cat_cols[i+1]:
            icon = CAT_ICONS.get(c,"")
            if st.button(f"{icon} {c}", use_container_width=True,
                         type="primary" if st.session_state.cat_f == c else "secondary",
                         key=f"cat_{c}"):
                st.session_state.cat_f = None if st.session_state.cat_f == c else c; st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Search
    search_val = st.text_input("search", placeholder="🔍  Search item code or description...",
                                label_visibility="collapsed", value=st.session_state.srch, key="srch_inp")
    if search_val != st.session_state.srch:
        st.session_state.srch = search_val; st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Active filters info
    info_parts = []
    if st.session_state.dn_f: info_parts.append(f"DN{st.session_state.dn_f}")
    if st.session_state.cat_f: info_parts.append(st.session_state.cat_f)
    if st.session_state.srch: info_parts.append(f'"{st.session_state.srch}"')

    fi_col1, fi_col2 = st.columns([5,1])
    with fi_col1:
        filter_txt = f"  ·  Filter: {', '.join(info_parts)}" if info_parts else ""
        st.markdown(f"<div style='font-weight:700;color:#334155;font-size:13px;padding:6px 0;'>{len(filtered)} items{filter_txt}</div>", unsafe_allow_html=True)
    with fi_col2:
        if info_parts:
            if st.button("✕ Clear", use_container_width=True):
                st.session_state.dn_f = None; st.session_state.cat_f = None; st.session_state.srch = ""; st.rerun()

    # Product Table Header
    h1,h2,h3,h4,h5,h6,h7 = st.columns([3,5,1,2,2,1,1.5])
    for hdr, col in zip(["CODE","DESCRIPTION","DN","TYPE","LIST PRICE","QTY","ADD"],[h1,h2,h3,h4,h5,h6,h7]):
        col.markdown(f"<div style='font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;background:#F8FAFC;padding:6px 4px;border-bottom:2px solid #E2E8F0;'>{hdr}</div>", unsafe_allow_html=True)

    # Product Rows
    if not filtered:
        st.info("No products found. Try clearing filters.")
    else:
        for prod in filtered:
            c1,c2,c3,c4,c5,c6,c7 = st.columns([3,5,1,2,2,1,1.5])
            with c1:
                st.markdown(f"<div style='font-family:monospace;font-size:10px;color:#64748B;padding:4px 2px;'>{prod['code']}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='font-weight:600;font-size:12px;color:#1E293B;padding:2px;'>{prod['desc']}<br><span style='font-size:10px;color:#94A3B8;'>{prod['sub']}</span></div>", unsafe_allow_html=True)
            with c3:
                if prod["dn"] > 0:
                    dc = DN_COLORS.get(prod["dn"],"#64748B")
                    st.markdown(f"<div style='text-align:center;'><span style='background:{dc}18;color:{dc};padding:2px 7px;border-radius:10px;font-size:11px;font-weight:800;'>{prod['dn']}</span></div>", unsafe_allow_html=True)
            with c4:
                cc = CAT_COLORS.get(prod["type"],"#64748B")
                st.markdown(f"<div style='text-align:center;'><span style='background:{cc}18;color:{cc};padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;'>{prod['type']}</span></div>", unsafe_allow_html=True)
            with c5:
                st.markdown(f"<div style='text-align:right;font-weight:700;font-size:13px;color:#1E293B;padding:4px 4px;'>{fmt(prod['price'])}</div>", unsafe_allow_html=True)
            with c6:
                qty = st.number_input("", min_value=1, value=1, step=1,
                                      label_visibility="collapsed", key=f"qty_{prod['code']}")
            with c7:
                tc2,_,_ = sh_colors(st.session_state.global_sh)
                if st.button(f"+ Add\n{st.session_state.global_sh}", key=f"add_{prod['code']}",
                             use_container_width=True, type="primary"):
                    add_to_boq(prod, qty)
                    st.toast(f"✅ Added {prod['desc']} → {st.session_state.global_sh}", icon="✅")
                    st.rerun()

            st.markdown("<hr style='margin:0;border:none;border-top:1px solid #F1F5F9;'>", unsafe_allow_html=True)

    if boq_len:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button(f"📋 View BOQ — {boq_len} items · {fmt(gt)}", type="primary", use_container_width=True):
            st.rerun()

# ══════════════════════════════════════════════
#  TAB 2 — BOQ
# ══════════════════════════════════════════════
with tab_boq:
    if not st.session_state.boq:
        st.info("BOQ is empty. Go to Catalog and add items.")
    else:
        # BOQ Controls
        bc1, bc2, bc3, bc4, bc5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
        with bc1:
            st.markdown(f"<div style='font-weight:700;font-size:15px;color:#0F172A;padding-top:8px;'>{st.session_state.proj or 'Huliot BOQ'}</div>", unsafe_allow_html=True)
        with bc2:
            g_disc = st.number_input("Global Discount %", min_value=0.0, max_value=100.0,
                                     value=float(st.session_state.g_disc), step=0.5, key="g_disc_inp")
            st.session_state.g_disc = g_disc
        with bc3:
            xl_data = export_excel()
            pn = (st.session_state.proj or "Huliot").replace(" ","_")
            st.download_button("⬇ Export Excel", data=xl_data,
                               file_name=f"{pn}_BOQ.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True, type="primary")
        with bc4:
            uploaded = st.file_uploader("Import Excel", type=["xlsx","xls"],
                                        label_visibility="collapsed", key="xl_up")
            if uploaded:
                n = import_excel(uploaded)
                st.toast(f"✅ Imported {n} items", icon="✅"); st.rerun()
        with bc5:
            if st.button("🗑 Clear BOQ", use_container_width=True):
                st.session_state.boq = []; st.rerun()

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # Shaft filter chips
        used_shafts = sorted(set(b.get("shaft","NA") for b in st.session_state.boq),
                             key=lambda x: ("" if x=="NA" else x))
        fsh_cols = st.columns(min(len(used_shafts)+1, 12))
        with fsh_cols[0]:
            if st.button(f"All ({boq_len})", use_container_width=True,
                         type="primary" if st.session_state.boq_fsh=="ALL" else "secondary",
                         key="fsh_all"):
                st.session_state.boq_fsh = "ALL"; st.rerun()
        for i, sh in enumerate(used_shafts):
            with fsh_cols[min(i+1, len(fsh_cols)-1)]:
                sh_cnt = sh_counts.get(sh, 0)
                if st.button(f"{sh} ({sh_cnt})", use_container_width=True,
                             type="primary" if st.session_state.boq_fsh==sh else "secondary",
                             key=f"fsh_{sh}"):
                    st.session_state.boq_fsh = sh; st.rerun()

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        # ── Build display data ──
        if st.session_state.boq_fsh == "ALL":
            # Aggregate same item codes across all shafts — combined qty, combined amount
            agg = {}
            for b in st.session_state.boq:
                key = b["code"]
                if key not in agg:
                    agg[key] = {
                        **b,
                        "qty": b["qty"],
                        "shafts": [b.get("shaft","NA")],   # track which shafts contribute
                        "_ids": [b["_id"]],
                    }
                else:
                    agg[key]["qty"] += b["qty"]
                    sh = b.get("shaft","NA")
                    if sh not in agg[key]["shafts"]:
                        agg[key]["shafts"].append(sh)
                    agg[key]["_ids"].append(b["_id"])
            display_rows = list(agg.values())
            is_all = True
        else:
            display_rows = [b for b in st.session_state.boq if b.get("shaft","NA")==st.session_state.boq_fsh]
            is_all = False

        display_total = sum(
            r["qty"] * net_rate(r) for r in display_rows
        )

        # ── Table header ──
        if is_all:
            bh = st.columns([0.4, 2.5, 4, 0.8, 1.2, 1.5, 0.8, 1.5, 1.8, 2.0])
            for hdr, col in zip(["#","CODE","DESCRIPTION","DN","TOTAL QTY","LIST PRICE","DISC%","NET RATE","AMOUNT","SHAFTS"], bh):
                col.markdown(f"<div style='font-size:9px;font-weight:700;color:#64748B;text-transform:uppercase;background:#F8FAFC;padding:6px 3px;border-bottom:2px solid #E2E8F0;text-align:center;'>{hdr}</div>", unsafe_allow_html=True)
        else:
            bh = st.columns([0.4, 1.2, 2.5, 4, 0.8, 1, 1.5, 0.8, 1.5, 1.8, 0.5])
            for hdr, col in zip(["#","LOC","CODE","DESCRIPTION","DN","QTY","LIST PRICE","DISC%","NET RATE","AMOUNT","DEL"], bh):
                col.markdown(f"<div style='font-size:9px;font-weight:700;color:#64748B;text-transform:uppercase;background:#F8FAFC;padding:6px 3px;border-bottom:2px solid #E2E8F0;text-align:center;'>{hdr}</div>", unsafe_allow_html=True)

        # ── Rows ──
        for idx, row in enumerate(display_rows):
            dc = DN_COLORS.get(row["dn"],"#64748B")
            nr = net_rate(row)
            total_amt = row["qty"] * nr

            if is_all:
                r = st.columns([0.4, 2.5, 4, 0.8, 1.2, 1.5, 0.8, 1.5, 1.8, 2.0])
                with r[0]:
                    st.markdown(f"<div style='text-align:center;color:#94A3B8;font-size:11px;padding:8px 0;'>{idx+1}</div>", unsafe_allow_html=True)
                with r[1]:
                    st.markdown(f"<div style='font-family:monospace;font-size:9px;color:#64748B;padding:8px 2px;'>{row['code']}</div>", unsafe_allow_html=True)
                with r[2]:
                    st.markdown(f"<div style='font-weight:600;font-size:12px;color:#1E293B;padding:4px 2px;'>{row['desc']}<br><span style='font-size:10px;color:#94A3B8;'>{row['sub']}</span></div>", unsafe_allow_html=True)
                with r[3]:
                    if row["dn"] > 0:
                        st.markdown(f"<div style='text-align:center;padding:8px 0;'><span style='background:{dc}18;color:{dc};padding:2px 6px;border-radius:8px;font-size:11px;font-weight:800;'>{row['dn']}</span></div>", unsafe_allow_html=True)
                with r[4]:
                    # Show total qty — bold, highlighted
                    st.markdown(f"<div style='text-align:center;padding:6px 2px;'><span style='background:#1D4ED820;color:#1D4ED8;padding:4px 10px;border-radius:8px;font-size:15px;font-weight:900;'>{row['qty']}</span></div>", unsafe_allow_html=True)
                with r[5]:
                    st.markdown(f"<div style='text-align:right;font-size:12px;padding:8px 4px;color:#64748B;'>{fmt(row['price'])}</div>", unsafe_allow_html=True)
                with r[6]:
                    st.markdown(f"<div style='text-align:center;font-size:12px;padding:8px 4px;color:#64748B;'>{eff_disc(row)}%</div>", unsafe_allow_html=True)
                with r[7]:
                    st.markdown(f"<div style='text-align:right;font-weight:700;color:#10B981;font-size:12px;padding:8px 4px;'>{fmt(nr)}</div>", unsafe_allow_html=True)
                with r[8]:
                    st.markdown(f"<div style='text-align:right;font-weight:800;font-size:13px;color:#1E293B;padding:8px 4px;'>{fmt(total_amt)}</div>", unsafe_allow_html=True)
                with r[9]:
                    # Show shaft badges
                    shafts = row.get("shafts", [row.get("shaft","NA")])
                    badges = ""
                    for sh in sorted(shafts):
                        tc_s, bc_s, _ = sh_colors(sh)
                        badges += f"<span style='background:{bc_s};color:{tc_s};border:1px solid {tc_s}44;padding:1px 6px;border-radius:6px;font-size:10px;font-weight:700;margin:1px;display:inline-block;'>{sh}</span>"
                    st.markdown(f"<div style='padding:6px 2px;line-height:1.8;'>{badges}</div>", unsafe_allow_html=True)

            else:
                # Per-shaft detail view (unchanged)
                b = row
                r = st.columns([0.4, 1.2, 2.5, 4, 0.8, 1, 1.5, 0.8, 1.5, 1.8, 0.5])
                with r[0]:
                    st.markdown(f"<div style='text-align:center;color:#94A3B8;font-size:11px;padding:8px 0;'>{idx+1}</div>", unsafe_allow_html=True)
                with r[1]:
                    new_sh = st.selectbox("sh", SH_CODES, index=SH_CODES.index(b.get("shaft","NA")),
                                          label_visibility="collapsed", key=f"bsh_{b['_id']}",
                                          format_func=lambda x: x)
                    if new_sh != b.get("shaft","NA"):
                        b["shaft"] = new_sh; st.rerun()
                with r[2]:
                    st.markdown(f"<div style='font-family:monospace;font-size:9px;color:#64748B;padding:8px 2px;'>{b['code']}</div>", unsafe_allow_html=True)
                with r[3]:
                    st.markdown(f"<div style='font-weight:600;font-size:12px;color:#1E293B;padding:4px 2px;'>{b['desc']}<br><span style='font-size:10px;color:#94A3B8;'>{b['sub']}</span></div>", unsafe_allow_html=True)
                with r[4]:
                    if b["dn"] > 0:
                        st.markdown(f"<div style='text-align:center;padding:8px 0;'><span style='background:{dc}18;color:{dc};padding:2px 6px;border-radius:8px;font-size:11px;font-weight:800;'>{b['dn']}</span></div>", unsafe_allow_html=True)
                with r[5]:
                    new_qty = st.number_input("qty", min_value=1, value=b["qty"], step=1,
                                              label_visibility="collapsed", key=f"bqty_{b['_id']}")
                    if new_qty != b["qty"]:
                        b["qty"] = new_qty; st.rerun()
                with r[6]:
                    st.markdown(f"<div style='text-align:right;font-size:12px;padding:8px 4px;color:#64748B;'>{fmt(b['price'])}</div>", unsafe_allow_html=True)
                with r[7]:
                    new_disc = st.number_input("disc", min_value=0.0, max_value=100.0,
                                               value=float(b["disc"]) if b["disc"] is not None else float(st.session_state.g_disc),
                                               step=0.5, label_visibility="collapsed", key=f"bdisc_{b['_id']}")
                    if new_disc != (b["disc"] if b["disc"] is not None else st.session_state.g_disc):
                        b["disc"] = new_disc; st.rerun()
                with r[8]:
                    st.markdown(f"<div style='text-align:right;font-weight:700;color:#10B981;font-size:12px;padding:8px 4px;'>{fmt(net_rate(b))}</div>", unsafe_allow_html=True)
                with r[9]:
                    st.markdown(f"<div style='text-align:right;font-weight:800;font-size:13px;color:#1E293B;padding:8px 4px;'>{fmt(amt(b))}</div>", unsafe_allow_html=True)
                with r[10]:
                    if st.button("✕", key=f"del_{b['_id']}", use_container_width=True):
                        st.session_state.boq = [x for x in st.session_state.boq if x["_id"]!=b["_id"]]; st.rerun()

            st.markdown("<hr style='margin:0;border:none;border-top:1px solid #F1F5F9;'>", unsafe_allow_html=True)

        # ── Grand Total ──
        lbl = "GRAND TOTAL — All Shafts Combined" if is_all else f"TOTAL — {st.session_state.boq_fsh}"
        item_count = f"{len(st.session_state.boq)} entries across {len(set(b.get('shaft','NA') for b in st.session_state.boq))} locations" if is_all else f"{len(display_rows)} items"
        st.markdown(f"""<div style="background:linear-gradient(90deg,#0F172A,#1E3A5F);color:white;padding:10px 14px;border-radius:0 0 10px 10px;display:flex;justify-content:space-between;align-items:center;margin-top:4px;">
        <div><span style="font-weight:700;font-size:14px;">{lbl}</span><br>
        <span style="font-size:11px;opacity:.6;">{item_count}</span></div>
        <span style="font-weight:900;font-size:20px;color:#FBBF24;">{fmt(display_total)}</span>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div class='footer-note'>⚠ Prices ex-factory/depot · GST extra as applicable · W.E.F April 2026 · Excel export includes separate sheet per Shaft/Kitchen</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 3 — SHAFT SUMMARY
# ══════════════════════════════════════════════
with tab_summary:
    if not st.session_state.boq:
        st.info("No data yet. Add items to BOQ first.")
    else:
        shaft_groups = {}
        for b in st.session_state.boq:
            sh = b.get("shaft","NA")
            shaft_groups.setdefault(sh,[]).append(b)

        sh_sorted = sorted(shaft_groups.keys(), key=lambda x: ("" if x=="NA" else x))
        sh_total  = lambda sh: sum(amt(b) for b in shaft_groups[sh])

        # Summary cards row
        total_sh = sum(sh_total(sh) for sh in sh_sorted if sh.startswith("SH"))
        total_k  = sum(sh_total(sh) for sh in sh_sorted if sh.startswith("K"))
        total_na = sh_total("NA") if "NA" in shaft_groups else 0

        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.markdown(f"""<div style="background:linear-gradient(135deg,#0F172A,#1E3A5F);border-radius:12px;padding:16px;color:white;">
        <div style="font-size:11px;opacity:.7;margin-bottom:4px;">GRAND TOTAL</div>
        <div style="font-size:26px;font-weight:900;color:#FBBF24;">{fmt(gt)}</div>
        <div style="font-size:11px;opacity:.6;">{boq_len} items · {len(sh_sorted)} locations</div>
        </div>""", unsafe_allow_html=True)
        sc2.markdown(f"""<div style="background:#EFF6FF;border:2px solid #BFDBFE;border-radius:12px;padding:16px;">
        <div style="font-size:11px;color:#1D4ED8;font-weight:700;margin-bottom:4px;">SHAFT TOTAL</div>
        <div style="font-size:22px;font-weight:900;color:#1D4ED8;">{fmt(total_sh)}</div>
        <div style="font-size:11px;color:#3B82F6;">{len([s for s in sh_sorted if s.startswith('SH')])} shafts</div>
        </div>""", unsafe_allow_html=True)
        sc3.markdown(f"""<div style="background:#F0FDF4;border:2px solid #A7F3D0;border-radius:12px;padding:16px;">
        <div style="font-size:11px;color:#065F46;font-weight:700;margin-bottom:4px;">KITCHEN TOTAL</div>
        <div style="font-size:22px;font-weight:900;color:#065F46;">{fmt(total_k)}</div>
        <div style="font-size:11px;color:#10B981;">{len([s for s in sh_sorted if s.startswith('K')])} kitchens</div>
        </div>""", unsafe_allow_html=True)
        sc4.markdown(f"""<div style="background:#F8FAFC;border:2px solid #CBD5E1;border-radius:12px;padding:16px;">
        <div style="font-size:11px;color:#64748B;font-weight:700;margin-bottom:4px;">UNASSIGNED</div>
        <div style="font-size:22px;font-weight:900;color:#64748B;">{fmt(total_na)}</div>
        <div style="font-size:11px;color:#94A3B8;">{len(shaft_groups.get('NA',[]))} items</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Per-shaft breakdown
        for sh in sh_sorted:
            items = shaft_groups[sh]
            sub = sh_total(sh)
            pct = round(sub/gt*100,1) if gt else 0
            tc4, bc4, brd4 = sh_colors(sh)

            sh_name = "Unassigned Items" if sh=="NA" else f"Shaft {int(sh[2:])}" if sh.startswith("SH") else f"Kitchen / Flat {int(sh[1:])}"

            st.markdown(f"""<div class="sh-group-hdr" style="background:{bc4};border-left:5px solid {brd4};">
            <div style="display:flex;align-items:center;gap:10px;">
            <span style="background:{tc4};color:white;padding:4px 12px;border-radius:8px;font-size:13px;font-weight:900;">{sh}</span>
            <span style="font-weight:700;color:#1E293B;font-size:14px;">{sh_name}</span>
            <span style="font-size:11px;color:#64748B;">{len(items)} items</span>
            <span style="font-size:11px;background:rgba(0,0,0,.08);padding:2px 8px;border-radius:10px;color:#475569;">{pct}% of total</span>
            </div>
            <div style="font-size:18px;font-weight:900;color:{tc4};">{fmt(sub)}</div>
            </div>""", unsafe_allow_html=True)

            # Progress bar
            st.markdown(f"""<div style="height:5px;background:#F1F5F9;margin-bottom:0;border-radius:0;">
            <div style="height:100%;width:{pct}%;background:{tc4};transition:width .4s;"></div></div>""", unsafe_allow_html=True)

            # Items table
            tbl_html = """<table class="boq-tbl"><thead><tr>
            <th style="text-align:center;">#</th>
            <th style="text-align:left;">Code</th>
            <th style="text-align:left;">Description</th>
            <th style="text-align:center;">DN</th>
            <th style="text-align:center;">Qty</th>
            <th style="text-align:right;">Net Rate</th>
            <th style="text-align:right;">Amount</th>
            </tr></thead><tbody>"""
            for i, b in enumerate(items, 1):
                dc = DN_COLORS.get(b["dn"],"#64748B") if b["dn"] else "#64748B"
                dn_badge = f"<span style='background:{dc}18;color:{dc};padding:1px 6px;border-radius:8px;font-size:11px;font-weight:800;'>{b['dn']}</span>" if b["dn"] else ""
                tbl_html += f"""<tr>
                <td style="text-align:center;color:#94A3B8;">{i}</td>
                <td style="font-family:monospace;font-size:10px;color:#64748B;">{b['code']}</td>
                <td><span style="font-weight:600;color:#1E293B;">{b['desc']}</span><br><span style="font-size:10px;color:#94A3B8;">{b['sub']}</span></td>
                <td style="text-align:center;">{dn_badge}</td>
                <td style="text-align:center;font-weight:700;">×{b['qty']}</td>
                <td style="text-align:right;color:#10B981;font-weight:700;">{fmt(net_rate(b))}</td>
                <td style="text-align:right;font-weight:800;color:#1E293B;">{fmt(amt(b))}</td>
                </tr>"""
            tbl_html += f"""</tbody><tfoot><tr style="background:{bc4};">
            <td colspan="5" style="padding:8px 10px;font-weight:700;color:{tc4};">Subtotal — {sh}</td>
            <td colspan="2" style="text-align:right;padding:8px 10px;font-weight:900;font-size:15px;color:{tc4};">{fmt(sub)}</td>
            </tr></tfoot></table>"""
            st.markdown(tbl_html, unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Export button
        xl_data2 = export_excel()
        pn2 = (st.session_state.proj or "Huliot").replace(" ","_")
        st.download_button("⬇ Export Full Excel (Shaft-wise Sheets)", data=xl_data2,
                           file_name=f"{pn2}_BOQ_ShaftWise.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True, type="primary")
