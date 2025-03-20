## Description

This project provides an implementation of an SMTP server/client in Python.

## Features

- Send and receive emails using the Simple Mail Transfer Protocol (SMTP).
- Supports authentication and secure connections (TLS/SSL).
- Easy to integrate and use in other Python applications.
- Generates and verifies email verification codes.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/harshil748/SMTP.git
    cd SMTP
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Here's an example of how to use the SMTP client to send a verification email:

1. Ensure you have a `config.py` file with the following variables:

    ```python
    SENDER_EMAIL = 'your_email@example.com'
    SENDER_PASSWORD = 'your_password'
    SMTP_SERVER = 'smtp.example.com'
    SMTP_PORT = 587
    CODE_EXPIRATION_SECONDS = 300
    MAX_VERIFICATION_ATTEMPTS = 5
    RESEND_COOLDOWN_SECONDS = 30
    ```

2. Run the `smtp.py` script:

    ```bash
    python smtp.py
    ```

3. Follow the prompts to enter your email address and verify with the code sent to your email.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or new features.
