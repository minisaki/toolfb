from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from Group.GroupManagerUi import Ui_DialogGroup


class GroupManager(QDialog, Ui_DialogGroup):
    def __init__(self, database):
        super(GroupManager, self).__init__()
        self.database = database
        self.group_set_key = set()
        self.fb_list = {}
        self.thread = {}

        self.setupUi(self)
        self.show()
        self.run()

    def run(self):
        self.render_list_fb()
        self.comboBox.currentIndexChanged.connect(self.combobox_select)
        self.lineText.returnPressed.connect(self.search_keywords)
        self.toolButtonGetList.clicked.connect(self.get_group_from_fb)
        self.toolButtonCreateGroup.clicked.connect(self.save_group_list_key)
        self.toolButtonSelectAll.clicked.connect(self.event_select_all)
        self.toolButtonRefesh.clicked.connect(self.combobox_select)

        self.combobox_select()

        self.exec()

    def render_list_fb(self):
        fb_list = self.database.get_list_fb(table_name='account_fb')
        if fb_list['check']:
            for fb in fb_list['data']:
                self.fb_list[fb[0].strip()] = fb
                self.comboBox.addItem(fb[1], fb[0])
        else:
            QMessageBox.about(self, 'Thông báo', 'Không có tài khoản nào được tìm thấy')

    def combobox_select(self):
        uid = self.comboBox.currentData()
        self.render_list_group_fb('group_fb', uid)

    def search_keywords(self):
        uid = self.comboBox.currentData()
        keywords = self.lineText.text()
        data = self.database.get_list_fb('group_fb', uid, keywords)
        if data['check']:
            self.render_list(data['data'])
        else:
            self.textEditResult.append(data['message'])

    def render_threading(self, id_group, name, uid):
        self.database.insert_table_group_fb(uid, id_group, name)
        # self.textEditResult.append(message)
        rows = self.tableWidgetGroup.rowCount()
        self.tableWidgetGroup.setRowCount(rows + 1)
        item = QTableWidgetItem(str(id_group))
        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        item.setCheckState(Qt.CheckState.Unchecked)
        self.tableWidgetGroup.setItem(rows, 0, item)
        self.tableWidgetGroup.setItem(rows, 1, QTableWidgetItem(str(name)))
        self.tableWidgetGroup.scrollToBottom()

    def get_group_from_fb(self):
        uid = self.comboBox.currentData()
        self.textEditResult.append("Đang quét group ngầm, vui lòng chờ...")
        self.tableWidgetGroup.setRowCount(0)
        self.thread[uid] = ThreadClass(uid=uid, fb=self.fb_list[uid])
        self.thread[uid].start()
        self.thread[uid].any_single.connect(self.render_threading)
        self.thread[uid].mess_login.connect(self.on_message_login)
        self.thread[uid].finished.connect(self.on_finished)

    def on_finished(self):
        self.textEditResult.append('Hoàn thành')

    def on_message_login(self, message):
        self.textEditResult.append(message)

    def render_list(self, data):
        self.tableWidgetGroup.setRowCount(0)
        for fb in data:
            rows = self.tableWidgetGroup.rowCount()
            self.tableWidgetGroup.setRowCount(rows + 1)
            item = QTableWidgetItem(str(fb[1]))
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.tableWidgetGroup.setItem(rows, 0, item)
            for idx, item in enumerate(fb):
                if idx > 1:
                    self.tableWidgetGroup.setItem(rows, idx-1, QTableWidgetItem(str(item)))
        self.tableWidgetGroup.resizeColumnsToContents()

    def render_list_group_fb(self, table_name, uid):
        data = self.database.get_list_fb(table_name, uid)
        if data['check']:
            self.render_list(data['data'])
        else:
            self.textEditResult.append(data['message'])

    def event_select_all(self):
        rows = self.tableWidgetGroup.rowCount()
        for row in range(rows):
            self.tableWidgetGroup.item(row, 0).setCheckState(Qt.CheckState.Checked)
            # self.group_list_key.append(self.tableWidgetGroup.item(row, 0).text())
        # print(self.group_list_key)

    def get_group_checked(self):
        rows = self.tableWidgetGroup.rowCount()
        self.group_set_key = set()
        for row in range(rows):
            if self.tableWidgetGroup.item(row, 0).checkState() == Qt.CheckState.Checked:
                self.group_set_key.add(self.tableWidgetGroup.item(row, 0).text())

    def save_group_list_key(self):
        uid = self.comboBox.currentData()
        group_key = self.lineText.text()
        group_name = self.lineText_name.text()
        self.get_group_checked()
        group_list_key = list(self.group_set_key)
        if not group_list_key:
            QMessageBox.about(self, "Thông báo", "Bạn chưa chọn nhóm")
            return
        if not group_name:
            QMessageBox.about(self, "Thông báo", "Vui lòng đặt tên nhóm cần tạo")
            return
        list_group_id = ','.join(group_list_key)
        message = self.database.insert_table_list_group_key(uid, list_group_id, group_name, group_key)
        self.textEditResult.append(message)




