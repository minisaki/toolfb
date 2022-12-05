from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QStandardItem
from Script.SettingGui import Ui_DialogSetting


class CheckableComboBox(QComboBox):
    def __init__(self):
        super().__init__()

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, wdiget, event):
        if wdiget == self.lineEdit():
            if event.type() == QEvent.Type.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if wdiget == self.view().viewport():
            if event.type() == QEvent.Type.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.CheckState.Checked:
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(Qt.CheckState.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.CheckState.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)
        self.lineEdit().setText(text)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        datalist = texts
        for i, text in enumerate(texts):
            try:
                data = str(datalist[i][0])
            except (TypeError, IndexError):
                data = None
            self.addItem(text[1], data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.CheckState.Checked:
                res.append(self.model().item(i).data())
        return res


class ScriptManager(Ui_DialogSetting):
    def __init__(self, database):
        super(ScriptManager, self).__init__()
        self.dialog = QDialog()
        self.database = database
        self.fb_list = {}
        self.reseult = {}

        self.setupUi(self.dialog)
        self.comboBox_4 = CheckableComboBox()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy)
        self.comboBox_4.setMinimumSize(QtCore.QSize(380, 35))
        self.comboBox_4.setObjectName("comboBox_4")
        self.horizontalLayout_3.addWidget(self.comboBox_4)

        self.comboBox_4.setEnabled(False)
        self.comboBox_2.setEnabled(False)
        self.comboBox_3.setEnabled(False)
        self.textEdit.setEnabled(False)
        self.textEdit_2.setEnabled(False)
        self.lineEdit_keyword.setEnabled(False)

        self.dialog.show()

        self.run()
        # self.event_checkbox()

    def run(self):
        self.comboBox.currentIndexChanged.connect(self.render_list_group)

        self.render_list_fb()
        self.render_list_post()
        self.render_list_group()

        self.checkBox_2.stateChanged.connect(self.toggle_checkbox_2)
        self.checkBox.stateChanged.connect(self.toggle_checkbox)
        self.checkBox_3.stateChanged.connect(self.toggle_checkbox_3)
        self.checkBox_4.stateChanged.connect(self.toggle_checkbox_4)
        self.toolButton.clicked.connect(self.add_run_script)
        self.toolButton_2.clicked.connect(self.close_dialog)

        self.dialog.exec()

    def render_list_fb(self):
        fb_list = self.database.get_list_fb(table_name='account_fb')
        if fb_list['check']:
            for fb in fb_list['data']:
                self.fb_list[fb[0].strip()] = fb
                self.comboBox.addItem(fb[1], fb[0])
        else:
            QMessageBox.about(self, 'Thông báo', 'Không có tài khoản nào được tìm thấy')

    def render_list_group(self):
        # self.comboBox_2.setEnabled(True)
        self.comboBox_2.clear()
        uid = self.comboBox.currentData()
        list_group_key = self.database.get_list_group_key(uid)
        # print(list_group_key['data'])
        if list_group_key['check']:
            if list_group_key['data']:
                for list_group in list_group_key['data']:
                    # self.fb_list[fb[0].strip()] = fb
                    self.comboBox_2.addItem(str(list_group[2]), list_group[0])
            else:
                self.comboBox_2.clear()
                self.comboBox_2.setEnabled(False)
        else:
            QMessageBox.about(self, 'Thông báo', 'Không có danh sách nhóm')

    def render_list_post(self):
        list_post = self.database.get_list_post()
        if list_post['check']:
            self.comboBox_4.addItems(list_post['data'])
            for post in list_post['data']:
                # self.fb_list[fb[0].strip()] = fb
                self.comboBox_3.addItem(str(post[1]), post[0])
                # self.comboBox_4.addItem(f"{str(post[0])}|{post[1]}")
        else:
            QMessageBox.about(self.dialog, 'Thông báo', 'Không có bài viết')

    def close_dialog(self):
        self.dialog.close()

    def select_checkbox(self):
        self.reseult['fb_id'] = self.comboBox.currentData()
        if self.checkBox_2.isChecked():
            self.reseult['group_key'] = self.comboBox_2.currentData()
            self.reseult['id_post'] = self.comboBox_3.currentData()
        else:
            self.reseult['group_key'] = ""
            self.reseult['id_post'] = ""

        if self.checkBox.isChecked():
            self.comboBox_4.setEnabled(True)
            self.reseult['post_wall'] = self.comboBox_4.currentData()
        else:
            self.reseult['post_wall'] = []

        if self.checkBox_3.isChecked():
            self.reseult['comment_post'] = self.textEdit.toPlainText()
        else:
            self.reseult['comment_post'] = ""

        if self.checkBox_4.isChecked():
            self.reseult['comment_group'] = self.textEdit_2.toPlainText()
            self.reseult['keyword'] = self.lineEdit_keyword.text()
        else:
            self.reseult['comment_group'] = ""
            self.reseult['keyword'] = ""

        # print(self.reseult)

    def add_run_script(self):
        self.select_checkbox()
        message = self.database.insert_table_run_script(self.reseult)
        QMessageBox.about(self.dialog, "Thêm cấu hình kịch bản", message)

    def toggle_checkbox(self):
        if self.checkBox.isChecked():
            self.comboBox_4.setEnabled(True)
        else:
            self.comboBox_4.setEnabled(False)

    def toggle_checkbox_2(self):
        if self.checkBox_2.isChecked():
            self.comboBox_2.setEnabled(True)
            self.comboBox_3.setEnabled(True)
        else:
            self.comboBox_2.setEnabled(False)
            self.comboBox_3.setEnabled(False)

    def toggle_checkbox_3(self):
        if self.checkBox_3.isChecked():
            self.textEdit.setEnabled(True)
        else:
            self.textEdit.setEnabled(False)

    def toggle_checkbox_4(self):
        if self.checkBox_4.isChecked():
            self.textEdit_2.setEnabled(True)
            self.lineEdit_keyword.setEnabled(True)
        else:
            self.textEdit_2.setEnabled(False)
            self.lineEdit_keyword.setEnabled(False)



