import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import date

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="FinanceFlow",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path("finance_data.csv")

COLUMNS = [
    "ID",
    "Date",
    "Type",
    "Category",
    "Description",
    "Amount"
]

INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Business",
    "Investment",
    "Gift",
    "Other Income"
]

EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Health",
    "Entertainment",
    "Rent",
    "Travel",
    "Other"
]


# =========================================================
# PREMIUM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f6f8fc;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

.sidebar-logo {
    font-size: 25px;
    font-weight: 800;
    color: white;
    margin-bottom: 4px;
}

.sidebar-subtitle {
    color: #9ca3af;
    font-size: 12px;
    margin-bottom: 30px;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Header */
.dashboard-title {
    font-size: 32px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 4px;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 14px;
}

/* Cards */
.metric-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 5px 20px rgba(17,24,39,0.04);
}

.metric-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.metric-label {
    color: #6b7280;
    font-size: 13px;
    font-weight: 600;
}

.metric-icon {
    width: 38px;
    height: 38px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f3f4f6;
    font-size: 19px;
}

.metric-value {
    font-size: 27px;
    font-weight: 800;
    color: #111827;
    margin-top: 18px;
}

.metric-positive {
    color: #059669;
    font-size: 12px;
    font-weight: 600;
}

.metric-negative {
    color: #dc2626;
    font-size: 12px;
    font-weight: 600;
}

/* Section */
.section-title {
    font-size: 20px;
    font-weight: 750;
    color: #111827;
    margin-top: 25px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #6b7280;
    font-size: 13px;
    margin-bottom: 15px;
}

/* White panels */
.panel {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 5px 20px rgba(17,24,39,0.04);
}

/* Budget */
.budget-box {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px;
    margin-top: 20px;
}

.budget-title {
    font-weight: 700;
    font-size: 16px;
    color: #111827;
}

.budget-amount {
    font-size: 24px;
    font-weight: 800;
    margin-top: 8px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    font-weight: 600;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #111827;
}

/* Form */
div[data-testid="stForm"] {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 25px;
}

/* Inputs */
input, textarea {
    border-radius: 10px !important;
}

/* Divider */
hr {
    border-color: #e5e7eb;
}

/* Transaction badge */
.income-badge {
    color: #047857;
    background: #ecfdf5;
    padding: 5px 10px;
    border-radius: 20px;
    font-weight: 600;
}

.expense-badge {
    color: #b91c1c;
    background: #fef2f2;
    padding: 5px 10px;
    border-radius: 20px;
    font-weight: 600;
}

/* Footer */
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 12px;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA FUNCTIONS
# =========================================================

def create_file():
    if not DATA_FILE.exists():
        pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)


def load_data():
    create_file()

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        return pd.DataFrame(columns=COLUMNS)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    return df


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


def add_transaction(transaction_type, category, description, amount, transaction_date):

    df = load_data()

    if df.empty:
        new_id = 1
    else:
        new_id = int(df["ID"].max()) + 1

    new_row = pd.DataFrame([{
        "ID": new_id,
        "Date": transaction_date,
        "Type": transaction_type,
        "Category": category,
        "Description": description,
        "Amount": amount
    }])

    df = pd.concat([df, new_row], ignore_index=True)

    save_data(df)


def delete_transaction(transaction_id):

    df = load_data()

    df = df[df["ID"] != transaction_id]

    save_data(df)


# =========================================================
# LOAD DATA
# =========================================================

df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">💰 FinanceFlow</div>
    <div class="sidebar-subtitle">Personal Finance Manager</div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")

    page = st.radio(
        "",
        [
            "🏠 Dashboard",
            "💳 Transactions",
            "📊 Analytics",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Monthly Budget")

    monthly_budget = st.number_input(
        "Budget",
        min_value=0.0,
        value=100000.0,
        step=5000.0,
        format="%.0f"
    )

    st.divider()

    st.caption("FinanceFlow v1.0")
    st.caption("Local & private")


# =========================================================
# CALCULATIONS
# =========================================================

income = df.loc[df["Type"] == "Income", "Amount"].sum()

expenses = df.loc[df["Type"] == "Expense", "Amount"].sum()

balance = income - expenses

if income > 0:
    savings_rate = (balance / income) * 100
else:
    savings_rate = 0

budget_used = expenses

if monthly_budget > 0:
    budget_percentage = min((budget_used / monthly_budget) * 100, 100)
else:
    budget_percentage = 0


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="dashboard-title">Good evening 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Here is your financial overview.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # ================= METRICS =================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">TOTAL INCOME</div>
                <div class="metric-icon">💵</div>
            </div>
            <div class="metric-value">Rs {income:,.0f}</div>
            <div class="metric-positive">Money received</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">TOTAL EXPENSES</div>
                <div class="metric-icon">💸</div>
            </div>
            <div class="metric-value">Rs {expenses:,.0f}</div>
            <div class="metric-negative">Money spent</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        balance_class = "metric-positive" if balance >= 0 else "metric-negative"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">BALANCE</div>
                <div class="metric-icon">💰</div>
            </div>
            <div class="metric-value">Rs {balance:,.0f}</div>
            <div class="{balance_class}">Available balance</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">SAVINGS RATE</div>
                <div class="metric-icon">📈</div>
            </div>
            <div class="metric-value">{savings_rate:.1f}%</div>
            <div class="metric-positive">Income saved</div>
        </div>
        """, unsafe_allow_html=True)

    # ================= BUDGET =================

    st.markdown(
        '<div class="section-title">Monthly Budget</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Track your spending against your monthly limit.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="budget-box">
            <div class="budget-title">Budget Used</div>
            <div class="budget-amount">
                Rs {budget_used:,.0f}
                <span style="font-size:14px;color:#6b7280;">
                    / Rs {monthly_budget:,.0f}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(budget_percentage / 100)

    if budget_used > monthly_budget:
        st.error(
            f"⚠️ Budget exceeded by Rs {budget_used - monthly_budget:,.0f}"
        )
    elif budget_percentage >= 80:
        st.warning(
            f"⚠️ You have used {budget_percentage:.1f}% of your budget."
        )
    else:
        st.success(
            f"✓ You have used {budget_percentage:.1f}% of your budget."
        )

    # ================= CHARTS =================

    st.markdown(
        '<div class="section-title">Financial Overview</div>',
        unsafe_allow_html=True
    )

    chart1, chart2 = st.columns(2)

    with chart1:

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        st.subheader("Income vs Expenses")

        if not df.empty:

            monthly = df.copy()

            monthly["Month"] = monthly["Date"].dt.strftime("%b %Y")

            monthly_summary = (
                monthly.groupby(["Month", "Type"])["Amount"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                monthly_summary,
                x="Month",
                y="Amount",
                color="Type",
                barmode="group"
            )

            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=20, b=10),
                plot_bgcolor="white",
                paper_bgcolor="white",
                showlegend=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        else:
            st.info("Add transactions to see your financial chart.")

        st.markdown("</div>", unsafe_allow_html=True)

    with chart2:

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        st.subheader("Spending by Category")

        expense_df = df[df["Type"] == "Expense"]

        if not expense_df.empty:

            category_data = (
                expense_df.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                category_data,
                names="Category",
                values="Amount",
                hole=0.55
            )

            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=20, b=10),
                showlegend=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        else:
            st.info("Add expenses to see spending categories.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ================= RECENT =================

    st.markdown(
        '<div class="section-title">Recent Transactions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Your latest financial activity.</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        recent = df.sort_values(
            "Date",
            ascending=False
        ).head(7).copy()

        recent["Date"] = recent["Date"].dt.strftime("%d %b %Y")

        recent["Amount"] = recent.apply(
            lambda row:
            f"+ Rs {row['Amount']:,.0f}"
            if row["Type"] == "Income"
            else f"- Rs {row['Amount']:,.0f}",
            axis=1
        )

        st.dataframe(
            recent[
                [
                    "Date",
                    "Type",
                    "Category",
                    "Description",
                    "Amount"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No transactions yet. Add your first transaction below.")


# =========================================================
# TRANSACTIONS
# =========================================================

elif page == "💳 Transactions":

    st.markdown(
        '<div class="dashboard-title">Transactions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Manage your income and expenses.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # ADD TRANSACTION

    st.markdown(
        '<div class="section-title">Add Transaction</div>',
        unsafe_allow_html=True
    )

    with st.form("transaction_form"):

        col1, col2 = st.columns(2)

        with col1:

            transaction_type = st.selectbox(
                "Transaction Type",
                ["Income", "Expense"]
            )

            category_list = (
                INCOME_CATEGORIES
                if transaction_type == "Income"
                else EXPENSE_CATEGORIES
            )

            category = st.selectbox(
                "Category",
                category_list
            )

            amount = st.number_input(
                "Amount (Rs)",
                min_value=0.0,
                step=100.0
            )

        with col2:

            transaction_date = st.date_input(
                "Date",
                value=date.today()
            )

            description = st.text_input(
                "Description",
                placeholder="e.g. Freelance project"
            )

        submitted = st.form_submit_button(
            "➕ Add Transaction",
            use_container_width=True
        )

        if submitted:

            if amount <= 0:
                st.error("Amount must be greater than zero.")

            else:

                add_transaction(
                    transaction_type,
                    category,
                    description,
                    amount,
                    transaction_date
                )

                st.success("Transaction added successfully!")

                st.rerun()

    # TRANSACTION HISTORY

    st.markdown(
        '<div class="section-title">Transaction History</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        f1, f2, f3 = st.columns(3)

        with f1:
            type_filter = st.selectbox(
                "Type",
                ["All", "Income", "Expense"]
            )

        with f2:
            categories = ["All"] + sorted(
                df["Category"].dropna().unique().tolist()
            )

            category_filter = st.selectbox(
                "Category",
                categories
            )

        with f3:
            search = st.text_input(
                "Search",
                placeholder="Search description..."
            )

        filtered = df.copy()

        if type_filter != "All":
            filtered = filtered[
                filtered["Type"] == type_filter
            ]

        if category_filter != "All":
            filtered = filtered[
                filtered["Category"] == category_filter
            ]

        if search:
            filtered = filtered[
                filtered["Description"]
                .astype(str)
                .str.contains(search, case=False, na=False)
            ]

        filtered = filtered.sort_values(
            "Date",
            ascending=False
        )

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="finance_transactions.csv",
            mime="text/csv"
        )

        st.markdown("### Delete Transaction")

        delete_id = st.number_input(
            "Transaction ID",
            min_value=1,
            step=1
        )

        if st.button("🗑️ Delete Transaction"):

            if delete_id in df["ID"].values:

                delete_transaction(int(delete_id))

                st.success("Transaction deleted.")

                st.rerun()

            else:

                st.error("Transaction ID not found.")

    else:

        st.info("No transactions available.")


# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="dashboard-title">Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Understand where your money goes.</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.info("Add transactions to generate analytics.")

    else:

        expense_df = df[df["Type"] == "Expense"]

        if not expense_df.empty:

            category_data = (
                expense_df.groupby("Category")["Amount"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )

            st.subheader("Expense Breakdown")

            fig = px.bar(
                category_data,
                x="Amount",
                y="Category",
                orientation="h"
            )

            fig.update_layout(
                height=500,
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.subheader("All Financial Activity")

        monthly = df.copy()

        monthly["Month"] = monthly["Date"].dt.strftime("%b %Y")

        monthly_summary = (
            monthly.groupby(["Month", "Type"])["Amount"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly_summary,
            x="Month",
            y="Amount",
            color="Type",
            markers=True
        )

        fig.update_layout(
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# SETTINGS
# =========================================================

elif page == "⚙️ Settings":

    st.markdown(
        '<div class="dashboard-title">Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">Manage your FinanceFlow preferences.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("Application")

    st.info(
        "Your financial data is stored locally in finance_data.csv."
    )

    st.subheader("Data")

    st.write(
        f"Total transactions: **{len(df)}**"
    )

    st.write(
        f"Data file: **{DATA_FILE}**"
    )

    if st.button("⚠️ Clear All Transactions"):

        save_data(
            pd.DataFrame(columns=COLUMNS)
        )

        st.success("All transactions cleared.")

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    FinanceFlow • Personal Finance Dashboard • Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)