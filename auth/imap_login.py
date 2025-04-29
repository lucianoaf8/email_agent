import imaplib2

def login_imap(host, port, username, password, ssl=True):
    if ssl:
        mail = imaplib2.IMAP4_SSL(host, port)
    else:
        mail = imaplib2.IMAP4(host, port)
    mail.login(username, password)
    return mail
