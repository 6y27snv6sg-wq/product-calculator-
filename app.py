import streamlit as st
import pandas as pd
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="4U2 - حاسبة التكاليف والمخزون",
    page_icon="📦",
    layout="wide"
)

# --- 1. تهيئة الذاكرة (Session State) ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"المنتج": "منتج A", "تكلفة الشراء (ر.س)": 50.0, "سعر البيع (ر.س)": 100.0},
        {"المنتج": "منتج B", "تكلفة الشراء (ر.س)": 30.0, "سعر البيع (ر.س)": 70.0}
    ])

# --- 2. القائمة الجانبية ---
st.sidebar.title("4U2 Admin")
im = st.sidebar.checkbox("تفعيل وضع المدير", value=True)

mo = ["🧮 حاسبة التكاليف الشاملة", "📦 إدارة المخزون"]
if im:
    mo.append("🛠️ لوحة المدير")

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

        # 5. عرض التقرير المباشر
        st.markdown("---")
        st.subheader("📄 معايرة وطباعة التقرير (PDF)")

        rows_html = "".join([f"<tr><td>{r['المنتج']}</td><td>{r['تكلفة الشراء (ر.س)']:.2f}</td><td>{r['حصة الشحن (ر.س)']:.2f}</td><td>{r['سعر البيع (ر.س)']:.2f}</td></tr>" for _, r in selected_df.iterrows()])

        preview_html = f"""
        <div style="border: 2px solid #cbd5e1; border-radius: 12px; padding: 20px; background-color: #ffffff; color: #1e293b; font-family: system-ui, sans-serif; direction: rtl;">
            <div style="text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; margin-bottom: 15px;">
                <h2 style="color: #1e3a8a; margin: 0;">4U2 للمحاسبة - تقرير الشحنة والتكاليف</h2>
                <p style="margin: 5px 0; color: #64748b;">التاريخ: {datetime.date.today()}</p>
            </div>
            
            <h4 style="color: #1e3a8a; margin-bottom: 8px;">تفاصيل المنتجات:</h4>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 14px;">
                <thead>
                    <tr style="background-color: #1e3a8a; color: white;">
                        <th style="padding: 6px; text-align: right;">المنتج</th>
                        <th style="padding: 6px; text-align: right;">الشراء</th>
                        <th style="padding: 6px; text-align: right;">حصة الشحن</th>
                        <th style="padding: 6px; text-align: right;">البيع</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>

            <h4 style="color: #1e3a8a; margin-bottom: 8px;">الملخص المالي:</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;">إجمالي المبيعات</td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0; font-weight: bold;">{total_sell:.2f} ر.س</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;">إجمالي الشراء والشحن</td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;">{(total_buy + actual_shipping):.2f} ر.س</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;">التكاليف التشغيلية والتسويق</td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;">{(mc + calc_overhead):.2f} ر.س</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;">العمولات والضرائب</td><td style="padding: 6px; border-bottom: 1px solid #e2e8f0;">{(gf + va):.2f} ر.س</td></tr>
                <tr style="background-color: #f0fdf4; color: #16a34a; font-weight: bold;"><td style="padding: 8px;">صافي الربح النهائي</td><td style="padding: 8px;">{npf:.2f} ر.س ({pm:.1f}%)</td></tr>
            </table>

            <div style="margin-top: 20px; text-align: center;">
                <button onclick="window.print()" style="background-color: #1e3a8a; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%;">
                    🖨️ حفظ التقرير كـ PDF / طباعة فورية
                </button>
            </div>
        </div>
        """
        st.components.v1.html(preview_html, height=520, scrolling=True)

    else:
        st.warning("يرجى اختيار منتج واحد على الأقل.")

# --- القسم الثاني: إدارة المخزون (تمت إضافة نموذج الإضافة هنا) ---
elif am == "📦 إدارة المخزون":
    st.header("📦 إدارة المخزون")
    
    # نموذج إضافة منتج جديد
    st.subheader("➕ إضافة منتج جديد")
    with st.form("add_product_form", clear_on_submit=True):
        col_name, col_buy, col_sell = st.columns(3)
        with col_name:
            new_name = st.text_input("اسم المنتج:")
        with col_buy:
            new_buy = st.number_input("تكلفة الشراء (ر.س):", min_value=0.0, step=1.0)
        with col_sell:
            new_sell = st.number_input("سعر البيع (ر.س):", min_value=0.0, step=1.0)
            
        submit_btn = st.form_submit_button("إضافة المنتج إلى المخزون")
        
        if submit_btn:
            if new_name.strip() == "":
                st.error("يرجى إدخال اسم المنتج.")
            else:
                new_row = pd.DataFrame([{"المنتج": new_name, "تكلفة الشراء (ر.س)": new_buy, "سعر البيع (ر.س)": new_sell}])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                st.success(f"تمت إضافة '{new_name}' بنجاح!")

    st.markdown("---")
    st.subheader("📋 قائمة المنتجات الحالية")
    st.dataframe(st.session_state.inventory, use_container_width=True)

# --- القسم الثالث: لوحة المدير ---
elif am == "🛠️ لوحة المدير":
    st.header("🛠️ لوحة التحكم والإعدادات")
    st.info("إعدادات النظام العامة.")
