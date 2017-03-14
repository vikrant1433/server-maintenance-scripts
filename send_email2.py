def send_email2(user, pwd, recipient, cc, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    CC = cc if type(cc) is list else [cc]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nCC: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), ", ".join(CC), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.cse.iitb.ac.in", 25)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO + CC, message)
        server.close()
        print('successfully sent the mail {0}'.format(message))
    except:
        print("failed to send mail {0}".format(message))


def send_email(to, cc, subject, body):
    send_email2('vikrant@cse.iitb.ac.in', '041291985aA@', to, cc, subject, body)
