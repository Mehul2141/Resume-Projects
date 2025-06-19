from SmartApi.smartConnect import SmartConnect
from core.config import settings
from services.utils import generate_totp


API_KEY = settings.ANGELONE_API_KEY

def get_client_code(jwt_token: str, refresh_token: str):
    obj = SmartConnect(access_token=jwt_token,refresh_token=refresh_token,api_key=API_KEY)
    print("getting user profile")
    user_profile = obj.getProfile(refreshToken=refresh_token)
    print(f"user profile: {user_profile}")
    client_code = user_profile["data"]["clientcode"]
    return client_code


def get_auth_tokens(client_code: str, password: str, topt_key: str):

    totp = generate_totp(topt_key)

    # Create SmartAPI object
    obj = SmartConnect(api_key=API_KEY)

    # Login
    login_data = obj.generateSession(client_code,password, totp)

    # Extract tokens
    jwt_token = login_data['data']['jwtToken']
    feed_token = login_data['data']['feedToken']
    refresh_token = login_data['data']['refreshToken']
    return jwt_token, feed_token, refresh_token