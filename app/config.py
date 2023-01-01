from pydantic import BaseSettings

# The 'BaseSettings' library helps with initialisatin of environment variables, ENSURING the datatype and notnull. Pydantic is case-insensitive, so if the user environment variable on the OS is uppercase, it is not a problem. 
class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
# print(settings)
# print(settings.database_name)