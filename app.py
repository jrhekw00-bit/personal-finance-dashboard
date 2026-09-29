import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import (
    init_database,
    get_user_by_id,
    get_user_transactions,
    add_transaction,
    delete_transaction,
    update_budget,
    get_all_users,
    update_user_status,
    count_users,
    count_active_users,
    count_transactions,
    total_income,
    total_expenses,
    get_all_transactions
)

from auth import (
    register_user,
    create_first_admin,
    login_user
)


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="FinanceFlow",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_database()


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5f7fb;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: #111827;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

.logo {
    font-size: 25px;
    font-weight: 800;
    color: white;
}

.logo-sub {
    color: #9ca3af;
    font-size: 12px;
    margin-bottom: 30px;
}

.page-title {
    font-size: 32px;
    font-weight: 800;
    color: #111827;
}

.page-subtitle {
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 25px;
}

.metric-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 5px 20px rgba(17,24,39,.04);
}

.metric-label {
    color: #6b7280;
    font-size: 12px;
    font-weight: 700;
}

.metric-value {
    color: #111827;
    font-size: 27px;
    font-weight: 800;
    margin-top: 15px;
}

.metric-small {
    color: #059669;
    font-size: 12px;
    font-weight: 600;
}

.panel {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 5px 20px rgba(17,24,39,.04);
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    margin-top: 28px;
    margin-bottom: 5px;
}

.login-box {
    max-width: 480px;
    margin: 70px auto;
    background: white;
    padding: 40px;
    border-radius: 24px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 15px 50px rgba(0,0,0,.08);
}

.login-logo {
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 5px;
}

.login-subtitle {
    text-align: center;
    color: #6b7280;
    margin-bottom: 30px;
}

.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
}

div[data-testid="stForm"] {
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    padding: 25px;
}

.admin-badge {
    display: inline-block;
    background: #ede9fe;
    color: #6d28d9;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.user-badge {
    display: inline-block;
    background: #ecfdf5;
    color: #047857;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #9ca3af;
    margin-top: 50px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None


# =========================================================
# LOGIN / SIGNUP
# =========================================================

def authentication_page():

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-logo">💰 FinanceFlow</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">Personal Finance Management</div>',
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs([
        "🔐 Login",
        "✨ Create Account"
    ])

    with login_tab:

        with st.form("login_form"):

            email = st.text_input(
                "Email",
                placeholder="you@example.com"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

            if submitted:

                success, message, user = login_user(
                    email,
                    password
                )

                if success:

                    st.session_state.logged_in = True
                    st.session_state.user_id = user["id"]

                    st.rerun()

                else:

                    st.error(message)

    with signup_tab:

        with st.form("signup_form"):

            name = st.text_input(
                "Full Name"
            )

            email = st.text_input(
                "Email Address"
            )

            password = st.text_input(
                "Password",
                type="password",
                help="At least 8 characters, uppercase, lowercase and number."
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if submitted:

                if password != confirm_password:

                    st.error("Passwords do not match.")

                else:

                    success, message = register_user(
                        name,
                        email,
                        password
                    )

                    if success:
                        st.success(
                            "Account created! You can now login."
                        )
                    else:
                        st.error(message)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# IF NOT LOGGED IN
# =========================================================

if not st.session_state.logged_in:

    authentication_page()

    st.stop()


# =========================================================
# CURRENT USER
# =========================================================

user = get_user_by_id(
    st.session_state.user_id
)

if not user:

    st.session_state.logged_in = False
    st.session_state.user_id = None

    st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="logo">💰 FinanceFlow</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="logo-sub">Personal Finance Manager</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"### 👋 {user['name']}"
    )

    if user["role"] == "admin":

        st.markdown(
            '<span class="admin-badge">ADMIN</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="user-badge">USER</span>',
            unsafe_allow_html=True
        )

    st.divider()

    if user["role"] == "admin":

        navigation = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "💳 Transactions",
                "📊 Analytics",
                "🛡️ Admin Panel",
                "⚙️ Settings"
            ]
        )

    else:

        navigation = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "💳 Transactions",
                "📊 Analytics",
                "⚙️ Settings"
            ]
        )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_id = None

        st.rerun()


# =========================================================
# USER DATA
# =========================================================

transactions = get_user_transactions(
    user["id"]
)

df = pd.DataFrame(transactions)

if not df.empty:

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )


income = (
    df.loc[df["type"] == "Income", "amount"].sum()
    if not df.empty
    else 0
)

expenses = (
    df.loc[df["type"] == "Expense", "amount"].sum()
    if not df.empty
    else 0
)

balance = income - expenses

savings_rate = (
    (balance / income) * 100
    if income > 0
    else 0
)


# =========================================================
# DASHBOARD
# =========================================================

if navigation == "🏠 Dashboard":

    st.markdown(
        '<div class="page-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="page-subtitle">Welcome back, {user["name"]}. Here is your financial overview.</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL INCOME</div>
            <div class="metric-value">Rs {income:,.0f}</div>
            <div class="metric-small">Money received</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL EXPENSES</div>
            <div class="metric-value">Rs {expenses:,.0f}</div>
            <div class="metric-small">Money spent</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">BALANCE</div>
            <div class="metric-value">Rs {balance:,.0f}</div>
            <div class="metric-small">Current balance</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SAVINGS RATE</div>
            <div class="metric-value">{savings_rate:.1f}%</div>
            <div class="metric-small">Income saved</div>
        </div>
        """, unsafe_allow_html=True)

    # Budget

    st.markdown(
        '<div class="section-title">Monthly Budget</div>',
        unsafe_allow_html=True
    )

    budget = user["budget"]

    budget_percentage = (
        (expenses / budget) * 100
        if budget > 0
        else 0
    )

    st.markdown(
        f"""
        <div class="panel">
            <b>Budget</b>
            <h2>Rs {expenses:,.0f} / Rs {budget:,.0f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(budget_percentage / 100, 1.0)
    )

    if budget_percentage >= 100:

        st.error(
            f"⚠️ Budget exceeded by Rs {expenses - budget:,.0f}"
        )

    elif budget_percentage >= 80:

        st.warning(
            f"⚠️ You have used {budget_percentage:.1f}% of your budget."
        )

    else:

        st.success(
            f"✓ You have used {budget_percentage:.1f}% of your budget."
        )

    # Charts

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

            chart_df = df.copy()

            chart_df["Month"] = chart_df["date"].dt.strftime(
                "%b %Y"
            )

            monthly = (
                chart_df
                .groupby(["Month", "type"])["amount"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                monthly,
                x="Month",
                y="amount",
                color="type",
                barmode="group"
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                ),
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        else:

            st.info(
                "Add transactions to see your chart."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with chart2:

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        st.subheader("Spending by Category")

        expense_df = (
            df[df["type"] == "Expense"]
            if not df.empty
            else pd.DataFrame()
        )

        if not expense_df.empty:

            category_df = (
                expense_df
                .groupby("category")["amount"]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                category_df,
                names="category",
                values="amount",
                hole=0.55
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        else:

            st.info(
                "Add expenses to see spending categories."
            )

        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TRANSACTIONS
# =========================================================

elif navigation == "💳 Transactions":

    st.markdown(
        '<div class="page-title">Transactions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Add and manage your financial activity.</div>',
        unsafe_allow_html=True
    )

    with st.form("add_transaction"):

        c1, c2 = st.columns(2)

        with c1:

            transaction_type = st.selectbox(
                "Type",
                ["Income", "Expense"]
            )

            if transaction_type == "Income":

                categories = [
                    "Salary",
                    "Freelance",
                    "Business",
                    "Investment",
                    "Gift",
                    "Other Income"
                ]

            else:

                categories = [
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

            category = st.selectbox(
                "Category",
                categories
            )

            amount = st.number_input(
                "Amount (Rs)",
                min_value=0.0,
                step=100.0
            )

        with c2:

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

                st.error(
                    "Amount must be greater than zero."
                )

            else:

                add_transaction(
                    user["id"],
                    transaction_date.isoformat(),
                    transaction_type,
                    category,
                    description,
                    amount
                )

                st.success(
                    "Transaction added successfully!"
                )

                st.rerun()

    st.markdown(
        '<div class="section-title">Transaction History</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        display_df = df.copy()

        display_df["date"] = display_df["date"].dt.strftime(
            "%d %b %Y"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = display_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv_data,
            "financeflow_transactions.csv",
            "text/csv"
        )

        st.markdown("### Delete Transaction")

        transaction_id = st.number_input(
            "Transaction ID",
            min_value=1,
            step=1
        )

        if st.button("🗑️ Delete"):

            delete_transaction(
                int(transaction_id),
                user["id"]
            )

            st.success(
                "Transaction deleted."
            )

            st.rerun()

    else:

        st.info(
            "No transactions yet."
        )


# =========================================================
# ANALYTICS
# =========================================================

elif navigation == "📊 Analytics":

    st.markdown(
        '<div class="page-title">Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Detailed view of your financial activity.</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.info(
            "Add transactions to generate analytics."
        )

    else:

        expense_df = df[
            df["type"] == "Expense"
        ]

        if not expense_df.empty:

            category_df = (
                expense_df
                .groupby("category")["amount"]
                .sum()
                .reset_index()
                .sort_values(
                    "amount",
                    ascending=False
                )
            )

            fig = px.bar(
                category_df,
                x="amount",
                y="category",
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

        monthly_df = df.copy()

        monthly_df["Month"] = monthly_df[
            "date"
        ].dt.strftime("%b %Y")

        monthly = (
            monthly_df
            .groupby(["Month", "type"])["amount"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly,
            x="Month",
            y="amount",
            color="type",
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
# ADMIN PANEL
# =========================================================

elif navigation == "🛡️ Admin Panel":

    if user["role"] != "admin":

        st.error(
            "Access denied."
        )

        st.stop()

    st.markdown(
        '<div class="page-title">Admin Panel</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Manage FinanceFlow users and system activity.</div>',
        unsafe_allow_html=True
    )

    users_count = count_users()
    active_count = count_active_users()
    transactions_count = count_transactions()
    system_income = total_income()
    system_expenses = total_expenses()

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL USERS</div>
            <div class="metric-value">{users_count}</div>
            <div class="metric-small">Registered accounts</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ACTIVE USERS</div>
            <div class="metric-value">{active_count}</div>
            <div class="metric-small">Currently enabled</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TRANSACTIONS</div>
            <div class="metric-value">{transactions_count}</div>
            <div class="metric-small">System-wide</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SYSTEM BALANCE</div>
            <div class="metric-value">Rs {system_income - system_expenses:,.0f}</div>
            <div class="metric-small">All users</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">User Management</div>',
        unsafe_allow_html=True
    )

    users = get_all_users()

    if users:

        users_df = pd.DataFrame(users)

        users_df["Status"] = users_df[
            "is_active"
        ].map({
            1: "Active",
            0: "Disabled"
        })

        st.dataframe(
            users_df[
                [
                    "id",
                    "name",
                    "email",
                    "role",
                    "Status",
                    "budget",
                    "created_at"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Change User Status")

        user_ids = [
            u["id"]
            for u in users
            if u["id"] != user["id"]
        ]

        if user_ids:

            selected_user = st.selectbox(
                "Select User",
                user_ids
            )

            selected_record = get_user_by_id(
                selected_user
            )

            st.write(
                f"**{selected_record['name']}** — {selected_record['email']}"
            )

            if selected_record["is_active"]:

                if st.button(
                    "🔒 Disable User",
                    use_container_width=True
                ):

                    update_user_status(
                        selected_user,
                        False
                    )

                    st.success(
                        "User disabled."
                    )

                    st.rerun()

            else:

                if st.button(
                    "🔓 Enable User",
                    use_container_width=True
                ):

                    update_user_status(
                        selected_user,
                        True
                    )

                    st.success(
                        "User enabled."
                    )

                    st.rerun()

    st.markdown(
        '<div class="section-title">All Transactions</div>',
        unsafe_allow_html=True
    )

    all_transactions = get_all_transactions()

    if all_transactions:

        all_df = pd.DataFrame(
            all_transactions
        )

        st.dataframe(
            all_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Export System Transactions",
            all_df.to_csv(
                index=False
            ).encode("utf-8"),
            "financeflow_all_transactions.csv",
            "text/csv"
        )

    else:

        st.info(
            "No system transactions yet."
        )


# =========================================================
# SETTINGS
# =========================================================

elif navigation == "⚙️ Settings":

    st.markdown(
        '<div class="page-title">Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Manage your account preferences.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="panel">
            <b>Name</b><br>
            {user["name"]}
            <br><br>
            <b>Email</b><br>
            {user["email"]}
            <br><br>
            <b>Account Type</b><br>
            {user["role"].title()}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Monthly Budget</div>',
        unsafe_allow_html=True
    )

    new_budget = st.number_input(
        "Monthly Budget (Rs)",
        min_value=0.0,
        value=float(user["budget"]),
        step=5000.0
    )

    if st.button(
        "💾 Save Budget"
    ):

        update_budget(
            user["id"],
            new_budget
        )

        st.success(
            "Budget updated successfully."
        )

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    FinanceFlow V2 • Secure Personal Finance Management
</div>
""", unsafe_allow_html=True)