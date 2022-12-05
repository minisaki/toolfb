from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, QObject, QSize
from PyQt6.QtGui import QFont, QColor
from Account.AccountMannagerUI import Ui_Dialog_fb
from Account.AddAccount import AddAccount
from PyQt6 import uic


class Account(QDialog, Ui_Dialog_fb):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.setupUi(self)
        # self.ui = uic.loadUi("AccountManagerGui.ui", self)
        self.style()
        self.show()
        self.run()

    def run(self):

        self.render_list_fb()
        self.pushButton_search.clicked.connect(self.search_list_fb)
        self.lineEdit_search_fb.returnPressed.connect(self.pushButton_search.click)
        self.pushButton_reset.clicked.connect(self.render_list_fb)
        self.pushButton_add_fb.clicked.connect(self.show_dialog)
        self.pushButton_edit_fb.clicked.connect(self.show_dialog_edit)
        self.pushButton_delete_fb.clicked.connect(self.delete_list_fb)

        self.exec()

    def style(self):
        self.setFont(QFont("Times New Roman", 12))
        self.tableWidget_fb.setFont(QFont("Times New Roman", 12))
        self.lineEdit_search_fb.setMinimumSize(QSize(0, 40))
        self.pushButton_search.setMinimumSize(QSize(0, 40))

    def show_dialog(self):
        AddAccount(self.database)

    def show_dialog_edit(self):
        data = self.event_select()
        if data:
            # dialog = QDialog()
            # ui = Ui_Dialog_Add_Account(self.database, data=data)
            AddAccount(self.database, data=data)
            # ui.setupUi(dialog)
            # dialog.exec()
        else:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn 1 tài khoản để sửa")

    def render_list(self, data):
        self.tableWidget_fb.setRowCount(0)
        for fb in data:
            rows = self.tableWidget_fb.rowCount()
            self.tableWidget_fb.setRowCount(rows + 1)
            item = QTableWidgetItem(str(fb[0]))
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            if rows % 2:
                item.setBackground(QColor("#ced4da"))
            self.tableWidget_fb.setItem(rows, 0, item)
            # self.tableWidget_fb.item(rows, 0).setBackground(QColor("#adb5bd"))
            for idx, item in enumerate(fb):
                if idx > 0:
                    widgetItem = QTableWidgetItem(item)
                    if rows % 2:
                        widgetItem.setBackground(QColor("#ced4da"))
                    self.tableWidget_fb.setItem(rows, idx, widgetItem)

        self.tableWidget_fb.resizeColumnsToContents()

            # self.tableWidget_fb.resizeRowsToContents()

    def render_list_fb(self):
        data = self.database.get_list_fb(table_name='account_fb')
        if data['check']:
            self.render_list(data=data['data'])
                # self.tableWidget_fb.resizeColumnsToContents()
        else:
            print(data['message'])

    def search_list_fb(self):
        uid = self.lineEdit_search_fb.text()
        data = self.database.search_fb(table_name='account_fb', uid=uid)

        if data['check']:
            self.render_list(data['data'])
        else:
            print(data['message'])

    def event_select(self):
        rows = self.tableWidget_fb.rowCount()
        for row in range(rows):
            if self.tableWidget_fb.item(row, 0).checkState() == Qt.CheckState.Checked:
                return [self.tableWidget_fb.item(row, 0).text(),
                        self.tableWidget_fb.item(row, 1).text(),
                        self.tableWidget_fb.item(row, 2).text(),
                        self.tableWidget_fb.item(row, 3).text(),
                        self.tableWidget_fb.item(row, 4).text(),
                        self.tableWidget_fb.item(row, 5).text()]

        return None

    def delete_list_fb(self):
        rows = self.tableWidget_fb.rowCount()
        for row in range(rows):
            if self.tableWidget_fb.item(row, 0).checkState() == Qt.CheckState.Checked:
                result = self.database.delete_table_fb(uid=self.tableWidget_fb.item(row, 0).text())
                if not result:
                    QMessageBox.critical(self, 'Xóa tài khoản', 'Xóa tài khoản không thành công')

        self.render_list_fb()
