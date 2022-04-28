'''
Below program is to read current processing consumed by your system and mail it.

'''

import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

class Mail: #mail class

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "testtomail007@gmail.com" #from which mail id you want to send the mail
        file = open('password.txt').readlines() #save your password in this file in your project
        self.password = str(file[0])

    def send(self, emails, subject, content):
        mail = MIMEMultipart('alternative')
        mail['Subject'] = subject
        mail['From'] = self.sender_mail
        mail['To'] = emails
        text_content = MIMEText(content.format(emails.split("@")[0]), 'plain') # this is the content policy need not have to worry abt this
        mail.attach(text_content)
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        service.sendmail(self.sender_mail,emails,mail.as_string()) #mail is being sent here


output = subprocess.check_output(['top', '-b', '-n 1']) # Explanation is given in below docstring
'''
-b  :Batch-mode operation
    Starts top in Batch mode, which could be useful for sending output
    from top to other programs or to a file.  In this mode, top will
    not accept input and runs until the iterations limit you've set
    with the `-n' command-line option or until killed.

-n  :Number-of-iterations limit as:  -n number
    Specifies the maximum number of iterations, or frames, top should
    produce before ending.
'''
final_output = str(output).replace("b'",'').split('\\n') # output we get will be in byte format so converting it to string and removing all the unwanted stuff

to_print = []
to_validate = []

#First 3 lines are important so have read it in one list
to_print.append(final_output[0])
to_print.append(final_output[1])
to_print.append(final_output[2])

# all the data other than first 3 lines are read in another list
for i in range(3,len(final_output)-1):#-1 is done here because in the end there was a extra block which i didnt need
    to_validate.append(final_output[i])

mail_body = '' # mail has to be in the form of string so will be concatenating all the values here
for val in to_print:
    mail_body+=val
    mail_body+='\n'
for val2 in range(0,10): # to check processing consumption i need just first 10 lines so range till 10
    mail_body+=to_validate[val2]
    mail_body+='\n'

print(mail_body)



mails = 'vishwanathsavai@gmail.com'
subject = 'Unix Health Check'
content = str(mail_body)

mail = Mail()
mail.send(mails, subject, content) # calling method send from object created from Mail class
