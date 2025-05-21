from pathlib import Path

from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

BaseDir = Path(__file__).parent.parent


class Settings(BaseSettings):
    postgres_host: str
    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    postgres_test_host: str
    postgres_test_port: str
    postgres_test_user: str
    postgres_test_password: str
    postgres_test_db: str

    @property
    def postgres_url(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")

    @property
    def postgres_test_url(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_test_user}:{self.postgres_test_password}"
                f"@{self.postgres_test_host}:{self.postgres_test_port}/{self.postgres_test_db}")

    db_echo: bool = False

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()

