from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Login import LoginFacebook
import time


class ThreadClass(QThread):
    any_single = pyqtSignal(str, str, str)
    mess_login = pyqtSignal(str)

    def __init__(self, uid="", fb=[]):
        super().__init__()
        self.uid = uid
        self.cookie = fb[2]
        self.is_running = True

    def run(self):
        self.driver_fb = LoginFacebook(uid=self.uid, driver_type='uc')
        message = self.driver_fb.login_cookie_uc(cookie_text=self.cookie)
        self.mess_login.emit(message)
        if 'thành công' in message:
            self.driver_fb.get_id_group()
            self.driver_fb.quit()
            for id_group, name in driver_fb.dict_group.items():
                time.sleep(0.2)
                self.any_single.emit(id_group, name, self.uid)

    def stop(self):
        self.is_running = False
        self.driver_fb.quit()
        self.terminate()
