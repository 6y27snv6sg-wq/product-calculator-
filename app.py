import streamlit as st
import pandas as pd
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="4U2 - حاسبة التكاليف والمخزون",
    page_icon="📦",
    layout="wide"
)

# --- 1. تهيئة الذاكرة (Session State) بشكل آمن مسبقاً ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"المنتج": "منتج A", "تكلفة الشراء (ر.س)": 50.0, "سعر البيع (ر.س)": 100.0},
        {"المنتج": "منتج B", "تكلفة الشراء (ر.س)": 30.0, "سعر البيع (ر.س)": 70.0}
    ])

# --- 2. القائمة الجانبية (بدون أخطاء الدوران اللانهائي) ---
st.sidebar.title("4U2 Admin")
im = st.sidebar.checkbox("تفعيل وضع المدير", value=True)

mo = ["🧮 حاسبة التكاليف الشاملة", "📦 إدارة المخزون"]
if im:
    mo.append("🛠️ لوحة المدير")

# اختيار القسم مباشرة بدون ربط مضاعف يتسبب في الدوران
am = st.sidebar.selectbox("اختر القسم:", mo)

# --- القسم الأول: حاسبة التكاليف الشاملة ---
if am == "🧮 حاسبة التكاليف الشاملة":
    st.header("🧮 حاسبة التكاليف والشحنات المجمعة")
    
    # 1. التكاليف العامة والعمولات
    st.subheader("1️⃣ التكاليف الإضافية والعمولات")
    col1, col2 = st.columns(2)
    
    with col1:
        mc = st.number_input("تكاليف التسويق الإجمالية (ر.س):", min_value=0.0, value=50.0)
        overhead_val = st.number_input("التكلفة العامة / التشغيلية الثابتة (ر.س):", min_value=0.0, value=30.0)
        overhead_rate_input = st.number_input("نسبة التكلفة العامة من المبيعات (%):", min_value=0.0, value=0.0)
        
    with col2:
        gr = st.number_input("نسبة بوابة الدفع / العمولة (%):", min_value=0.0, value=2.5) / 100.0
        iv = st.checkbox("خاضع لضريبة القيمة المضافة (15%)", value=True)

    # 2. حسبة رسوم الشحن
    st.markdown("---")
    st.subheader("2️⃣ حسبة رسوم الشحن")
    
    col_ship1, col_ship2 = st.columns(2)
    with col_ship1:
        shipping_calc_type = st.selectbox(
            "طريقة توزيع الشحن:",
            ["توزيع الإجمالي بالتساوي", "توزيع الإجمالي حسب تكلفة الشراء", "مبلغ شحن ثابت لكل قطعة"]
        )
    with col_ship2:
        if shipping_calc_type == "مبلغ شحن ثابت لكل قطعة":
            sc_per_item = st.number_input("رسوم الشحن للقطعة الواحدة (ر.س):", min_value=0.0, value=15.0)
            total_shipping = 0.0
        else:
            total_shipping = st.number_input("إجمالي رسوم الشحن للشحنة (ر.س):", min_value=0.0, value=40.0)
            sc_per_item = 0.0

    # 3. اختيار المنتجات وتوزيع التكاليف
    st.markdown("---")
    st.subheader("3️⃣ اختيار منتجات الشحنة")
    
    df = st.session_state.inventory
    selected_indices = st.multiselect(
        "اختر المنتجات المضمنة في التقرير:",
        options=list(df.index),
        format_func=lambda x: f"{df.loc[x, 'المنتج']} - سعر البيع: {df.loc[x, 'سعر البيع (ر.س)']} ر.س",
        default=list(df.index)
    )

    if selected_indices:
        selected_df = df.loc[selected_indices].copy()
        num_items = len(selected_df)
        total_buy_all = selected_df['تكلفة الشراء (ر.س)'].sum()

        # احتساب حصة كل منتج من الشحن
        if shipping_calc_type == "توزيع الإجمالي بالتساوي":
            selected_df['حصة الشحن (ر.س)'] = total_shipping / num_items if num_items > 0 else 0
        elif shipping_calc_type == "توزيع الإجمالي حسب تكلفة الشراء":
            selected_df['حصة الشحن (ر.س)'] = (selected_df['تكلفة الشراء (ر.س)'] / total_buy_all * total_shipping) if total_buy_all > 0 else 0
        else:
            selected_df['حصة الشحن (ر.س)'] = sc_per_item

        st.dataframe(selected_df[['المنتج', 'تكلفة الشراء (ر.س)', 'سعر البيع (ر.س)', 'حصة الشحن (ر.س)']], use_container_width=True)

        # 4. الحسابات المالية المجمعة
        total_buy = selected_df['تكلفة الشراء (ر.س)'].sum()
        total_sell = selected_df['سعر البيع (ر.س)'].sum()
        actual_shipping = selected_df['حصة الشحن (ر.س)'].sum()

        va = (total_sell - (total_sell / 1.15)) if iv else 0.0
        ns = total_sell - va
        gf = ns * gr
        
        # التكلفة العامة الإجمالية (المبلغ الثابت + النسبة)
        calc_overhead = overhead_val + (ns * (overhead_rate_input / 100.0))
        
        tc = total_buy + mc + actual_shipping + gf + calc_overhead
        npf = ns - tc
        pm = (npf / ns * 100) if ns > 0 else 0.0

        st.markdown("---")
        st.subheader("📊 الملخص المالي للشحنة")
        
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        res_col1.metric("إجمالي المبيعات", f"{total_sell:.2f} ر.س")
        res_col2.metric("إجمالي التكاليف", f"{tc:.2f} ر.س")
        res_col3.metric("صافي الربح", f"{npf:.2f} ر.س", delta=f"{pm:.1f}% هامش ربح")
        res_col4.metric("التكلفة العامة المستقطعة", f"{calc_overhead:.2f} ر.س")

        # 5. تصدير التقرير
        st.markdown("---")
        st.subheader("📄 تصدير التقرير")

        report_html = f"""<!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="UTF-8">
        <style>
            body {{ font-family: system-ui, sans-serif; padding: 20px; color: #1e293b; background: #fff; }}
            .card {{ border: 2px solid #e2e8f0; border-radius: 10px; padding: 20px; max-width: 650px; margin: auto; }}
            .h {{ text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 15px; }}
            td, th {{ padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: right; }}
            th {{ background: #1e3a8a; color: white; }}
            .tr {{ font-weight: bold; background: #f8fafc; }}
        </style></head><body>
        <div class="card">
            <div class="h">
                <h2>4U2 للمحاسبة - تقرير الشحنة والتكاليف</h2>
                <p>التاريخ: {datetime.date.today()}</p>
            </div>
            <h3>تفاصيل المنتجات والتكاليف:</h3>
            <table>
                <tr><th>المنتج</th><th>الشراء</th><th>حصة الشحن</th><th>البيع</th></tr>
                {"".join([f"<tr><td>{r['المنتج']}</td><td>{r['تكلفة الشراء (ر.س)']:.2f}</td><td>{r['حصة الشحن (ر.س)']:.2f}</td><td>{r['سعر البيع (ر.س)']:.2f}</td></tr>" for _, r in selected_df.iterrows()])}
            </table>
            <h3>الملخص المالي:</h3>
            <table>
                <tr><td>إجمالي المبيعات</td><td>{total_sell:.2f} ر.س</td></tr>
                <tr><td>إجمالي الشراء والشحن</td><td>{(total_buy + actual_shipping):.2f} ر.س</td></tr>
                <tr><td>التكاليف التشغيلية والتسويق</td><td>{(mc + calc_overhead):.2f} ر.س</td></tr>
                <tr><td>العمولات والضرائب</td><td>{(gf + va):.2f} ر.س</td></tr>
                <tr class="tr" style="color:#16a34a;"><td>صافي الربح النهائي</td><td>{npf:.2f} ر.س</td></tr>
                <tr class="tr"><td>هامش الربح</td><td>{pm:.1f}%</td></tr>
            </table>
        </div></body></html>"""

        st.download_button(
            label="📥 تنزيل التقرير (HTML/PDF)",
            data=report_html.encode('utf-8'),
            file_name=f"4U2_Report_{datetime.date.today()}.html",
            mime="text/html",
            use_container_width=True
        )
    else:
        st.warning("يرجى اختيار منتج واحد على الأقل.")

# --- القسم الثاني: إدارة المخزون ---
elif am == "📦 إدارة المخزون":
    st.header("📦 إدارة المخزون")
    st.dataframe(st.session_state.inventory, use_container_width=True)

# --- القسم الثالث: لوحة المدير ---
elif am == "🛠️ لوحة المدير":
    st.header("🛠️ لوحة التحكم والإعدادات")
    st.info("إعدادات النظام العامة.")
