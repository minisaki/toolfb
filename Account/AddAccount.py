from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QWidget, QFileDialog
from PyQt6.QtCore import QCoreApplication

from Account.AddAccountUi import Ui_Dialog_Add_Account


class AddAccount(QDialog, Ui_Dialog_Add_Account):
    def __init__(self, database, data=None):
        super(AddAccount, self).__init__()
        self.database = database
        self.data = data

        self.setupUi(self)
        self.show()
        self.run()

    def run(self):
        if self.data:
            self.render_edit()
            self.pushButton_add.setText("Sửa")

        self.toolButton_path.clicked.connect(self.folder_open)
        self.pushButton_cancel.clicked.connect(self.close_dialog)
        self.pushButton_add.clicked.connect(self.add_account)

        self.exec()

    def close_dialog(self):
        self.dialog.close()

    def render_edit(self):
        self.lineEdit_uid.setText(self.data[0])
        self.lineEdit_name.setText(self.data[1])
        self.lineEdit_cookie.setText(self.data[2])
        self.lineEdit_profile.setText(self.data[3])
        self.lineEdit_pass.setText(self.data[4])

    def folder_open(self):
        file_name = str(QFileDialog.getExistingDirectory(self, "Open Directory",  options=QFileDialog.Option.DontUseNativeDialog))
        print(file_name)
        if file_name:
            self.lineEdit_profile.setText(file_name)

    def add_account(self):
        uid = self.lineEdit_uid.text()
        name = self.lineEdit_name.text()
        cookie = self.lineEdit_cookie.text()
        profile = self.lineEdit_profile.text()
        pass_word = self.lineEdit_pass.text()

        if self.data:
            message = self.database.update_table_fb(uid, name, cookie, profile, pass_word)
            self.label_result.setText(message)
        else:
            message = self.database.insert_table_fb(uid, name, cookie, profile, pass_word)
            self.label_result.setText(message)

        if 'thành công' in message:
            self.lineEdit_uid.setText("")
            self.lineEdit_name.setText("")
            self.lineEdit_pass.setText("")
            self.lineEdit_cookie.setText("")
            self.lineEdit_profile.setText("")