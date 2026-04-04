import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable '{name}' is not set.")
    return value


def build_connection_url() -> str:
    server = _get_required_env("MSSQL_SERVER")
    port = _get_required_env("MSSQL_PORT")
    database = _get_required_env("MSSQL_DATABASE")
    username = _get_required_env("MSSQL_USER")
    password = _get_required_env("MSSQL_PASSWORD")
    driver = os.getenv("MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")
    encrypt = os.getenv("MSSQL_ENCRYPT", "no")
    trust_server_certificate = os.getenv("MSSQL_TRUST_SERVER_CERTIFICATE", "yes")

    odbc_params = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt={encrypt};"
        f"TrustServerCertificate={trust_server_certificate};"
    )

    return f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_params)}"


DATABASE_URL = build_connection_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)
