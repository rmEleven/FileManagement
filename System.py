from Storage import *
from File import *

import os
import pickle


def load_from_file(filename):
    '''从本地加载数据'''
    with open(filename, 'rb') as f:
        return pickle.load(f)

def save_to_file(filename, data):
    '''保存数据到本地'''
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


class FileSystem:
    '''模拟文件系统'''
    def __init__(self):
        if os.path.exists("disk.pickle"):
            self.disk = load_from_file("disk.pickle")  # 加载磁盘
        else:
            self.disk = Disk()  # 创建磁盘

        if os.path.exists("catalog.pickle"):
            self.root = load_from_file("catalog.pickle")  # 加载根目录
        else:
            self.root = Directory('root', '', None)  # 创建根目录

        self.cur_dir = self.root  # 当前所在目录

    def get_cur_path(self):
        # 获取当前路径
        return self.cur_dir.path + self.cur_dir.name + '/'

    def get_cur_content(self):
        # 获取当前路径下的所有文件和文件夹
        return self.cur_dir.files, self.cur_dir.dirs

    def cd_forward(self, selected_dir):
        # 打开文件夹后进入指定目录
        self.cur_dir = selected_dir

    def cd_backward(self):
        # 返回上一级目录
        father = self.cur_dir.father
        if father != None:
            self.cur_dir = father
    
    def add_dir(self, dir_name):
        # 添加文件夹
        # 判断命名是否重复
        for i in self.cur_dir.dirs:
            if dir_name == i.name:
                return False
        # 创建文件夹并添加
        new_path = self.get_cur_path()
        new_dir = Directory(dir_name, new_path, self.cur_dir)
        self.cur_dir.add_dir(new_dir)
        return True
    
    def add_file(self, file_name):
        # 添加文件
        # 判断命名是否重复
        for i in self.cur_dir.files:
            if file_name == i.name:
                return False
        # 创建文件并添加
        new_path = self.get_cur_path()
        new_file = File(file_name, new_path)
        self.cur_dir.add_file(new_file)
        return True

    def del_dir(self, selected_dir):
        # 删除文件夹
        self.cur_dir.remove_dir(selected_dir)
    
    def del_file(self, selected_file):
        # 删除文件
        self.disk.clear(selected_file.table)
        self.cur_dir.remove_file(selected_file)

    def rename_dir(self, selected_dir, new_name):
        # 文件夹重命名
        for i in self.cur_dir.dirs:
            if new_name == i.name and i != selected_dir:
                return False
        selected_dir.rename(new_name)
        return True

    def rename_file(self, selected_file, new_name):
        # 文件重命名
        for i in self.cur_dir.files:
            if new_name == i.name and i != selected_file:
                return False
        selected_file.rename(new_name)
        return True

    def read_file(self, selected_file):
        # 读文件内容
        return self.disk.read(selected_file.table)

    def write_file(self, selected_file, data):
        # 向文件写数据
        result, table = self.disk.write(data)  # 尝试写入
        if result == True:  # 写入成功
            self.disk.clear(selected_file.table)  # 清空原数据
            print('清空块', selected_file.table)
            selected_file.table = table
            selected_file.update_last_modified_time()
            print('写入成功')
            return True
        else:
            print('写入失败')
            return False  # 写入失败

    def format_system(self):
        # 格式化磁盘和目录
        self.root = Directory('root', '/', None)  # 创建根目录
        self.disk = Disk()  # 创建磁盘
        self.cur_dir = self.root  # 当前所在目录

    def save_system(self):
        # 保存磁盘和目录
        save_to_file("disk.pickle", self.disk)
        save_to_file("catalog.pickle", self.root)
