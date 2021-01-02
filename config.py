import os

ALPACA_API_URL = 'https://paper-api.alpaca.markets'
ALPACA_API_KEY = 'PKI36ROS1FUJVRPI1UK7'
ALPACA_SECRET_KEY = '8eQeOmvkoOBpsr1dWGvZryLGumP8uLn4PHzkcChU'

#Alpha Vantage
API_KEY_ALPHA = '2YZD8ZFQ58MAGZJ8'
API_KEY_ALPHA2= '3D5QFNFDYHGXSOBV'
#Polygon
API_KEY_POLY = 'hBd_TqcsNZpNZfiMbzLCppP4NOrZbNdN'

#IEX
API_URL_IEX = 'https://cloud.iexapis.com'
API_KEY_IEX = 'sk_ae6b8b3514c049b1a003c3d12adee4d8'
IEX_PUBLISHABLE_API ='pk_7782f3681b364de49ac86af6d82e5789'

EMAIL_ADDRESS = 'tradingnotifications.1@gmail.com'
EMAIL_PASSWORD = 'Shared123#'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_SMS = '7738383968@msg.fi.google.com'


#SIMFIN
SIMFIN_DIR = os.path.join("simfin_database")
API_KEY_SIMFIN = "vHOwuZOEK3CR3tLhv4wHjVohTK9Brv2h"



# Database
DB_USER="postgres"
DB_PASSWORD="Sunny@123"
DB_HOST="localhost"
DB_NAME="tradingapp"
DB_URL=f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


