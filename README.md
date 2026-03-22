# 🧹 Data Quality Checker

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-✓-green?style=flat-square)
![NumPy](https://img.shields.io/badge/NumPy-✓-yellow?style=flat-square)
![Logging](https://img.shields.io/badge/Logging-Built--in-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

An advanced end-to-end Python script that automatically detects
and fixes data quality issues in any CSV file — in one run.

Tested on 3 real-world datasets (2,020 to 12,600 rows) without crashes.

---

## 📌 Why I Built This

Every data analysis starts with the same problem:
you don't know if your data is clean until something breaks.

I built this script to automate the first 30 minutes of every
project — the part where you manually hunt for nulls, duplicates,
wrong data types, and outliers before doing any real work.

Point it at any CSV. Get a clean file and a full audit log.

---

## ⚙️ Pipeline (9 Steps)
```text
Raw CSV
   ↓
🔤 Header Cleaner           → strips spaces, lowercases, adds underscores
   ↓
🗂️ Duplicate Column Check   → removes duplicate columns
   ↓
💲 Symbol Cleaner           → strips $, %, , from numeric columns
   ↓
🔢 Datatype Fixer           → auto-converts string cols to numeric where safe
   ↓
📅 Date Cleaner             → detects and converts date/time columns
   ↓
🔁 Duplicate Row Removal    → drops exact duplicate rows
   ↓
🔍 Null Handler             → drops col if >50% null, median for numeric,
                              mode for categorical, ffill for datetime
   ↓
⚠️ Outlier Handler          → IQR method with winsorization
   ↓
🔤 Inconsistency Fixer      → title case on low cardinality string columns
   ↓
Clean CSV + Full Log File
```

---

## 🔄 Before vs After

**Before — Raw Data**

<img width="1200" height="866" alt="image" src="https://github.com/user-attachments/assets/9c2cc9a9-f6e3-43ee-89c7-a67754357c2c" />

**After — Cleaned Data**

<img width="1066" height="862" alt="image" src="https://github.com/user-attachments/assets/1e39a3fc-d3f9-4f8f-99c5-e4693db76e62" />

---

## 📊 Sample Log Output (Real Run — Marketing Campaign Dataset)
```text
File loaded: marketing_campaign_data_messy.csv | Shape: (2020, 12)

🔤 Headers cleaned:         Campaign_ID, Clicks  → campaign_id, clicks
🗂️ Duplicate columns:       1 removed. Columns remaining: 11
💲 Symbols removed:         '$' stripped from 'spend' column
📅 Dates converted:         'start_date', 'end_date' → datetime
🔁 Duplicates removed:      19 rows dropped. Rows remaining: 2001
🔍 Nulls handled:
      channel               100 values → filled with mode
      conversions           200 values → filled with median
⚠️  Outliers winsorized:
      clicks                11 values capped to IQR bounds
      spend                 74 values capped to IQR bounds
      conversions           110 values capped to IQR bounds
      Total: 195 outliers handled

✅ Cleaned data saved to Final_Data.csv
```

---

## ⚠️ Known Limitations

> These are deliberate trade-offs in building a generic script — not bugs.

| Limitation | What It Means |
|-----------|---------------|
| 🔤 Abbreviations get corrupted | `HR`, `USA`, `IT` get changed to `Hr`, `Usa`, `It` by the title case fixer |
| ✏️ Typos not fixed | `Facebok` or `Gogle` stay as-is — the script fixes casing, not spelling |
| ☑️ Boolean columns not normalized | `Yes / 1 / True / Y` are not unified into one standard value |
| 📅 Date detection by column name only | A date column named `recorded_at` or `ts` will be missed entirely |
| 📧 Spelling variants not unified | `E-Mail` and `Email` are treated as two different values |
| 🔢 Thresholds are approximations | The 90% cardinality and 50% numeric cutoffs work for most datasets but not all |

---

## 🚀 How to Use

**1. Clone the repo**
```bash
git clone https://github.com/sanketkambli04082001/Data_Quality_Checker.git
cd Data_Quality_Checker
```

**2. Install dependencies**
```bash
pip install -r requirement.txt
```

**3. Point it at your CSV**
```python
# In Data_Cleaning.py, update the last line:
clean_data(r'your_dataset.csv')
```

**4. Run it**
```bash
python Data_Cleaning.py
```

**5. Check your outputs**
- `Final_Data.csv` → cleaned dataset
- `data_cleaning.log` → full audit trail of every change made

---

## 📁 Project Structure
```text
Data_Quality_Checker/
│
├── Data_Cleaning.py                  # Main script (9-step cleaner)
├── Data_Cleaning_Exploration.ipynb   # Jupyter notebook version
├── requirement.txt                   # Dependencies
├── Sample_Datasets/                  # Test CSVs + before/after screenshots
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| pandas | Data loading, cleaning, null and duplicate handling |
| numpy | Numeric type detection and outlier calculations |
| logging (built-in) | Full audit trail of every change made |

---

## 👤 Author

**Sanket Kambli** — Entry-Level Data Analyst

[![GitHub](https://img.shields.io/badge/GitHub-sanketkambli04082001-181717?style=flat-square&logo=github)](https://github.com/sanketkambli04082001)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/YOUR-LINKEDIN-URL-HERE)
