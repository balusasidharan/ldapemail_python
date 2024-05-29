import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import ldap3
except ImportError:
    install('ldap3')
    import ldap3

try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
except ImportError:
    install('smtplib')
    install('email')
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

def get_email_from_ldap(ldap_server, ldap_user, ldap_password, search_base, search_filter):
    # Establish connection to the LDAP server
    server = ldap3.Server(ldap_server)
    conn = ldap3.Connection(server, ldap_user, ldap_password, auto_bind=True)
    
    # Search for the email ID
    conn.search(search_base, search_filter, attributes=['mail'])
    
    if conn.entries:
        email = conn.entries[0]['mail'].value
        return email
    else:
        return None

def send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, message):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add the message body
    msg.attach(MIMEText(message, 'plain'))
    
    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, to_email, msg.as_string())
    server.quit()

if __name__ == "__main__":
    # LDAP server details
    ldap_server = 'ldap://your_ldap_server'
    ldap_user = 'your_ldap_user_dn'
    ldap_password = 'your_ldap_password'
    search_base = 'ou=users,dc=example,dc=com'
    
    # Input LDAP ID
    ldap_id = input("Enter LDAP ID: ")
    
    # Construct the search filter
    search_filter = f'(uid={ldap_id})'
    
    # Get the email ID from LDAP
    email = get_email_from_ldap(ldap_server, ldap_user, ldap_password, search_base, search_filter)
    
    if email:
        print(f"Email ID retrieved: {email}")
        
        # SMTP server details
        smtp_server = 'smtp.your_email_provider.com'
        smtp_port = 587
        smtp_user = 'your_email@example.com'
        smtp_password = 'your_email_password'
        
        # Email details
        subject = 'Test Email'
        message = 'This is a test email sent from Python script.'
        
        # Send the email
        send_email(smtp_server, smtp_port, smtp_user, smtp_password, email, subject, message)
        print(f"Email sent to {email}")
    else:
        print("No email ID found for the given LDAP ID.")
