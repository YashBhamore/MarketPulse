MarketPulse

A role-based marketing analytics dashboard built with Streamlit, Python, and a custom analytical engine.

🚀 Overview

MarketPulse is an interactive analytics platform designed to simulate a real-world marketing intelligence system. It supports role-based access (Manager, Marketing Analyst, Data Analyst, Employee) and provides KPIs, dashboards, segmentation insights, and reporting tools.

This repository includes:

Streamlit UI application

Full analytical engine

Synthetic data pipeline

SQL/Blob storage connection logic (Azure-ready)

🔧 Tech Stack

Python

Streamlit

Pandas / NumPy

Plotly / Matplotlib

Azure SQL + Blob (optional integration)

Custom marketing analytics engine

📂 Project Structure

├── App.py                 # Main Streamlit app

├── dashboards.py          # Role-based dashboards

├── analytics_engine.py    # Core analytics logic

├── data_pipeline.py       # Data ingestion processing

├── assets/                # Images/icons

├── pages/                 # Multi-page UI 

└── .gitignore

▶️ How to Run

Install required packages:

pip install -r requirements.txt


Run the app:

streamlit run App.py

📈 Features

KPI cards

Customer segmentation

Campaign ROI analytics

Revenue dashboards

Synthetic data generator 

Authentication and role-based views

👨‍💻 Team
Lead Developer: Yash Bhamore
Database Handling: Mike Chastine 
