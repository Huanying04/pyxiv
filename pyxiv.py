class Pyxiv(object):
    def __init__(self, php_sessid='', user_agent=''):
        self._php_sessid = php_sessid
        self._user_agent = user_agent

    def get_php_sessid(self):
        return self._php_sessid

    def get_user_agent(self):
        return self._user_agent

    def set_php_sessid(self, php_sessid: str):
        self._php_sessid = php_sessid

    def set_user_agent(self, user_agent: str):
        self._user_agent = user_agent


p = Pyxiv()


def set_php_sessid(php_sessid: str):
    p.set_php_sessid(php_sessid)


def set_user_agent(user_agent: str):
    p.set_user_agent(user_agent)


def get_php_sessid():
    return p.get_php_sessid()


def get_user_agent():
    return p.get_user_agent()
