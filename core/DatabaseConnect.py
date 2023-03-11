import asyncio
import dataclasses
from configparser import ConfigParser
import asyncpg
from functools import lru_cache

from asyncpg import PostgresConnectionError


@dataclasses.dataclass(frozen=True)
class PostgresConnectionFields:
    host: str
    port: str
    user: str
    password: str
    database: str


class AsyncPgDbConnection:
    db_config_file: str | None = None
    __is_set = False

    @lru_cache
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'unique'):
            cls.unique = super().__new__(cls)
        return cls.unique

    def __init__(self, *, db_type="POSTGRESQL"):
        if self.db_config_file is not None:
            try:
                if self.__is_set is False:
                    self.__set_postgres_configs(db_config_file=self.db_config_file)
                    self.__is_set = True
            except Exception as e:
                raise Exception(e)
        else:
            raise ValueError("INVALID DATABASE")

    def __set_postgres_configs(self, *, db_config_file):
        conf = ConfigParser()
        conf.read(db_config_file)
        self.__POSTGRES_CONFIGS = PostgresConnectionFields(
            host=conf.get('DATABASE', 'host'),
            port=conf.getint('DATABASE', 'port'),
            user=conf.get('DATABASE', 'user'),
            password=conf.get('DATABASE', 'password'),
            database=conf.get('DATABASE', 'database')
        )

    async def __aenter__(self, ):
        try:
            self.__connection_object: asyncpg.connection.Connection = await asyncpg.connect(
                host=self.__POSTGRES_CONFIGS.host,
                port=self.__POSTGRES_CONFIGS.port,
                user=self.__POSTGRES_CONFIGS.user,
                password=self.__POSTGRES_CONFIGS.password,
                database=self.__POSTGRES_CONFIGS.database,
            )
            return self.__connection_object
        except PostgresConnectionError:
            raise PostgresConnectionError('CONNECTION FAILED')

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.__connection_object.close()
        except Exception as e:
            print(e)
            raise Exception(e)

    @staticmethod
    async def run_upsert_sql_command_with_returning(
                                                    sql_command: str,
                                                    *sql_args):
        try:
            async with AsyncPgDbConnection() as connection:
                async with connection.transaction():
                    if sql_args:
                        await connection.execute(
                            sql_command,
                            *sql_args)
                        return True
                    await connection.execute(sql_command)
                    return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    async def run_upsert_sql_command_without_returning(
                                                       sql_command: str,
                                                       *sql_args):
        try:
            async with AsyncPgDbConnection() as connection:
                async with connection.transaction():
                    if sql_args:
                        await connection.execute(
                            sql_command,
                            *sql_args)
                        return True
                    await connection.execute(sql_command)
                    return True
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    async def run_select_sql_command(
                                     sql_command: str,
                                     *sql_args):
        try:
            async with AsyncPgDbConnection() as connection:
                async with connection.transaction():
                    if not sql_args:
                        return await connection.fetch(
                            sql_command,
                            )
                    return await connection.fetch(
                        sql_command,
                        *sql_args)
        except Exception as e:
            print(e)
            raise e





