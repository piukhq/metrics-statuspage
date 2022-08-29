from pydantic import BaseSettings


class Settings(BaseSettings):
    prom_ips: str = "10.10.255.254,10.11.255.254"
    sp_api_key: str = "432537fe-12a0-4f9c-aa23-7964fb2053db"
    sp_page_id: str = "wx6qpqvzjkw1"
    retry_count: int = 3
    retry_delay: int = 15


settings = Settings()
