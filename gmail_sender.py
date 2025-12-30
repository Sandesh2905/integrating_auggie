#!/usr/bin/env python3
"""
Gmail Email Sender
A modular script for sending emails using Gmail's SMTP server with TLS encryption.
Supports both plain text and HTML email formats.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
import sys


class GmailSender:
    """
    A class to handle sending emails through Gmail's SMTP server.
    """
    
    # Gmail SMTP server configuration
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    def __init__(self, sender_email: str, password: str):
        """
        Initialize the Gmail sender with credentials.
        
        Args:
            sender_email: The Gmail address to send from
            password: The Gmail App Password (not regular password)
        """
        self.sender_email = sender_email
        self.password = password
    
    def send_email(
        self,
        recipient_email: str,
        subject: str,
        message_body: str,
        is_html: bool = False,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email using Gmail SMTP server.
        
        Args:
            recipient_email: Email address of the recipient
            subject: Email subject line
            message_body: The content of the email
            is_html: If True, send as HTML email; otherwise plain text
            cc: List of CC email addresses (optional)
            bcc: List of BCC email addresses (optional)
            attachments: List of file paths to attach (optional)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message container
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            
            # Add CC recipients if provided
            if cc:
                message['Cc'] = ', '.join(cc)
            
            # Determine message type (plain text or HTML)
            msg_type = 'html' if is_html else 'plain'
            message.attach(MIMEText(message_body, msg_type))
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    self._attach_file(message, file_path)
            
            # Prepare recipient list (To + CC + BCC)
            recipients = [recipient_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            # Connect to Gmail SMTP server
            print(f"Connecting to {self.SMTP_SERVER}:{self.SMTP_PORT}...")
            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            
            # Start TLS encryption
            print("Starting TLS encryption...")
            server.starttls()
            
            # Login to Gmail account
            print("Logging in...")
            server.login(self.sender_email, self.password)
            
            # Send email
            print("Sending email...")
            server.sendmail(self.sender_email, recipients, message.as_string())
            
            # Close connection
            server.quit()
            
            print(f"✓ Email sent successfully to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("✗ Authentication failed. Please check your email and App Password.")
            print("  Make sure you're using an App Password, not your regular Gmail password.")
            return False
            
        except smtplib.SMTPException as e:
            print(f"✗ SMTP error occurred: {str(e)}")
            return False
            
        except Exception as e:
            print(f"✗ An error occurred: {str(e)}")
            return False
    
    def _attach_file(self, message: MIMEMultipart, file_path: str) -> None:
        """
        Attach a file to the email message.
        
        Args:
            message: The MIMEMultipart message object
            file_path: Path to the file to attach
        """
        try:
            with open(file_path, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(file_path)}'
            )
            message.attach(part)
            print(f"  Attached: {os.path.basename(file_path)}")
            
        except FileNotFoundError:
            print(f"  Warning: File not found: {file_path}")
        except Exception as e:
            print(f"  Warning: Could not attach {file_path}: {str(e)}")


def send_simple_email(
    sender_email: str,
    password: str,
    recipient_email: str,
    subject: str,
    message_body: str,
    is_html: bool = False
) -> bool:
    """
    Convenience function to send a simple email without creating a GmailSender instance.

    Args:
        sender_email: The Gmail address to send from
        password: The Gmail App Password
        recipient_email: Email address of the recipient
        subject: Email subject line
        message_body: The content of the email
        is_html: If True, send as HTML email; otherwise plain text

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    sender = GmailSender(sender_email, password)
    return sender.send_email(recipient_email, subject, message_body, is_html)


def main():
    """
    Example usage of the GmailSender class.
    Demonstrates how to use environment variables for credentials.
    """
    # Get credentials from environment variables
    sender_email = os.getenv('GMAIL_SENDER')
    password = os.getenv('GMAIL_APP_PASSWORD')

    if not sender_email or not password:
        print("Error: Please set GMAIL_SENDER and GMAIL_APP_PASSWORD environment variables.")
        print("\nExample:")
        print("  export GMAIL_SENDER='your.email@gmail.com'")
        print("  export GMAIL_APP_PASSWORD='your-app-password'")
        sys.exit(1)

    # Example 1: Send a plain text email
    print("\n=== Example 1: Plain Text Email ===")
    sender = GmailSender(sender_email, password)
    sender.send_email(
        recipient_email="recipient@example.com",
        subject="Test Email - Plain Text",
        message_body="Hello! This is a test email sent using Python and Gmail SMTP."
    )

    # Example 2: Send an HTML email
    print("\n=== Example 2: HTML Email ===")
    html_content = """
    <html>
        <body>
            <h1 style="color: #4285f4;">Hello from Python!</h1>
            <p>This is an <strong>HTML email</strong> sent using Gmail SMTP.</p>
            <ul>
                <li>Feature 1: TLS Encryption</li>
                <li>Feature 2: HTML Support</li>
                <li>Feature 3: Error Handling</li>
            </ul>
        </body>
    </html>
    """
    sender.send_email(
        recipient_email="recipient@example.com",
        subject="Test Email - HTML",
        message_body=html_content,
        is_html=True
    )

    # Example 3: Send email with CC and BCC
    print("\n=== Example 3: Email with CC and BCC ===")
    sender.send_email(
        recipient_email="recipient@example.com",
        subject="Test Email - CC/BCC",
        message_body="This email has CC and BCC recipients.",
        cc=["cc1@example.com", "cc2@example.com"],
        bcc=["bcc@example.com"]
    )


if __name__ == "__main__":
    main()

