from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from http.cookies import SimpleCookie
import time
import random
import re
import math

import undetected_chromedriver as uc


class LoginFacebook:
    def __init__(self, uid="", index=0):
        self.uid = uid
        self.index = index
        self.driver = None
        self.dict_group = {}
        self.SCROLL_PAUSE_TIME = 1
        # self.create_driver()

    def create_driver_get_id_group(self):
        if self.driver_type == 'chrome':
            # service_obj = Service(ChromeDriverManager().install())
            service_obj = Service(executable_path='./driver/chrome/chromedriver_linux64/chromedriver')
            options = Options()
            width = 500
            higth = 600
            position_x = self.index*width if self.index < 4 else (self.index-4)*width
            position_y = 0 if self.index < 4 else 600
            # options.add_argument("--start-maximized")
            options.add_argument(f"--window-size={width},{higth}")
            options.add_argument(f"--window-position={position_x},{position_y}")
            options.add_experimental_option("detach", True)
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2
            })
            options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
            options.add_argument(f"--user-data-dir=./profile/{self.uid}")
            options.add_argument(f"--profile-directory=Default")
            self.driver = webdriver.Chrome(service=service_obj, options=options)
            self.driver.implicitly_wait(10)

        if self.driver_type == 'chorme-headless':
            service_obj = Service(ChromeDriverManager().install())
            options = Options()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(service=service_obj, options=options)
            self.driver.get('https://m.facebook.com/')
            self.driver.implicitly_wait(10)
            # self.driver = webdriver.Firefox(executable_path='./driver/firefox/geckodriver', options=options)

        if self.driver_type == 'firefox':
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        if self.driver_type == 'chrome_profile':
            print(self.path, self.profile)
            options = uc.ChromeOptions()
            # / home / tuan /.config / google - chrome
            # options.add_argument(f"user-data-dir={self.path}")
            # options.add_argument(f"profile-directory={self.profile}")
            # options.user_data_dir = self.path
            # options.profile_directory = self.profile
            options.add_argument(f"--user-data-dir={self.path}")
            options.add_argument(f"--profile-directory={self.profile}")
            # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
            print('https://www.facebook.com/')
            self.driver = uc.Chrome(options=options)

            self.driver.get('https://www.facebook.com/')

        if self.driver_type == 'uc':
            options = uc.ChromeOptions()
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2
            })
            self.driver = uc.Chrome(options=options, version_main=104)

    def login_cookie(self, cookie_text, driver_type):
        self.driver_type = driver_type
        self.create_driver_get_id_group()
        self.driver.get('https://www.facebook.com/')
        cookie = SimpleCookie()
        cookie.load(cookie_text)

        for key, morsel in cookie.items():
            self.driver.add_cookie({'name': key, 'value': morsel.value, 'domain': '.facebook.com'})

        self.driver.get('https://www.facebook.com/')
        time.sleep(random.random() * 2)
        self.driver.get(f"https://www.facebook.com/{self.uid}")
        login_text = self.driver.find_elements(By.XPATH, f"(//div[@aria-label='Messenger'])[1]")
        if login_text:
            return "Đăng nhập thành công"
        else:
            return "Vui lòng đăng nhập"

    def login_profile_uc(self, profile, driver_type):
        self.driver_type = driver_type
        *path, floder_file = profile.split('/')
        self.path = '/'.join(path)
        self.profile = floder_file
        # self.profile = profile
        self.create_driver_get_id_group()
        self.driver.get('https://www.facebook.com/')
        time.sleep(random.random() * 2)
        self.driver.get(f"https://www.facebook.com/{self.uid}")
        login_text = self.driver.find_elements(By.XPATH, f"(//div[@aria-label='Messenger'])[1]")
        if login_text:
            return "Đăng nhập profile thành công"
        else:
            return "Vui lòng đăng nhập"

    def login_cookie_uc(self, cookie_text, driver_type):
        self.driver_type = driver_type
        self.create_driver_get_id_group()
        self.driver.get('https://www.facebook.com/')
        cookie = SimpleCookie()
        cookie.load(cookie_text)

        for key, morsel in cookie.items():
            self.driver.add_cookie({'name': key, 'value': morsel.value, 'domain': '.facebook.com'})

        self.driver.get(f"https://www.facebook.com/")
        time.sleep(5)
        self.driver.get(f"https://www.facebook.com/{self.uid}")
        login_text = self.driver.find_elements(By.XPATH, f"(//div[@aria-label='Messenger'])[1]")
        if login_text:
            return "Đăng nhập cookie thành công"
        else:
            return "Vui lòng đăng nhập"

    def get_id_group(self):
        self.driver.get('https://m.facebook.com/groups_browse/your_groups/')
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        list_groups = self.driver.find_elements(By.XPATH, '//a[contains(@href, "/groups/")]')

        for idx, item in enumerate(list_groups):
            linkpost = item.get_attribute("href")
            group_name = item.find_element(By.XPATH, ".//div/div/div/div[1]")
            id_group = re.findall(r"groups/(.*)/\?ref", linkpost)
            self.dict_group[id_group[0]] = group_name.text

    def press_text(self, content, element):
        for charter in content:
            time.sleep(0.3)
            element.send_keys(charter)

    def upload_img(self, list_img):
        for img in list_img:
            element = self.driver.find_element(By.XPATH, "(//input[@type='file'])[3]")
            if element:
                element.send_keys(f'{img}')
            else:
                print('k thay')

            time.sleep(5)
            # while True:
            #     try:
            #         wait = WebDriverWait(self.driver, 10)
            #         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".img[src^='https://scontent']")))
            #         break
            #     except TimeoutException:
            #         self.driver.find_element(By.XPATH, "//div[@aria-label='Gỡ ảnh']").click()
            #         time.sleep(1)
            #         alert = self.driver.switch_to.alert
            #         alert.accept()

    def add_picture(self, img_path_list):
        element_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[name^='file']")
        len_path = len(img_path_list)
        if len_path <= len(element_inputs):
            for index, path in enumerate(img_path_list):
                element_inputs[index].send_keys(path)
                time.sleep(random.randint(1, 2))
        else:
            count = 0
            for index, path in enumerate(img_path_list):
                # element_inputs[index-count].send_keys(path)
                upload = self.driver.find_element(By.CSS_SELECTOR, f"input[name='file{index + 1 - count}']")
                upload.send_keys(path)
                time.sleep(random.randint(1, 2))
                if not ((index+1) % 3) and index+1 < len_path:
                    count += 3
                    time.sleep(random.randint(1, 2))
                    self.driver.find_element(By.XPATH, "//*[@name='add_photo_done']").click()
                    time.sleep(random.randint(1, 2))
                    addphoto = self.driver.find_element(By.XPATH, "//input[@name='view_photo']")
                    addphoto.click()
            # count_path = math.ceil(len_path / 3)
            # start = 0
            # for count in range(1, count_path + 1):
            #     end = count * 3
            #     for index in range(start, end):
            #         if len_path > index:
            #             upload = self.driver.find_element(By.CSS_SELECTOR, f"input[name='file{index + 1 - start}']")
            #             upload.send_keys(img_path_list[index])
            #     start = end
            #     time.sleep(random.randint(1, 2))
            #     self.driver.find_element(By.XPATH, "//*[@name='add_photo_done']").click()
            #     time.sleep(random.randint(3, 5))
            #     if len_path > end:
            #         addphoto = self.driver.find_element(By.XPATH, "//input[@name='view_photo']")
            #         addphoto.click()

    def post_group(self, group_id, content, img_path_list):
        url = f'https://mbasic.facebook.com/groups/{group_id}/'
        self.driver.get(url)

        content_element = self.driver.find_element(By.XPATH, "//textarea[@name='xc_message']")
        time.sleep(random.randint(2, 5))
        self.press_text(content, content_element)
        time.sleep(random.randint(2, 5))
        if img_path_list:
            self.driver.find_element(By.XPATH, "//input[@name='view_photo']").click()
            time.sleep(random.randint(2, 5))
            self.add_picture(img_path_list)
            time.sleep(random.randint(2, 5))
            self.driver.find_element(By.XPATH, "//*[@name='add_photo_done']").click()
            time.sleep(random.randint(2, 5))
            self.driver.find_element(By.XPATH, "//input[@name='view_post']").click()
        else:
            self.driver.find_element(By.XPATH, "//input[@name='view_post']").click()

        time.sleep(random.randint(5, 10))

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(random.randint(3, 5))
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(random.randint(2, 5))
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(random.randint(2, 5))
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(random.randint(2, 5))

        return f"post bài viết thành công {group_id}"

    def post_status(self, text_status, img):
        if img:
            list_path_img = img.split(',')
            self.driver.get(f"https://mbasic.facebook.com/{self.uid}/")
            time.sleep(random.randint(2, 6))
            ele_input = self.driver.find_element(By.XPATH, "//textarea[@name='xc_message']")
            self.press_text(text_status, ele_input)

            self.driver.find_element(By.XPATH, "//input[@name='view_photo']").click()
            time.sleep(random.randint(3, 7))
            self.add_picture(list_path_img)
            time.sleep(random.randint(2, 6))
            self.driver.find_element(By.XPATH, "//input[@name='add_photo_done']").click()
            time.sleep(random.randint(2, 6))
            self.driver.find_element(By.XPATH, "//input[@name='view_post']").click()
            time.sleep(random.randint(5, 10))

            actions = ActionChains(self.driver)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.randint(3, 5))
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.randint(2, 8))
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.randint(2, 8))
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.randint(2, 8))
            return 'Đăng bài viết xong'

        else:
            self.driver.get(f"https://www.facebook.com/{self.uid}/")
            time.sleep(random.randint(2, 8))
            ele_status = self.driver.find_element(By.XPATH, "//div[@data-isanimatedlayout='true']/div/div/div/div/div/div/div[@role='main']/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/span[1]")
            ele_status.click()
            time.sleep(random.randint(2, 8))
            element_background = self.driver.find_element(By.XPATH, "//div[@aria-label='Show Background Options']")
            time.sleep(random.randint(2, 8))
            if element_background:
                element_background.click()
                time.sleep(random.randint(2, 8))
                element = element_background.find_elements(By.XPATH, "//div[contains(@aria-label,'Gradient')]")
                if element:
                    element[0].click()
            else:
                time.sleep(random.randint(2, 8))
                element = self.driver.find_elements(By.XPATH, "//div[contains(@aria-label,'Gradient')]")
                if element:
                    element[0].click()
            # self.driver.find_element(By.XPATH, f"(//div[@class='lcfup58g fzd7ma4j fhfp1cgp'])[{random.randint(1,9)}]").click()

            time.sleep(random.randint(2, 8))
            action = ActionChains(self.driver)
            time.sleep(random.randint(2, 8))
            for item in text_status:
                action.send_keys(item).perform()
                time.sleep(random.random())
            time.sleep(random.randint(2, 8))
            self.driver.find_element(By.XPATH, "//div[@aria-label='Post']//div//div//div//span[1]").click()

            time.sleep(random.randint(5, 10))

            actions = ActionChains(self.driver)
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.randint(3, 5))
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.randint(2, 8))
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.randint(2, 8))
            actions.send_keys(Keys.SPACE).perform()
            time.sleep(random.randint(2, 8))

            return 'Đăng bài viết xong'

    def action_comment(self, ele, content):
        form_ele = ele.find_element(By.XPATH, ".//form[@role='presentation']//div[@role='textbox']")
        time.sleep(random.randint(1, 3))

        action = ActionChains(self.driver)
        action.move_to_element(form_ele).perform()
        time.sleep(random.randint(1, 3))
        form_ele.click()

        time.sleep(random.randint(1, 3))
        for item in content:
            action.send_keys(item).perform()
            time.sleep(random.random())
        time.sleep(random.randint(1, 3))
        print("comment xong")

    def comment_group(self, keyword_content, content, group_id):
        url = f'https://www.facebook.com/groups/{group_id}/'
        self.driver.get(url)
        time.sleep(random.randint(1, 3))
        self.driver.find_element(By.CSS_SELECTOR, "svg[title$='sort group feed by']").click()
        time.sleep(random.randint(1, 3))
        self.driver.find_element(By.XPATH, "//span[normalize-space()='Newest activity']").click()
        time.sleep(random.randint(1, 3))
        index_ele = 0
        key_words = keyword_content.split(',')
        print(key_words)
        for i in range(2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(1, 3))
            article_eles = self.driver.find_elements(By.XPATH,
                                                     "//div[@role='article'][@aria-posinset]/div[1]/div[1]/div[1]/div[1]/div[1]/div[8]/div[1]")
            len_list = len(article_eles)

            time.sleep(random.randint(1, 3))
            for idx in range(index_ele, len_list):
                text = article_eles[idx].find_element(By.XPATH, "./div[3]/div[1]/div[1]/div[1]")
                time.sleep(random.randint(1, 3))

                if any(word in f'''{text.text.lower()}''' for word in key_words):
                    self.action_comment(article_eles[idx], content)
                else:
                    print('k co trong tu khoa')

                time.sleep(random.randint(1, 3))
            index_ele = len_list

    def interaction(self, content):
        self.driver.get("https://www.facebook.com")
        time.sleep(random.randint(1, 3))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(1, 3))
        # self.driver.find_elements(By.XPATH, "//h4//a[@role='link'][starts-with(@href, 'https://www.facebook.com/')]")
        ele_post = self.driver.find_elements(By.XPATH, "//div[@class='b6ax4al1']")
        time.sleep(random.randint(1, 3))

        for ele in ele_post:
            try:
                link_ele = ele.find_element(By.XPATH, ".//h4//a[@role='link'][starts-with(@href, 'https://www.facebook.com/')]")
                if link_ele:
                    comment = ele.find_element(By.XPATH, ".//div[@aria-label][@role='textbox'][@contenteditable='true']")
                    time.sleep(random.randint(1, 3))
                    action = ActionChains(self.driver)
                    action.move_to_element(comment).perform()
                    time.sleep(random.randint(1, 3))
                    try:
                        ele.find_element(By.XPATH, ".//div[@aria-label='Remove Like']")
                        print('da like roi')
                    except NoSuchElementException:
                        like_ele = ele.find_element(By.XPATH, ".//div[@aria-label='Like']")
                        time.sleep(random.randint(1, 3))
                        if like_ele:
                            like_ele.click()
                            time.sleep(random.randint(1, 3))
                            comment.click()
                            time.sleep(random.randint(1, 3))
                            for item in content:
                                action.send_keys(item).perform()
                                time.sleep(random.random())
                            time.sleep(random.randint(1, 3))
                            action.send_keys(Keys.ENTER).perform()

            except NoSuchElementException:
                print('k co ele')



        # //div[@aria-label][@role='textbox'][@contenteditable='true']
        # //h4//a[@role='link'][starts-with(@href, "https://www.facebook.com/")]












        '''time.sleep(random.randint(1, 3))
        select = self.driver.find_element(By.XPATH, "//div[@role='feed']")

        article_eles = self.driver.find_elements(By.XPATH, "//div[@role='article'][@aria-posinset]/div[1]/div[1]/div[1]/div[1]/div[1]/div[8]/div[1]")
        print(len(article_eles))
        for ele in article_eles:
            # .//div[3]/div[1]/div[1]/div[1]
            # //body[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[8]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]
            print('vao day')
            time.sleep(random.randint(1, 3))
            try:
                # text = ele.find_element(By.XPATH, ".//div[contains(text(), *)]")
                text = ele.find_element(By.XPATH, "./div[3]/div[1]/div[1]/div[1]")
                time.sleep(random.randint(1, 3))
                print(text.text)
                # form_ele = ele.find_element(By.XPATH, ".//form[@role='presentation']//div[@role='textbox']/p[1]")
                # time.sleep(random.randint(1, 3))
                # like_ele = ele.find_element(By.XPATH, ".//div[@aria-label='Like']")
                # time.sleep(random.randint(1, 3))
                # like_ele.click()
                # print(form_ele.get_attribute('class'))
                # time.sleep(random.randint(1, 3))
                # form_ele.click()
                # action = ActionChains(self.driver)
                # time.sleep(random.randint(1, 3))
                # action.send_keys("so dep tratrc").perform()
                # time.sleep(random.randint(1, 3))
            except NoSuchElementException:
                print('k co')
                # continue
            # item = ele.find_element(By.XPATH, "//div[contains(text(),'sim')]")
            # if item:
            #     print(item.text)
            # else:
            #     print('k có')
        # //div[@data-ad-comet-preview='message']
        # //div[contains(text(),'bank')]






        # content = driver.find_element_by_name('xc_message')
        # time.sleep(random.randint(2, 5))
        # for character in text:
        #     content.send_keys(character)
        #     time.sleep(0.3)
        #
        # time.sleep(random.randint(3, 10))

        #
        # print('post ok {}'.format(id))
        # time.sleep(random.randint(5, 10))
        #
        # actions = ActionChains(driver)
        # actions.send_keys(Keys.SPACE).perform()
        # time.sleep(random.randint(3, 5))
        # actions.send_keys(Keys.SPACE).perform()
        # time.sleep(random.randint(2, 8))





 # element = self.driver.find_element(By.XPATH, "//div[@aria-label='Tạo bài viết công khai...']")
 #        time.sleep(1)
 #
 #        time.sleep(1)
 #        self.upload_img(img_path_list)
 #        self.driver.find_element(By.XPATH, "//div[@aria-label='Đăng']").click()
 #        time.sleep(5)
 #        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 #        print("upload img")'''


