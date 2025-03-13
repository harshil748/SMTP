"""
Configuration settings for email verification system.
Store sensitive data here and add this file to .gitignore.
"""

# Email configuration
SENDER_EMAIL = "sgp.noreplydce@gmail.com"
SENDER_PASSWORD = "haub ylen jpof ypse"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Verification settings
CODE_LENGTH = 6
CODE_EXPIRATION_SECONDS = 300  # 5 minutes
MAX_VERIFICATION_ATTEMPTS = 3
MAX_RESEND_ATTEMPTS = 3
RESEND_COOLDOWN_SECONDS = 30
