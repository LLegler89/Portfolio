import random
import tkinter as tk

class_modifiers = {
    "Rogue": {"Attack": 2, "Speed": 5, "Defense":2},
    "Barbarian": {"Attack": 4, "Speed": 2, "Defense":3},
    "Fighter": {"Attack": 3, "Speed": 3, "Defense":3}
}

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.stats = {
            "Attack": 10,
            "Speed": 10,
            "Defense": 5,
            "HP": 100,
            "Exp": 0,  # Experience points
            "Level": 1,
        }
        self.inventory = []

    def gain_exp(self, enemy_level):
        # Calculate experience based on level ratio
        exp_gain = int(enemy_level/(self.stats["Level"]) * 10)
        self.stats["Exp"] += exp_gain
        print(f"You gained {exp_gain} experience points!")
        self.check_level_up()

    def check_level_up(self):
    # Define the experience required per level (adjust as needed)
      exp_to_level = [0, 10, 50, 100, 200, 300, 600, 950]  # Experience needed for each level

      if self.stats["Exp"] >= exp_to_level[self.stats["Level"]]:
         self.stats["Level"] += 1
         print(f"Congratulations! You've leveled up to {self.stats['Level']}.")

      if self.char_class in ["Rogue", "Barbarian", "Fighter"]:
        modifiers = class_modifiers[self.char_class]
        for stat, modifier in modifiers.items():
            self.stats[stat] += modifier

      print("\nYour new stats are:")
      for stat, value in self.stats.items():
        print(f"{stat}: {value}")

      else:
        pass

    def Attack(self, target):
        damage = self.stats['Attack'] - target.stats['Defense']
        if damage < 0:
            damage = 0
        target.stats['HP'] -= damage
        print(f"{self.name} Attacks {target.name} for {damage} damage!")
    def special_attack(self, target):
        damage = self.stats['Attack'] * 1.5 - target.stats['Defense']
        if damage < 0:
            damage = 0
        target.stats['HP'] -= damage

    def addItem(self, item):
        self.inventory.append(item)

    def usePotion(self):
        if self.inventory:
            potion = self.inventory.pop(0)
            potion.use(self)
        else:
            print("You don't have any potions!")

    def block(self):
        if random.random() < 0.9:  # 90% chance to block
            return True
        return False

    def dodge(self):
        if random.random() < 0.5:  # 50% chance to dodge
            return True
        return False

class TheHammer:
    def __init__(self):
            self.attackup = 15
    def use(self, character):
           character.stats["Attack"] += self.attackup
           print("Rage fills your heart. Blood must be spilled. The Hammer has awakened")

class HPPotion:
    def __init__(self, healing_amount):
        self.healing_amount = healing_amount

    def use(self, character):
      character.stats['HP'] += self.healing_amount
      print(f"{character.name} used a HP potion and recovered {self.healing_amount} HP!")

def generate_enemies(location):
    if location == "open field":
        names = ["Goblin", "Orc", "Skeleton", "Troll"]
        classtype = ['Barbarian','Rogue','Fighter']
    elif location == "cave":
        names = ["Bat", "Bat", "Golem"]

    enemies = []

    for _ in range(random.randint(1,4)):
        name = random.choice(names)
        if location == "open field":
            if name == 'Goblin':
                char_class = 'Rogue'
            elif name == 'Orc' or name == 'Troll':
                char_class = 'Barbarian'
            elif name == 'Skeleton':
                char_class = 'Fighter'
        elif location == "cave":
            if name == 'Bat':
                char_class = 'Rogue'
            elif name == 'Golem':
                char_class = 'Barbarian'

        enemy = Character(name, char_class)
        enemy.stats['Level'] = random.randint(1,3)

        if name == 'Bat':
            enemy.stats['HP'] = 10
        elif name == 'Golem':
            enemy.stats['HP'] = 30
        else:
            enemy.stats['HP'] = random.randint(10,20)

        enemies.append(enemy)
    return enemies

def start_game():
    player_name = input("Welcome Player! What should I call you?    ")
    char_class = input("Choose your class(Barbarian, Rogue, Fighter):")
    location = "open field"
    print(f"Welcome to the {location}! It's time to begin your adventure. Please choose a direction to continue your quest.")
    player = Character(player_name, char_class)
    for _ in range(2):
        player.addItem(HPPotion(10))

    while True:
        direction = input("Which direction do you want to walk? (left/right/straight) ").lower()
        if direction == 'left' or direction == 'right' or direction == 'straight':
            print("You are walking...")
            if random.random() < 0.5:
                print("You encountered an enemy!")
                enemies = generate_enemies(location)
                result = battle_loop(player, enemies)
                if result == "win":
                    print('Great Job!!!')
                if result == 'loss':
                                        # Create a Tkinter window
                    defeat_window = tk.Tk()
                    defeat_window.title("Defeat")

                    # Create a label with the defeat message
                    defeat_label = tk.Label(defeat_window, text="You lose!")
                    defeat_label.pack()

                    # Run the Tkinter event loop
                    defeat_window.mainloop()
                    break
            else:
                input("Press Enter to continue...")
        else:
            print("Invalid direction. P\lease choose again.")


def battle_loop(player, enemies):
    special_used = False
    while True:
        characters = [player] + enemies
        characters.sort(key=lambda char: char.stats['Speed'], reverse=True)
        for character in characters:
            if character.stats['HP'] <= 0:
                continue
            if character is player:
                print(f"\n{player.name} (Level {player.stats['Level']}, HP: {player.stats['HP']})")
                print("Enemies:")
                for i, enemy in enumerate(enemies):
                    if enemy.stats['HP'] > 0:
                        print(f"{i+1}. {enemy.name} (HP: {enemy.stats['HP']})")
                    if enemy.stats['HP'] < 0:
                      player.gain_exp(enemy.stats['Level'])
                while True:
                    action = input("Attack (a), Potion (p), Special (s), Run (r): ").lower()
                    if action == 'a':
                        while True:
                            try:
                                target_index = int(input("Choose a target: ")) - 1
                                if 0 <= target_index < len(enemies) and enemies[target_index].stats['HP'] > 0:
                                    target = enemies[target_index]
                                    break
                                else:
                                    print("Invalid target.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        character.Attack(target)
                        break
                    elif action == 's' and not special_used:
                        special_used = True
                        for enemy in enemies:
                            if enemy.stats['HP'] > 0:
                                character.special_attack(enemy)
                        break
                    elif action == 's' and special_used:
                        print("Special attack has already been used this battle.")
                    elif action == 'r':
                        print("You have fled the battle!")
                        return
                    else:
                        print("Invalid command. Please try again.")
            if all(enemy.stats['HP'] <= 0 for enemy in enemies):
                return "win"
            else:  # Enemy turn
                target = player
                character.Attack(target)
                if target.block():
                    damage = character.stats['Attack'] // 2
                    print(f"{target.name} the {target.char_class} blocks and takes reduced damage ({damage})!")
                if target.dodge():
                    print(f"{target.name} the {target.char_class} dodges the Attack!")
                if target.stats['HP'] <= 0:
                    return "loss"

if __name__ == "__main__":
    start_game()
