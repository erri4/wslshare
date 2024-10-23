import imaplib
import email
from email.header import decode_header


emil = 'reef.abramson@gamil.com'
pas = 'reef033850900'
imapserver = 'imap.gmail.com'

def check_new_emails():
    mail = imaplib.IMAP4_SSL(imapserver)

    try:
        mail.login(emil, pas)
        mail.select('inbox')
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        if email_ids:
            print(f"You have {len(email_ids)} new email(s).")
            for email_id in email_ids:
                _, msg = mail.fetch(email_id, '(RFC822)')
                for response_part in msg:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg['Subject'])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else 'utf-8')
                        print(f"New email subject: {subject}")
        else:
            print("No new emails.")

    except imaplib.IMAP4.error as e:
        print(f"An error occurred: {e}")

    finally:
        mail.logout()

if __name__ == "__main__":
    check_new_emails()
