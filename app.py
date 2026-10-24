
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Superstore Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. LOAD AND PREPARE DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    data = pd.read_excel("data/Sample_Superstore.xls")

    # Standardize date columns
    for col in ["Order Date", "Ship Date"]:
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors="coerce")

    # Remove exact duplicate records
    original_rows = len(data)
    data = data.drop_duplicates().copy()
    duplicates_removed = original_rows - len(data)

    return data, original_rows, duplicates_removed


df, original_rows, duplicates_removed = load_data()

# --------------------------------------------------
# 3. SIDEBAR AND FILTERS
# --------------------------------------------------
st.sidebar.title("📊 Superstore Analytics")
st.sidebar.caption("Explore sales, profit, and customer orders")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "Sales & Trends",
        "Profitability & Discounts",
        "EDA & Correlation",
        "Data & Methodology"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("Filters")

regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
segments = sorted(df["Segment"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments
)

# Date range filter
if "Order Date" in df.columns and df["Order Date"].notna().any():
    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()

    date_range = st.sidebar.date_input(
        "Order date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    date_range = None

# Apply filters
filtered_df = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & df["Segment"].isin(selected_segments)
].copy()

if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        filtered_df["Order Date"].notna()
        & (filtered_df["Order Date"].dt.date >= start_date)
        & (filtered_df["Order Date"].dt.date <= end_date)
    ]

# --------------------------------------------------
# 4. REUSABLE KPI FUNCTION
# --------------------------------------------------
def show_kpis(data):
    sales = data["Sales"].sum()
    profit = data["Profit"].sum()
    quantity = data["Quantity"].sum()

    orders = (
        data["Order ID"].nunique()
        if "Order ID" in data.columns else 0
    )

    margin = profit / sales * 100 if sales != 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Total Sales", f"${sales:,.0f}")
    c2.metric("📈 Total Profit", f"${profit:,.0f}")
    c3.metric("📦 Quantity Sold", f"{quantity:,.0f}")
    c4.metric("🛒 Unique Orders", f"{orders:,}")

    st.caption(f"Profit margin: {margin:.2f}%")

# --------------------------------------------------
# 5. HEADER
# --------------------------------------------------
st.title("📊 United States Superstore Analytics")
st.caption(
    "An interactive exploration of retail sales, "
    "profitability, products, and customer segments."
)

st.info(
    f"Showing {len(filtered_df):,} records out of "
    f"{len(df):,} available records based on your filters."
)

# --------------------------------------------------
# 6. EXECUTIVE OVERVIEW
# --------------------------------------------------
if page == "Executive Overview":

    show_kpis(filtered_df)
    st.divider()

    if filtered_df.empty:
        st.warning("No records match your selected filters.")
        st.stop()

    left, right = st.columns(2)

    with left:
        st.subheader("Monthly Sales Trend")

        monthly_sales = (
            filtered_df.dropna(subset=["Order Date"])
            .set_index("Order Date")["Sales"]
            .resample("ME").sum()
        )

        st.line_chart(monthly_sales)

    with right:
        st.subheader("Sales by Category")

        category_sales = (
            filtered_df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(category_sales)

    left, right = st.columns(2)

    with left:
        st.subheader("Profit by Region")

        region_profit = (
            filtered_df.groupby("Region")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(region_profit)

    with right:
        st.subheader("Sales by Customer Segment")

        segment_sales = (
            filtered_df.groupby("Segment")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(segment_sales)

    st.divider()
    st.subheader("💡 Automatic Business Insights")

    best_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum().idxmax()
    )

    best_region = (
        filtered_df.groupby("Region")["Profit"]
        .sum().idxmax()
    )

    worst_subcategory = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum().idxmin()
    )

    st.markdown(
        f"- **Leading category by sales:** {best_category}"
    )
    st.markdown(
        f"- **Leading region by total profit:** {best_region}"
    )
    st.markdown(
        f"- **Lowest-profit subcategory:** {worst_subcategory}"
    )

    st.caption(
        "These rankings describe the current filtered records. "
        "They do not establish why a category or region performs differently."
    )

# --------------------------------------------------
# 7. SALES AND TRENDS
# --------------------------------------------------
elif page == "Sales & Trends":

    st.header("Sales Performance")
    show_kpis(filtered_df)

    if filtered_df.empty:
        st.warning("No records match your selected filters.")
        st.stop()

    monthly = (
        filtered_df.dropna(subset=["Order Date"])
        .set_index("Order Date")[["Sales", "Profit"]]
        .resample("ME").sum()
    )

    st.subheader("Monthly Sales and Profit")
    st.line_chart(monthly)

    left, right = st.columns(2)

    with left:
        st.subheader("Sales by Category")

        category_sales = (
            filtered_df.groupby("Category")["Sales"]
            .sum().sort_values(ascending=False)
        )
        st.bar_chart(category_sales)

    with right:
        st.subheader("Sales by Region")

        region_sales = (
            filtered_df.groupby("Region")["Sales"]
            .sum().sort_values(ascending=False)
        )
        st.bar_chart(region_sales)

    st.subheader("Monthly Sales by Category")

    monthly_category = (
        filtered_df.dropna(subset=["Order Date"])
        .groupby([
            pd.Grouper(key="Order Date", freq="ME"),
            "Category"
        ])["Sales"]
        .sum()
        .unstack(fill_value=0)
    )

    st.line_chart(monthly_category)

    st.subheader("Top 10 Products by Sales")

    if "Product Name" in filtered_df.columns:
        top_products = (
            filtered_df.groupby("Product Name")["Sales"]
            .sum().nlargest(10).sort_values()
        )
        st.bar_chart(top_products)

# --------------------------------------------------
# 8. PROFITABILITY AND DISCOUNTS
# --------------------------------------------------
elif page == "Profitability & Discounts":

    st.header("Profitability & Discount Analysis")
    show_kpis(filtered_df)

    if filtered_df.empty:
        st.warning("No records match your selected filters.")
        st.stop()

    left, right = st.columns(2)

    with left:
        st.subheader("Profit by Category")

        category_profit = (
            filtered_df.groupby("Category")["Profit"]
            .sum().sort_values(ascending=False)
        )
        st.bar_chart(category_profit)

    with right:
        st.subheader("Profit by Subcategory")

        subcategory_profit = (
            filtered_df.groupby("Sub-Category")["Profit"]
            .sum().sort_values()
        )
        st.bar_chart(subcategory_profit)

    st.subheader("Discount vs. Profit")

    fig, ax = plt.subplots(figsize=(10, 5))

    for category in filtered_df["Category"].dropna().unique():
        subset = filtered_df[
            filtered_df["Category"] == category
        ]

        ax.scatter(
            subset["Discount"],
            subset["Profit"],
            label=category,
            alpha=0.55
        )

    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Discount")
    ax.set_ylabel("Profit")
    ax.set_title("Discount vs. Profit by Category")
    ax.legend()
    ax.grid(alpha=0.2)

    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Each point represents a record. Points below zero indicate "
        "a loss on that record; correlation does not prove causation."
    )

    st.subheader("Loss-Making Subcategories")

    loss_table = (
        filtered_df.groupby("Sub-Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .query("Profit < 0")
        .sort_values("Profit")
    )

    if loss_table.empty:
        st.success(
            "No subcategories have negative total profit "
            "under the current filters."
        )
    else:
        st.dataframe(loss_table, use_container_width=True)

# --------------------------------------------------
# 9. EDA AND CORRELATION
# --------------------------------------------------
elif page == "EDA & Correlation":

    st.header("Exploratory Data Analysis")

    if filtered_df.empty:
        st.warning("No records match your selected filters.")
        st.stop()

    st.subheader("Numerical Distributions")

    numeric_cols = [
        col for col in ["Sales", "Discount", "Quantity", "Profit"]
        if col in filtered_df.columns
    ]

    chosen_numeric = st.selectbox(
        "Choose a numeric column",
        numeric_cols
    )

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.hist(
        filtered_df[chosen_numeric].dropna(),
        bins=25,
        edgecolor="white"
    )
    ax.set_title(f"Distribution of {chosen_numeric}")
    ax.set_xlabel(chosen_numeric)
    ax.set_ylabel("Number of records")
    ax.grid(axis="y", alpha=0.2)

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Sales Distribution by Category")

    fig, ax = plt.subplots(figsize=(9, 5))
    filtered_df.boxplot(
        column="Sales",
        by="Category",
        ax=ax
    )
    ax.set_title("Sales Distribution by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Sales")
    fig.suptitle("")

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Correlation Heatmap")

    # Exclude Postal Code because it is an identifier,
    # not a meaningful continuous measure.
    numeric_df = (
        filtered_df
        .drop(columns=["Row ID","Postal Code"], errors="ignore")
        .select_dtypes(include="number")
    )

    corr = numeric_df.corr()

    fig, ax = plt.subplots(
        figsize=(max(8, len(corr.columns)), 6)
    )

    image = ax.imshow(
        corr,
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )

    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)

    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            value = corr.iloc[i, j]
            if pd.notna(value):
                ax.text(
                    j, i, f"{value:.2f}",
                    ha="center", va="center", fontsize=8
                )

    fig.colorbar(image, ax=ax, label="Correlation")
    ax.set_title("Correlation Between Numeric Variables")
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    # Find the strongest non-self correlation
    upper = corr.where(
        np.triu(np.ones(corr.shape), k=1).astype(bool)
    )

    pairs = upper.stack()

    if not pairs.empty:
        strongest = pairs.abs().idxmax()
        value = corr.loc[strongest[0], strongest[1]]

        st.markdown("### Strongest Correlation")
        st.write(
            f"**{strongest[0]} and {strongest[1]}** "
            f"have the strongest absolute correlation "
            f"({value:.3f})."
        )

        st.caption(
            "Positive values indicate a positive linear relationship; "
            "negative values indicate an inverse relationship. "
            "Correlation does not establish causation."
        )

# --------------------------------------------------
# 10. DATA AND METHODOLOGY
# --------------------------------------------------
elif page == "Data & Methodology":

    st.header("Dataset & Methodology")

    st.markdown(
        """
        This project explores United States Superstore retail data
        to understand sales performance, profitability, product
        categories, customer segments, and time-based trends.
        """
    )

    st.markdown(
        "**Dataset source:** "
        "[United States Superstore Sales on Kaggle]"
        "(https://www.kaggle.com/datasets/abiodunonadeji/"
        "united-state-superstore-sales)"
    )

    st.subheader("Dataset Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Original Rows", f"{original_rows:,}")
    c2.metric("Rows After Deduplication", f"{len(df):,}")
    c3.metric("Duplicate Rows Removed", f"{duplicates_removed:,}")

    st.subheader("Data Quality Report")

    quality = pd.DataFrame({
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isna().sum(),
        "Missing (%)": (
            df.isna().mean().mul(100).round(2)
        )
    })

    st.dataframe(quality, use_container_width=True)

    st.subheader("Cleaning Decisions")

    st.markdown(
        """
        - **Duplicates:** Exact duplicate rows are removed.
        - **Dates:** Order Date and Ship Date are converted to datetime.
        - **Missing values:** Reported for review rather than
          automatically deleting every affected record.
        - **Outliers:** Investigated with distributions and box plots.
          Extreme values are not automatically discarded.
        - **Postal Code:** Excluded from numeric correlation analysis
          because it represents a location identifier.
        - **Unused columns:** Row ID, Customer Name, Country, and
          Product Name were considered for exclusion in the original
          notebook. This dashboard retains the source columns so that
          product-level analysis remains possible.
        """
    )

    st.subheader("Preview the Data")
    st.dataframe(filtered_df.head(100), use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_superstore_data.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# 11. FOOTER
# --------------------------------------------------
st.divider()
st.caption(
    "Superstore Analytics | Built with Python, Pandas, "
    "Matplotlib, and Streamlit"
)



# --------------------------------------------------
# PROJECT GOVERNANCE & INSTITUTIONAL ACKNOWLEDGMENTS
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align: center;">
        <h2>Project Governance & Institutional Acknowledgments</h2>
        <p>
            This analytics report and performance terminal were engineered
            as part of the Artificial Intelligence and Data Analytics program.
        </p>
        <p><i>Click each section below to view the project acknowledgments.</i></p>
    </div>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):
    with st.expander("👨‍💻 Data Analyst and Author", expanded=False):
        st.markdown("### Iftikhar Hussain Jaffari")
        st.write("**Role:** Data Analyst")
        st.write("**Program:** PSEB Bootcamp AI")
        st.write("**Institution:** Iqra University (H9), Islamabad")

    with st.expander("🎓 Bootcamp Trainer", expanded=False):
        st.markdown("### Respected Mam. Mahnoor Salman")
        st.write("**Designation:** Lead AI & Data Science Instructor")
        st.write("**Contribution:** Mentorship & Technical Guidance")

    with st.expander("📋 Bootcamp Coordinator", expanded=False):
        st.markdown("### Respected Mr Furqan")
        st.write("**Role:** Program Coordinator")
        st.write("**Contribution:** Cohort Management & Operational Support")

    with st.expander("🏛️ Bootcamp Organizers", expanded=False):
        st.markdown("### Pakistan Software Export Board (PSEB) & atomcamp")
        st.write("**Contribution:** National Tech Sector Enablers & Strategic Implementing Partners")

st.markdown(
    """
    <div style="text-align: center; padding: 12px 0;">
        <small>
            Artificial Intelligence & Data Analytics |
            PSEB Bootcamp AI @ Iqra University (H9), Islamabad
        </small>
    </div>
    """,
    unsafe_allow_html=True
)
