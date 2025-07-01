import pyotp
def generate_totp(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()