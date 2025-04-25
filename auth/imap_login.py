import imaplib

def login_imap(host, port, username, password, ssl=True):
    if ssl:
        mail = imaplib.IMAP4_SSL(host, port)
    else:
        mail = imaplib.IMAP4(host, port)
    mail.login(username, password)
    return mail
