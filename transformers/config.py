import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Read Environment Variables

    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") or False
    )

    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "transformers_db")
    TF_APP_ENVIRONMENT = os.getenv("TF_APP_ENVIRONMENT", "dev")

    if TF_APP_ENVIRONMENT == "dev":
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
            basedir, "transformers.db"
        )
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres-service:5432/{POSTGRES_DB}"

    # if POSTGRES_PASSWORD:
    #     print("Using postgres")
    #     SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres-service:5432/{POSTGRES_DB}"
    # else:
    #     print("Using sqlite")
    #     SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    #         basedir, "transformers.db"
    #     )

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
