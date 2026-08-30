import datetime
import pandas as pd
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="حاسبة تكاليف المنتجات", page_icon="📱", layout="centered"
)

# 2. قاعدة بيانات المشتركين وتاريخ التفعيل
SUBSCRIBERS_DATABASE = {
    "PRO-2026": datetime.date(2026, 8, 30),
    "VIP-9999": datetime.date(2026, 8, 30),
}

st.sidebar.title("🔐 بوابة المشتركين")
user_key = st.sidebar.text_input("أدخل مفتاح الاشتراك الخاص بك:", type="password")

if not user_key:
    st.title("📱 حاسبة تكاليف وهامش ربح المنتجات")
    st.warning(
        "⚠️ يرجى إدخال مفتاح الاشتراك في القائمة الجانبية للوصول إلى الخدمة."
    )
    st.stop()

if user_key not in SUBSCRIBERS_DATABASE:
    st.error("❌ مفتاح الاشتراك غير صحيح.")
    st.stop()

# فحص تاريخ انتهاء الاشتراك تلقائياً (بعد 365 يوم)
activation_date = SUBSCRIBERS_DATABASE[user_key]
expiration_date = activation_date + datetime.timedelta(days=365)
today = datetime.date.today()

if today > expiration_date:
    st.error(
        f"❌ انتهت صلاحية اشتراكك بتاريخ {expiration_date}. يرجى التواصل مع الدعم للتجديد."
    )
    st.stop()

days_left = (expiration_date - today).days

# 3. الواجهة الرئيسية للمشترك
st.title("📱 حاسبة تكاليف المنتجات والربحية")
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

# تجهيز بيانات بطاقة Excel بتنسيق HTML متوافق مع Excel مباشرة
html_card = f"""
<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40">
<head><meta charset="utf-8"/></head>
<body>
<table border="1" style="border-collapse:collapse; font-family:Calibri; text-align:center;">
    <tr style="background-color:#1F4E78; color:white; font-size:16px; font-weight:bold;">
        <td colspan="2">بطاقة منتج: {product_name}</td>
    </tr>
    <tr><td><b>رمز المنتج (SKU)</b></td><td>{sku}</td></tr>
    <tr><td><b>اسم المنتج</b></td><td>{product_name}</td></tr>
    <tr><td><b>تكلفة الشراء (ر.س)</b></td><td>{buy_price:.2f}</td></tr>
    <tr><td><b>تكلفة الشحن والجمارك (ر.س)</b></td><td>{shipping_price:.2f}</td></tr>
    <tr><td><b>تكلفة التسويق للوحدة (ر.س)</b></td><td>{marketing_cost:.2f}</td></tr>
    <tr><td><b>نسبة عمولة البوابة</b></td><td>{gateway_commission_pct}%</td></tr>
    <tr><td><b>عمولة البوابة المقدرة (ر.س)</b></td><td>{gateway_fee:.2f}</td></tr>
    <tr><td><b>نسبة ضريبة القيمة المضافة</b></td><td>{vat_pct}%</td></tr>
    <tr><td><b>قيمة الضريبة (ر.س)</b></td><td>{vat_amount:.2f}</td></tr>
    <tr style="font-weight:bold;"><td>إجمالي تكلفة الوحدة (ر.س)</td><td>{total_unit_cost:.2f}</td></tr>
    <tr><td><b>سعر البيع المستهدف (ر.س)</b></td><td>{target_sell_price:.2f}</td></tr>
    <tr style="background-color:{'#C6EFCE' if gross_profit > 0 else '#FFC7CE'}; color:{'#006100' if gross_profit > 0 else '#9C0006'}; font-weight:bold;">
        <td>هامش الربح الإجمالي (ر.س)</td><td>{gross_profit:.2f}</td>
    </tr>
    <tr style="background-color:{'#C6EFCE' if gross_profit > 0 else '#FFC7CE'}; color:{'#006100' if gross_profit > 0 else '#9C0006'}; font-weight:bold;">
        <td>نسبة هامش الربح</td><td>{profit_margin_pct:.1f}%</td>
    </tr>
</table>
</body>
</html>
"""

st.download_button(
    label="📥 تحميل بطاقة المنتج (Excel)",
    data=html_card.encode("utf-8"),
    file_name=f"Product_Card_{sku}.xls",
    mime="application/vnd.ms-excel",
    use_container_width=True,
)
