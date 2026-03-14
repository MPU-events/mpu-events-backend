import os
from dataclasses import dataclass
from dynaconf import Dynaconf

@dataclass(slots=True)
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str
    name: str
    driver: str = "postgresql+asyncpg"

    @property
    def dsn(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass(slots=True)
class AuthConfig:
    jwt_secret_key: str
    access_token_expire_minutes: int = 43200


@dataclass(slots=True)
class AppConfig:
    project_name: str
    version: str
    debug: bool
    database: DatabaseConfig
    auth: AuthConfig


def get_config() -> AppConfig:
    dynaconf = Dynaconf(
        settings_files=[
            os.getenv("CONFIG_FILE", "config/config.toml"),
            "config/.secrets_config.toml",
        ],
        environments=True,
        env_switcher="ENV_FOR_DYNACONF",
        default_env="default",
        merge_enabled=True,
        load_dotenv=True,
    )
    db = dynaconf.DATABASE
    auth = dynaconf.AUTH

    return AppConfig(
        project_name=dynaconf.PROJECT_NAME,
        version=dynaconf.VERSION,
        debug=dynaconf.DEBUG,
        database=DatabaseConfig(
            host=db.host,
            port=db.port,
            username=db.username,
            password=db.password,
            name=db.name,
        ),
        auth=AuthConfig(
            jwt_secret_key=auth.jwt_secret_key,
            access_token_expire_minutes=auth.access_token_expire_minutes,
        ),
    )


config: AppConfig = get_config()