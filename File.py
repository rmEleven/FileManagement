import time


class File:
    '''文件控制块模拟文件'''
    def __init__(self, name, path):
        self.name = name  # 文件名称
        self.type = 'file'
        self.path = path  # 文件路径

        self.table = []  # 索引表所在物理块的索引

        self.creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 创建时间
        self.last_modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 最近修改时间

    def show_info(self):
        # 用于调试
        print('---------------------')
        print(f'name: {self.name}')
        print(f'type: {self.type}')
        print(f'path: {self.path}')
        print(f'table: {self.table}')
        print(f'creation_time: {self.creation_time}')
        print(f'last_modified_time: {self.last_modified_time}')
        print('---------------------')

    def update_last_modified_time(self):
        self.last_modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def rename(self, new_name):
        self.name = new_name
        self.update_last_modified_time()


class Directory:
    '''模拟文件夹'''
    def __init__(self, name, path, father):
        self.name = name
        self.type = 'dir'
        self.path = path

        self.father = father

        self.creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 创建时间
        self.last_modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 最近修改时间

        self.files = []
        self.dirs = []
    
    def show_info(self):
        # 用于调试
        print('---------------------')
        print(f'name: {self.name}')
        print(f'type: {self.type}')
        print(f'path: {self.path}')
        print(f'father: {self.father.name}')
        print(f'creation_time: {self.creation_time}')
        print(f'last_modified_time: {self.last_modified_time}')
        print(f'files: {list(i.name for i in self.files)}')
        print(f'dirs: {list(i.name for i in self.dirs)}')
        print('---------------------')

    def update_last_modified_time(self):
        self.last_modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    def rename(self, new_name):
        self.name = new_name
        self.update_last_modified_time()
    
    def add_file(self, file):
        self.files.append(file)
        self.update_last_modified_time()

    def add_dir(self, dir):
        self.dirs.append(dir)
        self.update_last_modified_time()

    def remove_file(self, file):
        self.files.remove(file)
        self.update_last_modified_time()

    def remove_dir(self, dir):
        self.dirs.remove(dir)
        self.update_last_modified_time()
