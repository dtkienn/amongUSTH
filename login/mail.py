import smtplib
import json
from email.mime.text import MIMEText


class gmail():
    def send(receiver, u_names):
        dat = json.load(open('login/mail.json'))
        data = dat
        email = data['sender'][0]['email']
        password = data['sender'][0]['password']
    
        from_addr = "AmongUSTH"

        to_addr = receiver

        msg = MIMEText('Hi user,\nYou can use this following info for future loggings in \n\n\tUsername: ' + u_names + '\n\tPassword: ' + u_names)
        msg['From'] = from_addr + '<nhanlq.bi9178@st.usth.edu.vn>'
        msg['To'] = to_addr
        msg['Subject'] = "Account Login Information"

        try:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, to_addr, text)
            print('Email sent!')
            server.quit()
        except:
            print('Cannot send email!')
        
