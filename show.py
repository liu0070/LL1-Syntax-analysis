from window import Ui_MainWindow
import removeLeft
from PyQt5 import QtCore, QtWidgets
import sys


class My_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(My_Window, self).__init__()
        self.setupUi(self)
        self.infinite = {}
        self.name_get = []
        self.table = {}
        self.FIRST = {}
        self.FOLLOW = {}
        self.expression = ""
        filename = 'rule.txt'
        self.expression = removeLeft.expressGet(filename)
        self.infinite, self.name_get = removeLeft.removeLeft(self.expression)
        self.LL_judge = removeLeft.LL_judge(self.infinite)
        removeLeft.FIRST_get(self.infinite)
        removeLeft.FOLLOW_get(self.infinite, 0)
        if not self.LL_judge:
            QtWidgets.QMessageBox.warning(self, "警告", "当前文法不是LL(1)文法请修改文法内容，文法修改文件路径:rule.txt",
                                          QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
        else:
            self.table = removeLeft.LL_create_table(self.infinite)
            self.start = 0

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        if not self.LL_judge:
            QtWidgets.QMessageBox.warning(self, "警告", "当前文法不是LL(1)文法请修改文法内容，文法修改文件路径:rule.txt",
                                          QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
        else:
            expresses = self.plainTextEdit.toPlainText()
            print(expresses)
            expresses.strip()
            if len(expresses) == 0:
                QtWidgets.QMessageBox.warning(self, "警告", "表达式为空！", QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.Yes)
            else:
                if expresses[-1] != '#':
                    expresses += '#'
                temp_stack, temp_express, create_uses, actions = removeLeft.LL_analyse(self.table, expresses,
                                                                                       self.start)
                row = len(temp_stack)
                self.tableWidget.setRowCount(row)
                self.tableWidget.setColumnCount(4)
                for i in range(row):
                    item1 = QtWidgets.QTableWidgetItem(''.join(temp_stack[i]))
                    item2 = QtWidgets.QTableWidgetItem(''.join(temp_express[i]))
                    item3 = QtWidgets.QTableWidgetItem(''.join(create_uses[i]))
                    item4 = QtWidgets.QTableWidgetItem(str(actions[i]))
                    self.tableWidget.setItem(i, 0, item1)
                    self.tableWidget.setItem(i, 1, item2)
                    self.tableWidget.setItem(i, 2, item3)
                    self.tableWidget.setItem(i, 3, item4)

    @QtCore.pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.plainTextEdit.clear()
        self.tableWidget.clear()

    @QtCore.pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        row = len(self.table.keys())
        inputSet = set()
        for name in self.table.keys():
            for s in self.table[name].keys():
                inputSet.add(s)
        self.tableWidget.setRowCount(row + 1)
        self.tableWidget.setColumnCount(len(inputSet) + 1)
        j = 1
        for s in inputSet:
            item1 = QtWidgets.QTableWidgetItem(str(s))
            self.tableWidget.setItem(0, j, item1)
            j += 1
        i = 1
        for name in self.table.keys():
            item1 = QtWidgets.QTableWidgetItem(str(name))
            self.tableWidget.setItem(i, 0, item1)
            i += 1
        i = 1
        for name in self.table.keys():
            j = 1
            for s in inputSet:
                item1 = QtWidgets.QTableWidgetItem(str(self.table[name][s]))
                self.tableWidget.setItem(i, j, item1)
                j += 1
            i += 1

    @QtCore.pyqtSlot()
    def on_pushButton_4_clicked(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setColumnCount(len(self.infinite.keys()))
        self.tableWidget.setRowCount(2)
        j = 0
        for name in self.infinite.keys():
            item1 = QtWidgets.QTableWidgetItem(str(name))
            self.tableWidget.setItem(0, j, item1)
            item2 = QtWidgets.QTableWidgetItem(','.join(self.infinite[name].FIRST.keys()))
            self.tableWidget.setItem(1, j, item2)
            j += 1

    @QtCore.pyqtSlot()
    def on_pushButton_5_clicked(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setColumnCount(len(self.infinite.keys()))
        self.tableWidget.setRowCount(2)
        j = 0
        for name in self.infinite.keys():
            item1 = QtWidgets.QTableWidgetItem(str(name))
            self.tableWidget.setItem(0, j, item1)
            item2 = QtWidgets.QTableWidgetItem(','.join(self.infinite[name].FOLLOW))
            self.tableWidget.setItem(1, j, item2)
            j += 1

    @QtCore.pyqtSlot()
    def on_pushButton_6_clicked(self):
        file, ok = QtWidgets.QFileDialog.getOpenFileName(self, '选择文法文件', './', 'Files(*txt)')
        if ok:
            if file:
                self.expression = removeLeft.expressGet(file)
                if self.expression is None:
                    QtWidgets.QMessageBox.warning(self, "警告", "当前文法不是LL(1)文法请修改文法内容",
                                                  QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
                else:
                    self.infinite, self.name_get = removeLeft.removeLeft(self.expression)
                    removeLeft.FIRST_get(self.infinite)
                    removeLeft.FOLLOW_get(self.infinite, 0)
                    self.LL_judge = removeLeft.LL_judge(self.infinite)
                    if not self.LL_judge:
                        QtWidgets.QMessageBox.warning(self, "警告", "当前文法不是LL(1)文法请修改文法内容",
                                                      QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
                    else:
                        self.table = removeLeft.LL_create_table(self.infinite)
                        self.start = 0

    @QtCore.pyqtSlot()
    def on_pushButton_7_clicked(self):
        start, ok = QtWidgets.QInputDialog.getText(self, "请输入开始符号:", "设置")
        if ok:
            if start not in list(self.infinite.keys()):
                QtWidgets.QMessageBox.warning(self, "警告", "设置的开始符号不存在", QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.Yes)
            else:
                name_list = list(self.infinite.keys())
                self.start = name_list.index(start)
                QtWidgets.QMessageBox.information(self, "提示", "自定义开始符号成功", QtWidgets.QMessageBox.Yes,
                                                  QtWidgets.QMessageBox.Yes)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_window = My_Window()
    my_window.show()
    sys.exit(app.exec())
