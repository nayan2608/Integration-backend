from pathlib import Path
from enum import StrEnum, auto
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings
from starlette.config import Config
from pydantic import Field

ENV_FILEPATH: Path = Path(find_dotenv())
load_dotenv(ENV_FILEPATH)
config: Config = Config(ENV_FILEPATH)


class EnvFlavour(StrEnum):
    dev = auto()
    stg = auto()
    prod = auto()


class GlobalConfig(BaseSettings):
    """Global configurations."""

    FLAVOUR: EnvFlavour = Field(default=EnvFlavour.dev)

    NOTION_CLIENT_ID: str
    NOTION_CLIENT_SECRET: str

    AIRTABLE_CLIENT_ID: str
    AIRTABLE_CLIENT_SECRET: str

    HUBSPOT_CLIENT_ID: str
    HUBSPOT_CLIENT_SECRET: str


class DevConfig(GlobalConfig):
    """Development configurations."""

    RELOAD: bool = True


class StageConfig(GlobalConfig):
    """Staging configurations."""


class ProdConfig(GlobalConfig):
    """Production configurations."""


class FactoryConfig:
    """Returns a config instance depending on the env FLAVOUR variable."""

    def __init__(self, flavour: EnvFlavour):
        self.FLAVOUR = flavour

    def __call__(self) -> GlobalConfig:
        config: type[GlobalConfig] = GlobalConfig

        if self.FLAVOUR == EnvFlavour.dev:
            config = DevConfig

        elif self.FLAVOUR == EnvFlavour.stg:
            config = StageConfig

        elif self.FLAVOUR == EnvFlavour.prod:
            config = ProdConfig

        return config.model_validate({})


settings: GlobalConfig = FactoryConfig(
    config("FLAVOUR", default=EnvFlavour.dev, cast=EnvFlavour)
)()


__all__ = ["settings"]
