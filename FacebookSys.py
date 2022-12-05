from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QPushButton, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
# from MainUi import Ui_MainWindow
from MainProGui import Ui_MainWindow
# from AccountMannagerUI import Ui_Dialog_fb
from Account.AccountManager import Account
from Posts.PostManager import Post
from Group.GroupManager import GroupManager
from Script.ScriptManager import ScriptManager

from Database import DatabaseFacebook

from ThreadingRunScript import ThreadClassRunFb


class FacebookSystem(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.fb_thread = {}
        self.database = DatabaseFacebook('admin', 'admin123')

        self.setupUi(self)
        self.style()
        self.show()
        self.run()

        # self.ui = uic.loadUi("MainProUI.ui", self)
        # self.ui.show()

    def run(self):
        self.toolButton_account.clicked.connect(self.account_manager)
        self.toolButton_group.clicked.connect(self.group_manager)
        self.toolButton_posts.clicked.connect(self.post_manager)
        self.toolButton_add.clicked.connect(self.setting_manager)
        self.toolButton_view.clicked.connect(self.get_list_script)
        self.toolButton_delete.clicked.connect(self.delete_script)
        self.get_list_script()

    def style(self):
        self.label.setFont(QFont("Times New Roman", 12))
        self.label_2.setFont(QFont("Times New Roman", 12))

    def account_manager(self):
        Account(database=self.database)

    def group_manager(self):
        GroupManager(database=self.database)

    def post_manager(self):
        Post(database=self.database)

    def setting_manager(self):
        ScriptManager(database=self.database)

    def render_script(self, data):
        self.tableWidget.setRowCount(0)
        for fb in data:
            rows = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rows + 1)
            item = QTableWidgetItem(str(fb[0]))
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.tableWidget.setItem(rows, 0, item)
            for idx, item in enumerate(fb):
                if idx > 0:
                    self.tableWidget.setItem(rows, idx, QTableWidgetItem(str(item)))

        self.tableWidget.resizeColumnsToContents()

    def get_list_script(self):
        self.data = self.database.get_list_script()
        if self.data['check']:
            self.tableWidget.setRowCount(0)
            for idx, list_script in enumerate(self.data['data']):
                if list_script['id_status']:
                    id_posts = tuple(int(id_post) for id_post in list_script['id_status'].split(','))
                    list_post = self.database.get_list_post(id_posts=id_posts)
                    if list_post['check']:
                        self.data['data'][idx]['list_post_status'] = list_post['data']
                    else:
                        QMessageBox.critical(self, 'Lấy bài viết', list_post['message'])
                else:
                    self.data['data'][idx]['list_post_status'] = []

                list_action = []
                rows = self.tableWidget.rowCount()

                self.tableWidget.setRowCount(rows + 1)

                item = QTableWidgetItem(str(list_script['id']))
                self.tableWidget.setItem(rows, 0, item)
                self.tableWidget.setColumnHidden(0, True)

                item = QTableWidgetItem(str(list_script['account_fb_id']))
                item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                item.setCheckState(Qt.CheckState.Unchecked)

                self.tableWidget.setItem(rows, 1, item)

                self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(list_script['account_fb_name'])))
                self.btn_run = QPushButton('Chạy')
                font = QFont()
                font.setBold(False)
                font.setWeight(500)
                font.setPointSize(11)
                self.btn_run.setFont(font)
                self.btn_run.setStyleSheet("""QPushButton {
                
                                                background-color:  #339af0;
                                                color: #FFFFFF;
                                                border-style: outset;
                                                padding: 2px 10px;
                                                min-width: 5em;
                                            }
                                            QPushButton:hover {
                                                background-color: #1864ab;
                                                color: #FFFFFF;
                                            }
                                            QPushButton:pressed {
                                                background-color: white;
                                                color: black;
                                            }
                                            QPushButton:disabled {
                                                background-color:#adb5bd;
                                                color: #868e96;
                                            } 
                                             
                                            """)
                self.btn_run.clicked.connect(self.handle_btn_run)
                self.tableWidget.setCellWidget(rows, 3, self.btn_run)

                self.btn_stop = QPushButton('Dừng')
                self.btn_stop.setEnabled(False)
                self.btn_stop.setStyleSheet("""QPushButton {
                                                                background-color:  #339af0;
                                                                color: #FFFFFF;
                                                                border-style: outset;
                                                                padding: 2px 10px;
                                                                min-width: 5em;
                                                            }
                                                            QPushButton:hover {
                                                                background-color: #1864ab;
                                                                color: #FFFFFF;
                                                            }
                                                            QPushButton:pressed {
                                                                background-color: white;
                                                                color: black;
                                                            }
                                                            QPushButton:disabled {
                                                                background-color:#adb5bd;
                                                                color: #868e96;
                                                            }                                                        
                                                            """)
                self.btn_stop.clicked.connect(self.handle_btn_stop)

                self.tableWidget.setCellWidget(rows, 4, self.btn_stop)
                self.btn_exit = QPushButton('Tắt')
                self.btn_exit.setEnabled(False)
                self.btn_exit.setStyleSheet("""QPushButton {
                                                    background-color:  #339af0;
                                                    color: #FFFFFF;
                                                    border-style: outset;
                                                    padding: 2px 10px;
                                                    min-width: 5em;
                                                }
                                                QPushButton:hover {
                                                    background-color: #1864ab;
                                                    color: #FFFFFF;
                                                }
                                                QPushButton:pressed {
                                                    background-color: white;
                                                    color: black;
                                                }
                                                QPushButton:disabled {
                                                    background-color:#adb5bd;
                                                    color: #868e96;
                                                } 
                                                """)
                self.tableWidget.setCellWidget(rows, 5, self.btn_exit)
                self.btn_exit.clicked.connect(self.exit_thread)

                self.__setattr__(f'lineEdit_result_{rows}', QTextEdit())
                self.__getattribute__(f'lineEdit_result_{rows}').setFixedHeight(30)
                self.__getattribute__(f'lineEdit_result_{rows}').setText("Hiện kết quả chạy")
                self.__getattribute__(f'lineEdit_result_{rows}').setStyleSheet("""QTextEdit {background-color: #fff;
                                                                               color: #339af0;
                                                                                }""")
                # self.btn_sell.clicked.connect(self.handleButtonClicked)
                self.tableWidget.setCellWidget(rows, 6, self.__getattribute__(f'lineEdit_result_{rows}'))

                if list_script['group_name']:
                    list_action.append('Đăng bài group')
                if list_script['id_status']:
                    list_action.append('Đăng bài status')
                if list_script['interactive']:
                    list_action.append('Tương tác bạn bè')
                if list_script['comment_group']:
                    list_action.append('Bình luận vào bài viết trong group')

                action = '->'.join(list_action)
                self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(action)))
                if rows % 2:
                    self.tableWidget.item(rows, 1).setBackground(QColor('#868e96'))
                    self.tableWidget.item(rows, 2).setBackground(QColor('#868e96'))
                    # self.tableWidget.cellWidget(rows, 3).setStyleSheet("background-color: red")
                    # self.tableWidget.cellWidget(rows, 4).setStyleSheet("background-color: red")
                else:
                    self.tableWidget.item(rows, 1).setBackground(QColor('#495057'))
                    self.tableWidget.item(rows, 2).setBackground(QColor('#495057'))

            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
        else:
            QMessageBox.critical(self, 'Lấy bài viết', self.data['message'])

    def result(self, message, row):
        self.__getattribute__(f'lineEdit_result_{row}').setText(message)

    def on_finished(self, thread_fb):
        thread_fb.driver.close()

    def handle_btn_run(self):
        button = self.sender()
        button.setEnabled(False)
        index = self.tableWidget.indexAt(button.pos())
        button_stop = self.tableWidget.cellWidget(index.row(), 4)
        button_stop.setEnabled(True)
        if index.isValid():
            id_thread = index.row()
            if id_thread in self.fb_thread:
                self.fb_thread[id_thread].thread_resume()
                self.result(f"Đang hoạt động", id_thread)
            else:
                data_id_thread = self.data['data'][id_thread]
                print(f"data_id_thread {data_id_thread}")
                self.fb_thread[id_thread] = ThreadClassRunFb(dict_data=data_id_thread,
                                                             row=id_thread,
                                                             index=self.count)
                self.count += 1
                self.fb_thread[id_thread].start()
                self.fb_thread[id_thread].any_single.connect(self.result)
                # self.fb_thread[id_thread].finished.connect(self.fb_thread[id_thread].close_driver)

    def handle_btn_stop(self):
        button = self.sender()
        button.setEnabled(False)
        index = self.tableWidget.indexAt(button.pos())
        button_run = self.tableWidget.cellWidget(index.row(), 3)
        button_run.setEnabled(True)
        button_exit = self.tableWidget.cellWidget(index.row(), 5)
        button_exit.setEnabled(True)

        if index.isValid():
            id_thread = index.row()
            self.fb_thread[id_thread].thread_pause()
            self.result(f"Đang tạm dừng luồng {id_thread}", id_thread)

    def result_exit_thread(self, message, row):
        self.__getattribute__(f'lineEdit_result_{row}').setText(message)
        self.tableWidget.cellWidget(row, 4).setEnabled(True)

    def exit_thread(self):
        button = self.sender()
        button.setEnabled(False)
        index = self.tableWidget.indexAt(button.pos())
        button_run = self.tableWidget.cellWidget(index.row(), 3)
        button_run.setEnabled(True)
        button_stop = self.tableWidget.cellWidget(index.row(), 4)
        button_stop.setEnabled(False)

        if index.isValid():
            id_thread = index.row()
            self.fb_thread[id_thread].thread_stop()
            self.fb_thread[id_thread].any_single.connect(self.result_exit_thread)
            if self.fb_thread[id_thread].isFinished():
                self.result(f"Thoát luồng {id_thread}", id_thread)
                del self.fb_thread[id_thread]

    def delete_script(self):
        rows = self.tableWidget.rowCount()
        for row in range(rows):
            if self.tableWidget.item(row, 1).checkState() == Qt.CheckState.Checked:
                print(self.tableWidget.item(row, 0).text())
                result = self.database.delete_table_script(id_script=self.tableWidget.item(row, 0).text())
                if not result:
                    QMessageBox.critical(self, 'Xóa kịch bản', 'Xóa kịch bản không thành công')

        self.get_list_script()

