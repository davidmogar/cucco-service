import os

from app import create_app

config_object = os.getenv('APP_SETTINGS')
app = create_app(config_object)

if __name__ == '__main__':
    app.run()
