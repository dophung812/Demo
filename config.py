class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dauphong:20200477@localhost/salary_employee'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    DEBUG = True
