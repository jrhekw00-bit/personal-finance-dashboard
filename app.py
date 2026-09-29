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
    get_all_transactions,
)

from auth import (
    register_user,
    create_first_admin,
    login_user,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FinanceFlow",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATABASE
# =========================================================

init_database()


# =========================================================
# CLEAN CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fb;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* DO NOT HIDE HEADER
       Streamlit uses it for sidebar controls */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #e5e7eb;
    }

    /* Titles */

    .app-title {
        font-size: 32px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 4px;
    }

    .app-subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* Cards */

    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 22px;
        min-height: 135px;
        box-shadow: 0 4px 18px rgba(17, 24, 39, 0.05);
    }

    .metric-label {
        color: #6b7280;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }

    .metric-value {
        color: #111827;
        font-size: 27px;
        font-weight: 800;
        margin-top: 14px;
    }

    .metric-description {
        color: #059669;
        font-size: 12px;
        margin-top: 6px;
        font-weight: 600;
    }

    /* Panels */

    .panel {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 18px rgba(17, 24, 39, 0.04);
    }

    /* Login */

    .login-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #111827;
    }

    .login-subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 25px;
    }

    /* Buttons */

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
    }

    /* Footer */

    .app-footer {
        text-align: center;
        color: #9ca3af;
        margin-top: 50px;
        font-size: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None


# =========================================================
# AUTHENTICATION PAGE
# =========================================================

def authentication_page():

    st.markdown(
        '<div class="login-title">💰 FinanceFlow</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="login-subtitle">Personal Finance Management</div>',
        unsafe_allow_html=True,
    )

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    with login_tab:

        with st.form("login_form"):

            email = st.text_input(
                "Email",
                placeholder="you@example.com",
            )

            password = st.text_input(
                "Password",
                type="password",
            )

            login_clicked = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

            if login_clicked:

                if not email or not password:

                    st.error("Please enter email and password.")

                else:

                    success, message, logged_user = login_user(
                        email.strip(),
                        password,
                    )

                    if success:

                        st.session_state.logged_in = True
                        st.session_state.user_id = logged_user["id"]

                        st.rerun()

                    else:

                        st.error(message)

    # -----------------------------------------------------
    # SIGNUP
    # -----------------------------------------------------

    with signup_tab:

        with st.form("signup_form"):

            name = st.text_input(
                "Full Name",
                placeholder="Your full name",
            )

            email = st.text_input(
                "Email Address",
                placeholder="you@example.com",
            )

            password = st.text_input(
                "Password",
                type="password",
                help="At least 8 characters, uppercase, lowercase and number.",
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
            )

            signup_clicked = st.form_submit_button(
                "Create Account",
                use_container_width=True,
            )

            if signup_clicked:

                if not name.strip():

                    st.error("Please enter your name.")

                elif not email.strip():

                    st.error("Please enter your email.")

                elif password != confirm_password:

                    st.error("Passwords do not match.")

                else:

                    success, message = register_user(
                        name.strip(),
                        email.strip(),
                        password,
                    )

                    if success:

                        st.success(
                            "Account created successfully. You can now login."
                        )

                    else:

                        st.error(message)

    # -----------------------------------------------------
    # FIRST ADMIN
    # -----------------------------------------------------

    if count_users() == 0:

        st.divider()

        st.subheader("🛡️ First Admin Setup")

        st.info(
            "Create the first administrator account for FinanceFlow."
        )

        with st.form("admin_setup_form"):

            admin_name = st.text_input(
                "Admin Name",
                key="admin_name",
            )

            admin_email = st.text_input(
                "Admin Email",
                key="admin_email",
            )

            admin_password = st.text_input(
                "Admin Password",
                type="password",
                key="admin_password",
            )

            admin_confirm = st.text_input(
                "Confirm Admin Password",
                type="password",
                key="admin_confirm",
            )

            create_admin_clicked = st.form_submit_button(
                "Create Admin Account",
                use_container_width=True,
            )

            if create_admin_clicked:

                if admin_password != admin_confirm:

                    st.error("Passwords do not match.")

                else:

                    success, message = create_first_admin(
                        admin_name.strip(),
                        admin_email.strip(),
                        admin_password,
                    )

                    if success:

                        st.success(
                            "Admin account created. You can now login."
                        )

                    else:

                        st.error(message)


# =========================================================
# SHOW LOGIN IF NOT LOGGED IN
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
        "## 💰 FinanceFlow"
    )

    st.caption(
        "Personal Finance Manager"
    )

    st.divider()

    st.markdown(
        f"### 👋 {user['name']}"
    )

    if user["role"] == "admin":

        st.success("ADMIN")

    else:

        st.info("USER")

    st.divider()

    # Navigation

    if user["role"] == "admin":

        navigation = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "💳 Transactions",
                "📊 Analytics",
                "🛡️ Admin Panel",
                "⚙️ Settings",
            ],
        )

    else:

        navigation = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "💳 Transactions",
                "📊 Analytics",
                "⚙️ Settings",
            ],
        )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True,
    ):

        st.session_state.logged_in = False
        st.session_state.user_id = None

        st.rerun()


# =========================================================
# LOAD USER TRANSACTIONS
# =========================================================

transactions = get_user_transactions(
    user["id"]
)

df = pd.DataFrame(transactions)


if not df.empty:

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

    if "amount" in df.columns:

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce",
        )

        df["amount"] = df["amount"].fillna(0)


# =========================================================
# FINANCIAL CALCULATIONS
# =========================================================

if not df.empty and "type" in df.columns:

    income = df.loc[
        df["type"] == "Income",
        "amount"
    ].sum()

    expenses = df.loc[
        df["type"] == "Expense",
        "amount"
    ].sum()

else:

    income = 0
    expenses = 0


balance = income - expenses

if income > 0:

    savings_rate = (
        balance / income
    ) * 100

else:

    savings_rate = 0


# =========================================================
# DASHBOARD
# =========================================================

if navigation == "🏠 Dashboard":

    st.markdown(
        '<div class="app-title">Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="app-subtitle">
            Welcome back, {user["name"]}. Here is your financial overview.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">TOTAL INCOME</div>
                <div class="metric-value">Rs {income:,.0f}</div>
                <div class="metric-description">
                    Money received
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">TOTAL EXPENSES</div>
                <div class="metric-value">Rs {expenses:,.0f}</div>
                <div class="metric-description">
                    Money spent
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">BALANCE</div>
                <div class="metric-value">Rs {balance:,.0f}</div>
                <div class="metric-description">
                    Current balance
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">SAVINGS RATE</div>
                <div class="metric-value">{savings_rate:.1f}%</div>
                <div class="metric-description">
                    Income saved
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # BUDGET
    # -----------------------------------------------------

    st.markdown("### Monthly Budget")

    budget = float(user["budget"] or 0)

    if budget > 0:

        budget_percentage = (
            expenses / budget
        ) * 100

    else:

        budget_percentage = 0

    st.markdown(
        f"""
        <div class="panel">
            <strong>Monthly Budget</strong>
            <h2>Rs {expenses:,.0f} / Rs {budget:,.0f}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(
        min(max(budget_percentage / 100, 0), 1)
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

    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    st.markdown("### Financial Overview")

    chart1, chart2 = st.columns(2)

    # -----------------------------------------------------
    # INCOME VS EXPENSES
    # -----------------------------------------------------

    with chart1:

        st.subheader("Income vs Expenses")

        if not df.empty:

            chart_df = df.copy()

            chart_df["Month"] = chart_df[
                "date"
            ].dt.strftime("%b %Y")

            monthly = (
                chart_df
                .groupby(
                    ["Month", "type"],
                    as_index=False
                )["amount"]
                .sum()
            )

            fig = px.bar(
                monthly,
                x="Month",
                y="amount",
                color="type",
                barmode="group",
                title=None,
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10,
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "Add transactions to see your chart."
            )

    # -----------------------------------------------------
    # CATEGORY CHART
    # -----------------------------------------------------

    with chart2:

        st.subheader("Spending by Category")

        if not df.empty:

            expense_df = df[
                df["type"] == "Expense"
            ]

        else:

            expense_df = pd.DataFrame()

        if not expense_df.empty:

            category_df = (
                expense_df
                .groupby(
                    "category",
                    as_index=False
                )["amount"]
                .sum()
            )

            fig = px.pie(
                category_df,
                names="category",
                values="amount",
                hole=0.55,
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10,
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "Add expenses to see spending categories."
            )


# =========================================================
# TRANSACTIONS
# =========================================================

elif navigation == "💳 Transactions":

    st.markdown(
        '<div class="app-title">Transactions</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">Add and manage your financial activity.</div>',
        unsafe_allow_html=True,
    )

    with st.form("transaction_form"):

        col1, col2 = st.columns(2)

        with col1:

            transaction_type = st.selectbox(
                "Type",
                ["Income", "Expense"],
            )

            if transaction_type == "Income":

                categories = [
                    "Salary",
                    "Freelance",
                    "Business",
                    "Investment",
                    "Gift",
                    "Other Income",
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
                    "Other",
                ]

            category = st.selectbox(
                "Category",
                categories,
            )

            amount = st.number_input(
                "Amount (Rs)",
                min_value=0.0,
                step=100.0,
            )

        with col2:

            transaction_date = st.date_input(
                "Date",
                value=date.today(),
            )

            description = st.text_input(
                "Description",
                placeholder="e.g. Monthly salary",
            )

        add_clicked = st.form_submit_button(
            "➕ Add Transaction",
            use_container_width=True,
        )

        if add_clicked:

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
                    amount,
                )

                st.success(
                    "Transaction added successfully!"
                )

                st.rerun()

    st.markdown("### Transaction History")

    if not df.empty:

        display_df = df.copy()

        if "date" in display_df.columns:

            display_df["date"] = display_df[
                "date"
            ].dt.strftime("%d %b %Y")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = display_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv_data,
            "financeflow_transactions.csv",
            "text/csv",
        )

        st.markdown("### Delete Transaction")

        transaction_ids = display_df[
            "id"
        ].tolist()

        selected_transaction = st.selectbox(
            "Select Transaction",
            transaction_ids,
        )

        if st.button(
            "🗑️ Delete Selected Transaction"
        ):

            delete_transaction(
                int(selected_transaction),
                user["id"],
            )

            st.success(
                "Transaction deleted."
            )

            st.rerun()

    else:

        st.info(
            "No transactions yet. Add your first transaction above."
        )


# =========================================================
# ANALYTICS
# =========================================================

elif navigation == "📊 Analytics":

    st.markdown(
        '<div class="app-title">Analytics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">Detailed view of your financial activity.</div>',
        unsafe_allow_html=True,
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

            st.subheader("Expenses by Category")

            category_df = (
                expense_df
                .groupby(
                    "category",
                    as_index=False
                )["amount"]
                .sum()
                .sort_values(
                    "amount",
                    ascending=False,
                )
            )

            fig = px.bar(
                category_df,
                x="amount",
                y="category",
                orientation="h",
            )

            fig.update_layout(
                height=500,
                plot_bgcolor="white",
                paper_bgcolor="white",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        st.subheader("Monthly Activity")

        monthly_df = df.copy()

        monthly_df["Month"] = monthly_df[
            "date"
        ].dt.strftime("%b %Y")

        monthly = (
            monthly_df
            .groupby(
                ["Month", "type"],
                as_index=False
            )["amount"]
            .sum()
        )

        fig = px.line(
            monthly,
            x="Month",
            y="amount",
            color="type",
            markers=True,
        )

        fig.update_layout(
            height=450,
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
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
        '<div class="app-title">Admin Panel</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">Manage FinanceFlow users and system activity.</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # ADMIN METRICS
    # -----------------------------------------------------

    users_count = count_users()
    active_count = count_active_users()
    transactions_count = count_transactions()

    system_income = total_income()
    system_expenses = total_expenses()

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">TOTAL USERS</div>
                <div class="metric-value">{users_count}</div>
                <div class="metric-description">
                    Registered accounts
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">ACTIVE USERS</div>
                <div class="metric-value">{active_count}</div>
                <div class="metric-description">
                    Enabled accounts
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">TRANSACTIONS</div>
                <div class="metric-value">{transactions_count}</div>
                <div class="metric-description">
                    System-wide
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:

        system_balance = (
            system_income - system_expenses
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">SYSTEM BALANCE</div>
                <div class="metric-value">
                    Rs {system_balance:,.0f}
                </div>
                <div class="metric-description">
                    All users
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # USER MANAGEMENT
    # -----------------------------------------------------

    st.markdown("### User Management")

    users = get_all_users()

    if users:

        users_df = pd.DataFrame(users)

        users_df["Status"] = users_df[
            "is_active"
        ].map(
            {
                1: "Active",
                0: "Disabled",
            }
        )

        st.dataframe(
            users_df[
                [
                    "id",
                    "name",
                    "email",
                    "role",
                    "Status",
                    "budget",
                    "created_at",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        other_users = [
            u
            for u in users
            if u["id"] != user["id"]
        ]

        if other_users:

            st.markdown("#### Change User Status")

            user_options = {
                f"{u['name']} — {u['email']}": u["id"]
                for u in other_users
            }

            selected_label = st.selectbox(
                "Select User",
                list(user_options.keys()),
            )

            selected_user_id = user_options[
                selected_label
            ]

            selected_record = get_user_by_id(
                selected_user_id
            )

            if selected_record["is_active"]:

                if st.button(
                    "🔒 Disable Selected User",
                    use_container_width=True,
                ):

                    update_user_status(
                        selected_user_id,
                        False,
                    )

                    st.success(
                        "User disabled."
                    )

                    st.rerun()

            else:

                if st.button(
                    "🔓 Enable Selected User",
                    use_container_width=True,
                ):

                    update_user_status(
                        selected_user_id,
                        True,
                    )

                    st.success(
                        "User enabled."
                    )

                    st.rerun()

    else:

        st.info(
            "No users found."
        )

    # -----------------------------------------------------
    # ALL TRANSACTIONS
    # -----------------------------------------------------

    st.markdown("### All Transactions")

    all_transactions = get_all_transactions()

    if all_transactions:

        all_df = pd.DataFrame(
            all_transactions
        )

        st.dataframe(
            all_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Export System Transactions",
            all_df.to_csv(
                index=False
            ).encode("utf-8"),
            "financeflow_all_transactions.csv",
            "text/csv",
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
        '<div class="app-title">Settings</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">Manage your account preferences.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Account")

    st.info(
        f"Name: {user['name']}"
    )

    st.info(
        f"Email: {user['email']}"
    )

    st.info(
        f"Account Type: {user['role'].title()}"
    )

    st.markdown("### Monthly Budget")

    new_budget = st.number_input(
        "Monthly Budget (Rs)",
        min_value=0.0,
        value=float(user["budget"] or 0),
        step=5000.0,
    )

    if st.button(
        "💾 Save Budget",
        use_container_width=True,
    ):

        update_budget(
            user["id"],
            new_budget,
        )

        st.success(
            "Budget updated successfully."
        )

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="app-footer">
        FinanceFlow V2 • Secure Personal Finance Management
    </div>
    """,
    unsafe_allow_html=True,
)