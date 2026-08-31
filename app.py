import streamlit as st
import pandas as pd
import datetime
import base64

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="4U2 - نظام إدارة المحاسبة والمخزون",
    page_icon="📦",
    layout="wide"
)

# --- إدارة حالة الجلسة (Session State) ---
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "🧮 حاسبة التكاليف الشاملة"

if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"المنتج": "منتج A", "تكلفة الشراء (ر.س)": 50.0, "سعر البيع (ر.س)": 100.0},
        {"المنتج": "منتج B", "تكلفة الشراء (ر.س)": 30.0, "سعر البيع (ر.س)": 70.0}
    ])

# --- دالة طباعة HTML بديلة ومضمونة 100% بدون مكتبات خارجية ---
def get_html_print_button(df, mc, sc, gr, iv):
    total_buy = df['تكلفة الشراء (ر.س)'].sum()
    total_sell = df['سعر البيع (ر.س)'].sum()
    va = (total_sell - (total_sell / 1.15)) if iv else 0.0
    ns = total_sell - va
    gf = ns * gr
    tc = total_buy + mc + sc + gf
    npf = ns - tc
    pm = (npf / ns * 100) if ns > 0 else 0.0

    rows = "".join([
        f"<tr><td>{row['المنتج']}</td><td>{row['تكلفة الشراء (ر.س)']:.2f}</td><td>{row['سعر البيع (ر.س)']:.2f}</td></tr>" 
        for _, row in df.iterrows()
    ])

    html_code = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
    <meta charset="UTF-8">
    <title>تقرير الشحنة - 4U2</title>
    <style>
        body {{ font-family: system-ui, sans-serif; padding: 20px; color: #1e293b; background: #fff; }}
        .card {{ border: 1px solid #cbd5e1; border-radius: 8px; padding: 25px; max-width: 600px; margin: auto; }}
        .header {{ text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 15px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        th, td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right; }}
        th {{ background: #1e3a8a; color: white; }}
        .btn-print {{ background: #1e3a8a; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; margin-top: 15px; }}
        @media print {{ .btn-print {{ display: none; }} }}
    </style>
    </head>
    <body>
    <div class="card">
        <div class="header">
            <h2>4U2 للمحاسبة - تقرير الشحنة</h2>
            <p>التاريخ: {datetime.date.today()}</p>
        </div>
        <h3>تفاصيل المنتجات:</h3>
        <table>
            <tr><th>المنتج</th><th>تكلفة الشراء</th><th>سعر البيع</th></tr>
            {rows}
        </table>
        <h3>الملخص المالي:</h3>
        <table>
            <tr><td>إجمالي المبيعات</td><td>{total_sell:.2f} ر.س</td></tr>
            <tr><td>إجمالي التكاليف</td><td>{tc:.2f} ر.س</td></tr>
            <tr style="font-weight:bold; color:#16a34a;"><td>صافي الربح</td><td>{npf:.2f} ر.س</td></tr>
            <tr style="font-weight:bold;"><td>هامش الربح</td><td>{pm:.1f}%</td></tr>
        </table>
        <button class="btn-print" onclick="window.print()">🖨️ حفظ كـ PDF / طباعة</button>
    </div>
    </body>
    </html>
    """
    
    b64 = base64.b64encode(html_code.encode('utf-8')).decode('utf-8')
    return f'''
        <a href="data:text/html;base64,{b64}" target="_blank" 
           style="display: block; width: 100%; padding: 12px; color: white; background-color: #1e3a8a; 
                  text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
            📄 فتح التقرير للطباعة / الحفظ كـ PDF
        </a>
    '''

# --- القائمة الجانبية ---
st.sidebar.title("4U2 Admin")
im = st.sidebar.checkbox("تفعيل وضع المدير", value=True)

mo = ["🧮 حاسبة التكاليف الشاملة", "📦 إدارة المخزون"]
if im:
    mo.append("🛠️ لوحة المدير")

current_index = mo.index(st.session_state.current_tab) if st.session_state.current_tab in mo else 0

am = st.sidebar.selectbox("اختر القسم:", mo, index=current_index, key="nav_select")
st.session_state.current_tab = am

# --- القسم الأول ---
if st.session_state.current_tab == "🧮 حاسبة التكاليف الشاملة":
    st.header("🧮 حاسبة التكاليف والشحنات المجمعة")
    
    col1, col2 = st.columns(2)
    with col1:
        mc = st.number_input("تكاليف التسويق (ر.س):", min_value=0.0, value=50.0)
        sc = st.number_input("تكاليف الشحن (ر.س):", min_value=0.0, value=20.0)
    with col2:
        gr = st.number_input("نسبة البوابة/العمولة (%):", min_value=0.0, value=2.5) / 100
        iv = st.checkbox("خاضع لضريبة القيمة المضافة (15%)", value=True)

    df = st.session_state.inventory
    selected_indices = st.multiselect(
        "اختر المنتجات المضمنة في التقرير:",
        options=list(df.index),
        format_func=lambda x: f"{df.loc[x, 'المنتج']} - {df.loc[x, 'سعر البيع (ر.س)']} ر.س",
        default=list(df.index)
    )

    if selected_indices:
        selected_df = df.loc[selected_indices]
        st.dataframe(selected_df, use_container_width=True)
        st.markdown("---")
        
        # رابط الطباعة
        st.markdown(get_html_print_button(selected_df, mc, sc, gr, iv), unsafe_allow_html=True)

elif st.session_state.current_tab == "📦 إدارة المخزون":
    st.header("📦 إدارة المخزون")
    st.dataframe(st.session_state.inventory, use_container_width=True)

elif st.session_state.current_tab == "🛠️ لوحة المدير":
    st.header("🛠️ لوحة التحكم والإعدادات")
    st.info("إعدادات النظام العامة.")
