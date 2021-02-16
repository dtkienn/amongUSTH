import smtplib
import json
from email.mime.text import MIMEText


class gmail():
    def send(receiver, u_names, first_name):
        dat = json.load(open('login/mail.json'))
        email = dat['sender'][0]['email']
        password = dat['sender'][0]['password']
    
        from_addr = "AmongUSTH"

        msg = MIMEText('Hi {},\nYou can use this following info for future loggings in \n\n\tUsername: {} \n\tPassword: {}'.format(first_name, u_names, u_names))

        msg['From'] = from_addr + '<nhanlq.bi9178@st.usth.edu.vn>'
        msg['To'] = receiver
        msg['Subject'] = "Account Login Information"

        try:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, receiver, text)
            print('Email sent!')
            server.quit()
        except:
            print('cannot send email!')
