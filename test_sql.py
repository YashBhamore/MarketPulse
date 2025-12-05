import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

SERVER = "bidemoserver.database.windows.net"
DATABASE = "MarketingAnalyticsDB"
USERNAME = "bi-sql-admin"
PASSWORD = os.getenv("SQL_PASSWORD")

def test_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )

        print("✅ Connected to Azure SQL!")

        df = pd.read_sql("SELECT TOP 5 * FROM MarketingCampaign", conn)
        print(df)

        conn.close()
        print("🔌 Connection closed.")

    except Exception as e:
        print("❌ Connection failed!")
        print(e)

if __name__ == "__main__":
    test_connection()
