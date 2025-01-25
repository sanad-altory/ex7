import csv

# Global BST root
ownerRoot = None


########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")


########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    pass


def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    for poke in HOENN_DATA:
        if poke["ID"] == poke_id:
            return poke.copy()
    return None
    pass


def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    name = name.strip().lower()
    for poke in HOENN_DATA:
        if poke["Name"].lower() == name:
            return poke.copy()
    pass


def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    if not poke_list:
        print("There are no Pokemons in this Pokedex that match the criteria.")
    else:
        for poke in poke_list:
            print(f"ID: {poke['ID']}, Name: {poke['Name']}, Type: {poke['Type']}, "
                  f"HP: {poke['HP']}, Attack: {poke['Attack']}, Can Evolve: {poke['Can Evolve']}")
    pass


########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    if first_pokemon not in ["1","2","3"]:
        print("Invalid. No new Pokedex created.")
        return
    pokemon=None
    if first_pokemon=="1":
        pokemon=HOENN_DATA[0]
    elif first_pokemon=="2":
        pokemon=HOENN_DATA[3]
    else:
        pokemon=HOENN_DATA[6]
    owner_name = owner_name.strip()

    root={
        "name":owner_name,
        "pokedex":[],
        "left":None,
        "right":None,
    }
    root["pokedex"].append(pokemon)
    global ownerRoot
    ownerRoot =insert_owner_bst(ownerRoot, root)
    print(f"New Pokedex created for {owner_name} with the starter Pokemon {pokemon['Name']}.")
    pass


def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    if root is None:
        return new_node
    if new_node["name"] < root["name"]:
        root["left"] = insert_owner_bst(root["left"], new_node)
    elif new_node["name"] > root["name"]:
        root["right"] = insert_owner_bst(root["right"], new_node)

    return root
    pass


def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    if root is None:
        return None

    # Perform case-insensitive comparison (lowercase the names for comparison)
    if owner_name.lower() < root["name"].lower():
        return find_owner_bst(root["left"], owner_name)
    elif owner_name.lower() > root["name"].lower():
        return find_owner_bst(root["right"], owner_name)
    elif owner_name.lower() == root["name"].lower():
        return root

    return None
    pass

def find_parent(root,owner_name):
    if root is None:
        return None

    # Perform case-insensitive comparison (lowercase the names for comparison)
        if root["left"][]


    return None
    pass
def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    pass


def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    deleted_node = find_owner_bst(root, owner_name)
    if deleted_node is None:
        print(f"No owner named '{owner_name}' found.")
        return root
    elif deleted_node["left"] is None and deleted_node["right"] is None:
        deleted_node_parent = find_owner_bst(root, deleted_node["name"])
        deleted_node_parent["left"] = None
    pass


########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    pass


def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    pass


def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    pass


def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    pass


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    pokemon_id = input("Enter Pokemon ID to add: ")
    pokemon = get_poke_dict_by_id(int(pokemon_id))
    if not pokemon:
        print(f"ID{pokemon_id}not found in Honen data.")
        return
    for existing_pokemon in owner_node["pokedex"]:
        if existing_pokemon["ID"] == pokemon["ID"]:
            print(f"Pokemon already in the list. No changes made.")
            return
    owner_node["pokedex"].append(pokemon)
    print(f"Pokemon {pokemon["Name"]} (ID {pokemon_id}) added to {owner_node["name"]}'s Pokedex")
    pass

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    name_to_release = input("Enter Pokemon name to release: ").strip().lower()
    for poke in owner_node["pokedex"]:
        if poke["Name"].strip().lower() == name_to_release:
            owner_node["pokedex"].remove(poke)
            print(f"Pokemon {poke['Name']} has been released from {owner_node['name']}'s Pokedex.")
            return
    print(f"No Pokemon named '{name_to_release}'in {owner_node['name']}'s Pokedex.")

    pass


def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    name_to_evolve = input("Enter Pokemon name to evolve: ").strip().lower()

    # Find the Pokemon to evolve in the owner's Pokedex
    for poke in owner_node["pokedex"]:
        if poke["Name"].strip().lower() == name_to_evolve:
            if poke["Can Evolve"] == "FALSE":
                print(f"Pokemon {poke['Name']} cannot evolve.")
                return
            # Find the evolved Pokemon in Hoenn data
            evolution_id = poke["ID"] + 1  # Assuming evolution is the next ID
            evolved_poke = get_poke_dict_by_id(evolution_id)

            if not evolved_poke:
                print(f"No evolution found for Pokemon {poke['Name']} (ID {poke['ID']}).")
                return

            # Remove the original Pokemon
            owner_node["pokedex"].remove(poke)

            # Check if the evolved Pokemon already exists
            for existing_pokemon in owner_node["pokedex"]:
                if existing_pokemon["ID"] == evolved_poke["ID"]:
                    print(
                        f"Pokemon evolved from {poke['Name']} (ID {poke['ID']}) to {evolved_poke['Name']} (ID {evolved_poke['ID']}).")
                    print(f"{evolved_poke['Name']} was already present; releasing it immediately.")
                    return
            # Add the evolved Pokemon
            owner_node["pokedex"].append(evolved_poke)
            print(
                f"Pokemon evolved from {poke['Name']} (ID {poke['ID']}) to {evolved_poke['Name']} (ID {evolved_poke['ID']}).")
            return
    # If Pokemon not found
    print(f"No Pokemon named '{name_to_evolve}' found in {owner_node['name']}'s Pokedex.")
    pass


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    pass


def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    pass


def pre_order_print(node):
    """
    Helper to print data in pre-order.
    """
    pass


def in_order_print(node):
    """
    Helper to print data in in-order.
    """
    pass


def post_order_print(node):
    """
    Helper to print data in post-order.
    """
    pass


########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    choice = 0
    while choice != 7:
        print("""
    -- Display Filter Menu --
    1. Only a certain Type
    2. Only Evolvable
    3. Only Attack above __
    4. Only HP above __
    5. Only names starting with letter(s)
    6. All of them!
    7. Back
    """)
        choice = int(input("Your choice: "))
        filtered_pokedex = []

        match choice:
            case 1:
                poke_type = input("Which Type? (e.g. GRASS, WATER): ").strip().lower()
                filtered_pokedex = [poke for poke in owner_node["pokedex"] if poke["Type"].lower() == poke_type]
            case 2:
                filtered_pokedex = [poke for poke in owner_node["pokedex"] if poke["Can Evolve"] == "TRUE"]
            case 3:
                attack_threshold = int(input("Enter Attack threshold: "))
                filtered_pokedex = [poke for poke in owner_node["pokedex"] if poke["Attack"] > attack_threshold]
            case 4:
                hp_threshold = int(input("Enter HP threshold: "))
                filtered_pokedex = [poke for poke in owner_node["pokedex"] if poke["HP"] > hp_threshold]
            case 5:
                starting_letters = input("Starting letter(s): ").strip().lower()
                filtered_pokedex = [poke for poke in owner_node["pokedex"] if
                                    poke["Name"].lower().startswith(starting_letters)]
            case 6:
                filtered_pokedex = owner_node["pokedex"]
            case 7:
                print("Back to Pokedex Menu.")
                return
            case _:
                print("Invalid choice. Please try again.")
                continue

        if not filtered_pokedex:
            print("There are no Pokemons in this Pokedex that match the criteria.")
        else:
            display_pokemon_list(filtered_pokedex)
    pass


########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex():
    owner_name = input("Owner name: ").strip()
    existing_owner = find_owner_bst(ownerRoot, owner_name.lower())
    if not existing_owner:
        print(f"'{existing_owner["name"]}' not found.")
        return
    choice = 0
    while choice != 5:
        print(f"-- {existing_owner["name"]}'s Pokedex Menu --")
        print("1. Add Pokemon"
              "\n2. Display Pokedex"
              "\n3. Release Pokemon"
              "\n4. Evolve Pokemon"
              "\n5. Back to main")
        choice = int(input("Enter your choice: "))
        match choice:
            case 1:
                add_pokemon_to_owner(existing_owner)
            case 2:
                display_filter_sub_menu(existing_owner)
            case 3:
                release_pokemon_by_name(existing_owner)
            case 4:
                evolve_pokemon_by_name(existing_owner)



    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """


    pass


def main_menu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """
    choice = 0
    while choice != 6:
        print("""
    === Main Menu ===
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """)
        choice = int(input("Your choice: "))
        match choice:
            case 1:
                print(ownerRoot)
                owner_name = input("Owner name: ")
                owner_name_lower =owner_name.strip().lower()
                existing_owner = find_owner_bst(ownerRoot, owner_name_lower)
                if existing_owner:
                    print(f"Owner '{owner_name}' already exists. No new Pokedex created.")
                else:
                    first_pokemon = input("""
                               Choose your starter Pokemon:
                               1) Treecko
                               2) Torchic
                               3) Mudkip
                               Your choice: """)
                    create_owner_node(owner_name, first_pokemon)

            case 2:
                existing_pokedex()
            case 3:
                delete_owner_bst(ownerRoot, input("Owner name: ").strip().lower())
            # case 4:
            #     sort_owners()
            # case 5:
            #     print_all()
            case 6:
                print("Exiting...")
            case deafult:
                print("Invalid choice. Please try again.")
                continue

    pass


def main():
    """
    Entry point: calls main_menu().
    """
    main_menu();
    pass


if __name__ == "__main__":
    main()
