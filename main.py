from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Ui_Window import *
from Dialog import NewItemDialog, AttributeDialog, EditDialog, ErrorDialog
from System import *

import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.fs = FileSystem()

        self.update_path()
        self.update_tree()
        self.update_list()

        # 设置列表的上下文菜单策略
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # 右键点击列表触发显示菜单的槽函数
        self.listWidget.customContextMenuRequested.connect(self.show_menu)
        
        # 双击列表项触发打开文件或目录的槽函数
        #self.listWidget.doubleClicked.connect(self.open)
        self.listWidget.itemDoubleClicked.connect(self.open)

        # 返回上级目录的按钮
        self.back_button.clicked.connect(self.back_parent)
    
    def update_path(self):
        # 更新当前路径
        self.path_label.setText(f'>{self.fs.get_cur_path()}')
    
    def update_tree(self):
        # 更新文件树
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(1)
        
        froot = self.fs.root
        troot = QTreeWidgetItem(self.treeWidget)
        troot.setText(0, froot.name)

        tnodes = [troot]
        fnodes = [froot]

        while len(tnodes) != 0:
            cur_tnode = tnodes.pop(0)
            cur_fnode = fnodes.pop(0)

            for i in cur_fnode.files:
                new_tnode = QTreeWidgetItem(cur_tnode)
                new_tnode.setText(0, i.name)
            
            for i in cur_fnode.dirs:
                new_tnode = QTreeWidgetItem(cur_tnode)
                new_tnode.setText(0, i.name)
                tnodes.append(new_tnode)
                fnodes.append(i)
    
    def update_list(self):
        # 更新文件图标
        self.listWidget.clear()
        files, dirs = self.fs.get_cur_content()
        font = QFont()
        font.setPointSize(10)
        for file in files:
            item = QListWidgetItem(file.name)  # 创建列表项
            self.listWidget.addItem(item)  # 将列表项添加到文件列表控件中
            item.setIcon(QIcon("icons/file.svg"))  # 设置列表项的图标
            item.setFont(font)
        for dir in dirs:
            item = QListWidgetItem(dir.name)
            self.listWidget.addItem(item)
            item.setIcon(QIcon("icons/folder.svg"))
            item.setFont(font)

    def show_menu(self, pos):
        # 判断右击部位选择不同的菜单
        # global_pos = self.listWidget.mapToGlobal(pos)
        item = self.listWidget.itemAt(pos)
        if item is not None:
            # 右击了列表项
            self.show_item_menu(pos)
        else:
            # 右击了列表的其他部分
            self.show_list_menu(pos)

    def show_list_menu(self, pos):
        # 右击列表显示菜单并处理
        print('显示列表右键菜单')
        # 创建菜单
        menu = QMenu(self.listWidget)
        # 添加菜单项
        new_file_action = menu.addAction("新建文件")
        new_dir_action = menu.addAction("新建文件夹")
        format_action = menu.addAction("格式化")
        save_action = menu.addAction("保存")

        # 显示菜单，并等待用户选择
        action = menu.exec_(self.listWidget.mapToGlobal(pos))

        # 根据用户选择执行相应操作
        if action == new_file_action:
            # print('选择新建文件操作')
            self.new_file()
        elif action == new_dir_action:
            # print('选择新建文件夹操作')
            self.new_dir()
        elif action == format_action:
            # print('选择格式化操作')
            self.format_all()
        elif action == save_action:
            # print('选择保存操作')
            self.save_all()
    
    def show_item_menu(self, pos):
        # 右击列表显示菜单并处理
        print('显示选项右键菜单')
        # 创建菜单
        menu = QMenu(self.listWidget)
        # 添加菜单项
        open_action = menu.addAction("打开")
        delete_action = menu.addAction("删除")
        rename_action = menu.addAction("重命名")
        attribute_action = menu.addAction("属性")

        # 显示菜单，并等待用户选择
        action = menu.exec_(self.listWidget.mapToGlobal(pos))

        item = self.listWidget.itemAt(pos)
        print('选中', item.text())

        # 根据用户选择执行相应操作
        if action == open_action:
            print('选择打开操作')
            self.open(item)
        elif action == delete_action:
            print('选择删除操作')
            self.delete(item)
        elif action == rename_action:
            print('选择重命名操作')
            self.rename(item)
        elif action == attribute_action:
            print('选择属性操作')
            self.show_attribue(item)

    def new_file(self):
        # 新建文件
        dialog = NewItemDialog(self)  # 创建新建文件对话框
        dialog.setWindowTitle("新建文件")  # 设置对话框标题为"新建文件"

        if dialog.exec_() == QDialog.Accepted:  # 如果用户点击了对话框的"确定"按钮
            name = dialog.get_input_text()  # 获取用户输入的文件名
            if name:
                if self.fs.add_file(name):  # 在文件系统中创建文件
                    self.update_list()  # 刷新文件列表显示
                    self.update_tree()
                    print('新建文件', name)
                else:
                    QtWidgets.QMessageBox.warning(self, "错误", "文件已存在")  # 显示错误提示框，文件已存在
        else:
            dialog.close()  # 如果用户点击了对话框的"取消"按钮，关闭对话框

    def new_dir(self):
        # 新建文件夹
        dialog = NewItemDialog(self)  # 创建新建文件夹对话框
        dialog.setWindowTitle("新建文件夹")  # 设置对话框标题为"新建文件夹"

        if dialog.exec_() == QDialog.Accepted:  # 如果用户点击了对话框的"确定"按钮
            name = dialog.get_input_text()  # 获取用户输入的文件夹名称
            if name:
                if self.fs.add_dir(name):  # 在文件系统中创建文件夹
                    self.update_list()  # 刷新文件列表显示
                    self.update_tree()
                    print('新建文件夹', name)
                else:
                    QtWidgets.QMessageBox.warning(self, "错误", "文件夹已存在")  # 显示错误提示框，文件夹已存在
        else:
            dialog.close()  # 如果用户点击了对话框的"取消"按钮，关闭对话框

    def format_all(self):
        # 格式化磁盘和目录
        self.fs.format_system()
        self.update_path()
        self.update_list()
        self.update_tree()

    def save_all(self):
        # 保存磁盘和目录
        self.fs.save_system()

    def open(self, item: QListWidgetItem):
        # 进入文件夹或打开文件
        name = item.text()
        index = self.listWidget.row(item)
        files, dirs = self.fs.get_cur_content()

        if index < len(files):
            # 文件
            self.open_file(name, files)
        else:
            # 文件夹
            self.enter_dir(name, dirs)

    def enter_dir(self, name, dirs):
        # 进入文件夹
        for dir in dirs:
            if name == dir.name:
                self.fs.cd_forward(dir)
                print('进入文件夹', self.fs.cur_dir.name)
                self.update_path()
                self.update_list()
                return

    def open_file(self, name, files):
        # 打开文件
        for file in files:
            if name == file.name:
                data = self.fs.disk.read(file.table)
                print('打开文件', file.name)
                print('文件内容', data)
                edit_dialog = EditDialog(data)
                edit_dialog.setWindowTitle(file.name)
                if edit_dialog.exec_() == QDialog.Accepted:  # 点击保存按钮
                    new_data = edit_dialog.return_data()  # 获取新文本
                    print('新文本', new_data)
                    result = self.fs.write_file(file, new_data)
                    if result == False:
                        error_dialog = ErrorDialog("磁盘块不足，文本保存失败")
                        error_dialog.exec_()
                return

    def back_parent(self):
        # 返回上级目录
        self.fs.cd_backward()
        print('返回上级目录', self.fs.cur_dir.name)
        self.update_path()
        self.update_list()

    def rename(self, item: QListWidgetItem):
        # 文件和文件夹重命名
        name = item.text()
        print('重命名', name)
        index = self.listWidget.row(item)
        files, dirs = self.fs.get_cur_content()

        # 创建重命名对话框
        dialog = NewItemDialog(self)
        dialog.setWindowTitle("重命名")

        # 如果用户点击了对话框的确定按钮
        if dialog.exec_() == QDialog.Accepted:
            # 获取用户输入的新名称
            new_name = dialog.get_input_text()
            if new_name == '':
                QtWidgets.QMessageBox.warning(self, "错误", "命名不能为空")
            elif index < len(files):
                # 文件
                file = files[index]
                result = self.fs.rename_file(file, new_name)
                if result == True:
                    self.update_list()
                    self.update_tree()
                else:
                    QtWidgets.QMessageBox.warning(self, "错误", "文件命名已存在")
            else:
                # 文件夹
                dir = dirs[index - len(files)]
                result = self.fs.rename_dir(dir, new_name)
                if result == True:
                    self.update_list()
                    self.update_tree()
                else:
                    QtWidgets.QMessageBox.warning(self, "错误", "文件夹命名已存在")
        else:
            dialog.close()

    def delete(self, item: QListWidgetItem):
        # 删除文件和文件夹
        name = item.text()
        index = self.listWidget.row(item)
        files, dirs = self.fs.get_cur_content()

        if index < len(files):
            # 文件
            print('删除文件', name)
            self.fs.del_file(files[index])
        else:
            # 文件夹
            print('删除文件夹', name)
            self.fs.del_dir(dirs[index - len(files)])
        self.update_list()
        self.update_tree()

    def show_attribue(self, item: QListWidgetItem):
        # 显示文件和文件夹属性
        name = item.text()
        index = self.listWidget.row(item)
        files, dirs = self.fs.get_cur_content()

        if index < len(files):
            # 文件
            print('查看文件', name, '属性')
            target = files[index]
            attribute_dialog = AttributeDialog(target.name, target.type, 
            target.path, target.creation_time, target.last_modified_time, target.table)
        else:
            # 文件夹
            print('查看文件夹', name, '属性')
            target = dirs[index - len(files)]
            attribute_dialog = AttributeDialog(target.name, target.type, 
            target.path, target.creation_time, target.last_modified_time)
        
        attribute_dialog.exec_()


if __name__=='__main__':
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    sys.exit(app.exec_())