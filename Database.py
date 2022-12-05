from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox, QWidget
from PyQt6.QtCore import QThread
import time


class DatabaseFacebook(QWidget):
    def __init__(self, user, pass_word):
        super().__init__()
        self.user = user
        self.pass_word = pass_word
        self.con = self.connect()
        self.query = QSqlQuery(db=self.con)
        self.create_table_fb()
        self.create_table_group_fb()
        self.create_table_list_group_key()
        self.create_table_post()
        self.create_table_run_script()
        self.create_table_script_status()

    def connect(self):
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("fb.sqlite")
        con.setUserName(self.user)
        con.setPassword(self.pass_word)
        con.open()

        if not con.isOpen():
            QMessageBox.critical(self, "Connect Database",
                                 f"""Database Name Connect Error \n Database Error: {con.lastError().databaseText()}""")

            sys.exit(1)
        return con

    def create_table_fb(self):
        query = self.query.exec(
            """
            CREATE TABLE IF NOT EXISTS account_fb (
                id VARCHAR(100) PRIMARY KEY UNIQUE NOT NULL,
                name VARCHAR(255),
                cookie VARCHAR(1000),
                profile VARCHAR(200),
                pass_word VARCHAR(50),
                isAvail BOOLEAN DEFAULT TRUE,
                time timestamp DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        if query:
            print(self.con.tables())
        else:
            QMessageBox.warning(self, "Connect Table", f"Database Table Connect Error \n Error: "
                                                                f"{self.query.lastError().databaseText()}")

    def create_table_group_fb(self):
        # query = self.query.exec("DROP TABLE IF EXISTS group_fb")
        query = self.query.exec(
            """
            CREATE TABLE IF NOT EXISTS group_fb (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                group_id VARCHAR(100) NOT NULL,
                group_name VARCHAR(255),
                member VARCHAR(50),
                isAvail BOOLEAN DEFAULT TRUE,
                time timestamp DEFAULT CURRENT_TIMESTAMP,
                uid VARCHAR(100) NOT NULL,
                FOREIGN KEY(uid) REFERENCES account_fb (id)
            )
            """
        )
        if query:
            print(self.con.tables())
        else:
            QMessageBox.warning(self, "Connect or create Table", f"Database Table Connect Error \n Error: "
                                                                f"{self.query.lastError().databaseText()}")

    def create_table_list_group_key(self):
        # query = self.query.exec("DROP TABLE IF EXISTS group_fb")
        query = self.query.exec(
            """
            CREATE TABLE IF NOT EXISTS list_group_key (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                list_group_id TEXT NOT NULL,
                list_group_name VARCHAR(100),
                group_key VARCHAR(150),
                time timestamp DEFAULT CURRENT_TIMESTAMP,
                uid VARCHAR(100) NOT NULL,
                FOREIGN KEY(uid) REFERENCES account_fb (id)
            )
            """
        )
        if query:
            print(self.con.tables())
        else:
            QMessageBox.warning(self, "Connect or create Table", f"Database Table Connect Error \n Error: "
                                                                f"{self.query.lastError().databaseText()}")

    def create_table_post(self):
        # query = self.query.exec("DROP TABLE IF EXISTS group_fb")
        query = self.query.exec(
            """
            CREATE TABLE IF NOT EXISTS post (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                title VARCHAR(150),
                description TEXT,
                image TEXT,
                note VARCHAR(150),
                isAvail BOOLEAN DEFAULT TRUE,
                time timestamp DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        if query:
            print(self.con.tables())
        else:
            QMessageBox.warning(self, "Connect or create Table", f"Database Table Connect Error \n Error: "
                                                                f"{self.query.lastError().databaseText()}")

    def create_table_run_script(self):
        # query = self.query.exec("DROP TABLE IF EXISTS run_script")
        query = self.query.exec(
            """
            CREATE TABLE IF NOT EXISTS run_script (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                id_fb VARCHAR(50) NOT NULL,
                id_group_key VARCHAR(50),
                id_post_group VARCHAR(50),
                id_post VARCHAR(150),
                interactive TEXT,
                keyword_content VARCHAR(255) DEFAULT NULL,
                comment_group TEXT,
                isAvail BOOLEAN DEFAULT TRUE,
                time timestamp DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(id_fb) REFERENCES account_fb (id),
                FOREIGN KEY(id_group_key) REFERENCES list_group_key (id) ON DELETE SET NULL,
                FOREIGN KEY(id_post_group) REFERENCES post (id) ON DELETE SET NULL,
                FOREIGN KEY(id_post) REFERENCES post (id) ON DELETE SET NULL
            )
            """
        )
        if query:
            print(self.con.tables())
        else:
            QMessageBox.warning(self, "Connect or create Table", f"Database Table Connect Error \n Error: "
                                                                f"{self.query.lastError().databaseText()}")

    def create_table_script_status(self):
        # query = self.query.exec("DROP TABLE IF EXISTS run_script")
        query = self.query.exec(
            """
            CREATE TABLE IF NOT EXISTS script_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                id_script VARCHAR(50),
                id_status VARCHAR(50),               
                time timestamp DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(id_script) REFERENCES run_script (id) ON DELETE CASCADE,
                FOREIGN KEY(id_status) REFERENCES post (id) ON DELETE CASCADE
            )
            """
        )
        if query:
            print(self.con.tables())
        else:
            QMessageBox.warning(self, "Connect or create script status", f"Database Table Connect Error \n Error: "
                                                                 f"{self.query.lastError().databaseText()}")

    def insert_table_fb(self, uid, name, cookie, profile, pass_word):
        if uid == "":
            return "Vui lòng nhập trường Id"

        is_insert = self.query.exec(f"""INSERT INTO account_fb (id, name, cookie, profile, pass_word)
                    VALUES ('{uid}', '{name}', '{cookie}', '{profile}', '{pass_word}')""")

        if is_insert:
            return f"Thêm tài khoản {name} thành công"
        else:
            return f"Có lỗi tài khoản {name} \n error: {self.query.lastError().databaseText()}"

    def insert_table_group_fb(self, uid, id_group, group_name, member=""):
        if uid == "":
            return "Vui lòng nhập trường Id"

        self.query.exec(f"""SELECT id FROM group_fb WHERE EXISTS (SELECT 1 FROM group_fb 
                                        WHERE group_id='{id_group}' AND uid='{uid}')""")

        if not self.query.first():

            is_insert = self.query.exec(f"""INSERT INTO group_fb (group_id, group_name, member, uid)
                        VALUES ('{id_group}', '{group_name}', '{member}', '{uid}')""")

            if is_insert:
                return f"Thêm group {group_name} thành công"
            else:
                return f"Có lỗi group {group_name} \n error: {self.query.lastError().databaseText()}"
        else:
            # time.sleep(1)
            return f"{group_name} đã tồn tại trong dữ liệu"

    def insert_table_list_group_key(self, uid, list_group_id, list_group_name, group_key=""):
        if uid == "":
            return "Vui lòng nhập trường Id"

        if not list_group_id:
            return "Vui lòng nhập chọn group"

        is_insert = self.query.exec(f"""INSERT INTO list_group_key (list_group_id, list_group_name, group_key, uid)
                    VALUES ('{list_group_id}', '{list_group_name}', '{group_key}', '{uid}')""")

        if is_insert:
            return f"Thêm group {list_group_name} thành công"
        else:
            return f"Có lỗi group {list_group_name} \n error: {self.query.lastError().databaseText()}"

    def insert_table_post(self, title, description, image="", note=""):

        if not description:
            return "Vui lòng nhập nội dung bài viết"

        is_insert = self.query.exec(f"""INSERT INTO post (title, description, image, note)
                       VALUES ('{title}', '{description}', '{image}', '{note}')""")

        if is_insert:
            return f"Thêm group {title} thành công"
        else:
            return f"Có lỗi group {title} \n error: {self.query.lastError().databaseText()}"

    def insert_table_run_script(self, data):
        id_fb = data['fb_id']
        id_group_key = data['group_key']
        id_post_group = data['id_post']
        id_posts = data['post_wall']
        interactive = data['comment_post']
        comment_group = data['comment_group']
        keyword_content = data['keyword']

        if not id_fb:
            return "Bạn chưa chọn chọn tài khoản"

        is_insert = self.query.exec(f"""INSERT INTO run_script 
                                    (id_fb, id_group_key, id_post_group, id_post, interactive, keyword_content, comment_group)
                                    VALUES ('{id_fb}', '{id_group_key}', '{id_post_group}', '', 
                                        '{interactive}', '{keyword_content}' ,'{comment_group}')""")
        if id_posts:
            id_run_script_last = self.query.lastInsertId()
            for id_post in id_posts:
                self.query.exec(f"INSERT INTO script_status (id_script, id_status) VALUES ('{id_run_script_last}', '{id_post}')")

        if is_insert:
            return f"Thêm kịch bản thành công"
        else:
            return f"Có lỗi thêm kịch bản \n error: {self.query.lastError().databaseText()}"

    def update_table_fb(self, uid, name, cookie, profile, pass_word):
        # query = QSqlQuery(db=self.con)
        if uid == "":
            return "Vui lòng nhập trường Id"

        is_update = self.query.exec(f"""UPDATE account_fb 
                                        SET id = '{uid}',                                            
                                            name = '{name}', 
                                            cookie = '{cookie}', 
                                            profile = '{profile}',
                                            pass_word = '{pass_word}'
                                        WHERE id= '{uid}'""")

        if is_update:
            return f"Sửa tài khoản {name} thành công"
        else:
            return f"Có lỗi sửa tài khoản {name} \n error: {self.query.lastError().databaseText()}"

    def update_table_post(self, id_post, title, description, note, image):
        # query = QSqlQuery(db=self.con)
        if id_post == "":
            return "Vui lòng chọn 1 bài viết để sửa"

        is_update = self.query.exec(f"""UPDATE post 
                                        SET title = '{title}', 
                                            description = '{description}',
                                            note = '{note}',
                                            image = '{image}'                                            
                                        WHERE id= '{id_post}'""")

        if is_update:
            return f"Sửa tài khoản {title} thành công"
        else:
            return f"Có lỗi sửa tài khoản {title} \n error: {self.query.lastError().databaseText()}"

    def get_list_fb(self, table_name, uid="", keywords=""):
        if uid:
            is_select = self.query.exec(f"SELECT * FROM {table_name} WHERE uid='{uid}' ORDER BY group_name")
        # elif uid and keywords:
        #     list_key = keywords.split(',')
        #     str_sql = ""
        #     for index, key in enumerate(list_key):
        #         if index == len(list_key)-1:
        #             str_sql += F"group_name LIKE '%{key.strip()}%'"
        #         else:
        #             str_sql += F"group_name LIKE '%{key.strip()}%' OR "
        #     is_select = self.query.exec(f"SELECT * FROM {table_name} WHERE uid='{uid}' "
        #                                 f"AND {str_sql} ORDER BY group_name;")

        else:
            is_select = self.query.exec(f"SELECT * FROM {table_name}")
        data = []
        if is_select:
            counts = self.query.record().count()
            if keywords:
                while self.query.next():
                    list_temp = []
                    if any(text.casefold() in self.query.value(2).casefold() for text in keywords.split(',')):
                        for count in range(counts):
                            list_temp.append(self.query.value(count))
                        data.append(list_temp)
            else:
                while self.query.next():
                    list_temp = []
                    for count in range(counts):
                        list_temp.append(self.query.value(count))
                    data.append(list_temp)

            return {'check': True, 'data': data}

        else:
            return {'check': False, 'message': f"{self.query.lastError().databaseText()}"}

    def get_post(self, table_name, id_post):
        data = []
        if id_post:
            is_select = self.query.exec(f"SELECT * FROM {table_name} WHERE id='{id_post}'")

            if is_select:
                self.query.first()
                for item in range(self.query.record().count()):
                    data.append(self.query.value(item))
                return data
        return None

    def get_list_group_key(self, uid):
        if uid:
            is_select = self.query.exec(f"SELECT * FROM list_group_key WHERE uid='{uid}'")
            data = []
            if is_select:
                counts = self.query.record().count()
                while self.query.next():
                    list_temp = []
                    for count in range(counts):
                        list_temp.append(self.query.value(count))
                    data.append(list_temp)

                return {'check': True, 'data': data}

            else:
                return {'check': False, 'message': f"{self.query.lastError().databaseText()}"}

    def get_list_post(self, id_posts=None):
        if not id_posts:
            is_select = self.query.exec(f"SELECT * FROM post")
        elif len(id_posts) > 1:
            is_select = self.query.exec(f"SELECT * FROM post WHERE id IN {id_posts}")
        elif len(id_posts) <= 1:
            is_select = self.query.exec(f"SELECT * FROM post WHERE id = {id_posts[0]}")
        data = []
        if is_select:
            counts = self.query.record().count()
            while self.query.next():
                list_temp = []
                for count in range(counts):
                    list_temp.append(self.query.value(count))
                data.append(list_temp)

            return {'check': True, 'data': data}

        else:
            return {'check': False, 'message': f"{self.query.lastError().databaseText()}"}

    def get_list_script(self):
        query_string = f"""SELECT
                            run_script.id, run_script.interactive, run_script.comment_group, run_script.keyword_content, 
                            account_fb.id, account_fb.name, account_fb.cookie, account_fb.profile, account_fb.pass_word,
                            list_group_key.list_group_name, list_group_key.list_group_id,
                            post.description, post.image, GROUP_CONCAT(script_status.id_status)

                            FROM run_script
                            INNER JOIN account_fb ON account_fb.id = run_script.id_fb
                            LEFT JOIN list_group_key ON list_group_key.id = run_script.id_group_key
                            LEFT JOIN post ON post.id = run_script.id_post_group
                            LEFT JOIN script_status ON script_status.id_script = run_script.id
                            GROUP BY run_script.id
                        """

        is_select = self.query.exec(query_string)
        data = []
        if is_select:
            while self.query.next():
                list_temp = {'id': self.query.value('run_script.id'),
                             'interactive': self.query.value('run_script.interactive'),
                             'keyword_content': self.query.value('run_script.keyword_content'),
                             'comment_group': self.query.value('run_script.comment_group'),

                             'account_fb_id': self.query.value('account_fb.id'),
                             'account_fb_name': self.query.value('account_fb.name'),
                             'account_fb_cookie': self.query.value('account_fb.cookie'),
                             'account_fb_profile': self.query.value('account_fb.profile'),
                             'account_fb_pass': self.query.value('account_fb.pass_word'),

                             'group_name': self.query.value('list_group_key.list_group_name'),
                             'group_id': self.query.value('list_group_key.list_group_id'),

                             'description': self.query.value('post.description'),
                             'image': self.query.value('post.image'),
                             'id_status': self.query.value('GROUP_CONCAT(script_status.id_status)')
                             }
                data.append(list_temp)

            return {'check': True, 'data': data}

        else:
            return {'check': False, 'message': f"{self.query.lastError().databaseText()}"}

    def search_fb(self, table_name, uid):
        is_search = self.query.exec(f"SELECT * FROM {table_name} WHERE id LIKE '%{uid}%'")
        data = []
        if is_search:
            counts = self.query.record().count()
            while self.query.next():
                list_temp = []
                for count in range(counts):
                    list_temp.append(self.query.value(count))
                data.append(list_temp)
            return {'check': True, 'data': data}

        else:
            return {'check': False, 'message': f"{self.query.lastError().databaseText()}"}

    def search_post(self, title):
        is_search = self.query.exec(f"SELECT * FROM post WHERE title LIKE '%{title}%'")
        data = []
        if is_search:
            counts = self.query.record().count()
            while self.query.next():
                list_temp = []
                for count in range(counts):
                    list_temp.append(self.query.value(count))
                data.append(list_temp)
            return {'check': True, 'data': data}

        else:
            return {'check': False, 'message': f"{self.query.lastError().databaseText()}"}

    def delete_table_fb(self, uid):
        is_delete = self.query.exec(f"DELETE FROM account_fb WHERE id = '{uid}'")
        if is_delete:
            return True
        else:
            return False

    def delete_table_post(self, id_post):
        is_delete = self.query.exec(f"DELETE FROM post WHERE id = '{id_post}'")
        return is_delete

    def delete_table_script(self, id_script):
        is_delete = self.query.exec(f"DELETE FROM run_script WHERE id = '{id_script}'")
        return is_delete
