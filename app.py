import datetime
import random
import string
import pandas as pd
import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="4U2 للمحاسبة والمخزون",
    page_icon="📊",
    layout="wide"
)

# --- التنسيق البصري CSS ---
st.markdown("""
<style>
.stApp {
    background-color: #F8FAFC;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.main-header {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
    padding: 20px;
    border-radius: 12px;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 20px;
}
.main-header h1 {
    color: #FFFFFF !important;
    font-size: 24px !important;
    margin: 0;
}
.main-header p {
    color: #94A3B8 !important;
    font-size: 13px !important;
    margin-top: 5px;
}
.stButton>button {
    background: #2563EB;
    color: white !important;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 8px 16px;
}
</style>
""", unsafe_allow_html=True)

# --- إدارة حالة الجلسة (Session State) ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"المنتج": "سماعة بلوتوث", "الكمية": 15, "تكلفة الشراء (ر.س)": 40.0, "سعر البيع (ر.س)": 99.0},
        {"المنتج": "شاحن جداري", "الكمية": 5, "تكلفة الشراء (ر.س)": 15.0, "سعر البيع (ر.س)": 45.0}
    ])

if "subscribers_db" not in st.session_state:
    st.session_state.subscribers_db = {
        "K9X2-M7P4": datetime.date(2026, 8, 30),
        "H7T1-Z5W6": datetime.date(2026, 8, 30)
    }

MASTER_KEY = st.secrets.get("MASTER_KEY", "Abud")

def generate_random_code():
    chars = string.ascii_uppercase + string.digits
    return f"{''.join(random.choices(chars, k=4))}-{''.join(random.choices(chars, k=4))}"

# --- بوابة الوصول الآمن في القائمة الجانبية ---
st.sidebar.markdown("### 🔐 بوابة الوصول الآمن")
uk = st.sidebar.text_input("مفتاح الاشتراك:", type="password")

if not uk:
    st.markdown('<div class="main-header"><h1>4U2 للمحاسبة</h1><p>نظام الهندسة المالية وإدارة المخزون</p></div>', unsafe_allow_html=True)
    st.warning("🔒 أدخل مفتاح الاشتراك بالقائمة الجانبية للوصول للنظام.")
    st.stop()

is_master = (uk == MASTER_KEY)
db = st.session_state.subscribers_db
today = datetime.date.today()

if not is_master and uk not in db:
    st.error("❌ مفتاح الاشتراك غير صحيح.")
    st.stop()

if not is_master:
    if today > (db[uk] + datetime.timedelta(days=365)):
        st.error("❌ انتهت صلاحية الاشتراك.")
        st.stop()
    days_left = (db[uk] + datetime.timedelta(days=365) - today).days
    st.sidebar.caption(f"⏳ متبقي على اشتراكك: {days_left} يوم")

st.sidebar.markdown("---")

# --- التنقل في التطبيق ---
nav_options = ["🧮 حاسبة التكاليف الشاملة", "📦 إدارة المخزون"]
if is_master:
    nav_options.append("🛠️ لوحة المدير")

app_mode = st.sidebar.selectbox("اختر القسم:", nav_options)

# --- 1. قسم حاسبة التكاليف الشاملة ---
if app_mode == "🧮 حاسبة التكاليف الشاملة":
    st.markdown('<div class="main-header"><h1>حاسبة التكاليف والربحية الشاملة</h1></div>', unsafe_allow_html=True)

    # 1. التكاليف العامة والعمولات
    st.subheader("1️⃣ التكاليف الإضافية والعمولات")
    col1, col2 = st.columns(2)
    with col1:
        mc = st.number_input("تكاليف التسويق الإجمالية (ر.س):", min_value=0.0, value=50.0)
        overhead_val = st.number_input("التكلفة العامة / التشغيلية الثابتة (ر.س):", min_value=0.0, value=30.0)
        overhead_rate_input = st.number_input("نسبة التكلفة العامة من المبيعات (%):", min_value=0.0, value=0.0)
    with col2:
        gr = st.number_input("عمولة بوابة الدفع (%):", min_value=0.0, value=2.5) / 100.0
        iv = st.checkbox("احتساب ضريبة القيمة المضافة (15%)", value=True)

    # 2. حسبة رسوم الشحن
    st.markdown("---")
    st.subheader("2️⃣ حسبة رسوم الشحن")
    col_ship1, col_ship2 = st.columns(2)
    with col_ship1:
        shipping_calc_type = st.selectbox(
            "طريقة توزيع الشحن على المنتجات:",
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
    if not df.empty:
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

            st.dataframe(selected_df[['المنتج', 'الكمية', 'تكلفة الشراء (ر.س)', 'سعر البيع (ر.س)', 'حصة الشحن (ر.س)']], use_container_width=True)

            # الحسابات المالية
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
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("إجمالي المبيعات", f"{total_sell:.2f} ر.س")
            c2.metric("إجمالي التكاليف", f"{tc:.2f} ر.س")
            c3.metric("صافي الربح", f"{npf:.2f} ر.س")
            c4.metric("هامش الربح", f"{pm:.1f}%")

            if pm >= 30:
                st.success("🟢 هامش ربح ممتاز!")
            elif pm >= 15:
                st.info("🟡 هامش ربح متوسط.")
            else:
                st.error("🔴 هامش ربح منخفض أو خسارة!")

            # 4. التقرير المالي التفاعلي للطباعة والمباشرة كـ PDF
            st.markdown("---")
            st.subheader("📄 معااينة وطباعة التقرير (PDF)")

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
    else:
        st.info("لا توجد منتجات بالمخزون حالياً. يرجى إضافتها من قسم إدارة المخزون.")

# --- 2. قسم إدارة المخزون ---
elif app_mode == "📦 إدارة المخزون":
    st.markdown('<div class="main-header"><h1>إدارة المخزون</h1></div>', unsafe_allow_html=True)
    
    st.subheader("➕ إضافة منتج جديد")
    with st.form("add_product_form", clear_on_submit=True):
        c_name, c_qty, c_buy, c_sell = st.columns(4)
        with c_name:
            new_name = st.text_input("اسم المنتج:")
        with c_qty:
            new_qty = st.number_input("الكمية:", min_value=1, value=1, step=1)
        with c_buy:
            new_buy = st.number_input("تكلفة الشراء (ر.س):", min_value=0.0, value=10.0, step=1.0)
        with c_sell:
            new_sell = st.number_input("سعر البيع (ر.س):", min_value=0.0, value=20.0, step=1.0)
            
        submit_btn = st.form_submit_button("إضافة إلى المخزون")
        if submit_btn:
            if new_name.strip() == "":
                st.error("يرجى إدخال اسم المنتج.")
            else:
                new_row = pd.DataFrame([{"المنتج": new_name, "الكمية": new_qty, "تكلفة الشراء (ر.س)": new_buy, "سعر البيع (ر.س)": new_sell}])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                st.success(f"تمت إضافة '{new_name}' بنجاح!")
                st.rerun()

    st.markdown("---")
    st.subheader("📋 المنتجات الحالية")
    st.dataframe(st.session_state.inventory, use_container_width=True)

# --- 3. قسم لوحة المدير (لـ MASTER_KEY فقط) ---
elif app_mode == "🛠️ لوحة المدير" and is_master:
    st.markdown('<div class="main-header"><h1>لوحة تحكم المدير</h1></div>', unsafe_allow_html=True)
    
    with st.expander("⚙️ توليد أكواد اشتراك جديدة", expanded=True):
        if st.button("✨ توليد كود جديد"):
            nc = generate_random_code()
            while nc in db:
                nc = generate_random_code()
            db[nc] = today
            st.success(f"تم توليد الكود بنجاح: {nc}")

    st.subheader("🔑 الأكواد المفعّلة")
    sl = [{"الكود": k, "تاريخ التفعيل": str(v), "الحالة": "فعال"} for k, v in db.items()]
    st.dataframe(pd.DataFrame(sl), use_container_width=True)
