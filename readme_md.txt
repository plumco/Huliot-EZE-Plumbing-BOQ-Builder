# ⚙ Huliot EZE BOQ Builder — Streamlit App

**W.E.F April 2026 | HT Pro + Ultra Silent Price Lists**

---

## 📁 Files Required

```
your-repo/
├── app.py              ← Main application
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## 🚀 Deploy on Streamlit Community Cloud (Free)

### Step 1 — Push to GitHub
1. Create a new GitHub repository (e.g. `huliot-boq`)
2. Upload `app.py` and `requirements.txt` to the repo root
3. Commit the files

### Step 2 — Deploy on Streamlit Cloud
1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository and branch
5. Set **Main file path** → `app.py`
6. Click **"Deploy!"**

Your app will be live at:  
`https://your-app-name.streamlit.app`

---

## 💻 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

App opens at: **http://localhost:8501**

---

## 🔑 Features

| Feature | Description |
|---|---|
| 📍 Global Shaft Selector | Select NA / SH01–SH50 / K01–K50 — all added items tagged to selected location |
| ⚡ Quick Chips | One-click switch between NA, SH01–SH10, K01–K05 |
| 📦 Product Catalog | Filter by DN size, category, search — 250+ items from both product lines |
| 📋 BOQ Table | Editable qty, per-item discount, net rate, amount |
| 📊 Shaft Summary | Location-wise breakdown with subtotals and progress bars |
| ⬇ Excel Export | Full BOQ sheet + separate sheet per Shaft/Kitchen |
| ⬆ Excel Import | Import previously exported BOQ files |
| 🔶 HT Pro | Full product range — W.E.F April 2026 |
| 🔷 Ultra Silent | Full product range — W.E.F April 2026 |

---

## 📋 How to Use

1. **Enter project name** in the header
2. **Select product line** — HT Pro or Ultra Silent
3. **Select Location** from the dropdown (NA / SH01-SH50 / K01-K50)
4. Browse catalog — **filter by DN size and category**
5. Set **quantity** and click **+ Add [location]**
6. Switch location and add more items for that shaft/kitchen
7. Go to **📋 BOQ** tab to review and edit
8. Go to **📊 Shaft Summary** to see location-wise totals
9. Click **⬇ Export Excel** — generates one sheet per shaft/kitchen

---

## ⚠ Terms (as per Huliot price list)
- Prices ex-factory / depot
- GST extra as applicable  
- All prices provisional and subject to change without prior notice
- Payment — Advance Payment
- All disputes subject to Mumbai jurisdiction only
