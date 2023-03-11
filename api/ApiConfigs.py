class ApiConfigs:
    def __init__(self):
        from configparser import ConfigParser
        conf = ConfigParser()
        conf.read('api/API_CONFIG.ini')
        self.host = conf.get('API', 'host')
        self.email = conf.get('API', 'email')