from pydantic import (
    BaseModel,
)

from app.setup.config.database import PostgresSettings, SqlaEngineSettings
from app.setup.config.loader import ValidEnvs, get_current_env, load_full_config
from app.setup.config.logs import LoggingSettings


class AppSettings(BaseModel):
    postgres: PostgresSettings
    sqla: SqlaEngineSettings
    logs: LoggingSettings


def load_settings(env: ValidEnvs | None = None) -> AppSettings:
    if env is None:
        env = get_current_env()
    raw_config = load_full_config(env=env)
    return AppSettings.model_validate(raw_config)
