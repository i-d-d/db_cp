import secret

class DatabaseSettings:
    database_name = secret.database_name 
    database_host = secret.database_host
    database_user = secret.database_user
    database_password = secret.database_password
    database_port = secret.database_port

class BotSettings:
    bot_token = secret.bot_token

class AdminSettings:
    admin_pass = secret.admin_pass

class Settings(DatabaseSettings, 
               BotSettings,
               AdminSettings):
    pass

settings = Settings()