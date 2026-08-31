import datetime
import random
import string
import pandas as pd
import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="4U2 للمحاسبة", page_icon="📊", layout="centered")

# التنسيقات البصرية CSS
st.markdown("""
<style>
.stApp { background-color: #F8FAFC; font-family: sans-serif; }
.main-header {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
    padding: 20px;
    border-radius: 12px;
    color: #FFF;
    text-align: center;
    margin-bottom: 20px;
}
.main-header h1 { color: #FFF !important; font-size: 24px !important; }
.main-header p { color: #94A3B8 !important; font-size: 13px !important; }
.stButton > button {
    background: #2563EB;
    color: #FFF !important;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 8px 16px;
}
</style>
""", unsafe_allow_html=True)

# إدارة حالة الجلسة (Session State)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        'المنتج': ['سماعة بلوتوث', 'شاحن جداري'],
        'الكمية': [15, 5],
        'تكلفة الشراء (ر.س)': [40.0, 15.0],
        'سعر البيع (ر.س)': [99.0, 45.0]
    })

if "subscribers_db" not in st.session_state:
    st.session_state.subscribers_db = {
        "K9X2-M7P4": datetime.date(2026, 8, 30),
        "H7T1-Z5W6": datetime.date(2026, 8, 30)
    }

MASTER_KEY = st.secrets.get("MASTER_KEY", "Abud")

# دالة إنشاء تقرير HTML للشحنة المجمعة
def generate_batch_html_report(selected_items_df, mc, sc, gr, iv):
    total_buy = selected_items_df['تكلفة الشراء (ر.س)'].sum()
    total_sell = selected_items_df['سعر البيع (ر.س)'].sum()
    
    va = (total_sell - (total_sell / 1.15)) if iv else 0.0
    ns = total_sell - va
    gf = ns * gr
    tc = total_buy + mc + sc + gf
    npf = ns - tc
    pm = (npf / ns * 100) if ns > 0 else 0.0

    items_rows = ""
    for _, row in selected_items_df.iterrows():
        items_rows += f"<tr><td>{row['المنتج']}</td><td>{row['تكلفة الشراء (ر.س)']:.2f}</td><td>{row['سعر البيع (ر.س)']:.2f}</td></tr>"

    return f"""<!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="UTF-8"><title>تقرير الشحنة المجمعة</title>
<style>
body{{font-family:sans-serif;padding:20px;background:#fff;color:#1e293b;}}
.card{{border:2px solid #e2e8f0;border-radius:10px;padding:20px;max-width:650px;margin:auto;}}
.h{{text-align:center;border-bottom:2px solid #1e3a8a;padding-bottom:10px;margin-bottom:20px;}}
.t{{width:100%;border-collapse:collapse;margin-bottom:15px;}}
.t td,.t th{{padding:8px;border-bottom:1px solid #e2e8f0;text-align:right;}}
.tr{{font-weight:bold;background:#f8fafc;}}
.th-header{{background:#1e3a8a;color:#fff;}}
</style></head>
<body><div class="card"><div class="h"><h2>4U2 للمحاسبة - تقرير شحنة مجمعة</h2><p>التاريخ: {datetime.date.today()}</p></div>
<h3>المنتجات في الشحنة:</h3>
<table class="t">
<tr class="th-header"><th>المنتج</th><th>التكلفة</th><th>سعر البيع</th></tr>
{items_rows}
</table>
<h3>ملخص الهندسة المالية للشحنة:</h3>
<table class="t">
<tr><td>إجمالي المبيعات</td><td>{total_sell:.2f} ر.س</td></tr>
<tr><td>إجمالي الشراء المباشر</td><td>{total_buy:.2f} ر.س</td></tr>
<tr><td>التسويق</td><td>{mc:.2f} ر.س</td></tr>
<tr><td>الشحن الكلي للشحنة</td><td>{sc:.2f} ر.س</td></tr>
<tr><td>عمولة البوابة</td><td>{gf:.2f} ر.س</td></tr>
<tr><td>الضريبة (15%)</td><td>{va:.2f} ر.س</td></tr>
<tr class="tr"><td>إجمالي جميع التكاليف</td><td>{tc:.2f} ر.س</td></tr>
<tr class="tr" style="color:#16a34a;"><td>صافي الربح الكلي</td><td>{npf:.2f} ر.س</td></tr>
<tr class="tr"><td>هامش الربح الكلي</td><td>{pm:.1f}%</td></tr>
</table></div></body></html>"""

# دالة إنشاء تقرير HTML لكامل المخزون
def generate_inventory_html_report(df):
    rows = ""
    total_qty = df['الكمية'].sum()
    total_cost_val = (df['الكمية'] * df['تكلفة الشراء (ر.س)']).sum()
    total_sell_val = (df['الكمية'] * df['سعر البيع (ر.س)']).sum()

    for _, row in df.iterrows():
        rows += f"<tr><td>{row['المنتج']}</td><td>{row['الكمية']}</td><td>{row['تكلفة الشراء (ر.س)']:.2f}</td><td>{row['سعر البيع (ر.س)']:.2f}</td></tr>"

    return f"""<!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="UTF-8"><title>تقرير كامل المخزون</title>
<style>
body{{font-family:sans-serif;padding:30px;background:#fff;color:#1e293b;}}
.card{{border:2px solid #e2e8f0;border-radius:10px;padding:20px;max-width:700px;margin:auto;}}
.h{{text-align:center;border-bottom:2px solid #1e3a8a;padding-bottom:10px;margin-bottom:20px;}}
.t{{width:100%;border-collapse:collapse;}}
.t td,.t th{{padding:10px;border-bottom:1px solid #e2e8f0;text-align:right;}}
.tr{{font-weight:bold;background:#f8fafc;}}
.th-header{{background:#0f172a;color:#fff;}}
</style></head>
<body><div class="card"><div class="h"><h2>4U2 للمحاسبة - تقرير المخزون الشامل</h2><p>التاريخ: {datetime.date.today()}</p></div>
<table class="t">
<tr class="th-header"><th>المنتج</th><th>الكمية</th><th>تكلفة الشراء</th><th>سعر البيع</th></tr>
{rows}
<tr class="tr"><td>الإجمالي الكلي</td><td>{total_qty}</td><td>قيمة الشراء: {total_cost_val:.2f}</td><td>قيمة البيع: {total_sell_val:.2f}</td></tr>
</table></div></body></html>"""

# دالة إنشاء أكواد عشوائية
def generate_random_code():
    c = string.ascii_uppercase + string.digits
    return f"{''.join(random.choices(c, k=4))}-{''.join(random.choices(c, k=4))}"

# --- القائمة الجانبية والتحقق من الاشتراكات ---
st.sidebar.markdown("### 🔐 بوابة الوصول الآمن")
uk = st.sidebar.text_input("مفتاح الاشتراك:", type="password")

if not uk:
    st.markdown('<div class="main-header"><h1>4U2 للمحاسبة</h1><p>نظام الهندسة المالية</p></div>', unsafe_allow_html=True)
    st.warning("🔒 أدخل مفتاح الاشتراك بالقائمة الجانبية.")
    st.stop()

im = (uk == MASTER_KEY)
db = st.session_state.subscribers_db
td = datetime.date.today()

if not im and uk not in db:
    st.error("❌ مفتاح خطأ.")
    st.stop()

if not im:
    if td > (db[uk] + datetime.timedelta(days=365)):
        st.error("❌ منتهي.")
        st.stop()

st.sidebar.markdown("---")
mo = ["🧮 حاسبة التكاليف الشاملة", "📦 إدارة المخزون"]
if im:
    mo.append("🛠️ لوحة المدير")

am = st.sidebar.selectbox("القسم:", mo)

# --- قسم حاسبة التكاليف المجمعة ---
if am == "🧮 حاسبة التكاليف الشاملة":
    st.markdown('<div class="main-header"><h1>حاسبة الشحنات المجمعة</h1></div>', unsafe_allow_html=True)
    
    if im:
        with st.expander("⚙️ توليد أكواد"):
            if st.button("✨ توليد كود جديد"):
                nc = generate_random_code()
                while nc in db:
                    nc = generate_random_code()
                db[nc] = td
                st.success(f"تم إنشاء كود: {nc}")

    inventory_df = st.session_state.inventory
    product_list = inventory_df['المنتج'].tolist()

    if not product_list:
        st.warning("⚠️ لا توجد منتجات في المخزون. يرجى إضافة منتج من قسم إدارة المخزون أولاً.")
        st.stop()

    # اختيار أكثر من منتج لشحنة واحدة
    selected_products = st.multiselect(
        "اختر المنتجات المضمونة في هذه الشحنة:", 
        options=product_list,
        default=[product_list[0]]
    )

    if not selected_products:
        st.info("💡 اختر منتجاً واحداً على الأقل لحساب الشحنة.")
        st.stop()

    # فلترة المنتجات المختارة
    selected_items_df = inventory_df[inventory_df['المنتج'].isin(selected_products)]

    # المبالغ التجميعية للمنتجات
    total_buy = selected_items_df['تكلفة الشراء (ر.س)'].sum()
    total_sell = selected_items_df['سعر البيع (ر.س)'].sum()

    st.markdown("---")
    st.write(f"📦 **عدد المنتجات في الشحنة:** {len(selected_products)} منتج/منتجات")
    
    col_a, col_b = st.columns(2)
    bp = col_a.number_input("مجموع تكلفة المنتجات (ر.س)", min_value=0.0, value=float(total_buy))
    tsp = col_b.number_input("مجموع سعر بيع المنتجات (ر.س)", min_value=0.0, value=float(total_sell))
    
    col_c, col_d = st.columns(2)
    mc = col_c.number_input("مصاريف التسويق للشحنة", min_value=0.0, value=15.0)
    sc = col_d.number_input("تكلفة الشحن الكلية (تكلفة شحنة واحدة)", min_value=0.0, value=10.0)
    
    gr = st.number_input("عمولة البوابة %", min_value=0.0, value=2.5) / 100
    iv = st.checkbox("احتساب الضريبة 15%", True)

    # الحسابات المجمعة
    va = (tsp - (tsp / 1.15)) if iv else 0.0
    ns = tsp - va
    gf = ns * gr
    tc = bp + mc + sc + gf
    npf = ns - tc
    pm = (npf / ns * 100) if ns > 0 else 0.0

    # تقييم هامش الربح والألوان
    if pm >= 30:
        margin_status = "ممتاز 🚀"
        delta_color = "normal"
    elif 15 <= pm < 30:
        margin_status = "متوسط ⚖️"
        delta_color = "off"
    else:
        margin_status = "منخفض ⚠️"
        delta_color = "inverse"

    # عرض النتائج في البطاقات
    c1, c2, c3 = st.columns(3)
    c1.metric("التكاليف الكلية (ر.س)", f"{tc:.2f}")
    c2.metric("صافي الربح (ر.س)", f"{npf:.2f}")
    c3.metric("هامش الربح", f"{pm:.1f}%", delta=margin_status, delta_color=delta_color)

    # تحميل تقرير الشحنة المجمعة
    hr = generate_batch_html_report(selected_items_df, mc, sc, gr, iv)
    st.download_button("📄 تحميل تقرير الشحنة المجمعة (HTML)", hr, f"4U2_Shipment_{datetime.date.today()}.html", "text/html", use_container_width=True)

# --- قسم إدارة المخزون ---
elif am == "📦 إدارة المخزون":
    st.markdown('<div class="main-header"><h1>إدارة المخزون</h1></div>', unsafe_allow_html=True)

    # زر طباعة تقرير كامل المخزون
    inv_report_html = generate_inventory_html_report(st.session_state.inventory)
    st.download_button(
        "🖨️ تحميل تقرير كامل المخزون (HTML)", 
        inv_report_html, 
        f"4U2_Full_Inventory_{datetime.date.today()}.html", 
        "text/html", 
        use_container_width=True
    )
    st.markdown("---")

    st.subheader("📋 جدول المخزون الحالي")
    st.info("💡 يمكنك التعديل المباشر على الجدول أو إضافة وحذف الصفوف بالأسفل:")
    
    edited_df = st.data_editor(
        st.session_state.inventory,
        num_rows="dynamic",
        use_container_width=True,
        key="inventory_editor"
    )
    st.session_state.inventory = edited_df

    # نموذج إضافة منتج جديد
    with st.expander("➕ إضافة منتج جديد بسرعة"):
        with st.form("add_product_form", clear_on_submit=True):
            new_name = st.text_input("اسم المنتج")
            col1, col2, col3 = st.columns(3)
            new_qty = col1.number_input("الكمية", min_value=1, step=1, value=10)
            new_buy = col2.number_input("تكلفة الشراء", min_value=0.0, value=10.0)
            new_sell = col3.number_input("سعر البيع", min_value=0.0, value=20.0)

            submitted = st.form_submit_button("إضافة للمخزون")
            if submitted:
                if new_name.strip() != "":
                    new_row = pd.DataFrame([{
                        'المنتج': new_name,
                        'الكمية': new_qty,
                        'تكلفة الشراء (ر.س)': new_buy,
                        'سعر البيع (ر.س)': new_sell
                    }])
                    st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                    st.success(f"تمت إضافة المنتج '{new_name}' بنجاح!")
                    st.rerun()
                else:
                    st.warning("يرجى إدخال اسم المنتج.")

# --- قسم لوحة المدير ---
elif am == "🛠️ لوحة المدير" and im:
    st.markdown('<div class="main-header"><h1>لوحة المدير</h1></div>', unsafe_allow_html=True)
    sl = [{"الكود": k, "تاريخ التفعيل": str(v), "الحالة": "فعال"} for k, v in db.items()]
    st.dataframe(pd.DataFrame(sl), use_container_width=True)
