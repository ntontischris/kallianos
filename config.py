class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@host:port/database'  # Replace with your Supabase connection details
    SQLALCHEMY_TRACK_MODIFICATIONS = False
