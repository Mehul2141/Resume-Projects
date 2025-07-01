from SmartApi.smartConnect import SmartConnect
from core.config import settings
from services.utils import generate_totp
from models import UserBroker

API_KEY = settings.ANGELONE_API_KEY

def get_client_code(refresh_token: str,jwt_token:str,feed_token:str):
    obj = SmartConnect(refresh_token=refresh_token,api_key=API_KEY,access_token=jwt_token)
    user_profile = obj.getProfile(refreshToken=refresh_token)
    print(user_profile)
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


async def get_user_angelone_client(broker: UserBroker) -> SmartConnect:
    """Returns a SmartConnect client for a given user using their broker credentials."""
    return SmartConnect(
        api_key=broker.api_key or settings.ANGELONE_API_KEY,
        access_token=broker.jwt_token,
        refresh_token=broker.refresh_token,
        client_code=broker.client_code,
    )


def execute_order(user_id:str,tradingsymbol:str,symboltoken:str,Exchange:str,
                   transaction_type:str,ordertype:str,quantity:str,
                   producttype:str,squareof:str,stoploss:str,durantion:str,order_object: SmartConnect
                ):
    
    order_status = order_object.placeOrder(tradingsymbol=tradingsymbol,symboltoken=symboltoken,Exchange=Exchange,
                                           transaction_type=transaction_type,ordertype=ordertype,quantity=quantity,
                                           producttype=producttype,squareof=squareof,durantion=durantion,stoploss=stoploss,
                                           ordertag=user_id)
    
    if order_status["message"] == "success":
        return "order placed successfully"
    
    




