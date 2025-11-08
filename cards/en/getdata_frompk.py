import json
import csv

# Ruta de los archivos
INPUT_FILE = "sv10.json"
OUTPUT_FILE = "cards.csv"

# Columnas que tendrá el CSV
FIELDNAMES = [
    "id", "name", "id_category", "previous_stage",
    "img_small", "img_large", "id_ability", "regulation",
    "id_expansion", "number", "id_rarity", "id_type"
]

def parse_card(card):
    # Mapeo de category
    category_map = {
        "Pokémon": 1,
        "Trainer": 2,
        "Energy": 3
    }
    supertype = card.get("supertype", "")
    category = category_map.get(supertype, "")

    # Mapeo de ability
    ability_map = {
        "Wild Growth": 1,
        "Fermented Juice": 2,
        "Cast-Off Shell": 3,
        "Intimidating Fang": 4,
        "Psychic Draw": 5,
        "Heave-Ho Catcher": 7,
        "Lunar Cycle": 8,
        "Run Errand": 9,
        "Energized Steps": 10,
        "Healing Leaves": 11,
        "Stimulated Evolution": 12,
        "Inferno Fandango": 13,
        "Torrential Whirlpool": 14,
        "Distorted Future": 15,
        "Oceanic Curse": 16,
        "Ancient Wing": 17,
        "Look for Prey": 18,
        "Greedy Eater": 19,
        "Bouffer": 20,
        "Plume Protection": 21,
        "Regal Cheer": 22,
        "Torrid Scales": 24,
        "Mighty Shell": 25,
        "Gentle Fin": 26,
        "Dynamotor": 27,
        "Debut Performance": 28,
        "Craftsmanship": 29,
        "Sturdy": 30,
        "Poison Point": 31,
        "Gear Coating": 32,
        "Metallic Signal": 33,
        "Protective Cover": 34,
        "Buzzing Boost": 35,
        "Cheer On to Glory": 36,
        "Flower Curtain": 37,
        "Mysterious Rock Inn": 38,
        "Charging Up": 39,
        "Hurried Gait": 40,
        "Bonded by the Journey": 41,
        "Melt Away": 42,
        "Golden Flame": 43,
        "Flustered Leap": 44,
        "So Submerged": 45,
        "Repelling Veil": 46,
        "Diver's Catch": 47,
        "Snow Camouflage": 48,
        "Darkest Impulse": 49,
        "Power Saver": 50,
        "Stone Palace": 51,
        "Rocket Brain": 52,
        "Lose Cool": 53,
        "Sand Stream": 54,
        "Champion's Call": 55,
        "Mud Coat": 56,
        "Potent Glare": 57,
        "Sneaky Bite": 58,
        "Biting Spree": 59,
        "Smog Signals": 60,
        "Punk Up": 61,
        "X-Boot": 62,
        "Reconstitute": 63,
        "Greedy Order": 64
    }
    abilityraw = card.get("abilities", [{}])[0].get("name", "") if card.get("abilities") else ""
    ability = ability_map.get(abilityraw, "")

    # Mapeo de set
    setraw = 14

    # Mapeo de rarity
    rarity_map = {
        "Common": 1,
        "Uncommon": 2,
        "Rare": 3,
        "Double Rare": 4,
        "Ultra Rare": 5,
        "Illustration Rare": 6,
        "Special Illustration Rare": 7,
        "Hyper Rare": 8,
        "Promo": 9,
    }
    rarityraw = card.get("rarity", "")
    rarity = rarity_map.get(rarityraw, "")

    # Mapeo de type
    type_map = {
        "Colorless": 1,
        "Darkness": 2,
        "Water": 3,
        "Grass": 4,
        "Fire": 5,
        "Lightning": 6,
        "Fighting": 7,
        "Psychic": 8,
        "Metal": 9,
        "Dragon": 10,
        "Fairy": 11
    }
    typeraw = card.get("types", [None])[0] if card.get("types") else ""
    type = type_map.get(typeraw, "")

    return {
        "id": "",
        "name": card.get("name", ""),
        "id_category": category, 
        "previous_stage": card.get("evolvesFrom", ""),
        "img_small": card.get("images", {}).get("small", ""),
        "img_large": card.get("images", {}).get("large", ""),
        "id_ability": ability,
        "regulation": card.get("regulationMark", ""),
        "id_expansion": setraw,
        "number": card.get("number", ""),
        "id_rarity": rarity,
        "id_type": type
    }

def main():
    # Leer JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # data puede ser un dict o lista
    cards = data if isinstance(data, list) else data.get("data", [])

    # Crear CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        for card in cards:
            writer.writerow(parse_card(card))

    print(f"✅ Archivo CSV generado correctamente: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
