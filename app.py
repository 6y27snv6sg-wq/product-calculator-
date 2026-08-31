import streamlit as st
import pandas as pd
import datetime
import base64
from io import BytesIO

# مكتبات ReportLab الموثوقة لتوليد PDF بدون محركات خارجية
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="4U2 - نظام إدارة المحاسبة والمخزون",
    page_icon="📦",
    layout="wide"
)

# --- إدارة حالة الجلسة (Session State) للحفاظ على التنقل من الجوال ---
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "🧮 حاسبة التكاليف الشاملة"

if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"المنتج": "منتج A", "تكلفة الشراء (ر.س)": 50.0, "سعر البيع (ر.س)": 100.0},
        {"المنتج": "منتج B", "تكلفة الشراء (ر.س)": 30.0, "سعر البيع (ر.س)": 70.0}
    ])

# --- دالة إنشاء تقرير PDF المباشر ---
def generate_pdf_report(df, mc, sc, gr, iv):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )
    elements = []
    styles = getSampleStyleSheet()

    # أنماط النصوص
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading1'],
        alignment=1, # منتصف
        textColor=colors.HexColor('#1E3A8A'),
        fontSize=18,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        name='SubTitleStyle',
        parent=styles['Normal'],
        alignment=1,
        textColor=colors.HexColor('#64748B'),
        fontSize=10,
        spaceAfter=15
    )

    # 1. العنوان والترويسة
    elements.append(Paragraph("4U2 Accounting - Shipment Report", title_style))
    elements.append(Paragraph(f"Date: {datetime.date.today()}", subtitle_style))
    elements.append(Spacer(1, 10))

    # 2. جدول تفاصيل المنتجات
    table_data = [['Product', 'Buy Cost (SAR)', 'Sell Price (SAR)']]
    for _, row in df.iterrows():
        table_data.append([
            str(row['المنتج']),
            f"{row['تكلفة الشراء (ر.س)']:.2f}",
            f"{row['سعر البيع (ر.س)']:.2f}"
        ])

    items_table = Table(table_data, colWidths=[200, 130, 130])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1"))
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 15))

    # 3. الحسابات المالية
    total_buy = df['تكلفة الشراء (ر.س)'].sum()
    total_sell = df['سعر البيع (ر.س)'].sum()
    va = (total_sell - (total_sell / 1.15)) if iv else 0.0
    ns = total_sell - va
    gf = ns * gr
    tc = total_buy + mc + sc + gf
    npf = ns - tc
    pm = (npf / ns * 100) if ns > 0 else 0.0

    summary_data = [
        ['Metric', 'Amount (SAR)'],
        ['Total Sales', f"{total_sell:.2f}"],
        ['Total Costs', f"{tc:.2f}"],
        ['Net Profit', f"{npf:.2f}"],
        ['Profit Margin', f"{pm:.1f} %"]
    ]

    summary_table = Table(summary_data, colWidths=[230, 230])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TEXTCOLOR', (0,3), (1,3), colors.HexColor("#16A34A")) # لون صافي الربح أخضر
    ]))
    elements.append(summary_table)

    # بناء المستند
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# --- دالة تجهيز رابط التحميل المخصص للجوال (فتح في تبويب جديد) ---
def get_pdf_download_html(pdf_bytes, filename="Report.pdf"):
    b64 = base64.b64encode(pdf_bytes).decode('utf-8')
    return f'''
        <a href="data:application/pdf;base64,{b64}" target="_blank" download="{filename}" 
           style="display: block; width: 100%; padding: 12px; color: white; background-color: #1e3a8a; 
                  text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; 
                  font-size: 16px; margin-top: 10px;">
            📄 فتح / طباعة التقرير (PDF)
        </a>
    '''

# --- القائمة الجانبية والملاحة (محمية للجوال) ---
st.sidebar.title("4U2 Admin")
im = st.sidebar.checkbox("تفعيل وضع المدير", value=True)

mo = ["🧮 حاسبة التكاليف الشاملة", "📦 إدارة المخزون"]
if im:
    mo.append("🛠️ لوحة المدير")

# حفظ الصفحة المحفزة في session_state لتجنب الإغلاق على الجوال
current_index = mo.index(st.session_state.current_tab) if st.session_state.current_tab in mo else 0

am = st.sidebar.selectbox(
    "اختر القسم:",
    mo,
    index=current_index,
    key="navigation_select"
)
st.session_state.current_tab = am

# --- القسم الأول: حاسبة التكاليف ---
if st.session_state.current_tab == "🧮 حاسبة التكاليف الشاملة":
    st.header("🧮 حاسبة التكاليف والشحنات المجمعة")
    
    col1, col2 = st.columns(2)
    with col1:
        mc = st.number_input("تكاليف التسويق (ر.س):", min_value=0.0, value=50.0)
        sc = st.number_input("تكاليف الشحن (ر.س):", min_value=0.0, value=20.0)
    with col2:
        gr = st.number_input("نسبة البوابة/العمولة (%):", min_value=0.0, value=2.5) / 100
        iv = st.checkbox("خاضع لضريبة القيمة المضافة (15%)", value=True)

    st.subheader("إدارة عناصر الشحنة")
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
        st.subheader("تصدير التقرير")

        # إنشاء الـ PDF
        pdf_bytes = generate_pdf_report(selected_df, mc, sc, gr, iv)
        
        # زر التنزيل والفتح المخصص للجوال (يفتح التبويب الجديد ويمنع إعادة التعيين)
        st.markdown(
            get_pdf_download_html(pdf_bytes, f"4U2_Report_{datetime.date.today()}.pdf"),
            unsafe_allow_html=True
        )
    else:
        st.warning("يرجى اختيار منتج واحد على الأقل لتوليد التقرير.")

# --- القسم الثاني: إدارة المخزون ---
elif st.session_state.current_tab == "📦 إدارة المخزون":
    st.header("📦 إدارة المخزون")
    st.dataframe(st.session_state.inventory, use_container_width=True)

# --- القسم الثالث: لوحة المدير ---
elif st.session_state.current_tab == "🛠️ لوحة المدير":
    st.header("🛠️ لوحة التحكم والإعدادات")
    st.info("إعدادات النظام العامة وتعديل النسبة التلقائية.")
