import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import random
from datetime import datetime
import smtplib
from email.message import EmailMessage

# إعداد الصفحة
st.set_page_config(
    page_title="SmartDrive - تقرير القيادة الذكية",
    page_icon="🚗",
    layout="centered"
)

# توليد البيانات
def generate_metrics():
    return {
        "القيادة الذكية": random.randint(60, 100),
        "المنعطفات السلسة": random.randint(40, 100),
        "التوقفات الآمنة": random.randint(50, 100),
        "التركيز أثناء القيادة": random.randint(30, 100),
        "الالتزام بالسرعة": random.randint(70, 100),
        "الكفاءة في الوقود": random.randint(50, 100)
    }

# رسم الرسوم
def create_charts(metrics):
    fig1, ax1 = plt.subplots(figsize=(6,6))
    ax1.pie(metrics.values(), labels=metrics.keys(), autopct='%1.1f%%',
            colors=['#08F7FE', '#FE53BB', '#F5D300', '#00ff00', '#9d4edd', '#ff6d00'])
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(8,4))
    bars = ax2.bar(metrics.keys(), metrics.values(), color=['#08F7FE', '#FE53BB', '#F5D300', '#00ff00', '#9d4edd', '#ff6d00'])
    ax2.set_ylim(0, 110)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{height}%', ha='center', va='bottom')
    st.pyplot(fig2)

# إنشاء PDF
def generate_pdf(metrics, tip):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 15, "SmartDrive - تقرير القيادة الذكية", ln=True, align='C')
    pdf.set_font("Arial", '', 16)
    pdf.cell(0, 10, "النموذج الأولي - بيانات محاكاة عشوائية", ln=True, align='C')
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, "النتائج التفصيلية:", ln=True)
    pdf.set_font("Arial", '', 14)
    for key, value in metrics.items():
        pdf.cell(0, 10, f"{key}: {value}%", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "نصيحة القيادة الذكية:", ln=True)
    pdf.set_font("Arial", '', 14)
    pdf.multi_cell(0, 10, tip)
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    return pdf.output(dest="S").encode("latin1")

# إرسال البريد
def send_email(receiver_email, pdf_bytes):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"
    msg = EmailMessage()
    msg['Subject'] = "تقرير القيادة الذكية من SmartDrive"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("مرحبًا، تجد في المرفقات تقرير القيادة الذكية الخاص بك.\n\nتحيات SmartDrive 🚗")
    msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename="smartdrive_report.pdf")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

# واجهة المستخدم
st.title("🚗 SmartDrive - تقرير القيادة الذكية")
user_email = st.text_input("📧 أدخل بريدك الإلكتروني لاستلام التقرير:")
if st.button("🎯 توليد وإرسال التقرير"):
    if not user_email:
        st.warning("يرجى إدخال بريد إلكتروني صالح.")
    else:
        metrics = generate_metrics()
        weakest = min(metrics, key=metrics.get)
        tip = f"نصيحة: حاول تحسين مهارة {weakest} لتحقيق قيادة أفضل!"
        st.subheader("📊 نتائج التحليل")
        create_charts(metrics)
        st.subheader("📝 التفاصيل")
        for key, value in metrics.items():
            st.markdown(f"• *{key}*: {value}%")
        st.subheader("💡 نصيحة القيادة")
        st.info(tip)
        pdf_bytes = generate_pdf(metrics, tip)
        try:
            send_email(user_email, pdf_bytes)
            st.success(f"✅ تم إرسال التقرير إلى {user_email}")
        except Exception as e:
            st.error(f"❌ خطأ أثناء الإرسال: {e}")
        st.download_button(
            label="⬇ تحميل التقرير PDF",
            data=pdf_bytes,
            file_name="smartdrive_report.pdf",
            mime="application/pdf"
        )