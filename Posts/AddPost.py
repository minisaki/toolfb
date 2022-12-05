
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox
from Posts.AddPostUi import Ui_DialogAddPost


class AddPost(Ui_DialogAddPost, QDialog):
    def __init__(self, database, post=""):
        super(AddPost, self).__init__()

        self.database = database
        self.post = post

        self.setupUi(self)
        self.show()

        self.toolButton_img.clicked.connect(self.open_img)
        self.toolButton.clicked.connect(self.close_dialog)

        if self.post:
            self.toolButton_2.setText("Sửa")
            self.render_post_edit()
            self.toolButton_2.clicked.connect(self.edit_post)
        else:
            self.toolButton_2.setText("Thêm")
            self.toolButton_2.clicked.connect(self.add_post_new)

        self.run()

    def run(self):
        self.exec()

    def close_dialog(self):
        self.dialog.close()

    def add_post_new(self):
        title = self.lineEdit_title.text()
        description = self.textEdit_des.toPlainText()
        note = self.textEdit_note.toPlainText()
        img_path = self.lineEdit_img.text()

        message = self.database.insert_table_post(title, description, img_path, note)
        QMessageBox.about(self, "Save post", message)

    def open_img(self):
        file_name = QFileDialog.getOpenFileNames(self, "Open File Img", filter='img_files(*jpg *jpeg *png)',
                                                 options=QFileDialog.Option.DontUseNativeDialog)

        if file_name[0]:
            self.lineEdit_img.setText(','.join(file_name[0]))

    def render_post_edit(self):
        if self.post:
            self.lineEdit_title.setText(self.post[1])
            self.textEdit_des.setText(self.post[2])
            self.lineEdit_img.setText(self.post[3])
            self.textEdit_note.setText(self.post[4])

    def edit_post(self):
        title = self.lineEdit_title.text()
        description = self.textEdit_des.toPlainText()
        note = self.textEdit_note.toPlainText()
        img_path = self.lineEdit_img.text()

        message = self.database.update_table_post(self.post[0], title, description, note, img_path)
        QMessageBox.about(self, "Edit Post", message)