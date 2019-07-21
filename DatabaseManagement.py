import random
import ServerManagement
from pybloom_live import BloomFilter


class BloomData:
    capacity = 50
    error_rate = 0.2

    def __init__(self, capacity=50, error_rate=0.2):
        """存储布隆过滤器和真值
        :param capacity:布隆过滤器容量
        :param error_rate:错误率
        """
        self.bloom = BloomFilter(capacity=self.capacity, error_rate=self.error_rate)
        self.Ture_Data = []

    def AddDataToBloom(self, new_data, key=0):
        """添加数据到布隆过滤器
        :param new_data: 待添加数据
        :param key: 模式1：布隆数据；模式0：字符数据
        :return: 现布隆数据包含真值数量
        """
        if key == 0:
            self.Ture_Data.append(new_data)
            self.bloom.add(new_data)
        if key == 1:
            self.bloom.union(new_data.bloom)
            self.Ture_Data.extend(new_data.Ture_Data)
        return len(self.Ture_Data)


class DataBase:

    def __init__(self, number_data, Aggregation_Data):
        """ 生成初始数据，包括字符型数据和布隆数据
        :param number_data:初始化生成数据数量
        :param Aggregation_Data:所有字符类型集合
        """
        self.Aggregation_Data = Aggregation_Data
        self.String_Data = []
        for i in range(number_data):
            self.String_Data.append(random.choices(self.Aggregation_Data))
        self.Bloom_Data_0 = []
        self.Bloom_Data_1 = []

    def AddStringData(self, number_data):
        """增加字符型数据
        :param number_data: 增加字符型数据数量
        :return: 现有字符型数据数量
        """
        for i in range(number_data):
            self.String_Data.append(random.choices(self.Aggregation_Data))
        return len(self.String_Data)

    def UploadServer(self, group):
        """将数据上传服务器
        :param group: 上传者组号
        :return: 上传信息
        """
        server = ServerManagement.Server()
        bf = BloomData()
        for string_data in self.String_Data:
            bf.AddDataToBloom(string_data)
        for bloom_data in self.Bloom_Data_0:
            bf.bloom = bf.bloom.union(bloom_data.bloom)
            bf.Ture_Data += bloom_data.Ture_Data
        for bloom_data in self.Bloom_Data_1:
            bf.bloom = bf.bloom.union(bloom_data.bloom)
            bf.Ture_Data += bloom_data.Ture_Data
        self.Bloom_Data_0.clear()
        self.Bloom_Data_1.clear()
        self.String_Data.clear()
        server.Bloom.append(bf.bloom.copy())
        server.Ture_Data.append(bf.Ture_Data.copy())
        server.Move_Group.append(group)
        return bf

    def TpBloom(self):
        m = len(self.String_Data)
        n = 0
        while True:
            if m >= 3:
                n = random.randint(2, m)
            if m == 2:
                n = 2
            if m < 2:
                break
            m -= n
            bf = BloomData()
            for i in range(n):
                bf.AddDataToBloom(self.String_Data[0])
                self.String_Data.remove(self.String_Data[0])
            if random.random() > 0.1:
                self.Bloom_Data_0.append(bf)
            else:
                self.Bloom_Data_1.append(bf)
        return len(self.Bloom_Data_0) + len(self.Bloom_Data_1) + len(self.String_Data)

    def AddBloom(self, bloom_data):
        """添加布隆数据
        :param bloom_data: 添加的布隆数据
        :return: 现有布隆数据数量
        """
        self.Bloom_Data_0.append(bloom_data)

    def PostBloom(self, number_post):
        """发送数据
        :param number_post:发送数据数量
        :return:发送信息
        """
        Wait_0 = []
        if len(self.Bloom_Data_1) == 0:
            num = number_post
            for i in range(number_post):
                Wait_0.append(self.Bloom_Data_0[0])
                self.Bloom_Data_0.remove(self.Bloom_Data_0[0])
            if len(Wait_0) == 0:
                print("err0")
                return 0
            else:
                bf = Wait_0[0]
                Wait_0.remove(bf)
                for bf_0 in Wait_0:
                    bf.bloom = bf.bloom.union(bf_0.bloom)
                    bf.Ture_Data.extend(bf_0.Ture_Data)
        else:
            num = number_post - 1
            for i in range(number_post - 1):
                Wait_0.append(self.Bloom_Data_0[0])
                self.Bloom_Data_0.remove(self.Bloom_Data_0[0])
            if len(Wait_0) == 0:
                print("err1")
                return 0
            else:
                bf = self.Bloom_Data_1[0]
                self.Bloom_Data_1.remove(bf)
                for bf_0 in Wait_0:
                    bf.bloom = bf.bloom.union(bf_0.bloom)
                    bf.Ture_Data.extend(bf_0.Ture_Data)
        return bf, num

    def __del__(self):
        self.String_Data.clear()
        self.Bloom_Data_0.clear()
        self.Bloom_Data_1.clear()
        self.Aggregation_Data.clear()
