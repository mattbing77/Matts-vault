from app.menu import display_menu
from app.inventory import view_inventory
from app.inventory import view_inventory, add_item


def main():
    
    running = True
    while running:
        choice = display_menu()
        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            print("You Chose Search Inventory")
        elif choice == "4":
            print("You Chose Update Item")
        elif choice == "5":
            print("You Chose Delete Item")
        elif choice == "6":
            print("Goodbye!")
            running = False
        else: 
            print("Invalid Option Please Try Again")


if __name__ == "__main__":
    main()
    