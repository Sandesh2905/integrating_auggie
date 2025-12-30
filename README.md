# Gmail Email Sender with Python

A Python script for sending emails using Gmail's SMTP server with TLS encryption. Supports both plain text and HTML email formats, with proper error handling and security features.

## Features

- ✉️ Send plain text and HTML emails
- 🔒 TLS encryption for secure connections
- 📎 Support for file attachments
- 👥 CC and BCC recipient support
- ⚠️ Comprehensive error handling
- 🔑 Secure credential management using environment variables

## Prerequisites

- Python 3.6 or higher (uses standard library only)
- A Gmail account
- Gmail App Password (see setup instructions below)

## Gmail App Password Setup

Since May 2022, Google requires App Passwords for third-party applications to access Gmail via SMTP. Follow these steps:

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google," click on **2-Step Verification**
4. Click **Get Started** and follow the prompts to set up 2FA
5. You'll need to verify your identity with your phone number

### Step 2: Generate an App Password

1. After enabling 2FA, go back to **Security** settings
2. Under "Signing in to Google," click on **App passwords**
   - If you don't see this option, make sure 2FA is fully enabled
3. You may need to sign in again
4. At the bottom, select:
   - **Select app**: Choose "Mail" or "Other (Custom name)"
   - **Select device**: Choose your device or "Other (Custom name)"
5. Click **Generate**
6. Google will display a 16-character password (e.g., `abcd efgh ijkl mnop`)
7. **Copy this password** - you won't be able to see it again
8. Use this App Password in your script, NOT your regular Gmail password

### Important Notes

- App Passwords can only be created if 2FA is enabled
- Each App Password is unique and can be revoked independently
- Never share your App Password
- If compromised, you can revoke it and generate a new one

## Installation

No additional packages required! This script uses only Python's standard library:
- `smtplib` - SMTP protocol client
- `email` - Email message handling
- `os` - Environment variable access
- `typing` - Type hints

Simply download the `gmail_sender.py` file.

## Usage

### Method 1: Using Environment Variables (Recommended)

Set your credentials as environment variables:

```bash
# On Linux/Mac
export GMAIL_SENDER='your.email@gmail.com'
export GMAIL_APP_PASSWORD='your-16-char-app-password'

# On Windows (Command Prompt)
set GMAIL_SENDER=your.email@gmail.com
set GMAIL_APP_PASSWORD=your-16-char-app-password

# On Windows (PowerShell)
$env:GMAIL_SENDER='your.email@gmail.com'
$env:GMAIL_APP_PASSWORD='your-16-char-app-password'
```

Then run the example script:

```bash
python gmail_sender.py
```

### Method 2: Using the GmailSender Class

```python
from gmail_sender import GmailSender

# Initialize the sender
sender = GmailSender(
    sender_email='your.email@gmail.com',
    password='your-app-password'
)

# Send a plain text email
sender.send_email(
    recipient_email='recipient@example.com',
    subject='Hello from Python',
    message_body='This is a test email!'
)

# Send an HTML email
html_content = """
<html>
    <body>
        <h1>Hello!</h1>
        <p>This is an <strong>HTML</strong> email.</p>
    </body>
</html>
"""
sender.send_email(
    recipient_email='recipient@example.com',
    subject='HTML Email Test',
    message_body=html_content,
    is_html=True
)
```

### Method 3: Using the Convenience Function

```python
from gmail_sender import send_simple_email

success = send_simple_email(
    sender_email='your.email@gmail.com',
    password='your-app-password',
    recipient_email='recipient@example.com',
    subject='Quick Test',
    message_body='This is a simple email.'
)

if success:
    print("Email sent!")
else:
    print("Failed to send email.")
```

### Advanced Usage: CC, BCC, and Attachments

```python
from gmail_sender import GmailSender

sender = GmailSender('your.email@gmail.com', 'your-app-password')

sender.send_email(
    recipient_email='primary@example.com',
    subject='Project Update',
    message_body='Please see the attached report.',
    cc=['manager@example.com', 'team@example.com'],
    bcc=['archive@example.com'],
    attachments=['report.pdf', 'data.xlsx']
)
```

## Security Best Practices

### 1. Never Hardcode Credentials

❌ **DON'T DO THIS:**
```python
password = "abcd efgh ijkl mnop"  # Never hardcode passwords!
```

✅ **DO THIS INSTEAD:**
```python
import os
password = os.getenv('GMAIL_APP_PASSWORD')
```

### 2. Use Environment Variables

Create a `.env` file (and add it to `.gitignore`):

```bash
GMAIL_SENDER=your.email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

Load it using Python:

```python
import os

# Option 1: Manual loading
with open('.env') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# Option 2: Use python-dotenv package (requires: pip install python-dotenv)
from dotenv import load_dotenv
load_dotenv()
```

### 3. Use Configuration Files

Create a `config.ini` file (add to `.gitignore`):

```ini
[gmail]
sender = your.email@gmail.com
app_password = your-app-password
```

Load it:

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

sender_email = config['gmail']['sender']
password = config['gmail']['app_password']
```

### 4. Protect Your App Password

- ✅ Store in environment variables or secure config files
- ✅ Add config files to `.gitignore`
- ✅ Use different App Passwords for different applications
- ✅ Revoke App Passwords you no longer use
- ❌ Never commit credentials to version control
- ❌ Never share your App Password
- ❌ Never use your regular Gmail password

### 5. Rate Limiting

Gmail has sending limits:
- **Free Gmail accounts**: ~500 emails per day
- **Google Workspace**: ~2,000 emails per day

Implement delays between emails if sending in bulk:

```python
import time

for recipient in recipients:
    sender.send_email(recipient, subject, body)
    time.sleep(1)  # Wait 1 second between emails
```

## Troubleshooting

### Error: "Authentication failed"

**Possible causes:**
1. Using regular Gmail password instead of App Password
2. App Password entered incorrectly (remove spaces)
3. 2FA not enabled on your Google account
4. App Password was revoked

**Solutions:**
- Verify you're using an App Password, not your regular password
- Remove any spaces from the App Password (use `abcdefghijklmnop` not `abcd efgh ijkl mnop`)
- Check that 2FA is enabled: https://myaccount.google.com/security
- Generate a new App Password

### Error: "SMTPServerDisconnected"

**Possible causes:**
1. Network connectivity issues
2. Firewall blocking port 587
3. Gmail SMTP server temporarily unavailable

**Solutions:**
- Check your internet connection
- Verify firewall settings allow outbound connections on port 587
- Try again after a few minutes

### Error: "SMTPSenderRefused"

**Possible causes:**
1. Sender email doesn't match the authenticated account
2. Email format is invalid

**Solutions:**
- Ensure sender_email matches your Gmail account
- Verify email addresses are properly formatted

### Error: "SMTPRecipientsRefused"

**Possible causes:**
1. Recipient email address is invalid
2. Recipient's server is blocking emails

**Solutions:**
- Verify recipient email address is correct
- Check if recipient's email server is operational

### Error: "Connection timed out"

**Possible causes:**
1. Network issues
2. Corporate firewall blocking SMTP
3. ISP blocking port 587

**Solutions:**
- Try from a different network
- Contact your network administrator
- Some ISPs block port 587; try using a VPN

### Emails Going to Spam

**Solutions:**
- Avoid spam trigger words in subject/body
- Don't send too many emails too quickly
- Include an unsubscribe link for bulk emails
- Authenticate your domain with SPF/DKIM (for custom domains)
- Ask recipients to add you to their contacts

### "Less Secure App Access" Message

**Note:** Google deprecated "Less Secure App Access" in May 2022. You **must** use App Passwords now.

If you see this message:
1. Enable 2-Factor Authentication
2. Generate an App Password
3. Use the App Password in your script

## API Reference

### GmailSender Class

```python
GmailSender(sender_email: str, password: str)
```

**Methods:**

#### send_email()

```python
send_email(
    recipient_email: str,
    subject: str,
    message_body: str,
    is_html: bool = False,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    attachments: Optional[List[str]] = None
) -> bool
```

**Parameters:**
- `recipient_email` (str): Primary recipient's email address
- `subject` (str): Email subject line
- `message_body` (str): Email content (plain text or HTML)
- `is_html` (bool): Set to `True` for HTML emails, `False` for plain text
- `cc` (List[str], optional): List of CC recipients
- `bcc` (List[str], optional): List of BCC recipients
- `attachments` (List[str], optional): List of file paths to attach

**Returns:**
- `bool`: `True` if email sent successfully, `False` otherwise

### send_simple_email() Function

```python
send_simple_email(
    sender_email: str,
    password: str,
    recipient_email: str,
    subject: str,
    message_body: str,
    is_html: bool = False
) -> bool
```

Convenience function for sending simple emails without creating a GmailSender instance.

## Examples

See the `main()` function in `gmail_sender.py` for complete examples.

## License

This script is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues or pull requests for improvements.

## Disclaimer

This script is for educational purposes. Always comply with Gmail's Terms of Service and applicable laws when sending emails. Do not use for spam or unsolicited emails.

