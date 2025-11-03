import json
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    APP_NAME: str = "fastapi-mysql-app"
    APP_ENV: str = "local"

    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # 문자열/리스트 모두 허용 → 내부에선 list[str]로 통일
    CORS_ORIGINS: List[str] = []

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return (
            f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )

    # 빈 문자열, 콤마 구분, JSON 배열 모두 허용
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if s == "" or s.lower() in {"[]", "none", "null"}:
                return []
            # JSON 배열 시도
            if s.startswith("["):
                try:
                    arr = json.loads(s)
                    # 리스트가 아니면 실패로 간주하고 콤마 split로 진행
                    if isinstance(arr, list):
                        return [str(x).strip() for x in arr if str(x).strip()]
                except Exception:
                    pass
            # 콤마 구분
            return [x.strip() for x in s.split(",") if x.strip()]
        return v

    class Config:
        env_file = ".env"

settings = Settings()
