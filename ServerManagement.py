class Server:
    Bloom = []
    Ture_Data = []
    Pre_Data = []
    len_aggregation = 50
    Census_Ture = [0] * len_aggregation
    Census_Pre = [0] * len_aggregation
    Move_Group = []
    Attacker = []

    def SetPre(self, Aggregation_Data):
        """更新Pre_Data集合
        :param Aggregation_Data:所有字符类型集合
        :return: Pre_Data数据
        """
        for Bloom_0 in self.Bloom:
            Data = []
            for data in Aggregation_Data:
                x = [data]
                if x in Bloom_0:
                    Data.append(x)
            self.Pre_Data.append(Data.copy())
        return self.Pre_Data

    def SetCensus(self):
        """更新Census_Ture，Census_Pre集合
        """
        for i in range(len(self.Ture_Data)):
            for Data in self.Ture_Data[i]:
                self.Census_Ture[int(Data[0][1:])] += 1
        for i in range(len(self.Pre_Data)):
            for Data in self.Pre_Data[i]:
                self.Census_Pre[int(Data[0][1:])] += 1

    def FindAttacker(self, err="v50"):
        """寻找攻击者
        :param err:攻击者错误信息
        :return:攻击者路径
        """
        A = []
        i = 0
        for Bloom_0 in self.Bloom:
            if [err] in Bloom_0:
                A.append(self.Move_Group[i])
            i += 1
        self.Attacker.append(A.copy())
        return self.Attacker

    def clear(self):
        """
        clear
        """
        self.Bloom.clear()
        self.Census_Ture = [0] * self.len_aggregation
        self.Census_Pre = [0] * self.len_aggregation
        self.Move_Group.clear()
        self.Pre_Data.clear()
        self.Ture_Data.clear()
        self.Attacker.clear()
