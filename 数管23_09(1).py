# 云端修改代码
#      <meta http-equiv="X-UA-Compatible" content="IE=edge">
#      <meta name="viewport" content="width=device-width, initial-scale=1.0">
#      <title>志愿者管理系统</title>
#  </head>
#  <body>S
#haha
class volunteer:
    all_volunteers = {}
    def create_base_files():  # 创建基础数据所需要的txt文件
        file_path = "volunteer.txt"
        try:
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("id|姓名|性别|积分|活动记录\n")  # 预填志愿者信息
                f.write("001|李红|女|100|植树：2，垃圾清理：1\n")
                f.write("002|赵磊|男|80|垃圾清理：3，擦桌子：4\n")
                f.write("003|刘刚|男|120|垃圾清理：2，环保宣传：1\n")
                f.write("004|徐敏|女|90|植树：3\n")
            print(f"志愿者信息文件{file_path}创建成功")
        except Exception as e:
            print(f"创建志愿者信息文件时出错")


    def create_with_unique_id():  # 检验唯一性
        """创建志愿者对象并确保ID唯一"""
        while True:
            id = input("请输入志愿者ID: ")
            if id not in volunteer.all_volunteers:
                name = input("请输入姓名: ")
                sex = input("请输入性别: ")
                score = int(input("请输入积分: ") or 0)
                vol = volunteer(id, name, sex, score)
                volunteer.all_volunteers[id] = vol

                # 新增：将新志愿者信息写入文件
                volunteer.save_volunteer_to_file(vol)
                print(f"志愿者 {name} (ID:{id}) 创建成功！")
                return vol
            print(f"ID '{id}' 已存在，请重新输入")

    # 新增：保存志愿者信息到文件
    def save_volunteer_to_file(vol):
        file_path = "volunteer.txt"
        try:
            # 读取现有文件内容
            with open(file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            # 构造新志愿者数据行
            activity_record = "植树：0，垃圾清理：0"
            new_line = f"{vol.id}|{vol.name}|{vol.sex}|{vol.score}|{activity_record}\n"
            # 追加文件末尾（跳过表头）
            with open(file_path, "a", encoding='utf-8') as f:
                if len(lines) > 1:  # 如果不是空文件，先写入换行符
                    f.write("\n")
                f.write(new_line)

            print("志愿者信息已保存到文件")
        except Exception as e:
            print(f"保存志愿者信息时出错: {e}")

    # 查询志愿者积分功能
    def inquiry_volunteer():
        try:
            with open("volunteer.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()[1:]  # 跳过表头，得到所有数据行
                find = input("请输入要查询的志愿者ID: ")
                for line in lines:
                    data = line.strip().split("|")  # 按分隔符‘|’解析数据
                    if data[0] == find:  # 找到匹配ID的志愿者
                        # 解析活动记录字符串为字典 {"活动类型": 次数}
                        activities = {a.split("：")[0]: int(a.split("：")[1]) for a in data[4].split("，")}
                        print(f"\nID: {data[0]}, 姓名: {data[1]}")  # 输出基本信息
                        print(f"积分: {data[3]}")  # 输出积分
                        print(f"活动次数: {sum(activities.values())}")  # 计算总活动次数
                        # 格式化输出活动类型和次数
                        activity_distribution = []
                        for activity_type, count in activities.items():
                            activity_distribution.append(f"{activity_type}：{count}次")
                        print(f"活动分布: {', '.join(activity_distribution)}")
                        return
                print("未找到该志愿者")
        except Exception as e:
            print(f"查询时出错: {e}")

    # 更新志愿者积分功能
    def update_volunteer_score():
        try:
            with open("volunteer.txt", "r", encoding="utf-8") as f:  # 以读取模式打开志愿者数据文件
                lines = f.readlines()

            id_update = input("请输入要更新积分的志愿者ID: ")  # 获取需要更新分数的ID
            found = False  # 标记是否找到目标志愿者

            for i in range(1, len(lines)):
                data = lines[i].strip().split("|")
                if data[0] == id_update:  # 检查当前行ID是否与目标ID匹配
                    found = True  # 已经找到

                    current_score = int(data[3])  # 获取当前积分
                    change = int(input("请输入积分变化量: "))
                    new_score = current_score + change  # 计算新积分

                    reason = input("请输入积分变更原因: ")

                    # 时间：年-月-日 时:分:秒
                    from time import localtime, strftime
                    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())

                    operation = f"{timestamp}|积分变更|{change}|{reason}\n"

                    with open(f"operation_{id_update}.txt", "a", encoding="utf-8") as op_file:
                        op_file.write(operation)
                    data[3] = str(new_score)  # 更新当前行的积分数据
                    lines[i] = "|".join(data) + "\n"  # 重新拼接当前行数据‘|’分隔

                    print(f"\n积分更新成功！")
                    print(f"ID: {data[0]}, 姓名: {data[1]}")
                    print(f"原积分: {current_score} → 新积分: {new_score}")
                    print(f"变更原因: {reason}")
                    break

            if not found:
                print("未找到该志愿者")
            else:
                with open("volunteer.txt", "w", encoding="utf-8") as f:
                    f.writelines(lines)

        except Exception as e:
            print(f"更新积分时出错: {e}")

    def display_all_volunteers():
        """显示所有志愿者信息"""
        print("所有志愿者信息 :\n")
        if not volunteer.all_volunteers:
            print("暂无志愿者信息")
            return

        for vol_id, vol in volunteer.all_volunteers.items():
            print(f"\nID: {id}")
            print(f"姓名: {vol['name']}")
            print(f"性别: {vol['gender']}")
            print(f"积分: {vol['score']}")

            if not vol['activity_record']:
                print("活动记录: 无")
            else:
                print("活动记录:")
                for activity_name, count in vol['activity_record'].items():
                    print(f"  {activity_name}: {count}次")

    def display_operation_logs():
        """显示操作记录"""
        print("操作记录:\n")
        if not volunteer.operation_logs:
            print("暂无操作记录")
            return

        for log in volunteer.operation_logs:
            print(f"\n志愿者ID: {log['id']}")
            print(f"操作类型: {log['operation']}")
            print(f"操作原因: {log['reason']}")
            print(f"操作时间: {log['timestamp']}")

    def __init__(self, id, name, sex, score=0):
        self.id = id  # 志愿者id
        self.name = name  # 姓名
        self.sex = sex  # 性别
        self.score = score  # 得分
        self.activity_record = {"植树": 0, "垃圾清理": 0}  # 活动类型和参与次数
        self.now_activities = []  # 当前参与的活动
        self.operation_list = []  # 存储操作记录


if __name__ == "__main__":
    volunteer.create_base_files()



    while True:
        print("\n===== 志愿者管理系统 =====")
        print("1. 添加新志愿者")
        print("2. 查询志愿者积分")
        print("3. 更新志愿者积分")
        print("4. 显示所有志愿者信息")
        print("5. 显示志愿者操作记录")
        print("6. 退出")

        choice = input("请选择功能 (1-6): ")
        if choice == "1":
            volunteer.create_with_unique_id()
        elif choice == "2":
            volunteer.inquiry_volunteer()
        elif choice == "3":
            volunteer.update_volunteer_score()
        elif choice == "4":
            volunteer.display_all_volunteers()
        elif choice == "5":
            volunteer.display_operation_logs()
        elif choice == "6":
            print("退出系统")
            break
        else:
            print("无效选择，请重新输入")
