# configs.py
from pathlib import Path
from typing import Optional
import os
from pydantic import BaseSettings, Field, BaseModel
from os import environ


class AppConfig(BaseModel):
    """Application configurations."""

    VAR_A: int = 33
    VAR_B: float = 22.0

    # question classification settings
    SPACY_MODEL_IN_USE: str = "en_core_web_sm"

    # all the directory level information defined at app config level
    # we do not want to pollute the env level config with these information
    # this can change on the basis of usage

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    SETTINGS_DIR: Path = BASE_DIR.joinpath("settings")
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

    LOGS_DIR: Path = BASE_DIR.joinpath("logs")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    MODELS_DIR: Path = BASE_DIR.joinpath("models")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # These variables will be loaded from the .env file. However, if
    # there is a shell environment variable having the same name,
    # that will take precedence.

    APP_CONFIG: AppConfig = AppConfig()

    API_NAME: Optional[str] = Field(None, env="API_NAME")
    API_DESCRIPTION: Optional[str] = Field(None, env="API_DESCRIPTION")
    API_VERSION: Optional[str] = Field(None, env="API_VERSION")
    API_DEBUG_MODE: Optional[bool] = Field(None, env="API_DEBUG_MODE")

    # define global variables with the Field class
    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")

    # logging configuration file
    LOG_CONFIG_FILENAME: Optional[str] = Field(None, env="LOG_CONFIG_FILENAME")

    SQL_STRING: Optional[str] = None

    class Config:
        """Loads the dotenv file."""

        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "PROD_"


class FactoryConfig:
    """Returns a config instance depending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


class EnvConfig:
    def __init__(self):
        self.AI_URL = ""
        self.WINECELLAR_URL = ""
        self.API_NAME = "API"
        self.API_DESCRIPTION = ""
        self.API_VERSION = "1.0.0"
        self.LOG_CONFIG_FILENAME = "logging_config.yaml"
        self.APP_CONFIG: AppConfig = AppConfig()
        pass


settings = FactoryConfig(GlobalConfig().ENV_STATE)()

# if None == settings:
#     settings = EnvConfig()
# if "URL" in os.environ:
#     name = os.getenv("URL", "BAD_AI_URL_STRING")
#     settings.AI_URL = name
