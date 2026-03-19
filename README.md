# 🧹 Data Quality Checker

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-✓-green?style=flat-square)
![Logging](https://img.shields.io/badge/Logging-Built--in-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

An automated Python script that detects and fixes data quality 
issues in any CSV file — duplicates, nulls, outliers, and 
inconsistencies — in one run.

---

## 📌 Why I Built This

Every data analysis starts with the same problem: 
you don't know if your data is clean until something breaks.

I built this script to automate the first 30 minutes of 
every project — the part where you manually check for 
nulls, duplicates, and outliers before doing any real work.
Run it once on any CSV. Get a clean file and a full log.

---

## ⚙️ Pipeline
```
Raw CSV
   ↓
🔁 Duplicate Removal     → drops exact duplicate rows
   ↓
🔍 Null Handler          → fills numeric cols with mean,
                           text cols with mode
   ↓
⚠️ Outlier Detection     → IQR method, replaces with median
   ↓
🔤 Inconsistency Fixer   → standardizes text to title case
   ↓
Clean CSV + Log File
```

---

## 📊 Sample Results (Real Run)
```
File loaded: data.csv | Shape: (10500, 9)

🔁 Duplicates removed:     500 rows dropped
🔍 Nulls handled:
      salary               400 values filled
      performance_score    300 values filled
      city                 250 values filled
⚠️  Outliers replaced:     300 values in 'age' → median (40)
🔤  Inconsistencies fixed: 'gender' → 8 variants to 4

✅ Cleaned data saved to Final_Data.csv
```

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
# In csv_data_cleaning.py, update the last line:
clean_data(r'your_dataset.csv')
```

**4. Run it**
```bash
python csv_data_cleaning.py
```

**5. Check your outputs**
- `Final_Data.csv` → cleaned dataset
- `csv_data_cleaning.log` → full audit trail of every change

---

## 📁 Project Structure
```
Data_Quality_Checker/
│
├── csv_data_cleaning.py     # Main script
├── data_cleaning.ipynb      # Jupyter notebook version
├── requirement.txt          # Dependencies
├── Sample_Datasets/         # Test CSVs to try it on
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| pandas | Data loading, null handling, deduplication |
| logging | Audit trail of every change made |
| Python (built-in) | IQR outlier logic, text standardization |

---

## 👤 Author

**Sanket Kambli** — Entry-Level Data Analyst

[![GitHub](https://img.shields.io/badge/GitHub-sanketkambli04082001-181717?style=flat-square&logo=github)](https://github.com/sanketkambli04082001)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/YOUR-LINKEDIN-URL-HERE)
