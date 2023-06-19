BLOCK_SIZE = 1024
BLOCK_NUM = 1024


class Block:
    '''模拟磁盘上的物理块'''
    def __init__(self, id, block_size=BLOCK_SIZE):
        self.id = id                # 块编号
        self.capacity = block_size  # 块容量
        self.data = ''              # 存储的数据

    def show_info(self):
        # 用于调试
        print('---------------------')
        print(f'id: {self.id}')
        print(f'capacity: {self.capacity}')
        print(f'data: {self.data}')
        print('---------------------')
    
    def read_block(self):
        # 从磁盘中读取当前块的内容
        return self.data

    def write_block(self, data):
        # 向当前块覆盖写入内容 返回未写入的内容
        if len(data) > self.capacity:
            self.data = data[: self.capacity]
            return data[self.capacity:]
        else:
            self.data = data
            return ''

    def clear_block(self):
        # 清空当前块的内容
        self.data = ''


class Disk:
    '''模拟磁盘'''
    def __init__(self, block_num=BLOCK_NUM, block_size=BLOCK_SIZE):
        self.block_num = block_num
        self.block_size = block_size

        self.bitmap = []  # 位示图 0表示块未使用 1表示块被使用
        self.blocks = []  # 存储磁盘上所有的物理块
        for i in range(self.block_num):
            self.bitmap.append(0)
            self.blocks.append(Block(i))
    
    def show_info(self):
        # 用于调试
        print('*********************')
        print(f'block_num: {self.block_num}')
        print(f'block_size: {self.block_size}')
        print(f'bitmap: {self.bitmap}')
        print('*********************')
        for block in self.blocks:
            block.show_info()

    def read(self, table):
        # 读取索引表指定的块
        data = ''
        for i in table:
            data += self.blocks[i].read_block()
        return data
    
    def allocate_block(self):
        # 分配一个空闲块，更新位示图并返回块的编号
        for index, value in enumerate(self.bitmap):
            if value == 0:
                self.bitmap[index] = 1
                return index
        return None

    def write(self, data):
        # 寻找空闲块写入数据
        
        # 预先计算能否完整写入数据
        counter = 0
        for i in self.bitmap:
            if i == 0:
                counter += 1
        if counter * self.block_size < len(data):
            return False, []

        # 写入数据并返回索引表
        table = []
        while data != '':
            index = self.allocate_block()
            table.append(index)
            data = self.blocks[index].write_block(data)
        return True, table

    def clear(self, table):
        # 清空索引表指定的块
        for i in table:
            self.bitmap[i] = 0
            self.blocks[i].clear_block()
