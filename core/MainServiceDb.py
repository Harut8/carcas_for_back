from core.DatabaseConnect import AsyncPgDbConnection


class MainServiceDB:

    @staticmethod
    def get_user_from_db(*, user_id: str):
        ...

    @staticmethod
    def check_email_and_password(*, email: str, password: str):
        ...
