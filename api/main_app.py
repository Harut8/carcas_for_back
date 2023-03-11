from fastapi import FastAPI
from uvicorn import run
from core.DatabaseConnect import AsyncPgDbConnection
from services.MainService import MainService
from api.user_app import user_app
from api.ApiConfigs import ApiConfigs


fastapi_app = FastAPI()
fastapi_app.include_router(user_app)


@fastapi_app.get('/')
def start_server():
    return MainService.get_server_status()


def main():
    AsyncPgDbConnection.db_config_file = 'DB_CONFIG.ini'
    api_configs = ApiConfigs()
    run(fastapi_app, host=api_configs.host)
