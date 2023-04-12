from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # @root_validator
    # def get_database_url(cls, values):
    #     values['DATABASE_URL'] = (f'postgresql+asyncpg://{values["POSTGRES_USER"]}:{values["POSTGRES_PASSWORD"]}'
    #             f'@{values["POSTGRES_HOST"]}:{values["POSTGRES_PORT"]}/{values["POSTGRES_DB_NAME"]}')
    #     return values

    @property
    def DATABASE_URL(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:'
                f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
                f'{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}')

    class Config:
        env_file = 'app/.env'


settings = Settings()
