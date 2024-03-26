# Install the required library using pip
# pip install pyotp

import pyotp

# Generate a secret key for the user
secret_key = pyotp.random_base32()

# Create a Google Authenticator object
totp = pyotp.TOTP(secret_key, interval=30)

# Get the current OTP for the user
otp = totp.now()

# Print the OTP
print("Your OTP is:", otp)

# Validate the OTP entered by the user
user_input_otp = input("Enter the OTP from Google Authenticator: ")
if totp.verify(user_input_otp):
    print("OTP is valid. User authenticated successfully.")
else:
    print("Invalid OTP. Authentication failed.")
