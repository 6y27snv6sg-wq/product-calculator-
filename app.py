import datetime
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة والاسم الجديد
st.set_page_config(
    page_title="حاسبة التكاليف والربحية", page_icon="📊", layout="centered"
)

# 2. قاعدة بيانات كود الماستر والاشتراكات
MASTER_KEY = "Abud"

SUBSCRIBERS_DATABASE = {
    "PRO-1001": datetime.date(2026, 8, 30),
    "PRO-1002": datetime.date(2026, 8, 30),
    "PRO-1003": datetime.date(2026, 8, 30),
    "PRO-1004": datetime.date(2026, 8, 30),
    "PRO-1005": datetime.date(2026, 8, 30),
    "PRO-1006": datetime.date(2026, 8, 30),
    "PRO-1007": datetime.date(2026, 8, 30),
    "PRO-1008": datetime.date(2026, 8, 30),
    "PRO-1009": datetime.date(2026, 8, 30),
    "PRO-1010": datetime.date(2026, 8, 30),
    "PRO-1011": datetime.date(2026, 8, 30),
    "PRO-1012": datetime.date(2026, 8, 30),
    "PRO-1013": datetime.date(2026, 8, 30),
    "PRO-1014": datetime.date(2026, 8, 30),
    "PRO-1015": datetime.date(2026, 8, 30),
    "PRO-1016": datetime.date(2026, 8, 30),
    "PRO-1017": datetime.date(2026, 8, 30),
    "PRO-1018": datetime.date(2026, 8, 30),
    "PRO-1019": datetime.date(2026, 8, 30),
    "PRO-1020": datetime.date(2026, 8, 30),
    "PRO-1021": datetime.date(2026, 8, 30),
    "PRO-1022": datetime.date(2026, 8, 30),
    "PRO-1023": datetime.date(2026, 8, 30),
    "PRO-1024": datetime.date(2026, 8, 30),
    "PRO-1025": datetime.date(2026, 8, 30),
    "PRO-1026": datetime.date(2026, 8, 30),
    "PRO-1027": datetime.date(2026, 8, 30),
    "PRO-1028": datetime.date(2026, 8, 30),
    "PRO-1029": datetime.date(2026, 8, 30),
    "PRO-1030": datetime.date(2026, 8, 30),
}

st.sidebar.title("🔐 بوابة المشتركين")
user_key = st.sidebar.text_input("أدخل مفتاح الاشتراك الخاص بك:", type="password")

if not user_key:
    st.title("📊 حاسبة التكاليف والربحية")
    st.warning(
        "⚠️ يرجى إدخال مفتاح الاشتراك في القائمة الجانبية للوصول إلى الخدمة."
    )
    st.stop()

is_master = user_key == MASTER_KEY

if not is_master and user_key not in SUBSCRIBERS_DATABASE:
    st.error("❌ مفتاح الاشتراك غير صحيح.")
    st.stop()

if not is_master:
    activation_date = SUBSCRIBERS_DATABASE[user_key]
    expiration_date = activation_date + datetime.timedelta(days=365)
    today = datetime.date.today()

    if today > expiration_date:
        st.error(
            f"❌ انتهت صلاحية اشتراكك بتاريخ {expiration_date}. يرجى التواصل مع الدعم للتجديد."
        )
        st.stop()

    days_left = (expiration_date - today).days

# 3. الواجهة الرئيسية بالاسم الجديد
st.title("📊 حاسبة التكاليف والربحية")

if is_master:
    st.success("👑 أهلاً بك! تم تسجيل الدخول بواسطة كود الماستر (اشتراك مفتوح مدى الحياة).")
else:
    st.success(f"مرحباً بك! اشتراكك فعال (متبقي {days_left} يوم على الانتهاء).")

st.markdown("---")

st.subheader("📦 1. بيانات المنتج والتكاليف المباشرة")
col1, col2 = st.columns(2)
with col1:
    sku = st.text_input("رمز المنتج (SKU)", value="SKU-001")
    buy_price = st.number_input("تكلفة الشراء (ر.س)", value=45.0, step=1.0)
with col2:
    product_name = st.text_input("اسم المنتج", value="سماعات لاسلكية")
    shipping_price = st.number_input(
        "تكلفة الشحن والجمارك (ر.س)", value=5.0, step=1.0
    )

marketing_cost = st.number_input(
    "تكلفة التسويق للوحدة (ر.س)", value=15.0, step=1.0
)

st.subheader("🏛️ 2. الرسوم والضرائب والمبيعات")
col3, col4, col5 = st.columns(3)
with col3:
    gateway_commission_pct = st.number_input(
        "عمولة البوابة (%)", value=2.5, step=0.1
    )
with col4:
    vat_pct = st.number_input("الضريبة (%)", value=15.0, step=1.0)
with col5:
    target_sell_price = st.number_input(
        "سعر البيع المستهدف (ر.س)", value=120.0, step=5.0
    )

# الحسابات
vat_amount = target_sell_price * (vat_pct / 100.0)
gateway_fee = target_sell_price * (gateway_commission_pct / 100.0)
total_unit_cost = (
    buy_price + shipping_price + marketing_cost + gateway_fee + vat_amount
)
gross_profit = target_sell_price - total_unit_cost
profit_margin_pct = (
    (gross_profit / target_sell_price * 100) if target_sell_price > 0 else 0
)

st.markdown("---")
st.subheader("📊 ملخص البطاقة المالية للمنتج")

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("إجمالي التكلفة الشاملة", f"{total_unit_cost:.2f} ر.س")
kpi2.metric(
    "صافي هامش الربح",
    f"{gross_profit:.2f} ر.س",
    delta=f"{profit_margin_pct:.1f}%",
)
kpi3.metric("سعر البيع المستهدف", f"{target_sell_price:.2f} ر.س")

# تجهيز ملف HTML قادِر على الطباعة المباشرة وحفظه كـ PDF تلقائياً
printable_html = f"""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="utf-8">
<title>بطاقة تقرير - {product_name}</title>
<style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; direction: rtl; text-align: right; }}
    .card {{ border: 2px solid #1F4E78; border-radius: 10px; padding: 20px; max-width: 600px; margin: 0 auto; background-color: #fcfcfc; }}
    .header {{ background-color: #1F4E78; color: white; padding: 15px; border-radius: 8px; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 20px; }}
    .row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #ddd; font-size: 16px; }}
    .row.total {{ font-weight: bold; font-size: 18px; border-top: 2px solid #1F4E78; border-bottom: none; padding-top: 12px; }}
    .profit {{ background-color: {'#C6EFCE' if gross_profit > 0 else '#FFC7CE'}; color: {'#006100' if gross_profit > 0 else '#9C0006'}; padding: 10px; border-radius: 6px; font-weight: bold; margin-top: 15px; text-align: center; }}
    @media print {{
        .no-print {{ display: none; }}
        body {{ padding: 0; }}
        .card {{ border: none; max-width: 100%; }}
    }}
</style>
</head>
<body>
<div class="card">
    <div class="header">بطاقة تقرير: {product_name}</div>
    <div class="row"><span>رمز المنتج (SKU):</span><span><b>{sku}</b></span></div>
    <div class="row"><span>تكلفة الشراء:</span><span>{buy_price:.2f} ر.س</span></div>
    <div class="row"><span>تكلفة الشحن والجمارك:</span><span>{shipping_price:.2f} ر.س</span></div>
    <div class="row"><span>تكلفة التسويق للوحدة:</span><span>{marketing_cost:.2f} ر.س</span></div>
    <div class="row"><span>عمولة البوابة ({gateway_commission_pct}%):</span><span>{gateway_fee:.2f} ر.س</span></div>
    <div class="row"><span>ضريبة القيمة المضافة ({vat_pct}%):</span><span>{vat_amount:.2f} ر.س</span></div>
    <div class="row total"><span>إجمالي تكلفة الوحدة:</span><span>{total_unit_cost:.2f} ر.س</span></div>
    <div class="row total"><span>سعر البيع المستهدف:</span><span>{target_sell_price:.2f} ر.س</span></div>
    <div class="profit">
        صافي هامش الربح: {gross_profit:.2f} ر.س ({profit_margin_pct:.1f}%)
    </div>
</div>
<br>
<div style="text-align: center;" class="no-print">
    <button onclick="window.print()" style="padding: 12px 25px; background-color: #1F4E78; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer;">🖨️ طباعة التقرير / حفظ كـ PDF</button>
</div>
</body>
</html>
"""

st.markdown("---")
st.download_button(
    label="🖨️ تحميل التقرير للطباعة المباشرة (PDF/صفحة)",
    data=printable_html.encode("utf-8"),
    file_name=f"Report_{sku}.html",
    mime="text/html",
    use_container_width=True,
)
