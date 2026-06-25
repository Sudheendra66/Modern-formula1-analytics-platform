<div align="center">

# 🏎️ Formula 1 Analytics Platform

### *"To settle one of Formula 1's biggest debates... I built a data pipeline."*

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)](https://snowflake.com)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://getdbt.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

An end-to-end **Data Engineering** project that ingests Formula 1 race data, transforms it into analytics-ready models, and visualizes driver insights through an interactive dashboard.

</div>

---

## 📸 Dashboard Preview

| Home Dashboard | Driver Comparison |
|:-:|:-:|
| ![Home](images/dashboard_home.png) | ![Comparison](images/driver_comparison.png) |

---

## 🏗️ Architecture

<div align="center">

```
┌─────────────────────────┐
│     Jolpica REST API    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Custom Fivetran SDK    │  ← Incremental sync, pagination & retry
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Snowflake Data Warehouse│  ← Raw data storage
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│       dbt Models        │  ← Staging → Intermediate → Marts
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Streamlit Dashboard   │  ← Interactive analytics UI
└─────────────────────────┘
```

</div>

The platform follows a modern **ELT architecture** — raw data lands in Snowflake first, then gets transformed in-warehouse using dbt's layered modeling approach.

---

## 🚀 Features

| Category | Features |
|----------|----------|
| 📥 **Ingestion** | Custom Fivetran Connector SDK · Incremental API sync · Pagination & retry handling |
| 🗄️ **Storage** | Snowflake Data Warehouse · Historical F1 dataset |
| 🔄 **Transformation** | dbt layered models · Data quality tests |
| 📊 **Analytics** | GOAT ranking model · Championship analytics · Driver comparison |
| 🖥️ **Visualization** | Interactive Streamlit dashboard · Plotly performance charts |

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| 🐍 Language | Python |
| 🗄️ Data Warehouse | Snowflake |
| 🔄 Transformation | dbt |
| 📥 Ingestion | Custom Fivetran Connector SDK |
| 🖥️ Visualization | Streamlit |
| 📈 Charts | Plotly |
| 🗃️ Database | SQL |
| 🔧 Version Control | Git & GitHub |

---

## 📊 Dashboard Pages

<details>
<summary><strong>🏁 Home Dashboard</strong></summary>

- Formula 1 season overview
- KPI summary cards
- GOAT Podium highlight
- Performance trend charts
- Driver leaderboard

</details>

<details>
<summary><strong>👑 GOAT Leaderboard</strong></summary>

Ranks all-time drivers using a custom multi-factor scoring model:

- Career Points · Win Rate · Podiums · Race Wins · Consistency Score

</details>

<details>
<summary><strong>📈 Driver Analytics</strong></summary>

Interactive per-driver statistics:

- Career Points · Race Wins · Podiums · Average Finish · GOAT Score

</details>

<details>
<summary><strong>⚔️ Driver Comparison</strong></summary>

Head-to-head comparison of any two F1 drivers across all eras:

- Career statistics · GOAT Score · Win Rate · Podium Rate · Performance Metrics

</details>

<details>
<summary><strong>🏆 World Champions</strong></summary>

Season-by-season breakdown of every Formula 1 World Champion.

</details>

---

## 📂 Project Structure

```
F1_Project/
│
├── 📁 api/                        # API utilities
│
├── 📁 dbt_f1/                     # dbt project
│   ├── models/
│   │   ├── staging/               # Raw source cleaning
│   │   ├── intermediate/          # Business logic
│   │   └── marts/                 # Analytics-ready tables
│   ├── snapshots/
│   ├── tests/                     # Data quality checks
│   └── macros/
│
├── 📁 streamlit/                  # Dashboard app
│   ├── pages/
│   ├── assets/
│   ├── app.py
│   └── snowflake_connection.py
│
├── connector.py                   # Fivetran custom connector
├── configuration.json
└── README.md
```

---

## 📈 Data Pipeline

```
✅ Extract    →  Formula 1 data from Jolpica REST API
✅ Ingest     →  Custom Fivetran Connector with incremental sync
✅ Store      →  Raw tables in Snowflake Data Warehouse
✅ Transform  →  dbt models (Staging → Intermediate → Marts)
✅ Analyze    →  GOAT scores, championship stats, driver metrics
✅ Visualize  →  Interactive Streamlit + Plotly dashboard
```

---

## 🧪 dbt Modeling Layers

```
Sources  (raw Snowflake tables)
    │
    ▼
Staging Models     ← Rename, cast, light cleaning
    │
    ▼
Intermediate Models ← Joins, business logic, aggregations
    │
    ▼
Mart Models        ← Analytics-ready, dashboard-facing
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/<username>/Modern-formula1-analytics-platform.git
cd Modern-formula1-analytics-platform
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure your Snowflake connection**

Update `streamlit/snowflake_connection.py` and `configuration.json` with your credentials.

**4. Run dbt models**
```bash
dbt run
dbt test
```

**5. Launch the dashboard**
```bash
streamlit run streamlit/app.py
```

---

## 📌 Key Learnings

- 🔌 Built a **custom Fivetran Connector SDK** for REST API ingestion
- 🔁 Implemented **incremental sync**, pagination, and retry handling
- 🏗️ Designed a **layered dbt architecture** with staging, intermediate, and mart models
- 📊 Shipped an **end-to-end analytics platform** using Snowflake and Streamlit

---

## 💡 Roadmap

- [ ] Real-time race analytics
- [ ] Constructor team analytics
- [ ] Circuit performance breakdown
- [ ] Pit stop strategy analysis
- [ ] Qualifying lap performance
- [ ] Lap-by-lap telemetry data

---

## 👨‍💻 Author

**Sudheendra Nekkanti**

[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:your-email@example.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/your-profile)

---

<div align="center">

⭐ **If you found this project interesting, consider giving it a star!** ⭐

*Built with ❤️ and a passion for data + motorsport*

</div>
