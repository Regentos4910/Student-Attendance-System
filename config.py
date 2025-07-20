import os

# Get absolute path to instance folder
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

# Ensure instance folder exists
os.makedirs(instance_path, exist_ok=True)

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "app.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'your-secret-key-here'