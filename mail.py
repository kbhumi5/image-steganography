
import os
import ssl
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tkinter import messagebox


def send_email_with_image(receiver_email, key, image_path):
    """
    Sends an encrypted image or PDF attachment through Gmail.

    Gmail credentials are read from environment variables.
    The decryption key is NOT included in the email.
    Share the key separately through a trusted channel.
    """

    # Gmail credentials from environment variables
    sender_email = os.getenv("GMAIL_SENDER_EMAIL")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        messagebox.showerror(
            "Configuration Error",
            "Gmail credentials are not configured.\n\n"
            "Set GMAIL_SENDER_EMAIL and GMAIL_APP_PASSWORD "
            "as environment variables."
        )
        return

    if not os.path.exists(image_path):
        messagebox.showerror(
            "File Error",
            f"Encrypted file not found: {image_path}"
        )
        return

    subject = "Encrypted File - Steganography Security System"

    body = """
Hello,

Please find the encrypted file attached.

The decryption key is not included in this email.
Please obtain it separately through a trusted communication channel.

Regards,
Steganography Security System
"""

    try:
        # Create email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Attach encrypted image or PDF
        with open(image_path, "rb") as file:
            attachment = MIMEApplication(
                file.read(),
                Name=os.path.basename(image_path)
            )

            attachment["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(image_path)}"'
            )

            msg.attach(attachment)

        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Establish secure SMTP connection
        context = ssl.create_default_context()

        with smtplib.SMTP(
            smtp_server,
            smtp_port,
            timeout=30
        ) as server:

            server.ehlo()
            server.starttls(context=context)
            server.ehlo()

            server.login(sender_email, app_password)
            server.send_message(msg)

        messagebox.showinfo(
            "Success",
            f"Email sent successfully to {receiver_email}"
        )

    except smtplib.SMTPAuthenticationError:
        messagebox.showerror(
            "Authentication Error",
            "Gmail authentication failed.\n\n"
            "Check your Gmail credentials and App Password."
        )

    except smtplib.SMTPRecipientsRefused:
        messagebox.showerror(
            "Email Error",
            "The recipient email address was rejected."
        )

    except smtplib.SMTPConnectError:
        messagebox.showerror(
            "Network Error",
            "Unable to connect to Gmail SMTP. "
            "Check your internet connection."
        )

    except smtplib.SMTPException as error:
        messagebox.showerror(
            "SMTP Error",
            f"Email communication failed:\n{error}"
        )

    except (OSError, ValueError) as error:
        messagebox.showerror(
            "File or Configuration Error",
            str(error)
        )

    except Exception as error:
        messagebox.showerror(
            "Email Error",
            f"Failed to send email:\n{error}"
        )
