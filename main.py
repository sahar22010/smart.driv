import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import random
from datetime import datetime
import smtplib
from email.message import EmailMessage
import traceback

# إعدادات الصفحة
st.set_page_config(
    page_title="SmartDrive - تقرير القيادة الذكية",
    page_icon="🚗",
    layout="centered"
)

# توليد البيانات العشوائية
def generate_metrics():
    return {
        "القيادة الذكية": random.randint(60, 100),
        "المنعطفات السلسة": random.randint(40, 100),
        "التوقفات الآمنة": random.randint(50, 100),
        "التركيز أثناء القيادة": random.randint(30, 100),
        "الالتزام بالسرعة": random.randint(70, 100),
        "الكفاءة في الوقود": random.randint(50, 100)
    }

# إنشاء الرسوم البيانية
def create_charts(metrics):
    try:
        # رسم بياني دائري
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.pie(metrics.values(), labels=metrics.keys(), autopct='%1.1f%%',
                colors=['#08F7FE', '#FE53BB', '#F5D300', '#00ff00', '#9d4edd', '#ff6d00'])
        st.pyplot(fig1)

        # رسم بياني عمودي
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        bars = ax2.bar(metrics.keys(), metrics.values(), 
                      color=['#08F7FE', '#FE53BB', '#F5D300', '#00ff00', '#9d4edd', '#ff6d00'])
        ax2.set_ylim(0, 110)
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height, f'{height}%', 
                    ha='center', va='bottom')
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"خطأ في الرسوم البيانية: {str(e)}")

# إنشاء ملف PDF
def generate_pdf(metrics, tip):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('Arial', '', 'arial.ttf', uni=True)  # دعم العربية
        
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(0, 15, "SmartDrive - تقرير القيادة الذكية", ln=True, align='C')
        
        pdf.set_font("Arial", '', 16)
        pdf.cell(0, 10, "النموذج الأولي - بيانات محاكاة", ln=True, align='C')
        pdf.ln(15)
        
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(0, 10, "النتائج:", ln=True)
        
        pdf.set_font("Arial", '', 14)
        for key, value in metrics.items():
            pdf.cell(0, 10, f"{key}: {value}%", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "النصيحة:", ln=True)
        pdf.set_font("Arial", '', 14)
        pdf.multi_cell(0, 10, tip)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 12)
        pdf.cell(0, 10, f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        
        return pdf.output(dest="S").encode("latin1")
    except Exception as e:
        st.error(f"خطأ في إنشاء PDF: {str(e)}")
        return None

# إرسال البريد الإلكتروني
def send_email(receiver_email, pdf_bytes):
    try:
        # ⚠ استبدل هذه القيم ببياناتك (استخدم "App Password" من جيميل)
        sender_email = "smartdrive.report@gmail.com"
        sender_password = "owjj okgp ljbl gztg"
        
        if not sender_email or sender_password == "your_app_password_here":
            raise ValueError("❗ لم تكتمل إعدادات البريد")
            
        msg = EmailMessage()
        msg['Subject'] = "تقرير القيادة الذكية"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content("""
        مرحبًا،
        تجد مرفقًا تقرير قيادتك الذكية.
        شكرًا لاستخدامك SmartDrive! 🚗
        """)
        
        msg.add_attachment(
            pdf_bytes,
            maintype='application',
            subtype='pdf',
            filename="smartdrive_report.pdf"
        )
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"❌ فشل الإرسال: {str(e)}")
        st.text(traceback.format_exc())
        return False

# الواجهة الرئيسية
def main():
    st.title("🚗 SmartDrive - تقرير القيادة الذكية")
    
    with st.form("report_form"):
        user_email = st.text_input("📧 أدخل بريدك الإلكتروني:")
        submitted = st.form_submit_button("🎯 إنشاء التقرير")
        
        if submitted:
            if not user_email:
                st.warning("⚠ الرجاء إدخال بريد إلكتروني صحيح")
            else:
                with st.spinner("جارٍ إنشاء التقرير..."):
                    try:
                        metrics = generate_metrics()
                        weakest = min(metrics, key=metrics.get)
                        tip = f"نصيحة: ركز على تحسين {weakest} ({metrics[weakest]}%)"
                        
                        st.subheader("📊 النتائج")
                        create_charts(metrics)
                        
                        st.subheader("💡 النصيحة")
                        st.success(tip)
                        
                        pdf_bytes = generate_pdf(metrics, tip)
                        if pdf_bytes:
                            st.download_button(
                                label="⬇ تحميل PDF",
                                data=pdf_bytes,
                                file_name="smartdrive_report.pdf",
                                mime="application/pdf"
                            )
                            
                            if send_email(user_email, pdf_bytes):
                                st.success(f"✅ تم الإرسال إلى: {user_email}")
                    except Exception as e:
                        st.error(f"حدث خطأ: {str(e)}")

if __name__== "__main__":
    main()
