import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# ---------- ANALYTICAL ENGINE ----------
from analytics_engine import (
    refresh_data,
    get_manager_kpis,
    get_revenue_by_segment,
    get_segment_distribution,
    get_segment_spend_table,
    get_cluster_summary,
)
@st.cache_data(show_spinner=True)
def load_data():
    df, model = refresh_data()
    return df

# ---------- DATA ANALYST PAGE STATE ----------
def init_da_state():
    if "da_page" not in st.session_state:
        st.session_state.da_page = "home"


# --------------------------------------------------------
#  COMMON LOGOUT SIDEBAR FOR EVERY ROLE
# --------------------------------------------------------
def sidebar(role):
    st.sidebar.title("MarketPulse")
    st.sidebar.write(f"Role: **{role}**")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()
st.markdown("""
    <style>
        .stButton>button {
            background-color: #111827;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #000;
        }
    </style>
""", unsafe_allow_html=True)


# --------------------------------------------------------
#  MAIN ROUTER CALLED BY App.py
# --------------------------------------------------------

def show_dashboard():
    role = st.session_state.get("role", None)

    if role == "Manager":
        manager_dashboard()

    elif role == "Marketing Analyst":
        marketing_analyst_dashboard()

    elif role == "Data Analyst":
        data_analyst_router()

    elif role == "Employee":
        employee_dashboard()

    elif role == "Admin":
        admin_dashboard()

    else:
        st.error("No role found. Please log in again.")
        st.session_state.logged_in = False
    
# --------------------------------------------------------
#  MANAGER DASHBOARD  
# --------------------------------------------------------
def manager_dashboard():
    sidebar("Manager")

    # ---------------- Header ----------------
    st.title("Manager Dashboard")

    # ------ Load Real Data ------
    df = load_data()
    kpis = get_manager_kpis()

    total_customers = kpis["total_customers"]
    avg_spend = round(kpis["avg_customer_spend"], 2)
    total_revenue = round(kpis["total_revenue"], 2)
    campaign_rate = round(kpis["accepted_campaign_rate"] * 100, 2)

    # ---------------- KPI Cards ----------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Customers</div>
            <div class="metric-value">{total_customers}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Customer Spend</div>
            <div class="metric-value">${avg_spend}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Revenue</div>
            <div class="metric-value">${total_revenue}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Campaign Acceptance</div>
            <div class="metric-value">{campaign_rate}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ---------------- Revenue By Segment ----------------
    st.subheader("Revenue by Segment")
    seg_df = get_revenue_by_segment()

    if seg_df.empty:
        st.info("No revenue data available.")
    else:
        fig = px.bar(
            seg_df,
            x="Segment",
            y="Revenue",
            text="Revenue",
            color="Segment",
            height=380
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ---------- ROI SUMMARY TABLE ----------
    st.subheader("ROI Summary")
    st.caption("Return on investment for active and completed campaigns")

    roi_df = pd.DataFrame({
        "Campaign": ["Spring Sale 2025", "Email Newsletter", "Retargeting Campaign", "Social Media Ads"],
        "ROI": ["245%", "178%", "312%", "156%"],
        "Revenue": ["$38,450", "$28,900", "$52,100", "$21,340"],
        "Cost": ["$12,450", "$10,400", "$12,800", "$8,340"],
        "Status": ["Active", "Active", "Active", "Completed"]
    })

    st.dataframe(roi_df, use_container_width=True)


# --------------------------------------------------------
#  MARKETING ANALYST DASHBOARD
# --------------------------------------------------------
def marketing_analyst_dashboard():
    sidebar("Marketing Analyst")

    # ---------- HEADER ----------
    st.title("Marketing Analyst Dashboard")

    # ---------- GLOBAL CSS ----------
    st.markdown("""
        <style>
            .kpi-box {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                padding: 18px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            }
            .kpi-title {
                font-size: 13px;
                color: #6b7280;
                margin-bottom: 4px;
            }
            .kpi-value {
                font-size: 26px;
                font-weight: 600;
                color: #111827;
            }
            .kpi-mini {
                font-size: 12px;
                color: #10b981;
            }
            .header-btn {
                background-color: #111827;
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                font-size: 14px;
            }
            .header-btn:hover {
                background-color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)

    # ---------- Header ----------
    col_header1, col_header2 = st.columns([6, 1])
    with col_header1:
        st.title("Marketing Analyst Dashboard")
    with col_header2:
        st.markdown("""
            <button class="header-btn" onclick="window.location.href='/?create_campaign=true'">
                ➕ Create
            </button>
        """, unsafe_allow_html=True)


    # --------------------------------------------------------
    #  KPI ROW (STATIC FOR NOW)
    # --------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="kpi-box">
                <div class="kpi-title">Total Campaigns</div>
                <div class="kpi-value">42</div>
                <div class="kpi-mini">+5 this quarter</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="kpi-box">
                <div class="kpi-title">Avg ROI</div>
                <div class="kpi-value">189%</div>
                <div class="kpi-mini">+12% YoY</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="kpi-box">
                <div class="kpi-title">Customer Reach</div>
                <div class="kpi-value">1.2M</div>
                <div class="kpi-mini">+8.4%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="kpi-box">
                <div class="kpi-title">Engagement Rate</div>
                <div class="kpi-value">32%</div>
                <div class="kpi-mini">+3.5%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("")


    # --------------------------------------------------------
    #  ROI TREND (STATIC)
    # --------------------------------------------------------
    st.subheader("Campaign ROI Trend")
    st.caption("Performance across last 6 major campaigns")

    df_roi = pd.DataFrame({
        "Campaign": ["Holiday", "VIP", "Email", "Spring", "Members", "Flash Sale"],
        "ROI (%)": [312, 245, 178, 165, 198, 154]
    })

    fig_line = px.line(
        df_roi, x="Campaign", y="ROI (%)", markers=True
    )
    fig_line.update_traces(line_color="#1f77b4", marker_size=8)
    fig_line.update_layout(height=360)

    st.plotly_chart(fig_line, use_container_width=True)


    # --------------------------------------------------------
    #  SEGMENT PERFORMANCE (REAL DATA NOW)
    # --------------------------------------------------------
    st.subheader("Customer Segment Engagement Performance")
    st.caption("How different segments responded to campaigns")

    # Load real segment distribution from analytics engine
    seg_df = get_segment_distribution()  # Segment | CustomerCount

    if not seg_df.empty:
        fig_bar = px.bar(
            seg_df,
            x="CustomerCount",
            y="Segment",
            orientation="h",
            color="CustomerCount",
            color_continuous_scale="Blues",
            height=350
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No segment data found. Please refresh engine.")


    # --------------------------------------------------------
    #  CAMPAIGN SUMMARY TABLE (STATIC)
    # --------------------------------------------------------
    st.subheader("Campaign Summary Table")

    df_table = pd.DataFrame({
        "Campaign": ["Holiday Promo", "VIP Offer", "Spring Sale", "Email Blast", "Flash Sale"],
        "ROI": ["312%", "245%", "165%", "178%", "154%"],
        "Reach": ["410k", "320k", "280k", "190k", "220k"],
        "Cost": ["$12.8k", "$12.4k", "$10.1k", "$8.9k", "$7.1k"],
        "Status": ["Completed", "Active", "Active", "Active", "Completed"]
    })

    st.dataframe(df_table, use_container_width=True)





# --------------------------------------------------------
#  DATA ANALYST DASHBOARD
# --------------------------------------------------------
# =====================================================================
#                   DATA ANALYST DASHBOARD (ENGINE-INTEGRATED)
# =====================================================================

def data_analyst_home():
    sidebar("Data Analyst")

    st.title("Data Analyst Dashboard")

    # ---------- CSS ----------
    st.markdown("""
        <style>
            .card-click {
                background: #ffffff;
                padding: 24px;
                border-radius: 14px;
                border: 1px solid #e5e7eb;
                text-align: center;
                cursor: pointer;
                box-shadow: 0 1px 2px rgba(0,0,0,0.06);
                transition: 0.1s ease-in-out;
            }
            .card-click:hover {
                transform: translateY(-4px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.10);
            }
            .card-icon {
                font-size: 32px;
                margin-bottom: 10px;
            }
            .card-title {
                font-size: 18px;
                font-weight: 600;
            }
            .card-sub {
                font-size: 14px;
                color: #6b7280;
            }
        </style>
    """, unsafe_allow_html=True)

    # ---------- LOAD REAL DATA ----------
    df = load_data()
    seg_dist = get_segment_distribution()
    spend_table = get_segment_spend_table()

    # ---------- FEATURE CARDS ----------
    c1, c2, c3 = st.columns(3)

    # Card 1 – Insights
    with c1:
        if st.button("insights_hidden", key="ins_btn"):
            st.session_state.da_page = "insights"
            st.rerun()

        st.markdown("""
            <div class="card-click" onclick="document.querySelector('button[k=\'ins_btn\']').click()">
                <div class="card-icon">📈</div>
                <div class="card-title">View Insights</div>
                <div class="card-sub">Detailed segmentation analysis</div>
            </div>
        """, unsafe_allow_html=True)

    # Card 2 – Clusters
    with c2:
        if st.button("clusters_hidden", key="clu_btn"):
            st.session_state.da_page = "clusters"
            st.rerun()

        st.markdown("""
            <div class="card-click" onclick="document.querySelector('button[k=\'clu_btn\']').click()">
                <div class="card-icon">🧩</div>
                <div class="card-title">Cluster Insights</div>
                <div class="card-sub">Explore customer clusters</div>
            </div>
        """, unsafe_allow_html=True)

    # Card 3 – Report
    with c3:
        if st.button("report_hidden", key="rep_btn"):
            st.session_state.da_page = "report"
            st.rerun()

        st.markdown("""
            <div class="card-click" onclick="document.querySelector('button[k=\'rep_btn\']').click()">
                <div class="card-icon">📥</div>
                <div class="card-title">Generate Report</div>
                <div class="card-sub">Create campaign summary reports</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ---------- CUSTOMER SEGMENTATION ----------
    st.subheader("Customer Segmentation Overview")
    st.caption("Distribution of customers by segment")

    left, right = st.columns([1.4, 1])

    # PIE CHART (REAL ENGINE DATA)
    with left:
        if not seg_dist.empty:
            fig = px.pie(
                seg_dist,
                names="Segment",
                values="CustomerCount",
                hole=0.35
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No segmentation data available from engine.")

    # SEGMENT OVERVIEW (REAL)
    with right:
        if not seg_dist.empty:
            st.markdown("### Segment Overview")
            for _, row in seg_dist.iterrows():
                st.write(f"• **{row['Segment']}** → {row['CustomerCount']} customers")
        else:
            st.write("No overview data available.")

    # ---------- SPEND TABLE ----------
    st.subheader("Spend Analysis by Segment")
    st.caption("Detailed spending metrics for each customer segment")

    if not spend_table.empty:
        st.dataframe(spend_table, use_container_width=True)
    else:
        st.info("Spend data not available from engine yet.")



# =====================================================================
#                   DATA ANALYST – INSIGHTS (ENGINE)
# =====================================================================

def data_analyst_insights():
    sidebar("Data Analyst")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.da_page = "home"
        st.rerun()

    st.title("📈 Insights")
    st.caption("Real segmentation & customer behavior insights from Azure SQL")

    df = load_data()
    summary = get_cluster_summary()

    st.subheader("Cluster Summary")
    if not summary.empty:
        st.dataframe(summary, use_container_width=True)
    else:
        st.info("No cluster summary available.")



# =====================================================================
#                   DATA ANALYST – CLUSTERS (ENGINE)
# =====================================================================

def data_analyst_clusters():
    sidebar("Data Analyst")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.da_page = "home"
        st.rerun()

    st.title("🧩 Cluster Insights")
    st.caption("Machine-learning based cluster breakdown")

    df = load_data()

    # Cluster distribution chart
    st.subheader("Cluster Distribution")
    if "Cluster" in df.columns:
        st.bar_chart(df["Cluster"].value_counts().sort_index())
    else:
        st.info("Cluster column missing from engine output.")

    st.subheader("Sample Customers")
    st.dataframe(df.tail(20), use_container_width=True)



def data_analyst_report():
    sidebar("Data Analyst")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.da_page = "home"
        st.rerun()

    st.title("📥 Generate Report")
    st.caption("Explore dataset and generate insights")

    df = load_data()

    # ================================
    # SIMPLE EDA SECTION
    # ================================
    st.markdown("## 🔍 Exploratory Data Analysis (EDA)")

    # ------------------------------------------------
    # 1 — CLEAN DATASET SUMMARY (not JSON anymore)
    # ------------------------------------------------
    st.markdown("### 📘 Dataset Summary")

    summary_df = pd.DataFrame({
        "Metric": ["Rows", "Columns", "Numeric Columns", "Categorical Columns", "Missing Values", "Duplicate Rows"],
        "Value": [
            df.shape[0],
            df.shape[1],
            len(df.select_dtypes(include=np.number).columns),
            len(df.select_dtypes(exclude=np.number).columns),
            df.isna().sum().sum(),
            df.duplicated().sum()
        ]
    })

    st.dataframe(summary_df, use_container_width=True)
    st.markdown("---")

    # ------------------------------------------------
    # 2 — Data Preview
    # ------------------------------------------------
    st.markdown("### 👀 Data Preview")
    option = st.radio(
        "Choose view:",
        ["Head (Top 5)", "Tail (Bottom 5)", "Full Dataset"],
        horizontal=True
    )

    if option == "Head (Top 5)":
        st.dataframe(df.head())
    elif option == "Tail (Bottom 5)":
        st.dataframe(df.tail())
    else:
        st.dataframe(df)

    st.markdown("---")

    # ------------------------------------------------
    # 3 — Missing Values
    # ------------------------------------------------
    st.markdown("### ⚠ Missing Value Summary")
    missing_df = (
        df.isna().sum().reset_index()
        .rename(columns={"index": "Column", 0: "Missing Count"})
    )
    missing_df["Missing %"] = (missing_df["Missing Count"] / len(df) * 100).round(2)

    st.dataframe(missing_df, use_container_width=True)
    st.markdown("---")

    # ------------------------------------------------
    # 4 — Column Types
    # ------------------------------------------------
    st.markdown("### 🏷 Column Types")
    st.write(df.dtypes)
    st.markdown("---")

    # ------------------------------------------------
    # 5 — Distribution Explorer
    # ------------------------------------------------
    st.markdown("### 📊 Column Distribution Explorer")
    col_to_plot = st.selectbox("Select a column", df.columns)

    if col_to_plot:
        fig, ax = plt.subplots(figsize=(8, 4))

        if np.issubdtype(df[col_to_plot].dtype, np.number):
            sns.histplot(df[col_to_plot].dropna(), kde=True, ax=ax, color="#a855f7")
        else:
            df[col_to_plot].value_counts().plot(kind="bar", ax=ax, color="#a855f7")

        ax.set_title(f"Distribution of {col_to_plot}")
        st.pyplot(fig)

    st.markdown("---")

    # ------------------------------------------------
    # 6 — HALF CORRELATION HEATMAP (MASKED)
    # ------------------------------------------------
    st.markdown("### 🔥 Correlation Heatmap")

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] > 1:
        corr = numeric_df.corr()

        # MASK upper triangle for cleaner heatmap
        mask = np.triu(np.ones_like(corr, dtype=bool))

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            corr,
            mask=mask,
            annot=True,
            cmap="Purples",
            fmt=".2f",
            linewidths=0.5,
            square=True,
            cbar=True,
            ax=ax
        )
        st.pyplot(fig)
    else:
        st.info("Not enough numeric columns for correlation heatmap.")

    st.markdown("---")





# --------------------------------------------------------
#  EMPLOYEE DASHBOARD
# --------------------------------------------------------
def employee_dashboard():
    sidebar("Employee")

    st.title("Employee Dashboard")
    st.markdown("")  # small spacing

    # =========================================================
    #   CUSTOMER REG + MEMBERSHIP DETAILS (SIDE BY SIDE)
    # =========================================================
    left, right = st.columns([2, 1])

    # ======================= LEFT: CUSTOMER REGISTRATION =======================
    with left:
        st.markdown("### Customer Registration")
        st.caption("Add new customer to the system")

        st.markdown("""
            <style>
                .input-box {
                    background: #f3f4f6;
                    padding: 14px;
                    border-radius: 10px;
                    border: 1px solid #e5e7eb;
                }
                .submit-btn {
                    background-color: #111827 !important;
                    color: white !important;
                    border-radius: 10px !important;
                    padding: 10px 16px !important;
                    font-size: 15px !important;
                    border: none !important;
                }
            </style>
        """, unsafe_allow_html=True)

        with st.form("reg_form"):
            name = st.text_input("Full Name", placeholder="Enter customer name")
            email = st.text_input("Email Address", placeholder="Enter email address")
            phone = st.text_input("Phone Number", placeholder="Enter phone number")
            tier = st.selectbox("Membership Tier", ["Bronze", "Silver", "Gold"])

            submit = st.form_submit_button("➕ Add New Customer")

        if submit:
            st.success(f"Customer **{name}** added!")

    # ======================= RIGHT: MEMBERSHIP DETAILS =======================
    with right:
        st.markdown("### Membership Details")
        st.caption("Current membership tier breakdown")

        st.markdown("""
            <style>
                .tier-card {
                    background: white;
                    padding: 16px;
                    border-radius: 12px;
                    border: 1px solid #e5e7eb;
                    margin-bottom: 14px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .tier-left {
                    font-size: 16px;
                    font-weight: 600;
                }
                .tier-sub {
                    font-size: 13px;
                    color: #6b7280;
                }
                .tier-num {
                    font-size: 22px;
                    font-weight: 700;
                }
            </style>
        """, unsafe_allow_html=True)

        # Gold
        st.markdown("""
            <div class="tier-card">
                <div>
                    <div class="tier-left">🟨 Gold Members</div>
                    <div class="tier-sub">Free shipping, 20% off</div>
                </div>
                <div class="tier-num">145</div>
            </div>
        """, unsafe_allow_html=True)

        # Silver
        st.markdown("""
            <div class="tier-card">
                <div>
                    <div class="tier-left">⬜ Silver Members</div>
                    <div class="tier-sub">Free shipping, 10% off</div>
                </div>
                <div class="tier-num">328</div>
            </div>
        """, unsafe_allow_html=True)

        # Bronze
        st.markdown("""
            <div class="tier-card">
                <div>
                    <div class="tier-left">🟧 Bronze Members</div>
                    <div class="tier-sub">5% off purchases</div>
                </div>
                <div class="tier-num">892</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")  # nice separator line

    # =========================================================
    #   PURCHASE TRACKING SECTION
    # =========================================================
    st.markdown("### Purchase Tracking")
    st.caption("Recent customer transactions")

    purchases = pd.DataFrame({
        "Order ID": ["P001", "P002", "P003", "P004", "P005"],
        "Customer": ["John Smith", "Emma Johnson", "Michael Brown", "Sarah Davis", "James Wilson"],
        "Amount": ["$245.00", "$89.50", "$432.00", "$156.75", "$312.00"],
        "Date": ["2025-10-20", "2025-10-20", "2025-10-19", "2025-10-19", "2025-10-18"],
        "Status": ["Completed", "Completed", "Completed", "Pending", "Completed"]
    })

    def status_badge(status):
        if status == "Completed":
            return "<span style='background:#bbf7d0;padding:6px 12px;border-radius:12px;color:#166534;font-weight:600;'>Completed</span>"
        else:
            return "<span style='background:#fef3c7;padding:6px 12px;border-radius:12px;color:#92400e;font-weight:600;'>Pending</span>"

    purchases["Status"] = purchases["Status"].apply(status_badge)

    st.markdown("""
        <style>
            td, th { padding: 10px; font-size: 15px; }
        </style>
    """, unsafe_allow_html=True)

    st.write(
        purchases.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )


# --------------------------------------------------------
#  ADMIN DASHBOARD
# --------------------------------------------------------
def admin_dashboard():
    sidebar("Admin")
    st.title("Admin Dashboard")

    # --------------------------------------------------------
    # GLOBAL CSS
    # --------------------------------------------------------
    st.markdown("""
    <style>
        .status-banner {
            padding: 16px;
            background: #ecfdf5;
            border: 1px solid #bbf7d0;
            border-radius: 12px;
            font-size: 16px;
            color: #065f46;
            margin-bottom: 24px;
        }
        .metric-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .metric-title {
            font-size: 14px;
            color: #6b7280;
        }
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            margin-top: 4px;
        }
        .metric-sub {
            font-size: 14px;
            color: #10b981;
            margin-top: -4px;
        }
        .setting-card {
            padding: 18px 20px;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            background: #f9fafb;
            margin-top: 12px;
            margin-bottom: 10px;
        }
        .setting-title {
            font-size: 16px;
            font-weight: 600;
            color: #111827;
        }
        .setting-sub {
            font-size: 13px;
            color: #6b7280;
        }
        .backup-btn {
            background-color: #0f172a;
            color: white;
            padding: 14px;
            border-radius: 12px;
            font-size: 16px;
            text-align: center;
            cursor: pointer;
            border: none;
            width: 100%;
        }
        .backup-btn:hover {
            background-color: #000000;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # STATUS BANNER
    # --------------------------------------------------------
    st.markdown("<div class='status-banner'>✔ All systems operational. No issues detected.</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Total Users</div>
            <div class="metric-value">42</div>
            <div class="metric-sub">+5 this month</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">System Uptime</div>
            <div class="metric-value">99.8%</div>
            <div class="metric-sub">Last 30 days</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Database Size</div>
            <div class="metric-value">24.5 GB</div>
            <div class="metric-sub">of 100 GB</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Security Score</div>
            <div class="metric-value">A+</div>
            <div class="metric-sub" style="color:#10b981;">Excellent</div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # USER MANAGEMENT
    # --------------------------------------------------------
    st.subheader("User Management")
    st.caption("Manage system users and access")

    users = pd.DataFrame({
        "Name": ["John Manager", "Sarah Analyst", "Mike Employee", "Lisa Admin", "Tom Analyst"],
        "Email": ["john@company.com", "sarah@company.com", "mike@company.com", "lisa@company.com", "tom@company.com"],
        "Role": ["Manager", "Analyst", "Employee", "Admin", "Analyst"],
        "Status": ["Active", "Active", "Active", "Active", "Inactive"]
    })

    st.dataframe(users, use_container_width=True)
    st.markdown("---")

    # --------------------------------------------------------
    # SECURITY & BACKUP SETTINGS
    # --------------------------------------------------------
    st.subheader("Security & Backup Settings")
    st.caption("Configure system security and backup options")

    # Toggle 1
    with st.container():
        st.markdown("<div class='setting-card'>", unsafe_allow_html=True)
        a, b = st.columns([7, 1])
        with a:
            st.markdown("<div class='setting-title'>Automatic Backups</div><div class='setting-sub'>Daily at 2:00 AM</div>", unsafe_allow_html=True)
        with b:
            st.toggle("", key="auto_backup")
        st.markdown("</div>", unsafe_allow_html=True)

    # Toggle 2
    with st.container():
        st.markdown("<div class='setting-card'>", unsafe_allow_html=True)
        a, b = st.columns([7, 1])
        with a:
            st.markdown("<div class='setting-title'>Two-Factor Authentication</div><div class='setting-sub'>Required for admins</div>", unsafe_allow_html=True)
        with b:
            st.toggle("", key="two_factor")
        st.markdown("</div>", unsafe_allow_html=True)

    # Toggle 3
    with st.container():
        st.markdown("<div class='setting-card'>", unsafe_allow_html=True)
        a, b = st.columns([7, 1])
        with a:
            st.markdown("<div class='setting-title'>API Access</div><div class='setting-sub'>Enable external API connections</div>", unsafe_allow_html=True)
        with b:
            st.toggle("", key="api_access")
        st.markdown("</div>", unsafe_allow_html=True)

    # Manual Backup Button
    if st.button("💾 Run Manual Backup"):
        with st.spinner("Running backup..."):
            import time
            time.sleep(1)
            st.info("📡 Uploading to database…")
            time.sleep(1)
            st.success("✅ Backup completed successfully!")

    # --------------------------------------------------------
    # SYSTEM UPTIME (LINE CHART)
    # --------------------------------------------------------
    st.subheader("System Uptime (24 Hours)")
    df_up = pd.DataFrame({
        "Time": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"],
        "Uptime": [99.9, 99.76, 99.85, 100, 99.6, 99.82, 100]
    })
    fig = px.line(df_up, x="Time", y="Uptime", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # SYSTEM LOGS
    # --------------------------------------------------------
    st.subheader("System Logs")
    logs = pd.DataFrame({
        "Timestamp": ["2025-10-21 15:45", "2025-10-21 14:32", "2025-10-21 13:15"],
        "Event": ["Role Permission Updated", "User Login", "Data Upload"],
        "User": ["lisa@company.com", "john@company.com", "sarah@company.com"],
        "Status": ["Success", "Success", "Success"]
    })
    st.dataframe(logs, use_container_width=True)




# ---------- DATA ANALYST ROUTER ----------
def data_analyst_router():
    if st.session_state.da_page == "home":
        data_analyst_home()
    elif st.session_state.da_page == "insights":
        data_analyst_insights()
    elif st.session_state.da_page == "clusters":
        data_analyst_clusters()
    elif st.session_state.da_page == "report":
        data_analyst_report()
