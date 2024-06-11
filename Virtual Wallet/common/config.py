import os

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_NAME = os.getenv('DB_NAME', 'virtual_wallet')

# DB_USER = 'root'
# DB_PASSWORD = 'your_password'
# DB_HOST = 'localhost'
# DB_PORT = 3306
# DB_NAME = 'virtual_wallet'


MAILJET_API_KEY = 'acd66a47abcaf2331d2ded115e91d07a'
MAILJET_API_SECRET = '9a62384f893c70718918e66c7fd89a48'
ADMIN_EMAIL = 'nikolay.stankov1@gmail.com'


COINMARKETCAP_API_KEY='3f3a45bd-0152-46f9-8641-9850e53be791'

NEWS_API_KEY = 'b48b4a42bb9c4d099a21e4165f4ffc22'
