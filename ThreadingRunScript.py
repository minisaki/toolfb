from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Login import LoginFacebook
import time
import random


class ThreadClassRunFb(QThread):
    any_single = pyqtSignal(str, int)

    def __init__(self, dict_data, row, index):
        super().__init__()
        print(f"dict_data {dict_data}")
        self.index = index
        self.row = row

        self.uid = dict_data['account_fb_id']
        self.fb_name = dict_data['account_fb_name']
        self.cookie = dict_data['account_fb_cookie']
        self.profile = dict_data['account_fb_profile']

        self.group_name = dict_data['group_name']
        self.group_id = dict_data['group_id']

        self.post_status = dict_data['list_post_status']

        self.description = dict_data['description']
        self.image = dict_data['image']

        self.interactive = dict_data['interactive']
        self.keyword_content = dict_data['keyword_content']
        self.comment_group = dict_data['comment_group']

        self.is_running = True
        self.pause = False
        self.is_loop = True

    def run(self):
        # try:
        self.driver_fb = LoginFacebook(uid=self.uid, index=self.index)

        message = self.driver_fb.login_cookie(cookie_text=self.cookie, driver_type='uc')
        # if self.profile:
        #     message = self.driver_fb.login_profile_uc(profile=self.profile, driver_type='chrome_profile')
        # elif self.cookie:
        #     message = self.driver_fb.login_cookie_uc(cookie_text=self.cookie, driver_type='uc')
        # else:
        #     message = "Không có cookie và profile để login"

        print(message)
        self.any_single.emit(message, self.row)
        if 'thành công' in message:
            group_id_list = self.group_id.split(',')
            list_path = self.image.split(',')
            count = 0

            while count < len(group_id_list) or count < len(self.post_status):
                while self.pause:
                    time.sleep(5)
                    if self.is_loop:
                        self.is_loop = False
                        print('tam dung 1')
                    print('tam dung')
                    self.any_single.emit("Đang tạm dừng", self.row)
                if not self.is_loop:
                    self.is_loop = True

                try:
                    if self.group_name and count < len(group_id_list):
                        print('vao dang bai group')
                        if count > 10:
                            result = self.driver_fb.post_group(group_id_list[count], self.description, list_path)
                            self.any_single.emit(result, self.row)

                    if self.post_status and count < len(self.post_status):
                        print('Đăng bài status')
                        if count > 5:
                            self.any_single.emit("ĐĂng bài trên status", self.row)
                            mesage = self.driver_fb.post_status(text_status=self.post_status[count][2], img=self.post_status[count][3])
                            self.any_single.emit(mesage, self.row)

                    if self.interactive:
                        print('Tương tác bạn bè')
                        contents = self.keyword_content.split(',')
                        content = random.choice(contents)
                        self.driver_fb.interaction(content)

                    if self.comment_group and self.group_name and count < lend(group_id_list):
                        print('Bình luận vào bài viết trong group')
                        self.driver_fb.comment_group(self.keyword_content, self.comment_group, self.group_id_list[count])

                except Exception:
                    print(f'vao lỗi vi tri {count} - {group_id_list[count]}')
                count += 1
        else:
            self.any_single.emit('Kiểm tra thông tin đăng nhập tài kkhoản', self.row)
        # except Exception:
        #     print('vao lỗi')
        #     pass

    def thread_pause(self):
        self.pause = True

    def thread_resume(self):
        self.pause = False

    def thread_stop(self):
        if self.is_loop:
            self.any_single.emit("vui lòng chờ trình duyệt chạy xong", self.row)
            return
        self.close_driver()
        self.terminate()
        self.wait()

    def close_driver(self):
        self.driver_fb.driver.quit()


