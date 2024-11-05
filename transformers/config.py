import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "transformers.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") or False
    )
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
