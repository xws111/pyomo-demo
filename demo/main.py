from manager import StudentManager
from ui import StudentUI


def main():
    manager = StudentManager()
    ui = StudentUI(manager)

    while True:
        ui.show_menu()
        choice = ui.get_user_choice()

        if choice == "1":
            ui.handle_add()
        elif choice == "2":
            ui.handle_delete()
        elif choice == "3":
            ui.handle_update()
        elif choice == "4":
            ui.handle_search()
        elif choice == "5":
            ui.handle_display_all()
        elif choice == "6":
            ui.handle_statistics()
        elif choice == "0":
            print("感谢使用，再见！")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()