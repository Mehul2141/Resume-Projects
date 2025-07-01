# import asyncio
# import asyncpg

# async def test_connection():
#     try:
#         conn = await asyncpg.connect(
#             user='postgres',
#             password='admin123',
#             database='Nextun',
#             host='localhost',
#         )
#         print("Connection successful!")
#         await conn.close()
#     except Exception as e:
#         print("Failed to connect:", e)

# asyncio.run(test_connection())

# # {
# #   "full_name": "Brijraj",
# #   "email": "Brij12@example.com",
# #   "mobile": "9313518787",
# #   "password": "XO",
# #   "role": "user"
# # }


# from core.database import Base
# from sqlalchemy import inspect
# import models  # must import this

# # Print all table mappings
# print(Base.metadata.tables.keys())
# print(inspect(models.AuditLog).relationships)



import pyotp
import time

# Your TOTP secret key (Base32 encoded, like from Google Authenticator)
SECRET_KEY = "O4MTDBHMNXCO7VZSXE2A7XW6LA"

# Initialize TOTP
totp = pyotp.TOTP(SECRET_KEY)

def get_remaining_time():
    return totp.interval - time.time() % totp.interval

def generate_totp():
    current_otp = totp.now()
    print(f"TOTP: {current_otp} (valid for {int(get_remaining_time())} seconds)")
    return current_otp

def start_totp_loop():
    while True:
        generate_totp()
        time_to_wait = get_remaining_time()
        time.sleep(time_to_wait + 1)  # Wait until the next TOTP becomes valid

if __name__ == "__main__":
    start_totp_loop()

# import bcrypt

# password = "password123"
# hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# print(hashed.decode())
