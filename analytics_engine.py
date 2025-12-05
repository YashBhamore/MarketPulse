"""
analytics_engine.py
High-level helper functions for dashboards.
Builds on top of data_pipeline.py.
"""

from typing import Tuple, Dict, Optional
import pandas as pd

from data_pipeline import load_and_cluster_data

_df_cache: Optional[pd.DataFrame] = None
_model_cache = None



def refresh_data(force: bool = False) -> Tuple[pd.DataFrame, object]:
    """
    Load + clean + cluster the data.
    Uses a small cache to avoid hitting SQL multiple times.
    """
    global _df_cache, _model_cache

    if force or _df_cache is None:
        df, model = load_and_cluster_data()
        _df_cache = df
        _model_cache = model

    return _df_cache, _model_cache


def get_df() -> pd.DataFrame:
    """Return latest dataframe with Cluster column."""
    df, _ = refresh_data()
    return df

def get_cluster_summary() -> pd.DataFrame:
    """
    Summary for clusters:
    Cluster | Count | AvgIncome | AvgTotalSpend | AvgRecency
    """
    df = get_df()

    if "Cluster" not in df.columns:
        return pd.DataFrame(
            columns=["Cluster", "Count", "AvgIncome", "AvgTotalSpend", "AvgRecency"]
        )

    summary = (
        df.groupby("Cluster", as_index=False)
        .agg(
            Count=("Cluster", "size"),
            AvgIncome=("Income", "mean") if "Income" in df.columns else ("Cluster", "size"),
            AvgTotalSpend=("TotalSpend", "mean") if "TotalSpend" in df.columns else ("Cluster", "size"),
            AvgRecency=("Recency", "mean") if "Recency" in df.columns else ("Cluster", "size"),
        )
    )

    return summary



# ---------------------------------------------------------
#   MANAGER DASHBOARD METRICS
# ---------------------------------------------------------
def get_manager_kpis() -> Dict[str, float]:
    df = get_df()

    total_customers = len(df)
    avg_spend = float(df["TotalSpend"].mean()) if "TotalSpend" in df else 0
    total_revenue = float(df["TotalSpend"].sum()) if "TotalSpend" in df else 0

    if "AcceptedAnyCampaign" in df:
        campaign_rate = float(df["AcceptedAnyCampaign"].mean())
    else:
        campaign_rate = 0.0

    return {
        "total_customers": total_customers,
        "avg_customer_spend": avg_spend,
        "total_revenue": total_revenue,
        "accepted_campaign_rate": campaign_rate,
    }


def get_revenue_by_segment() -> pd.DataFrame:
    df = get_df()

    if "Cluster" not in df or "TotalSpend" not in df:
        return pd.DataFrame(columns=["Segment", "Revenue"])

    segment_map = {
        0: "High Value",
        1: "Medium Value",
        2: "Low Value",
        3: "At Risk",
    }

    tmp = df.copy()
    tmp["Segment"] = tmp["Cluster"].map(segment_map)

    return (
        tmp.groupby("Segment", as_index=False)
        .agg(Revenue=("TotalSpend", "sum"))
        .sort_values("Revenue", ascending=False)
    )


# ---------------------------------------------------------
#   DATA ANALYST DASHBOARD METRICS
# ---------------------------------------------------------
def get_segment_distribution() -> pd.DataFrame:
    df = get_df()

    if "Cluster" not in df:
        return pd.DataFrame(columns=["Segment", "CustomerCount"])

    segment_map = {
        0: "High Value",
        1: "Medium Value",
        2: "Low Value",
        3: "At Risk",
    }

    tmp = df.copy()
    tmp["Segment"] = tmp["Cluster"].map(segment_map)

    return (
        tmp.groupby("Segment", as_index=False)
        .agg(CustomerCount=("Segment", "size"))
        .sort_values("CustomerCount", ascending=False)
    )


def get_segment_spend_table() -> pd.DataFrame:
    df = get_df()

    if "Cluster" not in df or "TotalSpend" not in df:
        return pd.DataFrame(columns=["Segment", "CustomerCount", "AverageSpend", "TotalRevenue"])

    segment_map = {
        0: "High Value",
        1: "Medium Value",
        2: "Low Value",
        3: "At Risk",
    }

    tmp = df.copy()
    tmp["Segment"] = tmp["Cluster"].map(segment_map)

    return (
        tmp.groupby("Segment", as_index=False)
        .agg(
            CustomerCount=("Segment", "size"),
            AverageSpend=("TotalSpend", "mean"),
            TotalRevenue=("TotalSpend", "sum"),
        )
        .sort_values("TotalRevenue", ascending=False)
    )
