import datetime
import random
import string
import pandas as pd
import streamlit as st
from weasyprint import HTML

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


# 3. دالة إنشاء تقرير الـ PDF العربي الاحترافي
def generate_arabic_pdf_report(
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
    html_content = f"""<!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 15mm 12mm; background-color: #F8FAFC; }}
            body {{ font-family: 'Amiri', 'Tajawal', sans-serif; color: #0F172A; margin: 0; padding: 0; }}
            .header {{ background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); color: #FFFFFF; padding: 24px; border-radius: 12px; text-align: center; margin-bottom: 24px; }}
            .header h1 {{ margin: 0 0 6px 0; font-size: 24pt; color: #FFFFFF; }}
            .header p {{ margin: 0; font-size: 11pt; color: #94A3B8; }}
            .product-card {{ background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px 20px; margin-bottom: 20px; }}
            .product-card h2 {{ margin: 0 0 10px 0; font-size: 14pt; color: #1E3A8A; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; }}
            .metrics-grid {{ display: table; width: 100%; margin-bottom: 20px; }}
            .metric-cell {{ display: table-cell; width: 33.33%; padding: 5px; }}
            .metric-box {{ background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 14px; text-align: center; }}
            .metric-title {{ font-size: 9pt; color: #64748B; margin-bottom: 4px; }}
            .metric-value {{ font-size: 14pt; font-weight: bold; color: #0F172A; }}
            .metric-value.profit {{ color: #166534; }}
            table.details-table {{ width: 100%; border-collapse: collapse; background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0; }}
            table.details-table th {{ background: #1E293B; color: #FFFFFF; text-align: right; padding: 10px 14px; font-size: 10pt; }}
            table.details-table td {{ padding: 10px 14px; border-bottom: 1px solid #F1F5F9; font-size: 10pt; }}
            table.details-table tr:nth-child(even) {{ background-color: #F8FAFC; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 9pt; color: #94A3B8; border-top: 1px solid #E2E8F0; padding-top: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>4U2 للمحاسبة</h1>
            <p>تقرير التحليل المالي وهندسة الربحية للمنتج</p>
        </div>
        <div class="product-card">
            <h2>تفاصيل المنتج الأساسية</h2>
            <p style="margin: 4px 0;"><strong>اسم المنتج / الخدمة:</strong> {product_name}</p>
            <p style="margin: 4px 0;"><strong>تاريخ التقرير:</strong> {datetime.date.today().strftime('%Y-%m-%d')}</p>
        </div>
        <div class="metrics-grid">
            <div class="metric-cell">
                <div class="metric-box">
                    <div class="metric-title">إجمالي التكاليف</div>
                    <div class="metric-value">{total_costs:.2f} ر.س</div>
                </div>
            </div>
            <div class="metric-cell">
                <div class="metric-box">
                    <div class="metric-title">صافي الربح الحقيقي</div>
                    <div class="metric-value profit">{net_profit:.2f} ر.س</div>
                </div>
            </div>
            <div class="metric-cell">
                <div class="metric-box">
                    <div class="metric-title">هامش الربح الصافي</div>
                    <div class="metric-value profit">{profit_margin:.1f}%</div>
                </div>
            </div>
        </div>
        <table class="details-table">
            <thead>
                <tr>
                    <th>بند التكلفة / الإيراد</th>
                    <th>المبلغ (ريال سعودي)</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>سعر البيع المستهدف للعميل</td><td>{target_sell_price:.2f} ر.س</td></tr>
                <tr><td>ضريبة القيمة المضافة (15%)</td><td>{vat_amount:.2f} ر.س</td></tr>
                <tr><td>تكلفة الشراء والتوريد</td><td>{buy_price:.2f} ر.س</td></tr>
                <tr><td>تكلفة التسويق والإعلانات للقطعة</td><td>{marketing_cost:.2f} ر.س</td></tr>
                <tr><td>تكلفة الشحن والتغليف</td><td>{shipping_cost:.2f} ر.س</td></tr>
                <tr><td>عمولة بوابة الدفع والمنصة</td><td>{gateway_fee:.2f} ر.س</td></tr>
            </tbody>
        </table>
        <div class="footer">
            تم التوليد تلقائياً عبر منصة 4U2 للمحاسبة | جميع الحقوق محفوظة © {datetime.date.today().year}
        </div>
    </body>
    </html>
    """
    return HTML(string=html_content).write_pdf()


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

# 6. القائمة الجانبية وتعديل الهيدر
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

        csv_data = df_subs.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 تصدير السجل كملف Excel / CSV",
            data=csv_data,
            file_name=f"4U2_Subscribers_{today}.csv",
            mime="text/csv",
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

# 10. زر تنزيل تقرير الـ PDF
pdf_bytes = generate_arabic_pdf_report(
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
    label="📄 تحميل التقرير المالي المنسق (PDF)",
    data=pdf_bytes,
    file_name=f"4U2_Financial_Report_{product_name}.pdf",
    mime="application/pdf",
    use_container_width=True,
)
