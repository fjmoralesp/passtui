import passpy

UNLOCK_KEY = "__passtui_unlock__"
UNLOCK_PASSPHRASE = "unlock"


class PassCLI:
    def __init__(self):
        self.__store = passpy.Store()

    def get_store_key(self, key: str) -> str:
        key_data = self.__store.get_key(key)
        if key_data:
            return key_data

        return ""

    def unlock(self) -> bool:
        if UNLOCK_KEY not in self.__store:
            self.__store.set_key(UNLOCK_KEY, UNLOCK_PASSPHRASE)

        key = self.get_store_key(UNLOCK_KEY)
        return key.strip() == UNLOCK_PASSPHRASE

    def list_keys(self) -> list[str]:
        return self.__filter_app_keys(list(self.__store))

    def list_folders(self, path: str) -> list[str]:
        return self.__store.list_dir(path)[0]

    def __filter_app_keys(self, keys: list[str]) -> list[str]:
        return [entry for entry in keys if entry != UNLOCK_KEY]


passcli = PassCLI()
