import datetime
import random
import string
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(
    page_title="4U2 للمحاسبة | محرك التكاليف والربحية",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)

# 2. الهوية البصرية الرسمية (4U2 Accounting UI)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        padding: 24px;
        border-radius: 16px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
    }
    .main-header p {
        color: #94A3B8 !important;
        font-size: 14px !important;
        margin: 0 !important;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .stButton>button {
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%);
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1D4ED8 0%, #1E40AF 100%);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. دالة إنشاء تقرير HTML قابل للطباعة والحفظ كـ PDF للمنتجات
def generate_html_report(
    product_name,
    buy_price,
    target_sell_price,
    net_profit,
    profit_margin,
    total_costs,
    vat_amount,
    marketing_cost,
    shipping_cost,
    gateway_fee,
):
    html_content = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>تقرير مالي - {product_name}</title>
        <style>
            body {{ font-family: system-ui, -apple-system, sans-serif; padding: 40px; background-color: #fff; color: #1e293b; }}
            .card {{ border: 2px solid #e2e8f0; border-radius: 12px; padding: 30px; max-width: 650px; margin: auto; }}
            .header {{ text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 15px; margin-bottom: 25px; }}
            .header h2 {{ color: #1e3a8a; margin: 0; }}
            .table-data {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            .table-data td, .table-data th {{ padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right; }}
            .total-row {{ font-weight: bold; background-color: #f8fafc; font-size: 16px; }}
            .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #64748b; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>4U2 للمحاسبة - التقرير المالي</h2>
                <p>تاريخ التقرير: {datetime.date.today().strftime('%Y-%m-%d')}</p>
            </div>
            <h3>تفاصيل المنتج: {product_name}</h3>
            <table class="table-data">
                <tr><th>البيان</th><th>القيمة (ر.س)</th></tr>
                <tr><td>سعر البيع المستهدف</td><td>{target_sell_price:.2f}</td></tr>
                <tr><td>تكلفة الشراء / الإنتاج</td><td>{buy_price:.2f}</td></tr>
                <tr><td>تكلفة التسويق والإعلانات</td><td>{marketing_cost:.2f}</td></tr>
                <tr><td>تكلفة الشحن والتغليف</td><td>{shipping_cost:.2f}</td></tr>
                <tr><td>عمولة بوابة الدفع</td><td>{gateway_fee:.2f}</td></tr>
                <tr><td>ضريبة القيمة المضافة (15%)</td><td>{vat_amount:.2f}</td></tr>
                <tr class="total-row"><td>إجمالي التكاليف</td><td>{total_costs:.2f}</td></tr>
                <tr class="total-row" style="color: #16a34a;"><td>صافي الربح الحقيقي</td><td>{net_profit:.2f}</td></tr>
                <tr class="total-row"><td>هامش الربح الصافي</td><td>{profit_margin:.1f}%</td></tr>
            </table>
            <div class="footer">
                <p>تم استخراج هذا التقرير آلياً عبر نظام 4U2 الهندسة المالية</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


# دالة إنشاء تقرير HTML/PDF لسجل المشركين والأكواد
def generate_subscribers_html_report(sub_list, total_keys, active_keys):
    rows_html = ""
    for item in sub_list:
        status_color = "#16a34a" if "فعال" in item["الحالة"] else "#dc2626"
        rows_html += f"""
        <tr>
            <td style="font-family: monospace; font-weight: bold; font-size: 14px;">{item['الكود']}</td>
            <td>{item['تاريخ التفعيل']}</td>
            <td>{item['تاريخ الانتهاء']}</td>
            <td>{item['الأيام المتبقية']} يوم</td>
            <td style="color: {status_color}; font-weight: bold;">{item['الحالة']}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>سجل المشتركين والأكواد - 4U2</title>
        <style>
            body {{ font-family: system-ui, -apple-system, sans-serif; padding: 40px; background-color: #fff; color: #1e293b; }}
            .card {{ border: 2px solid #e2e8f0; border-radius: 12px; padding: 30px; max-width: 750px; margin: auto; }}
            .header {{ text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 15px; margin-bottom: 25px; }}
            .header h2 {{ color: #1e3a8a; margin: 0; }}
            .stats {{ display: flex; justify-content: space-around; background-color: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #e2e8f0; }}
            .table-data {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            .table-data td, .table-data th {{ padding: 10px 12px; border-bottom: 1px solid #e2e8f0; text-align: center; }}
            .table-data th {{ background-color: #0f172a; color: #ffffff; font-weight: 600; }}
            .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #64748b; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>4U2 للمحاسبة - سجل المشتركين والأكواد</h2>
                <p>تاريخ الاستخراج: {datetime.date.today().strftime('%Y-%m-%d')}</p>
            </div>
            
            <table style="width:100%; margin-bottom: 20px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; text-align: center;">
                <tr>
                    <td><div style="font-size: 13px; color: #64748b;">إجمالي الأكواد:</div><div style="font-size: 20px; font-weight: bold;">{total_keys}</div></td>
                    <td><div style="font-size: 13px; color: #64748b;">الأكواد الفعالة:</div><div style="font-size: 20px; font-weight: bold; color: #16a34a;">{active_keys}</div></td>
                </tr>
            </table>

            <table class="table-data">
                <thead>
                    <tr>
                        <th>الكود</th>
                        <th>تاريخ التفعيل</th>
                        <th>تاريخ الانتهاء</th>
                        <th>الأيام المتبقية</th>
                        <th>الحالة</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            
            <div class="footer">
                <p>تم استخراج هذا السجل آلياً عبر لوحة إدارة 4U2</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


# 4. دالة توليد الأكواد
def generate_random_code():
    chars = string.ascii_uppercase + string.digits
    p1 = "".join(random.choices(chars, k=4))
    p2 = "".join(random.choices(chars, k=4))
    return f"{p1}-{p2}"


# 5. ذاكرة الأكواد
if "subscribers_db" not in st.session_state:
    st.session_state.subscribers_db = {
        "K9X2-M7P4": datetime.date(2026, 8, 30),
        "B4L8-Q3V9": datetime.date(2026, 8, 30),
        "H7T1-Z5W6": datetime.date(2026, 8, 30),
        "G5N2-Y8T7": datetime.date(2026, 9, 1),
    }

MASTER_KEY = st.secrets.get("MASTER_KEY", "Abud")

# 6. القائمة الجانبية
st.sidebar.markdown("### 🔐 بوابة الوصول الآمن")
user_key = st.sidebar.text_input("مفتاح الاشتراك:", type="password")

if not user_key:
    st.markdown(
        """
        <div class="main-header">
            <h1>4U2 للمحاسبة</h1>
            <p>المنصة المتقدمة لهندسة التكاليف وحساب الربحية الحقيقية</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.warning("🔒 يرجى إدخال مفتاح الاشتراك الخاص بك في القائمة الجانبية للدخول.")
    st.stop()

is_master = user_key == MASTER_KEY
db = st.session_state.subscribers_db

if not is_master and user_key not in db:
    st.error("❌ مفتاح الاشتراك غير صحيح أو غير مفعّل.")
    st.stop()

today = datetime.date.today()

if not is_master:
    activation_date = db[user_key]
    expiration_date = activation_date + datetime.timedelta(days=365)
    if today > expiration_date:
        st.error(
            f"❌ انتهت صلاحية اشتراكك بتاريخ {expiration_date}. يرجى التواصل مع الإدارة للتجديد."
        )
        st.stop()
    days_left = (expiration_date - today).days

# 7. الواجهة الرئيسية
st.markdown(
    """
    <div class="main-header">
        <h1>4U2 للمحاسبة | نظام الهندسة المالية</h1>
        <p>حساب دقيق للتكاليف، الضرائب، التسويق، وصافي الهامش الربحي</p>
    </div>
""",
    unsafe_allow_html=True,
)

# لوحة الماستر (المالك)
if is_master:
    st.success("👑 تم تسجيل الدخول بصلاحية المالك (Master Admin)")
    with st.expander("⚙️ لوحة إدارة الاشتراك وتوليد الأكواد", expanded=False):
        st.subheader("⚡ إنشاء أكواد اشتراك جديدة")
        col_gen1, col_gen2 = st.columns([2, 3])
        with col_gen1:
            num_codes = st.number_input(
                "عدد الأكواد المطلوبة:", min_value=1, max_value=50, value=5
            )
        with col_gen2:
            st.write("")
            st.write("")
            if st.button("✨ توليد وسحب الأكواد فوراً", use_container_width=True):
                new_created = []
                for _ in range(num_codes):
                    code = generate_random_code()
                    while code in st.session_state.subscribers_db:
                        code = generate_random_code()
                    st.session_state.subscribers_db[code] = today
                    new_created.append(code)

                st.success(f"✅ تم توليد {num_codes} أكواد جديدة وتفعيلها!")
                st.code("\n".join(new_created), language="text")

        st.markdown("---")
        total_keys = len(db)
        sub_list = []
        active_keys = sum(
            1
            for act in db.values()
            if (act + datetime.timedelta(days=365) - today).days >= 0
        )

        for key, act_date in db.items():
            exp_date = act_date + datetime.timedelta(days=365)
            rem_days = (exp_date - today).days
            sub_list.append({
                "الكود": key,
                "تاريخ التفعيل": act_date.strftime("%Y-%m-%d"),
                "تاريخ الانتهاء": exp_date.strftime("%Y-%m-%d"),
                "الأيام المتبقية": max(rem_days, 0),
                "الحالة": "فعال ✅" if rem_days >= 0 else "منتهي ❌",
            })

        m1, m2 = st.columns(2)
        m1.metric("إجمالي الأكواد", f"{total_keys}")
        m2.metric("الأكواد الفعالة", f"{active_keys}")

        df_subs = pd.DataFrame(sub_list)
        st.dataframe(df_subs, use_container_width=True)

        subscribers_html_report = generate_subscribers_html_report(
            sub_list, total_keys, active_keys
        )

        st.download_button(
            label="📄 تصدير سجل المشتركين والأكواد (HTML / PDF)",
            data=subscribers_html_report,
            file_name=f"4U2_Subscribers_{today}.html",
            mime="text/html",
            use_container_width=True,
        )
else:
    st.info(f"🟢 مرحباً بك! اشتراكك فعال ومتبقي لك **{days_left} يوم**.")

# 8. مدخلات الحسابات
st.subheader("📥 مدخلات المنتج / الخدمة")
col_a, col_b = st.columns(2)
with col_a:
    product_name = st.text_input("اسم المنتج / الخدمة", value="سماعة لاسلكية")
    buy_price = st.number_input(
        "تكلفة التوريد / الإنتاج (ر.س)", value=50.0, step=5.0
    )
    marketing_cost = st.number_input(
        "تكلفة الإعلان المقدرة للقطعة (ر.س)", value=15.0, step=1.0
    )

with col_b:
    target_sell_price = st.number_input(
        "سعر البيع المستهدف للعميل (ر.س)", value=130.0, step=5.0
    )
    shipping_cost = st.number_input(
        "تكلفة الشحن والتغليف (ر.س)", value=10.0, step=1.0
    )
    gateway_rate = (
        st.number_input("عمولة بوابة الدفع/المنصة (%)", value=2.5, step=0.5) / 100
    )

include_vat = st.checkbox(
    "احتساب ضريبة القيمة المضافة (15%) ضمن سعر البيع", value=True
)

# 9. المخرجات والنتائج
vat_amount = (
    (target_sell_price - (target_sell_price / 1.15)) if include_vat else 0.0
)
net_sales = target_sell_price - vat_amount
gateway_fee = net_sales * gateway_rate
total_costs = buy_price + marketing_cost + shipping_cost + gateway_fee
net_profit = net_sales - total_costs
profit_margin = (net_profit / net_sales * 100) if net_sales > 0 else 0.0

st.markdown("---")
st.subheader("📊 نتائج التحليل المالي والربحية")

c1, c2, c3 = st.columns(3)
c1.metric("إجمالي التكاليف", f"{total_costs:.2f} ر.س")
c2.metric("صافي الربح الحقيقي", f"{net_profit:.2f} ر.س")
c3.metric("هامش الربح الصافي", f"{profit_margin:.1f}%")

if profit_margin >= 30:
    st.success("🟢 **هامش ربح ممتاز!** المنتج يمتلك ملاءة مالية عالية.")
elif profit_margin >= 15:
    st.info(
        "🟡 **هامش ربح متوسط.** يفضل مراقبة مصاريف الإعلانات لتحسين الربح."
    )
else:
    st.error(
        "🔴 **هامش ربح منخفض/مخاطرة!** التكاليف مرتفعة مقارنة بسعر البيع."
    )

# 10. زر تنزيل تقرير مالي منسق جاهز للطباعة والحفظ
html_report = generate_html_report(
    product_name,
    buy_price,
    target_sell_price,
    net_profit,
    profit_margin,
    total_costs,
    vat_amount,
    marketing_cost,
    shipping_cost,
    gateway_fee,
)

st.download_button(
    label="📄 تحميل التقرير المالي المنسق (HTML / PDF)",
    data=html_report,
    file_name=f"4U2_Report_{product_name}.html",
    mime="text/html",
    use_container_width=True,
)
