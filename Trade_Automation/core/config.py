from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ANGELONE_API_KEY : str
    ANGELONE_REDIRECT_URI: str
    ANGELONE_CLIENTCODE: str
    ANGELONE_TOTP_SECRET: str
    ANGELONE_APP_PASSWORD: str
    
    class Config:
        env_file = ".env"

settings = Settings()
print(settings.ANGELONE_API_KEY)