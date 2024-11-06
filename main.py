import imaplib
import email
from email.header import decode_header

# Email login credentials
username = "turboxic@gmail.com"
password = "vvkbkaebxmzklpgp"  # Use an app-specific password if you have 2FA enabled

# Connect to the Gmail IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")

# Log in to the account
mail.login(username, password)

# Select the mailbox (INBOX is the default)
mail.select("inbox")

# Search for all emails
status, messages = mail.search(None, "ALL")

# Get the latest email ID
latest_email_id = messages[0].split()[-1]

# Fetch the email by ID
status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

# Parse the email content
for response_part in msg_data:
    if isinstance(response_part, tuple):
        msg = email.message_from_bytes(response_part[1])

        # Decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        
        # Print the subject
        print("Subject:", subject)

        # Get the email content
        if msg.is_multipart():
            for part in msg.walk():
                # Check if the part is text/html
                if part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True).decode()
                    print("\nHTML content:\n", html_body)
                    break
        else:
            if msg.get_content_type() == "text/html":
                html_body = msg.get_payload(decode=True).decode()
                print("\nHTML content:\n", html_body)

# Close the connection
mail.close()
mail.logout()
