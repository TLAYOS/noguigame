import random
import time

print('----------SELECT YOUR HERO----------')
# HEROE'S STATS
hp = 0
atk = 0
arm = 0
pwr = 0
mn = 0
sp = 0
selected_hero = ""

# NAHUAL'S STATS
enemy_name = "NAHUAL"
nhp = 3000
natk = 250
narm = 75
npwr = 250
nmn = 10000
nsp = 75

hero_actions = {
    "MAGE":[("Guard", 0, 60, "buff_def", "none" ), ("Heal", -150, 40, "heal", "magic"), ("Magic Boom", 300, 60, "damage", "magic"), 
            ("Mystic Ties", 200, 40, "damage", "magic"), ("Meditate", 0, 50, "buff_power", "none"), ("Zap", 300, 50, "damage", "magic"), ("Staff Bonk", 5, 1,  "damage", "physical") ],
    
    "KNIGHT":[("Shield Up", 0, 15, "buff_def", "none"), ("Tackle", 100, 35, "damage", "physical"), ("Double Slash", 300, 60, "damage", "physical"), ("Sword Swipe", 150, 25, "damage", "physical"),
              ("War Cry", 0, 50, "buff_atk", "none"), ("Light Magic", 2, 15, "damage", "magic"), ("Stab", 75, 15, "damage", "physical")],
    
    "TANK":[("Muscle Flex", 0, 60, "buff_def", "none"), ("Sound Clap", 150, 25, "damage", "physical"), ("Earthquake", 200, 40, "damage", "magic"), ("Cannon Ball", 300, 50, "damage", "physical"), 
            ("Ultra Kick", 50, 15, "damage", "physical"), ("Mega Punch", 50, 10, "damage", "physical"), ("Wall Breaker", 250, 35,"damage", "physical")],
    
    "SAMURAI":[("Parry", 0, 15,"buff_def", "none"), ("Bamboo Cutter", 75, 15, "damage", "physical"), ("Inner Peace", 0, 70, "buff_atk", "none"), ("Forward Slash", 150, 25, "damage", "physical"), 
               ("Flash Attack", 250, 40, "damage", "none"), ("Shadow Attack", 250, 45, "damage", "none"), ("Lighthing Magic", 7, 15, "damage", "magic")]
}

enemy_actions = {
    "NAHUAL":[("HOWLING", 0, 50, "buff_def", "none"), ("BITE", 250, 50, "damage", "physical"), ("POUNCE", 200, 30, "damage", "physical"),
               ("WIND MAGIC", 300, 70, "damage", "magic"), ("DARK", 400, 90, "damage", "magic")],
    
    "IMP":[("EVIL LAUGHTER", 0, 50, "buff_atk", "none"), ("FIRE BREATH", 275, 70, "damage", "magic"), ("DARK FORCE", 350, 400, "damage", "magic"),
            ("TAIL WHIP", 200, 80, "damage", "physical"), ("SHRIEK", 150, 80, "damage", "physical")],
    
    "PROCRASTINATOR":[("LEECH", 100, 70, "heal_enemy", "magic"), ("DRAIN", 150, 100, "heal_enemy", "magic"), ("SLICE", 300, 90, "damage", "physical"),
                       ("TANTRUM", 0, 100, "buff_atk", "none"), ("SLAP", 250, 95, "damage", "physical")]
}

buffs = {
    "hero_attack": 0, "hero_power": 0, "hero_def": 0, "hero_sp": 0, "enemy_attack": 0,"enemy_power": 0, "enemy_def": 0
}

def dmg_calc(base_damage, attacker_stat, defender_stat, damage_type):
    if damage_type == "physical":
        final_damage = base_damage + (attacker_stat * 0.5) - (defender_stat * 0.3)
    elif damage_type == "magic":
        final_damage = base_damage + (attacker_stat - 0.5) - (defender_stat * 0.3)
    else:
        return 0
    return final_damage


def stats():
    print(f"""
          {selected_hero} STATUS:           HP: {hp}     POWER: {pwr}     ATTACK: {atk}     MANA: {mn}
          """)
    
def nahual():
    print(f"""
          NAHUAL HP: {nhp}""")
    
def apply_buff(target, buff_type):
    if target == "hero":
        if buff_type == "buff_atk":
            buffs["hero_attack"] = 2
            print(f"THE {selected_hero}'S ATTACK WILL INCREASE FOR 2 TURNS")
        elif buff_type == "buff_def":
            buffs["hero_def"] = 2
            print(f"THE {selected_hero}'S ARMOR WILL INCREASE FOR 2 TURNS")
        elif buff_type == "buff_power":
            buffs["hero_power"] = 2
            print(f"THE {selected_hero}'S POWER WILL INCREASE FOR 2 TURNS")
    elif target == "enemy":
        if buff_type == "buff_atk":
            buffs["enemy_attack"] = 2
            print("THE ENEMY'S ATTACK WILL INCREASE FOR THE NEXT 2 TURNS")
        elif buff_type == "buff_def":
            buffs["enemy_def"] = 2
            print("THE ENEMY'S DEFENSE WILL INCREASE FOR THE NEX 2 TURNS")
            
def attack_nahual(action_name, base_damage, mana_cost, action_type, damage_type):
    global nhp, hp, mn
    if mn < mana_cost:
        print(f"NOT ENOUGH MANA! {mn}/{mana_cost} NEEDED. TURN SKIPPED.")
        return 0
    
    mn -= mana_cost
    
    if action_type == "damage":
        attacker_stat = pwr if damage_type == "magic" else atk
        defender_stat = nsp if damage_type == "magic" else narm
        final_damage = dmg_calc(base_damage, attacker_stat, defender_stat, damage_type)
        nhp -= final_damage
        print(f"YOU USED {action_name}! IT DEALED {final_damage} {damage_type} DAMAGE!")
    elif action_type == "heal":
        hp += -base_damage
        print(f"YOU USED {action_name}! YOU RESTORED {-base_damage} HP.")
    elif action_type in ["buff_atk", "buff,def"]:
        apply_buff("hero", action_type)
    
    nhp = max(nhp, 0)
    if nhp == 0:
        print(f"YOU DEFEATED THE {enemy_name}!")
        return True
    return False 
                
def enemy_attack():
    global hp, nhp, nmn
    if nmn < 30:
        print(f"THE {enemy_name} IS OUT OF MANA AND CANNOT ATTACK!")
        return False
    
    action_name, base_damage, mana_cost, action_type, damage_type = random.choice(enemy_actions[enemy_name])
    if nmn < mana_cost:
        print(f"THE {enemy_name} DOESN'T HAVE ENOUGH MANA TO USE {action_name}")
        return False
    
    nmn -= mana_cost
    
    if action_type == "damage":
        attacker_stat = npwr if damage_type == "magic" else natk
        defender_stat = sp if damage_type == "magic" else arm
        final_damage = dmg_calc(base_damage, attacker_stat, defender_stat, damage_type)
        hp -= final_damage 
        print(f"THE {enemy_name} USED {action_name}! IT DEALT, {final_damage} {damage_type} DAMAGE.")
    elif action_type == "heal_enemy":
        nhp += base_damage
        print(f"THE {enemy_name} USED {action_name}! IT HEALED {base_damage} HP.")
    elif action_type in ["buff_atk", "buff_def"]:
        apply_buff("ene,y", action_type)
        
    hp = max(hp, 0)
    if hp == 0:
        print(F"YOU WERE DEFEATED BY THE {enemy_name}... GAME OVER!")
        return True
    return False

def battle():
    while nhp > 0 and hp > 0:
        stats()
        nahual()
        for buff in buffs:
            if buffs[buff] > 0:
                buffs[buff] -= 1
        
        print(f"------------- {selected_hero} ABILITY MENU ---------------")        
        abilities = hero_actions[selected_hero]
        for i, (ability, _, _, _, _) in enumerate(abilities, 1):
            print(f"{i} {ability}")
        print(f"{len(abilities) +1}) EXIT MENU")
        
        try:
            choice = int(input("CHOOSE AN ABILITY: "))
            if choice == len(abilities) +1:
                print("EXITING MENU...")
                break
            elif 1 <= choice <= len(abilities):
                action_name, damage, mana_cost, action_type, damage_type = abilities[choice -1]
                if attack_nahual(action_name, damage, mana_cost, action_type, damage_type):
                 break
            else:
                print("Invalid choice. Please select a valid action.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        time.sleep(1)
        
        if enemy_attack():
            break
        
        time.sleep(1)
        


while True:
    print("""
      1) MAGE
      2) KINGHT
      3) TANK
      4) SAMURAI""")
    try:
       charac = int(input("Chioce "))
    except ValueError:
        print("Invalido input. Please enter a number.")
        continue
    if charac not in [1, 2, 3, 4]:
        print("""PLEASE SELECT ONE OF THE FOLLOWING HEROES:""")
        continue
    
    opc = None
    
    if charac == 1:
        print("""THE MAGE HAS THE FOLLOWING STATS:
          HP: 1500
          ATTACK: 15
          ARMOR: 350
          POWER: 600
          MANA: 500
          SPIRIT: 400
          ARE YOU SURE YOU WANT THIS HERO?:
          1) YES
          2) NO""")
        try:
            opc = int(input("ANSWER: "))
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")
            continue
    if opc == 1:
        print("SO BE IT")
        selected_hero = "MAGE"
        hp += 1500
        atk += 15
        arm += 350
        pwr += 600
        mn += 500
        sp += 400
        break
    elif opc == 2:
        print("TAKE ANOTHER LOOK AT THE HEROES")
        
        continue
    
    elif charac == 2:
        print("""THE KNIGHT HAS THE FOLLOWING STATS:
              HP: 2000
              ATTACK: 300
              ARMOR: 200
              POWER: 15
              MANA: 200
              SPIRIT: 100
              ARE YOU SURE YOU WANT THIS HERO?
              1) YES
              2) NO""")
        try:
            opc = int(input("ANSWER: "))
        except ValueError:
            print("Invalid input. please enter 1 or 2")
            continue
    if opc == 1:
        print("SO BE IT")
        selected_hero = "KNIGHT"
        hp += 2000
        atk += 300
        arm += 200
        pwr += 15
        mn += 200
        sp += 100
        break
    elif opc == 2:
        print("TAKE ANOTHER LOOK AT THE HEROES")
        
        continue
    
    elif charac == 3:
        print("""THE TANK HAS THE FOLLOWING STATS:
              HP: 4000
              ATTACK: 175
              ARMOR: 400
              POWER: 100
              MANA: 300
              SPIRIT: 400
              ARE YOU SURE YOU WANT THIS HERO?
              1) YES
              2) NO""")
        try:
            opc = int(input("ANSWER: "))
        except ValueError:
            print("Invalid input. please enter 1 or 2")
            continue
    if opc == 1:
        print("SO BE IT")
        selected_hero = "TANK"
        hp += 4000
        atk += 175
        arm += 400
        pwr += 100
        mn += 300
        sp += 400
        break
    elif opc == 2:
        print("TAKE ANOTHER LOOK AT THE HEROES")
        
        continue
    
    elif charac == 4:
        print("""THE SAMURAI HAS THE FOLLOWING STATS:
              HP: 1500
              ATTACK: 400
              ARMOR: 250
              POWER: 50
              MANA: 200
              SPIRIT: 150
              ARE YOU SURE YOU WANT THIS HERO?:
              1) YES
              2) NO""")
        try:
            opc = int(input("ANSWER: "))
        except ValueError:
            print("Invalid input. please enter 1 or 2")
            continue
    if opc == 1:
        print("SO BE IT")
        selected_hero = "SAMURAI"
        hp += 1500
        atk += 400
        arm += 250
        pwr += 50
        mn += 200
        sp += 150
        break
    elif opc == 2:
         
         print("TAKE ANOTHER LOOK AT THE HEROES")
         
         continue
    

def act_menu():
    while True:
        print("ABILITIES MENU")
        abilities = hero_actions[selected_hero]
        for i, ability in enumerate(abilities, 1):
            print(f"{i} {ability}")
        print("8) EXIT")
        
        try:
            choice = int(input("Choose an ability: "))
            if choice == 5:
                print("Exiting menu...")
                break
            elif 1 <= choice <= 7: 
                print(f"YOU USED {abilities[choice -1]}!")
            else:
                print("Invalid choice. Please select an ability")
        except ValueError:
            print("Invalid Input. Please enter a number")
        


print("----------THE BATTLE BEGINS----------")

print("A NAHUAL APPEARS!")

battle()