import passpy

UNLOCK_KEY = "__passtui_unlock__"
UNLOCK_PASSPHRASE = "unlock"


class PassCLI:
    def __init__(self):
        self.store = passpy.Store()

    def get_store_key(self, key: str) -> str | None:
        return self.store.get_key(key)

    def unlock(self) -> bool:
        if UNLOCK_KEY not in self.store:
            self.store.set_key(UNLOCK_KEY, UNLOCK_PASSPHRASE)

        key = self.get_store_key(UNLOCK_KEY)
        if key:
            key = key.strip()

        return key == UNLOCK_PASSPHRASE


passcli = PassCLI()
