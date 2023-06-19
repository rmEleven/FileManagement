from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class NewItemDialog(QDialog):
    '''命名对话框'''
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建标签和输入框
        self.label = QLabel("请输入名称：")
        self.input_line = QLineEdit()

        # 创建确定和取消按钮
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")

        # 连接按钮的点击事件到槽函数
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # 创建垂直布局，并将标签、输入框和按钮添加到其中
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_line)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.ok_button)
        h_layout.addWidget(self.cancel_button)

        layout.addLayout(h_layout)

        # 设置对话框的布局
        self.setLayout(layout)

    def get_input_text(self):
        # 返回输入框中的文本
        return self.input_line.text()


class AttributeDialog(QDialog):
    '''属性对话框'''
    def __init__(self, name, f_type, path, creation_time, last_modified_time, table=[]):
        super(AttributeDialog, self).__init__()

        # 创建布局和标签
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"名称：{name}"))
        layout.addWidget(QLabel(f"类型：{f_type}"))
        layout.addWidget(QLabel(f"路径：{path}"))
        layout.addWidget(QLabel(f"创建时间：{creation_time}"))
        layout.addWidget(QLabel(f"最近修改时间：{last_modified_time}"))
        if f_type == 'file':
            layout.addWidget(QLabel(f"索引表：{table}"))

        # 设置布局
        self.setLayout(layout)
        self.setWindowTitle("属性")


class EditDialog(QDialog):
    '''文件对话框'''
    def __init__(self, data, parent=None):
        super().__init__(parent)

        # 创建界面布局
        layout = QVBoxLayout(self)

        # 创建用于编辑的文本框
        self.editText = QTextEdit()
        self.editText.setText(data)
        layout.addWidget(self.editText)

        # 创建保存按钮
        self.saveButton = QPushButton("保存")
        layout.addWidget(self.saveButton)
        self.saveButton.setMinimumSize(QtCore.QSize(50, 30))
        self.saveButton.setMaximumSize(QtCore.QSize(50, 30))

        # 连接保存按钮的点击事件到槽函数
        self.saveButton.clicked.connect(self.accept)

    def return_data(self):
        return self.editText.toPlainText()
    

class ErrorDialog(QDialog):
    '''错误提示对话框'''
    def __init__(self, error_message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("错误")
        
        # 创建一个 QLabel 用于显示错误信息
        error_label = QLabel(error_message)
        
        # 创建一个垂直布局，并将 QLabel 添加到其中
        layout = QVBoxLayout()
        layout.addWidget(error_label)
        
        # 将布局设置为对话框的主布局
        self.setLayout(layout)