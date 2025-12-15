from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from alchemyBase import Base, FishingLine, FishingPole, FishingBait, FishingReel, PoleBait, Inventory

# Create a session
db_url = "sqlite:///fishing_inventory.db"
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def generate_item_id():
    """Generate a unique item ID by incrementing the last item ID in the Inventory table."""
    last_item = session.query(func.max(Inventory.item_id)).scalar()  # Get the maximum item_id in the Inventory table
    if last_item is None:
        return 1  # Start with 1 if no items exist
    return last_item + 1  # Increment the last item ID


def main_menu():
    """Main menu for interacting with the database."""
    while True:
        print("\n--- Fishing Inventory Management ---")
        print("1. View Equipment Information")
        print("2. Add New Equipment")
        print("3. Remove Equipment")
        print("4. Increase Quantity")
        print("5. Decrease Quantity")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            view_equipment_menu()
        elif choice == "2":
            add_equipment_menu()
        elif choice == "3":
            remove_equipment_menu()
        elif choice == "4":
            modify_quantity("increase")
        elif choice == "5":
            modify_quantity("decrease")
        elif choice == "6":
            print("Exiting the system")
            break
        else:
            print("Invalid choice. Please try again.")


def view_equipment_menu():
    """Menu to view equipment information."""
    print("\n--- View Equipment Information ---")
    print("1. Fishing Bait")
    print("2. Fishing Line")
    print("3. Fishing Pole")
    print("4. Fishing Reel")
    choice = input("Select the equipment type (1-4): ").strip()

    if choice == "1":
        view_table(FishingBait)
    elif choice == "2":
        view_table(FishingLine)
    elif choice == "3":
        view_table(FishingPole)
    elif choice == "4":
        view_table(FishingReel)
    else:
        print("Invalid choice. Returning to main menu.")


def view_table(model):
    """Displays all data from the specified table with quantity from inventory."""
    try:
        # Perform a join between the equipment model and Inventory table
        rows = session.query(model, Inventory.quantity).join(Inventory, Inventory.item_id == model.item_id).all()
        
        if rows:
            print(f"\n--- {model.__name__.capitalize()} ---")
            for row in rows:
                equipment_item = row[0]  # The equipment data (model)
                quantity = row[1]  # The quantity from Inventory
                print(f"{equipment_item} | Quantity: {quantity}")
        else:
            print(f"No data found in {model.__name__}.")
    except Exception as e:
        print(f"Error viewing table {model.__name__}: {e}")


def add_equipment_menu():
    """Menu to add new equipment."""
    print("\n--- Add New Equipment ---")
    print("1. Add Fishing Bait")
    print("2. Add Fishing Line")
    print("3. Add Fishing Pole")
    print("4. Add Fishing Reel")
    choice = input("Select the equipment type to add (1-4): ").strip()

    if choice == "1":
        add_fishing_bait()
    elif choice == "2":
        add_fishing_line()
    elif choice == "3":
        add_fishing_pole()
    elif choice == "4":
        add_fishing_reel()
    else:
        print("Invalid choice. Returning to main menu.")


def add_fishing_bait():
    """Add a new fishing bait."""
    bait_id = input("Enter Bait ID: ").strip()
    bait_type = input("Enter Bait Type: ").strip()
    bait_color = input("Enter Bait Color: ").strip()

    item_id = generate_item_id()  # Generate unique item_id
    new_bait = FishingBait(bait_id=bait_id, bait_type=bait_type, bait_color=bait_color, item_id=item_id)
    session.add(new_bait)

    # Add to inventory
    inventory = Inventory(type="Fishing Bait", item_id=item_id, quantity=1)
    session.add(inventory)

    session.commit()
    print(f"Fishing bait added successfully with Item ID: {item_id}")


def add_fishing_line():
    """Add a new fishing line."""
    line_id = input("Enter Line ID: ").strip()
    line_material = input("Enter Line Material: ").strip()
    line_strength = input("Enter Line Strength: ").strip()
    line_length = input("Enter Line Length: ").strip()

    item_id = generate_item_id()  # Generate unique item_id
    new_line = FishingLine(line_id=line_id, line_material=line_material, line_strength=line_strength, line_length=line_length, item_id=item_id)
    session.add(new_line)

    # Add to inventory
    inventory = Inventory(type="Fishing Line", item_id=item_id, quantity=1)
    session.add(inventory)

    session.commit()
    print(f"Fishing line added successfully with Item ID: {item_id}")


def add_fishing_pole():
    """Add a new fishing pole."""
    pole_id = input("Enter Pole ID: ").strip()
    pole_length = input("Enter Pole Length: ").strip()
    pole_material = input("Enter Pole Material: ").strip()
    reel_id = input("Enter Reel ID: ").strip()
    line_id = input("Enter Line ID: ").strip()

    item_id = generate_item_id()  # Generate unique item_id
    new_pole = FishingPole(pole_id=pole_id, pole_length=pole_length, pole_material=pole_material, reel_id=reel_id, line_id=line_id, item_id=item_id)
    session.add(new_pole)

    # Add to inventory
    inventory = Inventory(type="Fishing Pole", item_id=item_id, quantity=1)
    session.add(inventory)

    # Optionally add relationships to Pole_bait
    while True:
        bait_id = input("Enter Bait ID to link to this pole (leave blank to skip): ").strip()
        if not bait_id:
            break
        pole_bait = PoleBait(pole_id=pole_id, bait_id=bait_id)
        session.add(pole_bait)

    session.commit()
    print(f"Fishing pole added successfully with Item ID: {item_id}")


def add_fishing_reel():
    """Add a new fishing reel."""
    reel_id = input("Enter Reel ID: ").strip()
    reel_size = input("Enter Reel Size: ").strip()

    item_id = generate_item_id()  # Generate unique item_id
    new_reel = FishingReel(reel_id=reel_id, reel_size=reel_size, item_id=item_id)
    session.add(new_reel)

    # Add to inventory
    inventory = Inventory(type="Fishing Reel", item_id=item_id, quantity=1)
    session.add(inventory)

    session.commit()
    print(f"Fishing reel added successfully with Item ID: {item_id}")


def remove_equipment_menu():
    """Menu to remove equipment."""
    print("\n--- Remove Equipment ---")
    equipment_type = input("Enter equipment type (Fishing Bait, Fishing Line, Fishing Pole, Fishing Reel): ").strip()
    item_id = input("Enter Item ID to remove: ").strip()

    # Mapping user input to class names
    equipment_mapping = {
        "Fishing Bait": FishingBait,
        "Fishing Line": FishingLine,
        "Fishing Pole": FishingPole,
        "Fishing Reel": FishingReel
    }

    if equipment_type not in equipment_mapping:
        print("Invalid equipment type. Returning to main menu.")
        return

    equipment_class = equipment_mapping[equipment_type]

    try:
        # Fetch the item to delete
        equipment_item = session.query(equipment_class).filter_by(item_id=item_id).first()
        inventory_item = session.query(Inventory).filter_by(item_id=item_id, type=equipment_type).first()

        if not equipment_item or not inventory_item:
            print(f"No such item with Item ID {item_id} found in {equipment_type}.")
            return

        # Delete the item
        session.delete(equipment_item)
        session.delete(inventory_item)
        session.commit()
        print(f"Item with Item ID {item_id} removed successfully from {equipment_type}.")

    except Exception as e:
        session.rollback()  # Rollback in case of an error
        print(f"Error removing item: {e}")

def modify_quantity(action):
    """Modify the quantity of an item in the inventory."""
    print("\n--- Modify Quantity ---")
    equipment_type = input("Enter equipment type (Fishing Bait, Fishing Line, Fishing Pole, Fishing Reel): ").strip()
    item_id = input(f"Enter Item ID: ").strip()
    amount = input("Enter the quantity to modify: ").strip()

    try:
        amount = int(amount)
        inventory = session.query(Inventory).filter_by(type=equipment_type, item_id=item_id).first()
        if inventory:
            if action == "increase":
                inventory.quantity += amount
            elif action == "decrease" and inventory.quantity >= amount:
                inventory.quantity -= amount
            else:
                print("Insufficient quantity to decrease.")
                return

            session.commit()
            print(f"{action.capitalize()}d quantity for {equipment_type} ID {item_id} by {amount}.")
        else:
            print(f"{equipment_type} with Item ID {item_id} not found in inventory.")
    except ValueError:
        print("Invalid input. Quantity must be a number.")
    except Exception as e:
        print(f"Error modifying quantity: {e}")


if __name__ == "__main__":
    main_menu()
    session.close()
