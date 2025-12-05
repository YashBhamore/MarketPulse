import logging
import os
import pyodbc
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from dotenv import load_dotenv

# load .env file
load_dotenv()

SERVER = "bidemoserver.database.windows.net"
DATABASE = "MarketingAnalyticsDB"
USERNAME = "bi-sql-admin"
PASSWORD = os.getenv("SQL_PASSWORD")

def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)


def load_and_cluster_data():
    logging.info("Connecting to Azure SQL...")
    conn = get_connection()

    try:
        # -----------------------------
        # 1. Load data from SQL
        # -----------------------------
        df = pd.read_sql("SELECT * FROM MarketingCampaign", conn)

        # Missing Income
        df["Income"] = df["Income"].fillna(df["Income"].median())

        # Drop junk columns
        df = df.drop(columns=[c for c in ["ID", "Z_CostContact", "Z_Revenue"] if c in df.columns], errors="ignore")

        # Compute age
        df["Age"] = pd.Timestamp("today").year - df["Year_Birth"]
        df = df[(df["Age"] >= 18) & (df["Age"] <= 100)]

        # Parse customer date
        if "Dt_Customer" in df.columns:
            df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], errors="coerce")
            df["Dt_Customer"] = df["Dt_Customer"].fillna(df["Dt_Customer"].mode()[0])
            df["Customer_Tenure"] = (pd.Timestamp("today") - df["Dt_Customer"]).dt.days

        # Fill nulls
        num_cols = df.select_dtypes(include="number").columns
        cat_cols = df.select_dtypes(include="object").columns

        for col in num_cols:
            df[col] = df[col].fillna(df[col].median())
        for col in cat_cols:
            df[col] = df[col].fillna(df[col].mode()[0])

        # Feature engineering
        df["TotalSpend"] = df[[c for c in df.columns if c.startswith("Mnt")]].sum(axis=1)
        df["TotalPurchases"] = df[[c for c in df.columns if c.endswith("Purchases")]].sum(axis=1)

        if set(["Kidhome", "Teenhome"]).issubset(df.columns):
            df["FamilySize"] = df["Kidhome"] + df["Teenhome"]
            df["IsParent"] = (df["FamilySize"] > 0).astype(int)

        # accepted campaign columns
        camp_cols = [c for c in df.columns if c.lower().startswith("acceptedcmp")]
        if "Response" in df.columns:
            camp_cols.append("Response")
        df["AcceptedAnyCampaign"] = (df[camp_cols].sum(axis=1) > 0).astype(int)

        # outlier handling
        for col in ["Income", "TotalSpend"]:
            low, high = df[col].quantile([0.01, 0.99])
            df[col] = df[col].clip(lower=low, upper=high)

        df = df.drop(columns=["Dt_Customer"], errors="ignore")

        # encode + scale
        encoded = pd.get_dummies(df, drop_first=True)
        encoded = encoded.replace([np.inf, -np.inf], np.nan).fillna(encoded.median())

        scaler = StandardScaler()
        scaled = encoded.copy()
        scaled[encoded.columns] = scaler.fit_transform(encoded)

        # KMeans
        kmeans = KMeans(n_clusters=4, random_state=42, n_init="auto")
        scaled["Cluster"] = kmeans.fit_predict(scaled)

        df["Cluster"] = scaled["Cluster"]

        return df, kmeans

    finally:
        conn.close()
