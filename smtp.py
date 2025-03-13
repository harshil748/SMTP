import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import sys
from config import (
    SENDER_EMAIL,
    SENDER_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
    CODE_EXPIRATION_SECONDS,
    MAX_VERIFICATION_ATTEMPTS,
    RESEND_COOLDOWN_SECONDS,
)


def generate_verification_code():
    return "".join(random.choices(string.digits, k=6))


def send_verification_email(receiver_email, code):
    subject = "Your Two Factor Verification Code"
    body = f"Your verification code is: {code}"

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email failed to send: {e}")
        return False


def is_code_expired(creation_time):
    """Check if the verification code has expired."""
    current_time = time.time()
    return (current_time - creation_time) > CODE_EXPIRATION_SECONDS


def main():
    print("Two-Factor Email Verification System")

    # Get email address from user
    email = input("\nEnter your email address: ")
    if not email:
        print("Error: Email address cannot be empty!")
        return

    print("\nSending verification code...")

    # Generate and send verification code
    verification_code = generate_verification_code()
    success = send_verification_email(email, verification_code)
    code_creation_time = time.time()
    last_sent_time = code_creation_time

    if not success:
        print("Error: Failed to send email. Please try again.")
        return

    print("Success: Verification code sent to your email!")
    print(f"This code will expire in {CODE_EXPIRATION_SECONDS//60} minutes.")

    verified = False
    verification_attempts = 0
    resend_attempts = 0

    while not verified:
        # Check if maximum verification attempts reached
        if verification_attempts >= MAX_VERIFICATION_ATTEMPTS:
            print(
                f"\nError: Maximum verification attempts ({MAX_VERIFICATION_ATTEMPTS}) reached. Please try again later."
            )
            return

        # Check if code has expired
        if is_code_expired(code_creation_time):
            print("\nYour verification code has expired. Please request a new one.")
            user_input = "r"  # Auto-trigger resend
        else:
            # Get verification code from user
            remaining_time = int(
                CODE_EXPIRATION_SECONDS - (time.time() - code_creation_time)
            )
            print(
                f"\nPlease check your email for the verification code (expires in {remaining_time} seconds)."
            )
            print(
                "Enter the verification code or 'r' to resend (can resend after 30 seconds):"
            )
            user_input = input("> ")

        if user_input.lower() == "r":
            current_time = time.time()
            time_elapsed = current_time - last_sent_time

            if time_elapsed < RESEND_COOLDOWN_SECONDS:
                print(
                    f"Please wait {int(RESEND_COOLDOWN_SECONDS - time_elapsed)} more seconds before requesting a new code."
                )
                continue

            # Check if maximum resend attempts reached
            if resend_attempts >= MAX_VERIFICATION_ATTEMPTS:
                print(
                    f"Error: Maximum resend attempts ({MAX_VERIFICATION_ATTEMPTS}) reached. Please try again later."
                )
                return

            resend_attempts += 1
            print(
                f"\nResending verification code... (Attempt {resend_attempts}/{MAX_VERIFICATION_ATTEMPTS})"
            )
            verification_code = generate_verification_code()
            success = send_verification_email(email, verification_code)
            code_creation_time = time.time()
            last_sent_time = code_creation_time

            if success:
                print("Success: New verification code sent to your email!")
                print(
                    f"This code will expire in {CODE_EXPIRATION_SECONDS//60} minutes."
                )
            else:
                print("Error: Failed to send email. Please try again.")
        else:
            verification_attempts += 1

            # Verify the code
            if is_code_expired(code_creation_time):
                print(
                    "\nError: Your verification code has expired. Please request a new one."
                )
            elif user_input == verification_code:
                print("\nSuccess: Email verified successfully!")
                verified = True
            else:
                print(
                    f"\nError: Invalid verification code. ({verification_attempts}/{MAX_VERIFICATION_ATTEMPTS} attempts)"
                )
                print("Try again or request a new code.")


if __name__ == "__main__":
    main()
