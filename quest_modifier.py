import os
import re

def load_monster_list():
    """
    Charge la liste des monstres dans un dictionnaire pour une recherche rapide.
    """
    monster_list = {
        0x01: "Rathian",
        0x02: "Rathalos",
        0x03: "Qurupeco",
        0x04: "Gigginox",
        0x05: "Barioth",
        0x06: "Diablos",
        0x07: "Deviljho",
        0x08: "Barroth",
        0x09: "Uragaan",
        0x0A: "Jaggi",
        0x0B: "Jaggia",
        0x0C: "Great Jaggi",
        0x0D: "Baggi",
        0x0E: "Great Baggi",
        0x0F: "Lagiacrus",
        0x10: "Royal Ludroth",
        0x11: "Ludroth",
        0x12: "Gobul",
        0x13: "Agnaktor",
        0x14: "Ceadeus",
        0x15: "Uroktor",
        0x16: "Delex",
        0x17: "Epioth",
        0x18: "Alatreon",
        0x19: "Jhen Mohran",
        0x1A: "Giggi",
        0x1B: "Aptonoth",
        0x1C: "Popo",
        0x1D: "Rhenoplos",
        0x1E: "Felyne",
        0x1F: "Melynx",
        0x20: "Fish",
        0x21: "Altaroth",
        0x22: "Kelbi",
        0x23: "Giggi Egg",
        0x24: "Bnahabra (Blue)",
        0x25: "Bnahabra (Red)",
        0x26: "Bnahabra (Green/Brown) (either or)",
        0x27: "Bnahabra (Green/Brown) (either or)",
        0x28: "Boulder (Underwater)",
        0x29: "Zinogre",
        0x2A: "Arzuros",
        0x2B: "Lagombi",
        0x2C: "Volvidon",
        0x2D: "Great Wroggi",
        0x2E: "Duramboros",
        0x2F: "Nibelsnarf",
        0x30: "Wroggi",
        0x31: "Slagtoth",
        0x32: "Gargwa",
        0x33: "Crimson Qurupeco",
        0x34: "Baleful Gigginox",
        0x35: "Sand Barioth",
        0x36: "Jade Barroth",
        0x37: "Steel Uragaan",
        0x38: "Purple Ludroth",
        0x39: "Glacial Agnaktor",
        0x3A: "Black Diablos",
        0x3B: "Nargacuga",
        0x3C: "Green Nargacuga",
        0x3D: "Lucent Nargacuga",
        0x3E: "Pink Rathian",
        0x3F: "Gold Rathian",
        0x40: "Azure Rathalos",
        0x41: "Silver Rathalos",
        0x42: "Plesioth",
        0x43: "Green Plesioth",
        0x44: "Ivory Lagiacrus",
        0x45: "Abyssal Lagiacrus",
        0x46: "Goldbeard Ceadeus",
        0x47: "Savage Deviljho",
        0x48: "Stygian Zinogre",
        0x49: "Rust Duramboros",
        0x4A: "Brachydios",
        0x4B: "Dire Miralis",
        0x4C: "Bullfango",
        0x4D: "Anteka",
        0x4E: "Slagtoth (Red)",
        0x4F: "Boulder (Deserted Island)",
        0x50: "Boulder (Sandy Plains)",
        0x51: "Boulder (Flooded Forest)",
        0x52: "Boulder (Tundra)",
        0x53: "Boulder (Volcano)",
        0x54: "Boulder (Misty Peaks)",
        0x55: "Hallowed Jhen Mohran",
        0x56: "Aptonoth",
        0x57: "Aptonoth",
        0x58: "Aptonoth",
    }
    return monster_list

def identify_monsters(file_path, monster_list, numfile):
    """
    Identifie jusqu'à cinq monstres dans un fichier binaire.
    Chaque monstre occupe 11 octets.
    """
    monsters = []
    try:
        with open(file_path, "rb") as file:
            # Se positionner à la position du premier monstre (432 octets avant la fin)
            file.seek(-432, os.SEEK_END)

            for i in range(5):  # Lire jusqu'à 5 monstres
                monster_data = file.read(11)  # Chaque monstre utilise 11 octets
                if len(monster_data) < 11:
                    break  # Pas assez de données pour un autre monstre

                # Le premier octet contient l'ID du monstre
                # Se positionner à la position du premier monstre (432 octets avant la fin)
            if numfile < 60000:
                file.seek(-432, os.SEEK_END)
            elif numfile == 60003 or numfile == 60008 or numfile == 60010: 
                file.seek(-1345, os.SEEK_END)
            else:
                file.seek(-1300, os.SEEK_END)
            
            for i in range(5):  # Lire jusqu'à 5 monstres
                pos = file.tell()  # Position actuelle dans le fichier
                monster_data = file.read(11)  # Chaque monstre utilise 11 octets
                if len(monster_data) < 11:
                    break  # Pas assez de données pour un autre monstre
                monster_id = int.from_bytes(monster_data[:1], "big")
                HP = monster_data[4]
                attack = monster_data[5]
                defense = monster_data[6]
                size = monster_data[9]
                size_variation = monster_data[8]
                fatigue = monster_data[10]
                monster_name = monster_list.get(monster_id)
                if(monster_name is not None):
                    monsters.append((pos, monster_id, monster_name, HP, attack, defense, fatigue))

    except Exception as e:
        return [f"Error: {e}"]

    return monsters


def process_directory_for_all_monsters(directory):
    """
    Parcours un dossier et identifie tous les monstres dans chaque fichier binaire.
    """
    monster_list = load_monster_list()
    results = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            match = re.match(r"q_(\d+)\.mib", file_name)
            if not match:
                continue  # Ignorer les fichiers non conformes

            numero = int(match.group(1))
            file_path = os.path.join(root, file_name)
            monsters = identify_monsters(file_path, monster_list, numero)
            if monsters:
                results.append((file_name, monsters))
 
    results2 = sorted(results, key=lambda x: x[0])
    return results2


def update_monsters(file_path, monsters, numero):
    """
    Divise la défense par 3 pour les monstres spécifiés et réécrit le fichier.
    """
    try:
        if(numero == 60001 or numero == 60004 or numero == 60008 or numero == 60009):
           defense_multipli = 0.5
           hp_multipli = 0.75
        elif(numero == 60002 or numero == 60005 or numero == 60010 or numero == 60011):
           defense_multipli = 0.25
           hp_multipli = 0.5
        elif(numero == 60000 or numero == 60003 or numero == 6006 or numero == 6007):
           defense_multipli = 1
           hp_multipli = 1
        else:
           defense_multipli = 0.25
           hp_multipli = 0.80
           fatigue_minus = 0
            
        with open(file_path, "r+b") as file:
            for pos, monster_id, _, HP, attack, defense, fatigue in monsters:
                new_defense = min(max(1, round(defense * defense_multipli)), 255)  # Évite une défense de 0
                new_HP = min(max(1, round(HP * hp_multipli)), 255)
                new_attack = min(max(1, attack - 8), 255)
                new_fatigue = min(max(0, fatigue - fatigue_minus), 255)
                # Positionner le curseur à la position correcte et écrire la nouvelle défense
               	file.seek(pos + 4)
                file.write(new_HP.to_bytes(1, "big"))
                file.seek(pos + 5)
                file.write(new_attack.to_bytes(1, "big"))
                file.seek(pos + 6)  # La défense est le 7ème octet (index 6)
                file.write(new_defense.to_bytes(1, "big"))

    except Exception as e:
        print(f"Error updating {file_path}: {e}")


def update_multi(directory):
    """
    Parcours le dossier, identifie les monstres dans les fichiers multi G-Rank,
    et met à jour leur défense.
    """
    monster_list = load_monster_list()

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            match = re.match(r"q_(\d+)\.mib", file_name)
            if not match:
                continue  # Ignorer les fichiers non conformes

            numero = int(match.group(1))
            if (numero > 11100 and numero < 12000) or (numero >= 12201) or (numero == 2904):  # Identifier les fichiers multi G-Rank
                monsters = identify_monsters(file_path, monster_list, numero)
                if monsters:
                    print(f"Updating file: {file_name}, Monsters: {monsters}")
                    update_monsters(file_path, monsters, numero)
                    
def printResult(results):
    printed = False
    printedSoloLR = False
    printedSoloHR = False
    printedMultiLR = False
    printedMultiHR = False
    printedMultiGR = False
    printedSoloUrgent = False
    printedMultiUrgent = False
    printedArena = False
    print("----------SOLO----------")
    for file_name, monsters in results:
        match = re.match(r"q_(\d+)\.mib", file_name)
        if match:
            numero = int(match.group(1))
            if(numero > 10000 and printed is False):
                print("-----------MULTI------------")
                printed = True
            if((numero > 1000 and printedSoloLR is False)):
                print("-----------LOWRANK------------")
                printedSoloLR = True
            if((numero > 1600 and printedSoloHR is False)):
                print("-----------HIGHRANK------------")
                printedSoloHR = True
            if((numero > 2000 and printedSoloUrgent is False)):
                print("-----------URGENT------------")
                printedSoloUrgent = True
            if((numero > 11000 and printedMultiLR is False)):
                print("-----------LOWRANK------------")
                printedMultiLR = True
            if((numero > 11300 and printedMultiHR is False)):
                print("-----------HIGHRANK------------")
                printedMultiHR = True
            if(numero > 11600 and printedMultiGR is False):
                print("-----------GRANK------------")
                printedMultiGR = True
            if((numero > 12000 and printedMultiUrgent is False)):
                print("-----------URGENT------------")
                printedMultiUrgent = True
            if((numero >= 60000 and printedArena is False)):
                print("-----------ARENA------------")
                printedArena = True
            if(len(monsters) != 0):
                if any(monster[2] == "Dire Miralis" for monster in monsters):
                    monstersPrint = []
                    for monster in monsters:
                        monstersPrint.append((monster[2], monster[3], monster[4], monster[5], monster[6]))
                    print(f"Fichier: {file_name}, Monstres: {monstersPrint}")


directory = "arcfs/quest/eu"
#update_multi(directory)
results = process_directory_for_all_monsters(directory)
printResult(results)

