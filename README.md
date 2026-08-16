# Wealth Management Analytics Platform

An end-to-end **Wealth Management Analytics Platform** developed during a Data Engineering & AI Internship. The project focuses on transforming raw financial data into structured analytical datasets, Data Marts, APIs, dashboards, and AI-powered client reporting.

## 📌 Project Overview

The platform processes wealth management data using **Databricks and PySpark**, organizes the data using a dimensional data warehouse architecture, creates analytical Data Marts, exposes selected data through REST APIs, and presents insights through **Power BI and AI-generated reports**.

The project demonstrates an end-to-end data engineering workflow from raw data processing to business-level analytics.

## 🚀 Key Features

* Raw financial data processing using PySpark
* Data cleaning and transformation
* Dimension and Fact table creation
* Data Warehouse implementation using Delta tables
* Multiple analytical Data Marts
* REST API development for accessing Mart data
* Power BI executive dashboard
* AI-powered portfolio report generation
* Client portfolio analytics
* SIP, redemption, revenue and scheme analytics

## 🏗️ Project Architecture

```text
Raw CSV Data
      ↓
Databricks / PySpark
      ↓
Data Cleaning & Transformation
      ↓
Dimension Tables + Fact Tables
      ↓
Data Warehouse
      ↓
Data Marts
      ↓
REST APIs
      ↓
Power BI Dashboard
      ↓
AI-Powered Analytical Reports
```

## 🛠️ Technologies Used

### Data Engineering

* Databricks
* Apache Spark
* PySpark
* Delta Lake
* Data Warehousing
* Dimensional Modeling

### Backend & APIs

* Node.js
* Express.js
* REST APIs
* Databricks SQL Connector
* Postman

### Analytics & Visualization

* Power BI
* Python
* CSV datasets

### AI

* OpenRouter API
* AI-powered report generation

### Development Tools

* GitHub
* GitHub Desktop
* Visual Studio Code

## 📂 Repository Structure

```text
Wealth-Management-Analytics-Platform/
│
├── Source_Code/
│   └── Node.js and REST API source files
│
├── Dimension_Tables/
│   └── PySpark dimension table notebooks
│
├── Fact_Tables/
│   └── PySpark fact table notebooks
│
├── Mart/
│   └── Analytical Data Mart notebooks
│
├── PowerBI_Dashboard/
│   └── Power BI dashboard
│
├── Screenshots/
│   └── Project outputs and visualizations
│
└── README.md
```

## 🗄️ Data Warehouse

The project follows a structured warehouse approach consisting of:

* Dimension Tables
* Fact Tables
* Data Marts

Important dimensions include client, advisor, scheme and time-related information.

The Data Marts were created for different analytical requirements such as:

* Executive Dashboard
* Client Portfolio Summary
* Advisor Performance
* Scheme Performance
* Revenue Analytics
* SIP Analytics
* Redemption Analytics
* AMC Analytics

## 📊 Power BI Dashboard

An executive-level Power BI dashboard was created using the Executive Dashboard Mart.

The dashboard includes key metrics such as:

* Total Clients
* Total Advisors
* Total AUM
* Total Investment
* Total Redemption
* Total Revenue
* Active SIPs
* Active Schemes

## 🔗 REST API

REST APIs were developed using Node.js and Express.js to retrieve data from Databricks Data Marts.

The APIs provide structured JSON responses that can be consumed by applications and reporting workflows.

API testing was performed using Postman.

## 🤖 AI-Powered Reporting

The project also includes AI-assisted financial reporting.

Portfolio data retrieved through the API is processed and provided to an AI model to generate a structured client-ready wealth management report in HTML format.

The generated report focuses on portfolio information available in the dataset and avoids assuming unavailable values.

## 📈 Key Outcomes

* Implemented an end-to-end data engineering workflow
* Created structured Dimension and Fact tables
* Developed multiple analytical Data Marts
* Built REST APIs for Mart-level data access
* Created an executive Power BI dashboard
* Integrated AI-assisted analytical report generation
* Gained practical experience with Databricks, PySpark, APIs, Power BI and AI technologies

## 🔮 Future Enhancements

* Real-time market data integration
* Advanced portfolio risk analytics
* Automated dashboard refresh pipelines
* Authentication and authorization for APIs
* Deployment on cloud infrastructure
* More advanced AI-based financial insights
* Automated report delivery

## 👨‍💻 Author

**Sarish Adeel**


The datasets used for this project are sample/dummy datasets created for educational and internship project purposes.
