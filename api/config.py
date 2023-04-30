from datetime import timedelta


class Config:
    SECRET_KEY = 'romawoman22842069'
    ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    REFRESH_TOKEN_EXPIRES = timedelta(days=30)
