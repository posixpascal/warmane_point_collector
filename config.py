import configparser


# Reads and stores the config.ini file
class Config(object):
    CONFIG_FILE = "./config.ini"

    def __init__(self):
        self.config_file = configparser.ConfigParser()
        self.config_file.read(Config.CONFIG_FILE)

        self.selectors = self.config_file["selectors"]
        self.endpoint = self.config_file["endpoint"]
        self.chrome = self.config_file["chrome"]
        self.bot = self.config_file["bot"]
        self.twocaptcha = self.config_file["2captcha"]

        self.accounts = []

        # parse accounts
        for section in self.config_file.sections():
            if not section.startswith("account_"):
                continue

            account = {
                "username": self.config_file[section]["username"],
                "password": self.config_file[section]["password"]
            }

            self.accounts.append(account)


config = Config()
