from pydantic import SecretStr, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = '.env'
    )

    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int
    db_name: str


    @computed_field
    @property
    def database_url(self) -> str:
        return str(MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.db_user,
                password=self.db_password.get_secret_value(),
                host=self.db_host,
                port=self.db_port,
                path=self.db_name,
            )
        )


settings = Settings() # type: ignore

