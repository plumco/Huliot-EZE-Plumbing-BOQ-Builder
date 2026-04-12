# ⚙️ Huliot EZE Plumbing BOQ Builder

**Huliot Pipes & Fittings Pvt. Ltd.**  
Price List W.E.F April 2026 | HT Pro + Ultra Silent  
Built for site plumbers & MEP consultants to prepare fast, accurate Bills of Quantities.

---

## 📁 File Structure

```
your-repo/
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
└── .streamlit/
    └── config.toml         ← App theme & server config
```

---

## 🚀 Deploy on Streamlit Cloud (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Huliot BOQ Builder initial commit"
git remote add origin https://github.com/YOUR_USERNAME/huliot-boq.git
git push -u origin main
```

### Step 2 — Deploy
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository, branch `main`, and main file `app.py`
5. Click **"Deploy!"**

Your app will be live at:  
`https://YOUR_USERNAME-huliot-boq-app-XXXXXX.streamlit.app`

---

## 💻 Run Locally

```bash
# 1. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

App opens at: **http://localhost:8501**

---

## 🧰 Features

| Feature | Details |
|---|---|
| **Product Lines** | HT Pro 🟠 and Ultra Silent 🔵 |
| **Total Products** | 350+ items from official April 2026 price list |
| **DN Filter** | Click DN32 → DN200 size pills to filter instantly |
| **Category Filter** | Pipe / Bend / Branch / Trap / Coupler / Reducer / Inspection / Clamp / Accessory |
| **Search** | Search by item code, description, or size |
| **Add to BOQ** | Tick checkbox + set quantity → Add selected items |
| **Edit in BOQ** | Directly edit Qty and per-item Discount % in BOQ table |
| **Global Discount** | Single % applied to all items (overridable per item) |
| **Totals** | Line items, total units, list value, savings, net amount |
| **Export Excel** | Formatted BOQ with header, alternating rows, grand total, terms sheet |
| **Import Excel** | Re-load a previously exported BOQ file |
| **Project Name** | Appears in header and exported filename |

---

## 📊 Excel Export Format

The exported `.xlsx` file includes:
- **BOQ sheet** — Project name, date, price list reference
- Formatted table with: Sr.No | Item Code | Description | Category | DN | Product Line | Unit | Qty | List Price | Disc% | Net Rate | Amount
- Grand Total row (highlighted)
- **Terms & Conditions sheet** — Huliot T&C auto-included

---

## 📦 Product Coverage

### HT Pro (Orange 🟠)
- Pipes: S/S and D/S in 250mm / 500mm / 1000mm / 1500mm / 2000mm / 3000mm lengths
- Bends: 15° / 30° / 45° / 87.5° (standard + door versions, L/R)
- Branches: Single Y, Reducing Y, Tee, Swept Tee, Door Swept Tee, Double Branch, Corner Branch
- Traps: P Trap, S Trap, Nahani Trap, MFT, HAFF Stack, Height Risers, Hoppers
- Couplers, Reducers, End Caps, Vent Cowls, Boss Connectors, WC Connectors
- Split Clamps DN40 → DN200

### Ultra Silent (Blue 🔵)
- Pipes: S/S and D/S in all special lengths + DN32 → DN200
- Bends: 15° / 30° / 45° / 67.5° / 87.5° (door versions included)
- Branches: Full wye, tee, swept tee, corner branch, double branch range
- Traps: P Trap, S Trap, MFT (with/without ring/socket), Nahani, SmartLock, HAFF Stack
- Couplers, Lock Seals, End Locks, Reducers, Technical Bends, Rubber Gaskets
- HD Acoustic Clamps DN40 → DN200

---

## ⚠️ Disclaimer

All prices are ex-factory/depot, provisional and subject to change without prior notice.  
GST extra as applicable. All disputes subject to Mumbai jurisdiction only.  
Prices at time of dispatch/invoicing shall be final and binding.

---

*Developed for internal use by PVL Ltd. MEP Consulting Team.*
