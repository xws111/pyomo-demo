students = [
    {"name": "张三", "age": 18, "gender": "男", "score": 85},
    {"name": "李四", "age": 19, "gender": "女", "score": 92},
    {"name": "王五", "age": 17, "gender": "男", "score": 78},
    {"name": "赵六", "age": 18, "gender": "女", "score": 88},
    {"name": "钱七", "age": 20, "gender": "男", "score": 73},
    {"name": "孙八", "age": 18, "gender": "女", "score": 95},
    {"name": "周九", "age": 19, "gender": "男", "score": 81},
    {"name": "吴十", "age": 17, "gender": "女", "score": 90},
    {"name": "郑十一", "age": 18, "gender": "男", "score": 76},
    {"name": "冯十二", "age": 19, "gender": "女", "score": 89},
    {"name": "陈十三", "age": 20, "gender": "男", "score": 84},
    {"name": "楚十四", "age": 18, "gender": "女", "score": 91},
    {"name": "卫十五", "age": 17, "gender": "男", "score": 79},
    {"name": "蒋十六", "age": 19, "gender": "女", "score": 87},
    {"name": "沈十七", "age": 18, "gender": "男", "score": 82},
    {"name": "韩十八", "age": 20, "gender": "女", "score": 94},
    {"name": "杨十九", "age": 17, "gender": "男", "score": 77},
    {"name": "朱二十", "age": 18, "gender": "女", "score": 93},
    {"name": "秦廿一", "age": 19, "gender": "男", "score": 80},
    {"name": "尤廿二", "age": 18, "gender": "女", "score": 86},
]

for i, student in enumerate(students, 1):
    print(f"{i}. 姓名: {student['name']}, 年龄: {student['age']}, 性别: {student['gender']}, 成绩: {student['score']}")