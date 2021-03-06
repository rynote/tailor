import smtplib
import threading
import pickle
import email
from .config import Config as pkConfig


class SenderThread(threading.Thread):
    def __init__(self, address, filename):
        threading.Thread.__init__(self)
        self.address = address
        self.filename = filename

    def run(self):
        sender = pkConfig.get('email', 'sender')
        subject = pkConfig.get('email', 'subject')
        auth_file = '/home/mjolnir/git/PURIKURA/secrets'

        msg = email.MIMEMultipart.MIMEMultipart('mixed')
        msg['subject'] = subject
        msg['from'] = sender
        msg['to'] = self.address

        body = email.mime.Text.MIMEText('Here\'s your photo!\n\nThank you!\n\n')
        msg.attach(body)

        file_msg = email.mime.base.MIMEBase('image', 'jpeg')
        file_msg.set_payload(open(self.filename).read())
        email.encoders.encode_base64(file_msg)
        file_msg.add_header(
            'Content-Disposition',
            'attachment;filname=photo.jpg')
        msg.attach(file_msg)

        with open(auth_file) as fh:
            auth = pickle.load(fh)
            auth = auth['smtp']

        with open('email.log', 'a') as fh:
            fh.write('{}\t{}\n'.format(self.address, self.filename))

        smtpout = smtplib.SMTP(auth['host'])
        smtpout.login(auth['username'], auth['password'])
        smtpout.sendmail(sender, [self.address], msg.as_string())
        smtpout.quit()
