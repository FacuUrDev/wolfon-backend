from pydantic import Field
from pydantic_settings import BaseSettings


class MongoCreds(BaseSettings):
    username: str = Field(validation_alias='MONGO_USER')
    password: str = Field(validation_alias='MONGO_PASSWORD')

    @property
    def url(self) -> str:
        return f"mongodb+srv://{self.username}:{self.password}@wolfon-database.hovcqap.mongodb.net/?retryWrites=true&w=majority&appName=wolfon-database&uuidrepresentation=standard"

    class Config:
        env_file = '.env'