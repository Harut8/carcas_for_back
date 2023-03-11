from core.MainServiceDb import MainServiceDB


class MainService:

    @staticmethod
    def get_server_status():
        return {
                "status": "Server is running"
            }

    @staticmethod
    def get_user_from_db(*, user_id: str):
        ...

    @staticmethod
    def check_email_and_password(*, email: str, password: str):
        ...


