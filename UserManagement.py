import random
import math
import DatabaseManagement
from simhash import Simhash
import time


class Individual:

    def __init__(self, ID, group, Aggregation_Data):
        """初始化用户的各种属性，可修改
        :param ID: 用户id
        :param group: 设定组数
        :param Aggregation_Data: 所有字符类型集合
        """
        self.id = ID
        self.number_news = 5  # 初始信息量
        self.bid_price = random.randint(21, 100)  # 投标价格
        self.address = [random.randint(0, 1000), random.randint(0, 1000)]  # 位置区间
        self.group = random.randint(1, group)  # 初始化组号
        self.group_num = group  # 组数
        self.Move_Group = []
        self.money = random.randint(0, 1000)  # 初始化金钱
        self.Snapshot = []  # 快照
        self.buy_price = random.randint(21, 100)  # 购买价格
        self.count = 0
        self.Aggregation_Data = Aggregation_Data
        self.Data = DatabaseManagement.DataBase(self.number_news, self.Aggregation_Data)
        self.y = random.randint(1, 20)
        self.x = random.randint(1, 20)
        self.transaction_price = 0

    def print_all(self):
        """打印用户信息
        """
        print("ID：", self.id)
        print("信息量：", self.number_news)
        print("竞标价：", self.bid_price)
        print("购买价格", self.buy_price)
        print("金钱：", self.money)
        print("位置：", self.address)
        print("组号：", self.group)
        print("字符信息：", self.Data.String_Data)
        print("hash信息：", self.Data.Bloom_Data_0)
        print("hash信息：", self.Data.Bloom_Data_1)
        str_0 = ""
        if len(self.Snapshot) > 0:
            for individual in self.Snapshot:
                str_0 = str_0 + individual.id + " "
        print("快照成员: [ ", str_0, "]")

    def Bidding(self, mod=0):
        """拍卖并交易过程
        :param mod: 拍卖模式：0为多次竞价，1为simhsah比对
        :return: [平均时间，竞拍次数]
        """
        time_set = cn = 0
        if self.number_news > 1:
            n = random.randint(1, len(self.Data.Bloom_Data_0))
        else:
            n = 0
        Deal = []
        buy_price_max = self.buy_price
        buy_price_min = self.buy_price - self.x
        if len(self.Snapshot) > 0:
            for individual in self.Snapshot:
                if buy_price_max >= individual.bid_price >= buy_price_min or \
                        buy_price_max >= individual.bid_price + self.y >= buy_price_min:
                    Deal.append(individual)
            time1 = time.time()
            t = 0  # 用户传送数据时间
            for individual_0 in Deal:
                if mod == 0:
                    self.transaction_price = buy_price_min
                    individual_0.transaction_price = individual_0.bid_price + self.y
                    for i_0 in range(self.x):
                        time.sleep(t)
                        if self.transaction_price < individual_0.transaction_price:
                            self.transaction_price += 1
                            individual_0.transaction_price -= 1
                            cn += 1
                        else:
                            break
                    if self.transaction_price < individual_0.transaction_price:
                        individual_0.transaction_price = -1
                if mod == 1:
                    aa = ""
                    bb = ""
                    for i_0 in range(buy_price_min, buy_price_max + 1):
                        aa += (str(i_0) + ",")
                    for i_0 in range(individual_0.bid_price, individual_0.bid_price + self.y):
                        bb += (str(i_0) + ",")
                    time.sleep(t)
                    dis = Simhash(aa, f=32).distance(Simhash(bb, f=32))
                    if 15 < dis <= 25:
                        individual_0.transaction_price = buy_price_max - int(self.x / 2)
                    if 0 < dis <= 15:
                        individual_0.transaction_price = buy_price_min
                    if dis > 25:
                        individual_0.transaction_price = -1
            time2 = time.time()
            # print(time2 -time1)
            if len(Deal) > 0:
                time_set = (time2 - time1) / len(Deal)
                nn = 0
                while True:
                    if n >= 3:
                        nn = random.randint(2, n)
                    if n < 2:
                        break
                    if n == 2:
                        nn = 2
                    if len(self.Data.Bloom_Data_1) < 2 and self.count > 0:
                        break
                    individual_0 = random.choice(Deal)
                    if self.money < individual_0.transaction_price:
                        n -= 1
                        continue
                    if individual_0.transaction_price == -1:
                        continue
                    n -= nn
                    self.money -= individual_0.transaction_price
                    individual_0.money += individual_0.transaction_price
                    self.number_news -= nn
                    blf, cc = self.Data.PostBloom(nn)
                    self.count = 1
                    if blf != 0:
                        individual_0.Data.AddBloom(blf)
                    individual_0.number_news += 1
        self.Snapshot.clear()
        return [time_set, cn]

    def initialization(self, mod=0):
        """初始化
        :param mod: 模式：1为大轮初始化；0为小轮初始化
        """
        if mod == 0:
            self.number_news = len(self.Data.Bloom_Data_0) + len(self.Data.Bloom_Data_1) + len(self.Data.String_Data)
            self.Snapshot.clear()
            self.address[0] = random.randint(0, 1000)
            self.address[1] = random.randint(0, 1000)
            self.transaction_price = 0
        if mod == 1:
            self.Data.UploadServer(self.group)
            self.Move_Group.append(self.group)
            self.group = random.randint(1, self.group_num)
            self.number_news = 0
            self.count = 0


class Crowed:
    population = []
    individual = []
    max_add_news = 5  # 最大信息收集量
    max_num_news = 10  # 信息保存阈值
    range_search = 10000  # 快照范围
    convey_new = 1  # 单次传递信息量

    def __init__(self, num_i, num_g, Aggregation_Data):
        """初始化用户群体
        :param num_i:群体大小
        :param num_g:组数
        :param Aggregation_Data:字符命名空间
        """
        self.num_population = num_i
        self.num_group = num_g
        self.Distribution_Population = []
        self.Population = []
        self.Aggregation_Data = Aggregation_Data
        for num in range(self.num_population):
            individual = Individual(ID=str(num), group=self.num_group, Aggregation_Data=self.Aggregation_Data)
            self.Population.append(individual)
            self.individual = []

    def AddNews(self):
        """用户收集信息阶段
        """
        self.Distribution_Population = []
        for individual in self.Population:
            n = random.randint(0, self.max_add_news)
            individual.number_news += n
            individual.Data.AddStringData(n)
            if len(individual.Data.String_Data) > self.max_num_news:  # 达到阈值，str数据转化为bloom数据
                individual.number_news = individual.Data.TpBloom()
            if len(individual.Data.Bloom_Data_0) > self.max_num_news:  # 达到阈值，将用户加入待传递组
                self.Distribution_Population.append(individual)

    def SearchSnapshot(self):
        """待传递用户快照阶段
        """
        for individual_0 in self.Distribution_Population:
            for individual_1 in self.Population:
                if individual_0.group == individual_1.group:
                    distance = math.sqrt(math.pow((individual_0.address[0] - individual_1.address[0]), 2) +
                                         math.pow((individual_0.address[0] - individual_1.address[0]), 2))
                    if distance < self.range_search:
                        if individual_0.id != individual_1.id:
                            individual_0.Snapshot.append(individual_1)

    def Bidding(self, mod):
        """拍卖过程
        :param mod: 拍卖模式：0为多次竞价，1为simhsah比对
        :return: [平均时间，竞拍次数]
        """
        time_set = []
        num = []
        for individual in self.Distribution_Population:
            a = individual.Bidding(mod)
            time_set.append(a[0])
            num.append(a[1])
        self.Distribution_Population.clear()
        return [time_set, num]

    def Initialization(self, mod=0):
        """更新参数
        :param mod: 模式：1为大轮初始化；0为小轮初始化
        """
        if mod == 0:
            self.range_search += int(random.randint(-100, 100))
            for individual in self.Population:
                individual.initialization()
        if mod == 1:
            for individual in self.Population:
                individual.initialization(mod=1)

    def ErrNew(self, xx):
        """错误信息生成
        :param xx: 攻击者比率
        """
        for i_0 in range(int(self.num_population * xx)):
            if random.random() > 0.5:
                self.Population[i_0].number_news += 1
                self.Population[i_0].Data.String_Data.append(["v50"])
