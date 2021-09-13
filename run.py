from decouple import config

from config import config_dict
from app import create_app


# Get app config based on DEBUG environment
DEBUG = config('DEBUG', default=True, cast=bool)
config_name = 'Debug' if DEBUG else 'Production'
app_config = config_dict.get(config_name)

app = create_app(app_config)

if DEBUG:
    app.logger.info(f'DEBUG: {str(DEBUG)}')
    app.logger.info(f'Environment: {config_name}')
    app.logger.info(f'Prism Host: {app_config.PRISM_HOST}')

if __name__ == "__main__":
    app.run()
