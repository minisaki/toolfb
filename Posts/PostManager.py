from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QDialog
from PyQt6.QtCore import Qt
# from Posts.AddPost import AddPost
from Posts.AddPost import AddPost

from Posts.PostManagerUi import Ui_DialogPost


class Post(QDialog, Ui_DialogPost):
    def __init__(self, database):
        super(Post, self).__init__()

        self.database = database

        self.setupUi(self)
        self.show()

        self.pushButton_search.clicked.connect(self.search_post)
        self.toolButton_get_list.clicked.connect(self.get_post)
        self.toolButton_add.clicked.connect(self.show_add_post)
        self.toolButton_edit.clicked.connect(self.show_edit_post)
        self.toolButton_del.clicked.connect(self.delete_post)

        self.get_post()

        self.run()

    def run(self):
        self.exec()

    def show_add_post(self):
        AddPost(database=self.database)

    def show_edit_post(self):
        post = self.select_post()
        if post:
            AddPost(database=self.database, post=post)
        else:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn 1 tài khoản để sửa")

    def render_post(self, posts):
        self.tableWidgetPost.setRowCount(0)
        for post in posts:
            rows = self.tableWidgetPost.rowCount()
            self.tableWidgetPost.setRowCount(rows + 1)
            item = QTableWidgetItem(str(post[0]))
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.tableWidgetPost.setItem(rows, 0, item)
            for idx, item in enumerate(post):
                if idx > 0:
                    self.tableWidgetPost.setItem(rows, idx, QTableWidgetItem(str(item)))
        self.tableWidgetPost.resizeColumnsToContents()

    def get_post(self):
        post_list = self.database.get_list_fb(table_name='post')
        if post_list['check']:
            self.render_post(post_list['data'])
            # for post in post_list['data']:
            #     self.fb_list[fb[0].strip()] = fb
            #     self.comboBox.addItem(f"{fb[0]}|{fb[1]}")
        else:
            QMessageBox.about(self, 'Thông báo', 'Không có tài khoản nào được tìm thấy')

    def select_post(self):
        rows = self.tableWidgetPost.rowCount()
        columns = self.tableWidgetPost.columnCount()
        data = []
        for row in range(rows):
            if self.tableWidgetPost.item(row, 0).checkState() == Qt.CheckState.Checked:
                for col in range(columns):
                    data.append(self.tableWidgetPost.item(row, col).text())
                return data

        return None

    def delete_post(self):
        rows = self.tableWidgetPost.rowCount()
        for row in range(rows):
            if self.tableWidgetPost.item(row, 0).checkState() == Qt.CheckState.Checked:
                result = self.database.delete_table_post(self.tableWidgetPost.item(row, 0).text())
                if not result:
                    QMessageBox.critical(self, 'Xóa tài khoản', 'Xóa tài khoản không thành công')

        self.get_post()

    def search_post(self):
        title = self.lineEdit_search.text()
        post_list = self.database.search_post(title)
        if post_list['check']:
            self.render_post(post_list['data'])
        else:
            QMessageBox.about(self, 'Thông báo', 'Không có tài khoản nào được tìm thấy')