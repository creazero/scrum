import os


API_V1_STR = '/api/v1'

SECRET_KEY = os.getenvb(b'SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

POSTGRES_SERVER = os.getenv('POSTGRES_SERVER', 'localhost')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'scrum')
SQLALCHEMY_DATABASE_URI = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}'
)

FIRST_SUPERUSER = os.getenv('FIRST_SUPERUSER', 'admin')
FIRST_SUPERUSER_PASSWORD = os.getenv('FIRST_SUPERUSER_PASSWORD', '123456')
