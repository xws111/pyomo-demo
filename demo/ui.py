from manager import StudentManager
from student import Student


class StudentUI:
    def __init__(self, manager: StudentManager):
        self.manager = manager

    def show_menu(self):
        print("\n" + "=" * 40)
        print("        学生管理系统")
        print("=" * 40)
        print("  1. 添加学生")
        print("  2. 删除学生")
        print("  3. 修改学生信息")
        print("  4. 查找学生")
        print("  5. 显示全部学生")
        print("  6. 统计信息")
        print("  7. 导出到Excel")
        print("  0. 退出")
        print("=" * 40)

    def get_user_choice(self) -> str:
        return input("请选择操作: ").strip()

    def handle_add(self):
        print("\n--- 添加学生 ---")
        try:
            name = input("姓名: ").strip()
            if not name:
                print("姓名不能为空")
                return

            age = int(input("年龄: ").strip())
            if age <= 0:
                print("年龄必须是正整数")
                return

            gender = input("性别: ").strip()
            if gender not in ["男", "女"]:
                print("性别必须是 '男' 或 '女'")
                return

            score = float(input("成绩: ").strip())
            if score < 0 or score > 100:
                print("成绩必须在 0-100 之间")
                return

            student = Student(name=name, age=age, gender=gender, score=score)
            self.manager.add_student(student)
            print(f"添加成功！学号: {student.student_id}")
        except ValueError:
            print("输入格式错误")

    def handle_delete(self):
        print("\n--- 删除学生 ---")
        student_id = input("请输入学号: ").strip()
        if self.manager.remove_student(student_id):
            print("删除成功")
        else:
            print("未找到该学号的学生")

    def handle_update(self):
        print("\n--- 修改学生信息 ---")
        student_id = input("请输入学号: ").strip()
        student = self.manager.find_student(student_id)

        if student is None:
            print("未找到该学号的学生")
            return

        print(f"当前信息: {student.name}, {student.age}岁, {student.gender}, 成绩{student.score}")

        try:
            name = input(f"姓名 [{student.name}]: ").strip()
            age_str = input(f"年龄 [{student.age}]: ").strip()
            gender = input(f"性别 [{student.gender}]: ").strip()
            score_str = input(f"成绩 [{student.score}]: ").strip()

            updates = {}
            if name:
                updates["name"] = name
            if age_str:
                updates["age"] = int(age_str)
            if gender:
                if gender not in ["男", "女"]:
                    print("性别必须是 '男' 或 '女'")
                    return
                updates["gender"] = gender
            if score_str:
                score = float(score_str)
                if score < 0 or score > 100:
                    print("成绩必须在 0-100 之间")
                    return
                updates["score"] = score

            if updates:
                self.manager.update_student(student_id, **updates)
                print("修改成功")
            else:
                print("未做任何修改")
        except ValueError:
            print("输入格式错误")

    def handle_search(self):
        print("\n--- 查找学生 ---")
        print("1. 按学号查找")
        print("2. 按姓名查找")
        choice = input("请选择: ").strip()

        if choice == "1":
            student_id = input("请输入学号: ").strip()
            student = self.manager.find_student(student_id)
            if student:
                self._display_student(student)
            else:
                print("未找到该学号的学生")
        elif choice == "2":
            name = input("请输入姓名: ").strip()
            students = self.manager.find_by_name(name)
            if students:
                for s in students:
                    self._display_student(s)
            else:
                print("未找到匹配的学生")
        else:
            print("无效选择")

    def handle_display_all(self):
        print("\n--- 所有学生 ---")
        students = self.manager.list_students(sort_by="name")

        if not students:
            print("暂无学生信息")
            return

        print(f"共 {len(students)} 名学生:")
        print("-" * 50)
        for s in students:
            self._display_student(s)

    def handle_statistics(self):
        print("\n--- 统计信息 ---")
        stats = self.manager.get_statistics()
        print(f"学生总数: {stats['total']}")
        if stats['total'] > 0:
            print(f"平均分: {stats['average_score']:.2f}")
            print(f"最高分: {stats['max_score']:.2f}")
            print(f"最低分: {stats['min_score']:.2f}")

    def handle_export(self):
        print("\n--- 导出到Excel ---")
        filename = input("请输入文件名 (默认: students.xlsx): ").strip()
        if not filename:
            filename = "students.xlsx"
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"

        if self.manager.export_to_excel(filename):
            print(f"导出成功: {filename}")
        else:
            print("导出失败: 没有学生数据")

    def _display_student(self, student: Student):
        print(f"学号: {student.student_id} | 姓名: {student.name} | "
              f"年龄: {student.age} | 性别: {student.gender} | 成绩: {student.score}")