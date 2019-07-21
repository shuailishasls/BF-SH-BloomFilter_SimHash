from UserManagement import Crowed

if __name__ == '__main__':
    """
    收集数据空间生成
    """
    place = []
    string = "v"
    for i in range(50):
        place.append(string + str(i))
    """
    生成群体，分组
    """
    x = Crowed(1000, 20, place)
    """
    任务进行
    """
    for j in range(10):
        print("!!!!!第", j, "个时间片!!!!!")
        for i in range(20):
            print("##########第", i, "轮##########")
            print("*****收集信息*****")
            x.AddNews()
            print("*****初始化*****")
            x.Initialization()
            print("*****快照*****")
            x.SearchSnapshot()
            print("*****传递信息*****")
            x.Bidding(1)
        x.Initialization(mod=1)

