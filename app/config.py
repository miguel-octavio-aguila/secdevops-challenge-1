# Import settings management form Pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings and environment variables.

    This class uses Pydantic's BaseSettings to automatically load configuration values from environment variables or a .env file
    """
    
    # Define the variable
    VIRUS_TOTAL_API_KEY: str
    
    # Configure Pydantic to load variables form a .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
# Create a single, reusable instance of the settings
settings = Settings()
