import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import threading

smtp_lock = threading.Lock()

def send_mail_with_attachment(to, subject, body, attachment_data, attachment_name, to_mail, program='sa', imgpath=None, tree_attachment=None):
    assert isinstance(to, list)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'rkkapil2004@gmail.com'
    smtp_password = 'vajxivztzdjqltvs'

    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = to_mail

        msg.attach(MIMEText(body, 'html'))

        if program == 'msa':
            part1 = MIMEApplication(attachment_data, Name=attachment_name, _subtype='fasta')
            part1['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
            msg.attach(part1)
            if tree_attachment is not None:
                part2 = MIMEApplication(tree_attachment, Name='tree.txt', _subtype='txt')
                part2['Content-Disposition'] = 'attachment; filename="tree.txt"'
                msg.attach(part2)
        else:
            part1 = MIMEApplication(attachment_data, Name=attachment_name, _subtype='txt')
            part1['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
            msg.attach(part1)

        if imgpath:
            img = MIMEImage(open(imgpath, 'rb').read(), _subtype="png")
            img.add_header('Content-Disposition', 'attachment', filename='f{program}_result.png')
            msg.attach(img)

        # Establish a connection explicitly before sending the email
        with smtp_lock:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                print("Sending email...")
                server.starttls()
                print("starttls called, Logging in...")
                server.login(smtp_username, smtp_password)
                print("login called, sending mail...")
                # Now,  the starttls method is guaranteed to be called before login and sendmail
                server.sendmail(smtp_username, to, msg.as_string())
                print("sendmail called, quitting...")
                server.quit()
    except Exception as e:
        print(f"Error {e}")
        raise e

# unused 
if __name__ == '__main__':
    to = ['rkkapil2004@gmail.com']
    subject = 'Test Subject'
    body = '<p>This is a test email</p>'
    attachment_data = b'This is a test attachment'
    attachment_name = 'test_attachment.txt'
    to_mail = 'rkkapil2004@gmail.com'

    send_mail_with_attachment(to, subject, body, attachment_data, attachment_name, to_mail)

