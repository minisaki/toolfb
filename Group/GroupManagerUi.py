# Form implementation generated from reading ui file 'GroupManagerGui.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Login import LoginFacebook
from ThreadChrome import ThreadClass
import time
import threading


class Ui_DialogGroup(QWidget):
    # def __init__(self, database):
    #     super().__init__()
    #     self.database = database
    #     self.fb_list = {}
    #     self.group_set_key = set()
    #     self.thread = {}

    def setupUi(self, DialogGroup):
        DialogGroup.setObjectName("DialogGroup")
        DialogGroup.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        DialogGroup.setEnabled(True)
        DialogGroup.resize(800, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DialogGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(DialogGroup)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label.setMinimumSize(QtCore.QSize(150, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 35))
        self.comboBox.setObjectName("comboBox")

        # self.render_list_fb()

        # self.comboBox.currentTextChanged.connect(self.combobox_select)
        # self.comboBox.currentTextChanged.connect(self.thed)
        self.horizontalLayout.addWidget(self.comboBox)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_1 = QtWidgets.QLabel(self.widget)
        self.label_1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_1.setMinimumSize(QtCore.QSize(150, 16777215))
        self.label_1.setObjectName("label_1")
        self.label_1.setText("T??? kh??a")
        self.horizontalLayout_3.addWidget(self.label_1)
        self.lineText = QtWidgets.QLineEdit(self.widget)
        self.lineText.setMinimumSize(QtCore.QSize(0, 35))
        self.lineText.setObjectName("lineText")
        self.lineText.setPlaceholderText("Ch???n nh??m theo t??? kh??a, m???i t??? kh??a c??ch nhau b???i d???u (,)")

        # self.lineText.returnPressed.connect(self.search_keywords)
        self.horizontalLayout_3.addWidget(self.lineText)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_2.setMinimumSize(QtCore.QSize(150, 16777215))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("T??n danh s??ch nh??m:")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.lineText_name = QtWidgets.QLineEdit(self.widget)
        self.lineText_name.setMinimumSize(QtCore.QSize(0, 35))
        self.lineText_name.setObjectName("lineText_name")
        self.lineText_name.setPlaceholderText("T??n danh s??ch nh??m")

        self.horizontalLayout_4.addWidget(self.lineText_name)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableWidgetGroup = QtWidgets.QTableWidget(self.widget)
        self.tableWidgetGroup.setObjectName("tableWidgetGroup")
        self.tableWidgetGroup.setColumnCount(3)
        self.tableWidgetGroup.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetGroup.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetGroup.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetGroup.setHorizontalHeaderItem(2, item)
        self.tableWidgetGroup.horizontalHeader().setDefaultSectionSize(180)
        self.tableWidgetGroup.verticalHeader().setDefaultSectionSize(40)
        self.verticalLayout.addWidget(self.tableWidgetGroup)
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toolButtonGetList = QtWidgets.QToolButton(DialogGroup)
        self.toolButtonGetList.setMinimumSize(QtCore.QSize(40, 35))
        self.toolButtonGetList.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.toolButtonGetList.setObjectName("toolButtonGetList")

        # self.toolButtonGetList.clicked.connect(self.get_group_from_fb)
        self.horizontalLayout_2.addWidget(self.toolButtonGetList)
        self.toolButtonCreateGroup = QtWidgets.QToolButton(DialogGroup)
        self.toolButtonCreateGroup.setMinimumSize(QtCore.QSize(0, 35))
        self.toolButtonCreateGroup.setObjectName("toolButtonCreateGroup")

        # self.toolButtonCreateGroup.clicked.connect(self.save_group_list_key)
        self.horizontalLayout_2.addWidget(self.toolButtonCreateGroup)

        self.toolButtonSelectAll = QtWidgets.QToolButton(DialogGroup)
        self.toolButtonSelectAll.setText("Ch???n t???t c???")
        self.toolButtonSelectAll.setMinimumSize(QtCore.QSize(0, 35))
        self.toolButtonSelectAll.setObjectName("toolButtonSelectAll")

        # self.toolButtonSelectAll.clicked.connect(self.event_select_all)
        self.horizontalLayout_2.addWidget(self.toolButtonSelectAll)

        self.toolButtonRefesh = QtWidgets.QToolButton(DialogGroup)
        self.toolButtonRefesh.setText("L??m m???i")
        self.toolButtonRefesh.setMinimumSize(QtCore.QSize(0, 35))
        self.toolButtonRefesh.setObjectName("toolButtonRefesh")

        # self.toolButtonRefesh.clicked.connect(self.combobox_select)
        self.horizontalLayout_2.addWidget(self.toolButtonRefesh)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        # self.toolButtonShowList = QtWidgets.QToolButton(DialogGroup)
        # self.toolButtonShowList.setMinimumSize(QtCore.QSize(0, 35))
        # self.toolButtonShowList.setObjectName("toolButtonShowList")
        self.textEditResult = QtWidgets.QTextEdit(DialogGroup)
        self.textEditResult.setMaximumSize(200, 100)
        self.textEditResult.setText("K???t qu???")
        self.horizontalLayout_2.addWidget(self.textEditResult)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(DialogGroup)
        QtCore.QMetaObject.connectSlotsByName(DialogGroup)

        # self.combobox_select()

    def retranslateUi(self, DialogGroup):
        _translate = QtCore.QCoreApplication.translate
        DialogGroup.setWindowTitle(_translate("DialogGroup", "Qu???n l?? nh??m Facebook"))
        self.label.setText(_translate("DialogGroup", "Ch???n t??i kho???n:"))
        item = self.tableWidgetGroup.horizontalHeaderItem(0)
        item.setText(_translate("DialogGroup", "Id"))
        item = self.tableWidgetGroup.horizontalHeaderItem(1)
        item.setText(_translate("DialogGroup", "Name"))
        item = self.tableWidgetGroup.horizontalHeaderItem(2)
        item.setText(_translate("DialogGroup", "Member"))
        self.toolButtonGetList.setText(_translate("DialogGroup", "Qu??t nh??m"))
        self.toolButtonCreateGroup.setText(_translate("DialogGroup", "T???o danh s??ch nh??m"))
        # self.toolButtonShowList.setText(_translate("DialogGroup", "Hi???n th??? nh??m"))

    # def render_list_fb(self):
    #     fb_list = self.database.get_list_fb(table_name='account_fb')
    #     if fb_list['check']:
    #         for fb in fb_list['data']:
    #             self.fb_list[fb[0].strip()] = fb
    #             self.comboBox.addItem(f"{fb[0]}|{fb[1]}")
    #     else:
    #         QMessageBox.about(self, 'Th??ng b??o', 'Kh??ng c?? t??i kho???n n??o ???????c t??m th???y')
    #
    # def combobox_select(self):
    #     uid = self.comboBox.currentText().split('|')[0].strip()
    #     # print(self.fb_list[uid])
    #     self.render_list_group_fb('group_fb', uid)
    #
    # def search_keywords(self):
    #     uid = self.comboBox.currentText().split('|')[0].strip()
    #     keywords = self.lineText.text()
    #     data = self.database.get_list_fb('group_fb', uid, keywords)
    #     if data['check']:
    #         self.render_list(data['data'])
    #     else:
    #         self.textEditResult.append(data['message'])
    #
    # def render_threading(self, id_group, name, uid):
    #     self.database.insert_table_group_fb(uid, id_group, name)
    #     # self.textEditResult.append(message)
    #     rows = self.tableWidgetGroup.rowCount()
    #     self.tableWidgetGroup.setRowCount(rows + 1)
    #     item = QTableWidgetItem(str(id_group))
    #     item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
    #     item.setCheckState(Qt.CheckState.Unchecked)
    #     self.tableWidgetGroup.setItem(rows, 0, item)
    #     self.tableWidgetGroup.setItem(rows, 1, QTableWidgetItem(str(name)))
    #     self.tableWidgetGroup.scrollToBottom()
    #
    # def get_group_from_fb(self):
    #     uid = self.comboBox.currentText().split('|')[0].strip()
    #     self.textEditResult.append("??ang qu??t group ng???m, vui l??ng ch???...")
    #     self.tableWidgetGroup.setRowCount(0)
    #     self.thread[uid] = ThreadClass(uid=uid, fb=self.fb_list[uid])
    #     self.thread[uid].start()
    #     self.thread[uid].any_single.connect(self.render_threading)
    #     self.thread[uid].mess_login.connect(self.on_message_login)
    #     self.thread[uid].finished.connect(self.on_finished)
    #
    # def on_finished(self):
    #     self.textEditResult.append('Ho??n th??nh')
    #
    # def on_message_login(self, message):
    #     self.textEditResult.append(message)
    #
    # def render_list(self, data):
    #     self.tableWidgetGroup.setRowCount(0)
    #     for fb in data:
    #         rows = self.tableWidgetGroup.rowCount()
    #         self.tableWidgetGroup.setRowCount(rows + 1)
    #         item = QTableWidgetItem(str(fb[1]))
    #         item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
    #         item.setCheckState(Qt.CheckState.Unchecked)
    #         self.tableWidgetGroup.setItem(rows, 0, item)
    #         for idx, item in enumerate(fb):
    #             if idx > 1:
    #                 self.tableWidgetGroup.setItem(rows, idx-1, QTableWidgetItem(str(item)))
    #     self.tableWidgetGroup.resizeColumnsToContents()
    #
    # def render_list_group_fb(self, table_name, uid):
    #     data = self.database.get_list_fb(table_name, uid)
    #     if data['check']:
    #         self.render_list(data['data'])
    #     else:
    #         self.textEditResult.append(data['message'])
    #
    # def event_select_all(self):
    #     rows = self.tableWidgetGroup.rowCount()
    #     for row in range(rows):
    #         self.tableWidgetGroup.item(row, 0).setCheckState(Qt.CheckState.Checked)
    #         # self.group_list_key.append(self.tableWidgetGroup.item(row, 0).text())
    #     # print(self.group_list_key)
    #
    # def get_group_checked(self):
    #     rows = self.tableWidgetGroup.rowCount()
    #     self.group_set_key = set()
    #     for row in range(rows):
    #         if self.tableWidgetGroup.item(row, 0).checkState() == Qt.CheckState.Checked:
    #             self.group_set_key.add(self.tableWidgetGroup.item(row, 0).text())
    #
    # def save_group_list_key(self):
    #     uid = self.comboBox.currentText().split('|')[0].strip()
    #     group_key = self.lineText.text()
    #     group_name = self.lineText_name.text()
    #     self.get_group_checked()
    #     group_list_key = list(self.group_set_key)
    #     if not group_list_key:
    #         QMessageBox.about(self, "Th??ng b??o", "B???n ch??a ch???n nh??m")
    #         return
    #     if not group_name:
    #         QMessageBox.about(self, "Th??ng b??o", "Vui l??ng ?????t t??n nh??m c???n t???o")
    #         return
    #     list_group_id = ','.join(group_list_key)
    #     message = self.database.insert_table_list_group_key(uid, list_group_id, group_name, group_key)
    #     self.textEditResult.append(message)


