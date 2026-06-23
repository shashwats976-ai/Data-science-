import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Warehouse Inventory Intelligence Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using CSS injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    /* Overall layout styling */
    .stApp {
        background-color: #0d0f13;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #121620;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-title {
        background: linear-gradient(135deg, #00d2ff 0%, #a55eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 5px;
        font-family: 'Outfit', sans-serif;
    }
    
    .subtitle {
        color: #8898aa;
        font-size: 1.1rem;
        margin-bottom: 25px;
        font-weight: 400;
    }
    
    /* Premium glassmorphic metric cards */
    .metric-container {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
    }
    
    .metric-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 20px;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #00d2ff, #a55eea);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 210, 255, 0.3);
        box-shadow: 0 15px 35px rgba(0, 210, 255, 0.1);
        background: rgba(255, 255, 255, 0.05);
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #8898aa;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
    }
    
    .metric-sub {
        font-size: 0.75rem;
        color: #00d2ff;
        margin-top: 5px;
    }
    
    /* Clean, premium panels */
    .content-panel {
        background: rgba(20, 25, 35, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
    }
    
    /* Badges */
    .badge {
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        display: inline-block;
    }
    
    .badge-in {
        background: rgba(0, 210, 255, 0.15);
        color: #00d2ff;
        border: 1px solid rgba(0, 210, 255, 0.3);
    }
    
    .badge-low {
        background: rgba(255, 159, 67, 0.15);
        color: #ff9f43;
        border: 1px solid rgba(255, 159, 67, 0.3);
    }
    
    .badge-out {
        background: rgba(255, 118, 117, 0.15);
        color: #ff7675;
        border: 1px solid rgba(255, 118, 117, 0.3);
    }
    
    /* Sub-tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        color: #8898aa;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 10px 20px;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.06);
        color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 210, 255, 0.15) 0%, rgba(165, 94, 234, 0.15) 100%);
        color: #ffffff;
        border-color: rgba(0, 210, 255, 0.3);
        font-weight: 600;
    }
    
    /* Scrollbar customization */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d0f13;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e2430;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #2d3647;
    }
</style>
""", unsafe_allow_html=True)

# Data loading function with session caching
@st.cache_data
def load_original_csv():
    # Path to original file
    file_path = "warehouse_messy_data (2).csv"
    df = pd.read_csv(file_path)
    # Ensure raw types
    df['Product ID'] = df['Product ID'].astype(int)
    df['Quantity'] = df['Quantity'].astype(float)
    df['Price'] = df['Price'].astype(float)
    df['Last Restocked'] = pd.to_datetime(df['Last Restocked']).dt.strftime('%Y-%m-%d')
    return df

# Initialize data in session state to allow modifications (Restock simulator)
if 'df_raw' not in st.session_state:
    st.session_state['df_raw'] = load_original_csv()

# Data cleaning pipeline
def apply_cleaning(df, fix_status, deduplicate_ids, consolidate_locations):
    cleaned = df.copy()
    
    # 1. Fix Status Inconsistencies
    if fix_status:
        conditions = [
            cleaned['Quantity'] <= 0,
            (cleaned['Quantity'] > 0) & (cleaned['Quantity'] <= 100),
            cleaned['Quantity'] > 100
        ]
        choices = ['Out Of Stock', 'Low Stock', 'In Stock']
        cleaned['Status'] = np.select(conditions, choices, default='In Stock')
        
    # 2. De-duplicate Product IDs
    if deduplicate_ids:
        # Identify Product IDs that have different names, categories, price or suppliers
        group_cols = ['Product ID', 'Product Name', 'Category', 'Price', 'Supplier']
        unique_groups = cleaned[group_cols].drop_duplicates().copy()
        
        # Sort values to guarantee deterministic rank assignment
        unique_groups = unique_groups.sort_values(group_cols)
        unique_groups['group_rank'] = unique_groups.groupby('Product ID').cumcount()
        unique_groups['num_groups_for_id'] = unique_groups.groupby('Product ID')['Product ID'].transform('count')
        
        def make_new_id(row):
            pid = row['Product ID']
            rank = row['group_rank']
            total = row['num_groups_for_id']
            if total > 1:
                suffix = chr(65 + rank) # Suffixes A, B, C...
                return f"{pid}-{suffix}"
            return str(pid)
            
        unique_groups['Cleaned Product ID'] = unique_groups.apply(make_new_id, axis=1)
        
        # Merge back to apply new cleaned IDs
        cleaned = cleaned.merge(
            unique_groups[group_cols + ['Cleaned Product ID']], 
            on=group_cols, 
            how='left'
        )
        cleaned['Product ID'] = cleaned['Cleaned Product ID']
        cleaned = cleaned.drop(columns=['Cleaned Product ID'])
    else:
        # Convert Product ID to string so that type matches the cleaned version
        cleaned['Product ID'] = cleaned['Product ID'].astype(str)

    # 3. Consolidate Duplicate Locations
    if consolidate_locations:
        # Group duplicates (same product, warehouse, location, price, supplier)
        # Note: If de-duplicated, Product ID is unique per product profile. If not, it might not be.
        group_by_cols = ['Product ID', 'Product Name', 'Category', 'Warehouse', 'Location', 'Price', 'Supplier']
        
        # Sum quantities and keep the latest restocking date
        agg_dict = {
            'Quantity': 'sum',
            'Last Restocked': 'max'
        }
        
        consolidated = cleaned.groupby(group_by_cols, as_index=False).agg(agg_dict)
        
        # Recalculate status based on new consolidated quantity
        if fix_status:
            conditions = [
                consolidated['Quantity'] <= 0,
                (consolidated['Quantity'] > 0) & (consolidated['Quantity'] <= 100),
                consolidated['Quantity'] > 100
            ]
            choices = ['Out Of Stock', 'Low Stock', 'In Stock']
            consolidated['Status'] = np.select(conditions, choices, default='In Stock')
        else:
            # Aggregate status: take the status associated with the latest restock
            # To do this safely, we can merge back or compute a default. Let's just re-evaluate status based on quantity anyway
            # for physical consistency, but if fix_status is disabled, we'll keep the status from the original first item
            first_status = cleaned.groupby(group_by_cols)['Status'].first().reset_index()
            consolidated = consolidated.merge(first_status, on=group_by_cols, how='left')
            
        cleaned = consolidated

    return cleaned

# ----------------- SIDEBAR & CONTROL PANEL -----------------
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h3 style="margin-bottom: 0; background: linear-gradient(135deg, #00d2ff 0%, #a55eea 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CONTROL CENTER</h3>
    <span style="font-size: 0.75rem; color: #8898aa;">Configure Rules & Filters</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("🛡️ Data Cleaning Engine")
st.sidebar.caption("Toggle cleaning rules dynamically to see their effect on key metrics in real-time.")

clean_status = st.sidebar.toggle("Fix Status Inconsistencies", value=True, help="Recalculate status labels based on quantity thresholds: <=100 is Low, >100 is In Stock.")
clean_ids = st.sidebar.toggle("De-duplicate Product IDs", value=True, help="Generate unique IDs (e.g. 1001-A, 1001-B) for different products sharing the exact same numeric ID.")
clean_locations = st.sidebar.toggle("Consolidate Duplicate Locations", value=True, help="Combine multiple stock batches of the same product at the same warehouse and aisle by summing quantities.")

# Dynamically apply data cleaning based on selections
df_display = apply_cleaning(
    st.session_state['df_raw'], 
    fix_status=clean_status, 
    deduplicate_ids=clean_ids, 
    consolidate_locations=clean_locations
)

st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
st.sidebar.header("🔍 Interactive Filters")

# Sidebar Filter Options
selected_categories = st.sidebar.multiselect(
    "Categories", 
    options=sorted(df_display['Category'].unique()),
    default=None,
    placeholder="All Categories"
)

selected_warehouses = st.sidebar.multiselect(
    "Warehouses", 
    options=sorted(df_display['Warehouse'].unique()),
    default=None,
    placeholder="All Warehouses"
)

selected_suppliers = st.sidebar.multiselect(
    "Suppliers", 
    options=sorted(df_display['Supplier'].unique()),
    default=None,
    placeholder="All Suppliers"
)

selected_statuses = st.sidebar.multiselect(
    "Inventory Status", 
    options=sorted(df_display['Status'].unique()),
    default=None,
    placeholder="All Statuses"
)

# Apply filters
df_filtered = df_display.copy()
if selected_categories:
    df_filtered = df_filtered[df_filtered['Category'].isin(selected_categories)]
if selected_warehouses:
    df_filtered = df_filtered[df_filtered['Warehouse'].isin(selected_warehouses)]
if selected_suppliers:
    df_filtered = df_filtered[df_filtered['Supplier'].isin(selected_suppliers)]
if selected_statuses:
    df_filtered = df_filtered[df_filtered['Status'].isin(selected_statuses)]

# ----------------- EXPORT CLEANED DATA BUTTON -----------------
st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
st.sidebar.header("💾 Export Engine")
st.sidebar.caption("Download the processed dataset with the current cleaning configurations.")

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

cleaned_csv = convert_df_to_csv(df_filtered)

st.sidebar.download_button(
    label="📥 Download Processed CSV",
    data=cleaned_csv,
    file_name=f"warehouse_inventory_cleaned_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
    use_container_width=True
)


# ----------------- MAIN INTERFACE -----------------

# Page title and subtitle
st.markdown("<div class='main-title'>WAREHOUSE INVENTORY INTELLIGENCE</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A premium real-time diagnostics, visual analysis, and interactive data cleaning dashboard</div>", unsafe_allow_html=True)

# Tabs
tab_overview, tab_explorer, tab_health, tab_simulator = st.tabs([
    "📊 Overview Analytics", 
    "🔍 Inventory Explorer", 
    "🛡️ Data Health & Diagnostics", 
    "🔄 Restock Simulator"
])

# ----------------- TAB 1: OVERVIEW ANALYTICS -----------------
with tab_overview:
    # 1. KPI Cards Row (Using premium HTML cards)
    total_products = df_filtered['Product ID'].nunique()
    total_items = int(df_filtered['Quantity'].sum())
    total_value = (df_filtered['Quantity'] * df_filtered['Price']).sum()
    avg_price = df_filtered['Price'].mean() if len(df_filtered) > 0 else 0
    
    out_of_stock = len(df_filtered[df_filtered['Status'] == 'Out Of Stock'])
    low_stock = len(df_filtered[df_filtered['Status'] == 'Low Stock'])
    
    # Render custom metrics using columns
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Inventory Value</div>
            <div class="metric-val" style="background: linear-gradient(135deg, #00d2ff 0%, #00a8ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${total_value:,.2f}</div>
            <div class="metric-sub">Across {len(df_filtered)} recorded batches</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Items in Stock</div>
            <div class="metric-val" style="background: linear-gradient(135deg, #a55eea 0%, #8854d0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{total_items:,} units</div>
            <div class="metric-sub">{total_products} unique product tags</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Product Price</div>
            <div class="metric-val" style="background: linear-gradient(135deg, #2bcbba 0%, #0fb9b1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${avg_price:.2f}</div>
            <div class="metric-sub">Value density indicator</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Stock Status Alerts</div>
            <div class="metric-val" style="color: #ff7675;">{out_of_stock} <span style="font-size: 1rem; color: #8898aa; font-weight: normal;">Out</span> / <span style="color: #ff9f43;">{low_stock}</span> <span style="font-size: 1rem; color: #8898aa; font-weight: normal;">Low</span></div>
            <div class="metric-sub">Require immediate attention</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Charts Row
    st.markdown("<h3 style='margin-bottom:15px;'>📦 Inventory Visual Analysis</h3>", unsafe_allow_html=True)
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("<div class='content-panel'>", unsafe_allow_html=True)
        st.markdown("<h4>Valuation & Quantity by Category</h4>", unsafe_allow_html=True)
        
        # Calculate totals per category
        cat_data = df_filtered.copy()
        cat_data['Valuation'] = cat_data['Quantity'] * cat_data['Price']
        cat_summary = cat_data.groupby('Category').agg({
            'Valuation': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
        # Altair double bar / stacked bar or side-by-side
        chart_cat = alt.Chart(cat_summary).mark_bar(
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8,
            color='#00d2ff'
        ).encode(
            x=alt.X('Category:N', title='Category', axis=alt.Axis(labelAngle=0, labelColor='#8898aa', titleColor='#8898aa')),
            y=alt.Y('Valuation:Q', title='Total Valuation ($)', axis=alt.Axis(labelColor='#8898aa', titleColor='#8898aa')),
            tooltip=['Category', alt.Tooltip('Valuation:Q', format='$,.2f'), alt.Tooltip('Quantity:Q', format=',.0f')]
        ).properties(
            height=300
        ).configure_view(
            strokeWidth=0
        )
        
        st.altair_chart(chart_cat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_chart2:
        st.markdown("<div class='content-panel'>", unsafe_allow_html=True)
        st.markdown("<h4>Stock Distribution by Warehouse</h4>", unsafe_allow_html=True)
        
        # Calculate totals per warehouse
        wh_summary = df_filtered.groupby('Warehouse')['Quantity'].sum().reset_index()
        
        chart_wh = alt.Chart(wh_summary).mark_arc(innerRadius=60, stroke='#141923').encode(
            theta=alt.Theta(field="Quantity", type="quantitative"),
            color=alt.Color(field="Warehouse", type="nominal", scale=alt.Scale(
                domain=['Warehouse 1', 'Warehouse 2', 'Warehouse 3'],
                range=['#00d2ff', '#a55eea', '#2bcbba']
            ), legend=alt.Legend(title="Warehouse", labelColor='#8898aa', titleColor='#8898aa')),
            tooltip=['Warehouse', alt.Tooltip('Quantity:Q', format=',.0f')]
        ).properties(
            height=300
        )
        
        st.altair_chart(chart_wh, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Price vs. Quantity Distribution Scatter Plot
    st.markdown("<div class='content-panel'>", unsafe_allow_html=True)
    st.markdown("<h4>Product Valuation Matrix (Price vs. Quantity)</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; color:#8898aa; margin-top:-10px;'>Hover over items to see product details. Status groups reflect current cleaning state.</p>", unsafe_allow_html=True)
    
    chart_scatter = alt.Chart(df_filtered).mark_circle(size=100, opacity=0.7).encode(
        x=alt.X('Price:Q', title='Price ($)', scale=alt.Scale(domain=[0, 60]), axis=alt.Axis(labelColor='#8898aa', titleColor='#8898aa')),
        y=alt.Y('Quantity:Q', title='Stock Quantity', scale=alt.Scale(domain=[0, 350]), axis=alt.Axis(labelColor='#8898aa', titleColor='#8898aa')),
        color=alt.Color('Status:N', scale=alt.Scale(
            domain=['In Stock', 'Low Stock', 'Out Of Stock'],
            range=['#00d2ff', '#ff9f43', '#ff7675']
        ), legend=alt.Legend(title="Inventory Status", labelColor='#8898aa', titleColor='#8898aa')),
        tooltip=['Product ID', 'Product Name', 'Category', 'Warehouse', 'Location', 'Quantity', 'Price', 'Supplier', 'Status']
    ).properties(
        height=350
    ).interactive()
    
    st.altair_chart(chart_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ----------------- TAB 2: INVENTORY EXPLORER -----------------
with tab_explorer:
    st.markdown("<div class='content-panel'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>🔍 Browse Inventory Database</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; color:#8898aa; margin-top:-10px;'>Fully searchable inventory records. Sort by columns and download structured subsets.</p>", unsafe_allow_html=True)
    
    # Search input
    search_query = st.text_input("🔍 Quick Search (Search by Product Name or Product ID)", "", placeholder="Type name or product ID...")
    
    # Filter by search query
    df_search = df_filtered.copy()
    if search_query:
        df_search = df_search[
            df_search['Product Name'].str.contains(search_query, case=False, na=False) |
            df_search['Product ID'].astype(str).str.contains(search_query, case=False, na=False)
        ]
    
    # Setup dataframe column configuration for gorgeous formatting in Streamlit
    st.dataframe(
        df_search.sort_values(by="Product ID"),
        column_config={
            "Product ID": st.column_config.TextColumn("Product ID", help="Unique identifier for product record"),
            "Product Name": st.column_config.TextColumn("Product Name"),
            "Category": st.column_config.TextColumn("Category"),
            "Warehouse": st.column_config.TextColumn("Warehouse"),
            "Location": st.column_config.TextColumn("Location"),
            "Quantity": st.column_config.NumberColumn("Quantity", format="%.0f units"),
            "Price": st.column_config.NumberColumn("Price", format="$%.2f"),
            "Supplier": st.column_config.TextColumn("Supplier"),
            "Status": st.column_config.SelectboxColumn("Status", options=["In Stock", "Low Stock", "Out Of Stock"]),
            "Last Restocked": st.column_config.TextColumn("Last Restocked")
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Quick Summary Info for matching records
    st.markdown(f"<div style='font-size:0.85rem; color:#8898aa; text-align:right; margin-top:10px;'>Showing {len(df_search)} of {len(df_display)} database rows</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ----------------- TAB 3: DATA HEALTH & DIAGNOSTICS -----------------
with tab_health:
    st.markdown("<h3 style='margin-top:0;'>🛡️ Warehouse Integrity Diagnostics Report</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; color:#8898aa; margin-top:-10px;'>This report pinpoints integrity issues in the messy raw CSV data and details how the cleaning engine resolves them.</p>", unsafe_allow_html=True)
    
    raw_df = st.session_state['df_raw'].copy()
    
    # Calculate anomaly stats
    # 1. Product ID reuse anomalies
    prod_id_groups = raw_df.groupby('Product ID').nunique()
    reused_ids = prod_id_groups[(prod_id_groups['Product Name'] > 1) | (prod_id_groups['Category'] > 1) | (prod_id_groups['Supplier'] > 1) | (prod_id_groups['Price'] > 1)]
    reused_ids_count = len(reused_ids)
    
    reused_records_count = raw_df[raw_df['Product ID'].isin(reused_ids.index)].shape[0]
    
    # 2. Status mismatch anomalies
    # Anomaly condition: Out of Stock but Quantity > 0 OR In Stock but Quantity <= 100 OR Low Stock but Quantity > 100 or Quantity <= 0
    status_mismatch_mask = (
        ((raw_df['Status'] == 'Out Of Stock') & (raw_df['Quantity'] > 0)) |
        ((raw_df['Status'] == 'In Stock') & (raw_df['Quantity'] <= 100)) |
        ((raw_df['Status'] == 'Low Stock') & ((raw_df['Quantity'] > 100) | (raw_df['Quantity'] <= 0)))
    )
    mismatch_count = status_mismatch_mask.sum()
    
    # 3. Duplicate location entries
    dup_loc_mask = raw_df.duplicated(subset=['Product ID', 'Warehouse', 'Location'], keep=False)
    dup_loc_count = raw_df.duplicated(subset=['Product ID', 'Warehouse', 'Location']).sum()
    
    # Diagnostic cards
    c_diag1, c_diag2, c_diag3 = st.columns(3)
    with c_diag1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="color: #ff7675;">Product ID Overlaps</div>
            <div class="metric-val">{reused_ids_count} <span style="font-size:1rem; color:#8898aa;">IDs shared</span></div>
            <div class="metric-sub" style="color:#ff7675;">Affects {reused_records_count} raw database rows</div>
        </div>
        """, unsafe_allow_html=True)
    with c_diag2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="color: #ff9f43;">Status Discrepancies</div>
            <div class="metric-val">{mismatch_count} <span style="font-size:1rem; color:#8898aa;">mismatch rows</span></div>
            <div class="metric-sub" style="color:#ff9f43;">Labels disconnected from physical stock</div>
        </div>
        """, unsafe_allow_html=True)
    with c_diag3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label" style="color: #00d2ff;">Duplicate Locations</div>
            <div class="metric-val">{dup_loc_count} <span style="font-size:1rem; color:#8898aa;">extra batches</span></div>
            <div class="metric-sub" style="color:#00d2ff;">Multiple restocks at same warehouse aisle</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed diagnosis sections
    col_det1, col_det2 = st.columns(2)
    
    with col_det1:
        st.markdown("<div class='content-panel'>", unsafe_allow_html=True)
        st.markdown("<h4>🔍 Sample of Product ID Conflict Anomalies</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.8rem; color:#8898aa; margin-top:-10px;'>Rows with identical numeric Product IDs but representing completely different products:</p>", unsafe_allow_html=True)
        
        if reused_ids_count > 0:
            sample_reused_id = reused_ids.index[0]
            conflict_df = raw_df[raw_df['Product ID'] == sample_reused_id]
            st.dataframe(conflict_df, use_container_width=True, hide_index=True)
            st.info(f"💡 **Cleaning Resolution**: When 'De-duplicate Product IDs' is enabled in the sidebar, these rows are assigned suffix codes (e.g. `{sample_reused_id}-A`, `{sample_reused_id}-B`, `{sample_reused_id}-C`) based on their distinct names and categories. This instantly separates them in the database.")
        else:
            st.success("No Product ID conflicts detected in the current session data!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='content-panel'>", unsafe_allow_html=True)
        st.markdown("<h4>🗺️ Sample of Duplicate Aisle Location Batches</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.8rem; color:#8898aa; margin-top:-10px;'>Same product stored in multiple batches at the same warehouse and location:</p>", unsafe_allow_html=True)
        
        if dup_loc_count > 0:
            sample_dup_locations = raw_df[dup_loc_mask].sort_values(['Product ID', 'Warehouse', 'Location']).head(6)
            st.dataframe(sample_dup_locations[['Product ID', 'Product Name', 'Warehouse', 'Location', 'Quantity', 'Last Restocked']], use_container_width=True, hide_index=True)
            st.info("💡 **Cleaning Resolution**: When 'Consolidate Duplicate Locations' is enabled, the cleaning engine sums up these quantities and retains the most recent restocking date, consolidating the warehouse map.")
        else:
            st.success("No duplicate location records detected!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_det2:
        st.markdown("<div class='content-panel'>", unsafe_allow_html=True)
        st.markdown("<h4>⚖️ Raw vs. Cleaned Status Distribution</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.8rem; color:#8898aa; margin-top:-10px;'>Below we compare how stock status labels change when correcting quantity-to-status discrepancies:</p>", unsafe_allow_html=True)
        
        # Prepare data for before/after chart
        raw_status = raw_df['Status'].value_counts().reset_index()
        raw_status['Dataset'] = 'Raw Data (Inconsistent)'
        
        cleaned_temp = apply_cleaning(raw_df, fix_status=True, deduplicate_ids=False, consolidate_locations=False)
        cleaned_status = cleaned_temp['Status'].value_counts().reset_index()
        cleaned_status['Dataset'] = 'Cleaned Data (Calibrated)'
        
        status_comparison = pd.concat([raw_status, cleaned_status])
        
        chart_compare = alt.Chart(status_comparison).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X('Status:N', title='Inventory Status Label', axis=alt.Axis(labelAngle=0, labelColor='#8898aa', titleColor='#8898aa')),
            y=alt.Y('count:Q', title='Number of Records', axis=alt.Axis(labelColor='#8898aa', titleColor='#8898aa')),
            color=alt.Color('Dataset:N', scale=alt.Scale(
                domain=['Raw Data (Inconsistent)', 'Cleaned Data (Calibrated)'],
                range=['#ff7675', '#00d2ff']
            ), legend=alt.Legend(orient='bottom', labelColor='#8898aa', titleColor='#8898aa')),
            xOffset='Dataset:N'
        ).properties(
            height=300
        )
        
        st.altair_chart(chart_compare, use_container_width=True)
        
        st.write("🔍 **Status Discrepancy Breakdown (Raw Data):**")
        st.write("- **Out of Stock items containing products**: In the raw dataset, items marked as 'Out Of Stock' actually represent physical units. For instance, a record marked Out Of Stock with 300 quantity! This leads to major reporting errors.")
        st.write("- **Low Stock items with high quantity**: Lots of products with quantity 300 are labeled 'Low Stock', which blocks logical restocking algorithms.")
        st.markdown("</div>", unsafe_allow_html=True)


# ----------------- TAB 4: RESTOCK SIMULATOR -----------------
with tab_simulator:
    st.markdown("<div class='content-panel'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;'>🔄 Warehouse Inventory Simulator</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; color:#8898aa; margin-top:-10px;'>Simulate restocking operations or introduce new products into the warehouse catalog. Submitting updates will modify the active session data, updating all charts instantly.</p>", unsafe_allow_html=True)
    
    # Form to add/update product
    with st.form("inventory_action_form"):
        st.markdown("<h4>📋 Product Entry Details</h4>", unsafe_allow_html=True)
        
        sim_col1, sim_col2 = st.columns(2)
        
        with sim_col1:
            # Let the user choose to edit an existing Product ID or add a new one
            action_type = st.radio("Choose Operation Type", ["Update Existing Product / Restock", "Register Brand New Product ID"])
            
            if action_type == "Update Existing Product / Restock":
                # Get lists of unique product options from RAW data
                existing_pids = sorted(st.session_state['df_raw']['Product ID'].unique())
                selected_pid = st.selectbox("Select Product ID to Restock", options=existing_pids)
                
                # Fetch existing details to pre-populate or inform
                ref_rows = st.session_state['df_raw'][st.session_state['df_raw']['Product ID'] == selected_pid]
                st.caption(f"ℹ️ *This ID currently references {len(ref_rows)} row(s) in the database.*")
                
                # We will pick the attributes of the first match as defaults
                default_name = ref_rows.iloc[0]['Product Name']
                default_cat = ref_rows.iloc[0]['Category']
                default_supplier = ref_rows.iloc[0]['Supplier']
                default_price = float(ref_rows.iloc[0]['Price'])
                default_wh = ref_rows.iloc[0]['Warehouse']
                default_loc = ref_rows.iloc[0]['Location']
                default_qty = float(ref_rows.iloc[0]['Quantity'])
            else:
                # Add new
                max_pid = int(st.session_state['df_raw']['Product ID'].max())
                selected_pid = max_pid + 1
                st.caption(f"🆕 *Assigning new unique numeric ID: {selected_pid}*")
                
                default_name = "gadget x"
                default_cat = "Electronics"
                default_supplier = "Supplier A"
                default_price = 19.99
                default_wh = "Warehouse 1"
                default_loc = "Aisle 1"
                default_qty = 100.0
                
            prod_name = st.selectbox(
                "Product Name", 
                options=["gadget x", "gadget y", "gadget z", "widget a", "widget b", "widget c"], 
                index=["gadget x", "gadget y", "gadget z", "widget a", "widget b", "widget c"].index(default_name)
            )
            
            prod_cat = st.selectbox(
                "Category", 
                options=["Electronics", "Clothing", "Toys", "Furniture"], 
                index=["Electronics", "Clothing", "Toys", "Furniture"].index(default_cat)
            )
            
            prod_supplier = st.selectbox(
                "Supplier", 
                options=["Supplier A", "Supplier B", "Supplier C", "Supplier D"], 
                index=["Supplier A", "Supplier B", "Supplier C", "Supplier D"].index(default_supplier)
            )
            
        with sim_col2:
            prod_price = st.number_input("Unit Price ($)", min_value=1.0, max_value=1000.0, value=default_price, step=0.01)
            
            prod_wh = st.selectbox(
                "Warehouse Destination", 
                options=["Warehouse 1", "Warehouse 2", "Warehouse 3"], 
                index=["Warehouse 1", "Warehouse 2", "Warehouse 3"].index(default_wh)
            )
            
            prod_loc = st.selectbox(
                "Aisle Location", 
                options=["Aisle 1", "Aisle 2", "Aisle 3", "Aisle 4", "Aisle 5"], 
                index=["Aisle 1", "Aisle 2", "Aisle 3", "Aisle 4", "Aisle 5"].index(default_loc)
            )
            
            # The main adjustment - Quantity
            if action_type == "Update Existing Product / Restock":
                prod_qty = st.number_input("New Stock Level (Quantity in Warehouse)", min_value=0.0, max_value=10000.0, value=default_qty, step=10.0, help="This replaces the quantity of the record.")
            else:
                prod_qty = st.number_input("Initial Stock Level (Quantity)", min_value=0.0, max_value=10000.0, value=100.0, step=10.0)
                
            # Date restocked
            restock_date = st.date_input("Last Restocked Date", value=datetime.today())
            
            # Simulated Status input
            st.markdown("<p style='font-size:0.85rem; font-weight: 500; margin-bottom: 2px;'>Manual Status Assignment (for raw data simulator)</p>", unsafe_allow_html=True)
            status_input = st.selectbox(
                "Status Label (Simulate raw inconsistency)",
                options=["In Stock", "Low Stock", "Out Of Stock"],
                index=0,
                help="This simulates how the data is recorded raw. If 'Fix Status Inconsistencies' is checked in the sidebar, this value will be automatically recalibrated based on the quantity."
            )
            
        submit_btn = st.form_submit_button("⚡ Apply Inventory Transaction", use_container_width=True)
        
        if submit_btn:
            # We will edit st.session_state['df_raw']
            df_temp = st.session_state['df_raw'].copy()
            restock_date_str = restock_date.strftime('%Y-%m-%d')
            
            if action_type == "Update Existing Product / Restock":
                # Find matching rows in df_raw
                match_indices = df_temp[
                    (df_temp['Product ID'] == selected_pid) & 
                    (df_temp['Warehouse'] == prod_wh) & 
                    (df_temp['Location'] == prod_loc)
                ].index
                
                if len(match_indices) > 0:
                    # Update existing record
                    df_temp.loc[match_indices[0], 'Product Name'] = prod_name
                    df_temp.loc[match_indices[0], 'Category'] = prod_cat
                    df_temp.loc[match_indices[0], 'Supplier'] = prod_supplier
                    df_temp.loc[match_indices[0], 'Price'] = prod_price
                    df_temp.loc[match_indices[0], 'Quantity'] = prod_qty
                    df_temp.loc[match_indices[0], 'Last Restocked'] = restock_date_str
                    df_temp.loc[match_indices[0], 'Status'] = status_input
                    st.success(f"Successfully updated inventory for Product ID {selected_pid} in {prod_wh}, {prod_loc}!")
                else:
                    # If Product ID matches but in a new location, append it as a new batch!
                    new_row = {
                        'Product ID': int(selected_pid),
                        'Product Name': prod_name,
                        'Category': prod_cat,
                        'Warehouse': prod_wh,
                        'Location': prod_loc,
                        'Quantity': float(prod_qty),
                        'Price': float(prod_price),
                        'Supplier': prod_supplier,
                        'Status': status_input,
                        'Last Restocked': restock_date_str
                    }
                    df_temp = pd.concat([df_temp, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"Added new warehouse batch for Product ID {selected_pid} in {prod_wh}, {prod_loc}!")
            else:
                # Add completely new product
                new_row = {
                    'Product ID': int(selected_pid),
                    'Product Name': prod_name,
                    'Category': prod_cat,
                    'Warehouse': prod_wh,
                    'Location': prod_loc,
                    'Quantity': float(prod_qty),
                    'Price': float(prod_price),
                    'Supplier': prod_supplier,
                    'Status': status_input,
                    'Last Restocked': restock_date_str
                }
                df_temp = pd.concat([df_temp, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Successfully registered new Product ID {selected_pid} in the database!")
                
            # Update session state
            st.session_state['df_raw'] = df_temp
            st.rerun()

    # Reset option to restore original file content
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
    if st.button("🗑️ Reset Database to Original Messy CSV", use_container_width=True):
        st.session_state['df_raw'] = load_original_csv()
        st.success("Database reset to the original messy dataset successfully!")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
