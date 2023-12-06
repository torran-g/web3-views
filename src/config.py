from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    rpc_endpoint: str
    contract_abi_path: str
    contract_address: str


settings = Settings()
