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

    while True:
        user_input = input(prompt)
        if user_input.lstrip("-").isdigit():
            return int(user_input)
        print("Invalid input. Please enter a valid integer.")


def get_poke_dict_by_id(poke_id):

    for poke in HOENN_DATA:
        if poke["ID"] == poke_id:
            return poke.copy()
    return None
    pass


def get_poke_dict_by_name(name):

    name = name.strip().lower()
    for poke in HOENN_DATA:
        if poke["Name"].lower() == name:
            return poke.copy()
    pass


def display_pokemon_list(poke_list):

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

    first_pokemon = str(first_pokemon)
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
    print(f" New Pokedex created for {owner_name} with starter {pokemon['Name']}.")
    pass


def insert_owner_bst(root, new_node):

    if root is None:
        return new_node
    if new_node["name"] < root["name"]:
        root["left"] = insert_owner_bst(root["left"], new_node)
    elif new_node["name"] > root["name"]:
        root["right"] = insert_owner_bst(root["right"], new_node)

    return root
    pass


def find_owner_bst(root, owner_name):
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

def min_node(node):

    current = node
    while current and current["left"] is not None:
        current = current["left"]
    return current


def delete_owner_bst(root, owner_name):

    if owner_name.lower() < root["name"].lower():
        root["left"] = delete_owner_bst(root["left"], owner_name)
    elif owner_name.lower() > root["name"].lower():
        root["right"] = delete_owner_bst(root["right"], owner_name)
    else:
        # Step 2: Node found, handle deletion cases
        # Case 1: Node has no children (leaf node)
        if root["left"] is None and root["right"] is None:
            return None
        # Case 2: Node has only one child (right child)
        elif root["left"] is None:
            return root["right"]
        elif root["right"] is None:
            return root["left"]
        else:
            # Case 3: Node has two children
            # Find the in-order successor (leftmost node in the right subtree)
            successor = min_node(root["right"])
            # Replace current node's value with the successor's value
            root["name"] = successor["name"]
            root["pokedex"] = successor["pokedex"]
            # Delete the successor node
            root["right"] = delete_owner_bst(root["right"], successor["name"])

    return root

########################
# 3) BST Traversals
########################

def bfs_traversal(root):

    if not root:
        return
    # Initialize a list to represent a queue for level-order traversal
    queue = [root]

    while queue:
        current_node = queue.pop(0)
        print(f"\nOwner: {current_node['name']}")

        # Print each Pokemon in the owner's Pokedex
        for poke in current_node['pokedex']:
            print(f"ID: {poke['ID']}, Name: {poke['Name']}, Type: {poke['Type']}, HP: {poke['HP']}"
                  f", Attack: {poke['Attack']}, Can Evolve: {poke['Can Evolve']}")
        # Enqueue the left and right children
        if current_node['left']:
            queue.append(current_node['left'])
        if current_node['right']:
            queue.append(current_node['right'])


def pre_order(root):

    if root:
        print(f"Owner: {root['name']}")
        # Print each Pokemon in the owner's Pokedex
        for poke in root['pokedex']:
            print(f"ID: {poke['ID']}, Name: {poke['Name']}, Type: {poke['Type']}, HP: {poke['HP']}"
                  f", Attack: {poke['Attack']}, Can Evolve: {poke['Can Evolve']}")
        # Traverse the left subtree
        pre_order(root['left'])
        # Traverse the right subtree
        pre_order(root['right'])

def in_order(root):

    if root:
        # Traverse the left subtree
        in_order(root['left'])
        print(f"Owner: {root['name']}")
        # Print each Pokemon in the owner's Pokedex
        for poke in root['pokedex']:
            print(f"ID: {poke['ID']}, Name: {poke['Name']}, Type: {poke['Type']}, HP: {poke['HP']}"
                  f", Attack: {poke['Attack']}, Can Evolve: {poke['Can Evolve']}")
        # Traverse the right subtree
        in_order(root['right'])


def post_order(root):

    if root:
        # Traverse the left subtree
        post_order(root['left'])
        # Traverse the right subtree
        post_order(root['right'])
        print(f"Owner: {root['name']}")
        # Print each Pokemon in the owner's Pokedex
        for poke in root['pokedex']:
            print(f"ID: {poke['ID']}, Name: {poke['Name']}, Type: {poke['Type']}, HP: {poke['HP']}"
                  f", Attack: {poke['Attack']}, Can Evolve: {poke['Can Evolve']}")

########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):

    pokemon_id = read_int_safe("Enter Pokemon ID to add: ")
    pokemon = get_poke_dict_by_id(int(pokemon_id))
    if not pokemon:
        print(f"ID {pokemon_id} not found in Honen data.")
        return
    for existing_pokemon in owner_node["pokedex"]:
        if existing_pokemon["ID"] == pokemon["ID"]:
            print(f"Pokemon already in the list. No changes made.")
            return
    owner_node["pokedex"].append(pokemon)
    print(f"Pokemon {pokemon['Name']} (ID {pokemon_id}) added to {owner_node['name']}'s Pokedex.")
    pass

def release_pokemon_by_name(owner_node):

    name_to_release = input("Enter Pokemon Name to release: ").strip().lower()
    for poke in owner_node["pokedex"]:
        if poke["Name"].strip().lower() == name_to_release:
            owner_node["pokedex"].remove(poke)
            print(f"Releasing{poke['Name']} from {owner_node['name']}.")
            return
    print(f"No Pokemon named '{name_to_release}' in {owner_node['name']}'s Pokedex.")

    pass


def evolve_pokemon_by_name(owner_node):
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

    if root:
        gather_all_owners(root["left"], arr)
        arr.append(root)  # Collect the current node
        gather_all_owners(root["right"], arr)

def sort_owners_by_num_pokemon():

    if not ownerRoot:
        print("No owners at all.")
        return

    owners = []
    gather_all_owners(ownerRoot, owners)
    print("=== The Owners we have, sorted by number of Pokemons ===")

    # Sort by the size of the pokedex, then by name (case-insensitive)
    owners.sort(key=lambda owner: (len(owner["pokedex"]), owner["name"].lower()))

    # Print sorted results
    for owner in owners:
        num_pokemons = len(owner["pokedex"])
        print(f"Owner: {owner['name']} (has {num_pokemons} Pokemon)")
        if num_pokemons == 0:
            print("There are no Pokémons in this Pokedex that match the criteria.")

########################
# 6) Print All
########################

def print_all_owners(root):

    print("1) BFS")
    print("2) Pre-Order")
    print("3) In-Order")
    print("4) Post-Order")
    traversal_choice = read_int_safe("Your choice: ")
    if traversal_choice == 1:
        bfs_traversal(root)
    elif traversal_choice == 2:
        pre_order(root)
    elif traversal_choice == 3:
        in_order(root)
    elif traversal_choice == 4:
        post_order(root)
    else:
        print("Invalid choice.")

########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):

    choice = 0
    while choice != 7:
        print("\n-- Display Filter Menu --"
              "\n1. Only a certain Type"
              "\n2. Only Evolvable"
              "\n3. Only Attack above __"
              "\n4. Only HP above __"
              "\n5. Only names starting with letter(s)"
              "\n6. All of them!"
              "\n7. Back")
        choice = read_int_safe("Your choice: ")
        filtered_pokedex = []
        if choice == 1:
            poke_type = input("Which Type? (e.g. GRASS, WATER): ").strip().lower()
            filtered_pokedex = [poke for poke in owner_node["pokedex"] if poke["Type"].lower() == poke_type]
        elif choice == 2:
            filtered_pokedex = [poke for poke in owner_node["pokedex"] if poke["Can Evolve"] == "TRUE"]
        elif choice == 3:
            attack_threshold = read_int_safe("Enter Attack threshold: ")
            filtered_pokedex = [poke for poke in owner_node["pokedex"] if poke["Attack"] > attack_threshold]
        elif choice == 4:
            hp_threshold = read_int_safe("Enter HP threshold: ")
            filtered_pokedex = [poke for poke in owner_node["pokedex"] if poke["HP"] > hp_threshold]
        elif choice == 5:
            starting_letters = input("Starting letter(s): ").strip().lower()
            filtered_pokedex = [poke for poke in owner_node["pokedex"] if
                                poke["Name"].lower().startswith(starting_letters)]
        elif choice == 6:
            filtered_pokedex = owner_node["pokedex"]
        elif choice == 7:
            print("Back to Pokedex Menu.")
            return
        else:
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
        print(f"Owner'{owner_name}' not found.")
        return
    choice = 0
    while choice != 5:
        print(f"\n-- {existing_owner['name']}'s Pokedex Menu --")
        print("1. Add Pokemon"
              "\n2. Display Pokedex"
              "\n3. Release Pokemon"
              "\n4. Evolve Pokemon"
              "\n5. Back to Main")
        choice = read_int_safe("Your choice: ")

        if choice == 1:
            add_pokemon_to_owner(existing_owner)
        elif choice == 2:
            display_filter_sub_menu(existing_owner)
        elif choice == 3:
            release_pokemon_by_name(existing_owner)
        elif choice == 4:
            evolve_pokemon_by_name(existing_owner)
        elif choice == 5:
            print("Back to Main Menu.")
        else:
            print("Invalid choice. Please try again.")
    pass


def main_menu():
    global ownerRoot

    choice = 0
    while choice != 6:
        print("\n=== Main Menu ==="
              "\n1. New Pokedex"
              "\n2. Existing Pokedex"
              "\n3. Delete a Pokedex"
              "\n4. Display owners by number of Pokemon"
              "\n5. Print All"
              "\n6. Exit")
        choice = read_int_safe("Your choice: ")

        if choice == 1:
            owner_name = input("Owner name: ")
            owner_name_lower = owner_name.strip().lower()
            existing_owner = find_owner_bst(ownerRoot, owner_name_lower)
            if existing_owner:
                print(f"Owner '{owner_name}' already exists. No new Pokedex created.")
            else:
                first_pokemon = read_int_safe("Choose your starter Pokemon:"
                                              "\n1) Treecko"
                                              "\n2) Torchic"
                                              "\n3) Mudkip"
                                              "\nYour choice:")
                create_owner_node(owner_name, first_pokemon)

        elif choice == 2:
            existing_pokedex()
        elif choice == 3:
            owner_name = input("Owner name: ").strip()
            existing_owner = find_owner_bst(ownerRoot, owner_name)
            if existing_owner:
                ownerRoot = delete_owner_bst(ownerRoot, owner_name)
                print(f"Pokedex belonging to '{owner_name}' has been deleted.")
            else:
                print(f"'{owner_name}' not found in the database.")
        elif choice == 4:
            sort_owners_by_num_pokemon()
        elif choice == 5:
            print_all_owners(ownerRoot)
        elif choice == 6:
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")
    pass

def main():

    main_menu()
    pass

if __name__ == "__main__":
    main()
