import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class Notifier:
    def send_email(self, products):
        sender_email = "your-email@example.com"
        receiver_email = "receiver-email@example.com"
        password = "your-password"
        
        subject = "Temu Monitor 新品报告"
        body = """
        <html>
          <head></head>
          <body>
            <h2>发现 {} 款新品</h2>
            <ul>
              {}
            </ul>
          </body>
        </html>
        """.format(len(products), ''.join(f"<li>{product['title']} - {product['price']}</li>" for product in products))
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        # 附加PDF报告
        with open('report.pdf', 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name='report.pdf')
            part['Content-Disposition'] = 'attachment; filename="report.pdf"'
            msg.attach(part)
        
        try:
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print("📧 邮件通知已发送")
        except Exception as e:
            print(f"🔥 发送邮件失败: {str(e)}")