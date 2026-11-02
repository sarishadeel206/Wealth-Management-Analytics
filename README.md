<div align="center">

<img src="https://capsule-render.vercel.app/api?type=soft&color=0:111827,45:7C3AED,100:EC4899&height=200&section=header&text=Wealth%20Management%20Analytics&fontSize=30&fontColor=FFFFFF&fontAlignY=39&desc=Data%20Engineering%20%7C%20Financial%20Insights%20%7C%20AI%20Reporting&descSize=13&descAlignY=63" width="100%" alt="Wealth Management Analytics Platform"/>

# Wealth Management Analytics Platform

### From Raw Financial Data to Decision-Ready Insights

**Developed by Sarish Adeel**

<br>

<img src="https://img.shields.io/badge/Databricks-EA580C?style=for-the-badge&logo=databricks&logoColor=white" alt="Databricks"/>
<img src="https://img.shields.io/badge/PySpark-F97316?style=for-the-badge&logo=apachespark&logoColor=white" alt="PySpark"/>
<img src="https://img.shields.io/badge/Delta%20Lake-7C3AED?style=for-the-badge" alt="Delta Lake"/>
<img src="https://img.shields.io/badge/Power%20BI-D97706?style=for-the-badge&logo=powerbi&logoColor=white" alt="Power BI"/>
<img src="https://img.shields.io/badge/Node.js-15803D?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js"/>
<img src="https://img.shields.io/badge/AI%20Reporting-DB2777?style=for-the-badge" alt="AI Reporting"/>

<br><br>

[View Repository](https://github.com/sarishadeel206/Wealth-Management-Analytics)

</div>

---

## 📌 Project Snapshot

The **Wealth Management Analytics Platform** is an end-to-end data engineering and analytics project developed during a Data Engineering & AI Internship. It transforms raw wealth management data into structured warehouse tables, analytical Data Marts, API-accessible datasets, Power BI dashboards, and AI-assisted client reports.

The platform demonstrates how financial data can move through a complete pipeline—from preparation and modeling to business reporting.

## 🎯 What the Platform Delivers

- **Data Engineering:** Clean and transform raw financial datasets using Databricks and PySpark.
- **Dimensional Modeling:** Build Dimension and Fact tables for organized analytical querying.
- **Data Warehouse:** Store structured data using Delta tables.
- **Data Marts:** Prepare subject-specific datasets for executive, client, advisor, scheme, SIP, redemption, revenue, and AMC analysis.
- **REST APIs:** Expose selected Data Mart data through Node.js and Express.js endpoints.
- **Business Intelligence:** Present key metrics through an executive Power BI dashboard.
- **AI-Assisted Reporting:** Convert portfolio data into structured HTML reports for client-facing review.

## 🏗️ Architecture at a Glance

<div align="center">

<table>
<tr><td align="center"><b>01 · Source</b><br/>Raw CSV Data</td></tr>
<tr><td align="center">↓</td></tr>
<tr><td align="center"><b>02 · Process</b><br/>Databricks + PySpark<br/>Cleaning & Transformation</td></tr>
<tr><td align="center">↓</td></tr>
<tr><td align="center"><b>03 · Model</b><br/>Dimension Tables + Fact Tables<br/>Delta Lake Data Warehouse</td></tr>
<tr><td align="center">↓</td></tr>
<tr><td align="center"><b>04 · Serve</b><br/>Analytical Data Marts<br/>REST APIs with Node.js / Express</td></tr>
<tr><td align="center">↓</td></tr>
<tr><td align="center"><b>05 · Insights</b><br/>Power BI Dashboard<br/>AI-Powered Portfolio Reports</td></tr>
</table>

</div>

## 📊 Analytical Coverage

| Data Mart / Analysis | Business Focus |
|---|---|
| Executive Dashboard | High-level wealth management KPIs |
| Client Portfolio Summary | Client-level portfolio overview |
| Advisor Performance | Advisor-related analysis |
| Scheme Performance | Scheme-level metrics |
| Revenue Analytics | Revenue trends and summaries |
| SIP Analytics | Systematic Investment Plan metrics |
| Redemption Analytics | Redemption activity |
| AMC Analytics | Asset Management Company analysis |

## 💼 Executive Dashboard

The Power BI dashboard uses the Executive Dashboard Mart to surface important business metrics, including:

- Total Clients and Total Advisors
- Total Assets Under Management (AUM)
- Total Investment and Total Redemption
- Total Revenue
- Active SIPs and Active Schemes

These metrics provide a consolidated view of key wealth management activity.

## 🔌 REST API Layer

The backend uses **Node.js and Express.js** to expose selected Data Mart data through REST APIs. The endpoints return structured JSON responses for downstream applications and reporting workflows.

**API workflow:** Request → Express endpoint → Databricks Data Mart → JSON response

API behavior was tested using Postman.

## 🤖 AI-Powered Portfolio Reporting

Portfolio data retrieved through the API is passed to an AI model through the OpenRouter API to generate a structured HTML wealth management report.

The report is based on information available in the supplied portfolio data and is intended to help present that information clearly. It should not be treated as regulated financial advice, and unavailable values should not be assumed.

## 🧰 Technology Stack

| Area | Tools & Technologies |
|---|---|
| Data Engineering | Databricks, Apache Spark, PySpark |
| Storage & Warehouse | Delta Lake, Data Warehouse, Dimensional Modeling |
| Backend & APIs | Node.js, Express.js, REST APIs |
| API Testing | Postman, Databricks SQL Connector |
| Analytics & Visualization | Power BI, Python |
| AI Integration | OpenRouter API |
| Development | GitHub, GitHub Desktop, Visual Studio Code |

## 📁 Repository Structure

```text
Wealth-Management-Analytics/
├── Source_Code/
│   └── Node.js and REST API source files
├── Dimension_Tables/
│   └── PySpark dimension table notebooks
├── Fact_Tables/
│   └── PySpark fact table notebooks
├── Mart/
│   └── Analytical Data Mart notebooks
├── PowerBI_Dashboard/
│   └── Power BI dashboard files
├── Screenshots/
│   └── Project outputs and visualizations
└── README.md
```

## 🌱 Future Enhancements

- Integrate real-time market data sources.
- Add advanced portfolio risk analytics.
- Automate dashboard refresh and pipeline monitoring.
- Implement authentication and authorization for APIs.
- Deploy the platform on cloud infrastructure.
- Expand AI-generated insights and report delivery workflows.

## 👩‍💻 About

This project was developed as part of a Data Engineering & AI Internship and demonstrates practical work across data pipelines, dimensional modeling, Data Marts, APIs, BI dashboards, and AI-assisted reporting.

**Author:** Sarish Adeel

*Datasets used in this project are sample/dummy datasets intended for educational and internship project purposes.*

---

<div align="center">

### Engineering Data. Enabling Insights.

<sub>Databricks · PySpark · Delta Lake · Power BI · REST APIs · Generative AI</sub>

</div>
