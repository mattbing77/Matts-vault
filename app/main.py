
from app.menu import display_menu
from app.inventory import (
    view_inventory,
    add_item,
    search_inventory,
    update_item,
    delete_item,
)


def main():
    running = True

    while running:
        choice = display_menu()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            search_inventory()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            print("Goodbye!")
            running = False
        else:
            print(
                "Error: Invalid menu option. "
                "Please enter a number between 1 and 6."
            )


if __name__ == "__main__":
    main()
