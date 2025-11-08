import json

# Ruta de los archivos
INPUT_FILE = "sv10.json"
OUTPUT_FILE = "cards_subcategory.csv"

def parse_card(card):
    subcategories = []
    
    # Verificar subtypes (Basic, Stage 1, Stage 2, etc)
    if "subtypes" in card:
        for subtype in card["subtypes"]:
            if subtype in ["Basic", "Stage 1", "Stage 2", "MEGA"]:
                subcategories.append({"type": subtype, "id": {
                    "Basic": 5,
                    "Stage 1": 6,
                    "Stage 2": 7,
                    "MEGA": 8
                }.get(subtype)})
    
    # Verificar supertype para Trainer cards
    if card.get("supertype") == "Trainer":
        if "subtypes" in card:
            for subtype in card["subtypes"]:
                if subtype in ["Supporter", "Stadium", "Item", "Pokémon Tool"]:
                    subcategories.append({"type": subtype, "id": {
                        "Supporter": 1,
                        "Stadium": 2,
                        "Item": 3,
                        "Pokémon Tool": 4
                    }.get(subtype)})
    
    # Verificar si es un Pokémon-ex
    if "subtypes" in card and "ex" in card["subtypes"]:
        subcategories.append({"type": "ex", "id": 9})

    # Generar consultas SQL
    setraw = 16  # MEG
    card_id = f"(SELECT id FROM card c WHERE c.id_expansion = '{setraw}' AND c.`number` = '{card.get('number', '')}' LIMIT 1)"
    
    sql_queries = []
    for subcategory in subcategories:
        if subcategory["id"]:  # Solo si tenemos un ID válido
            sql_queries.append(
                f"INSERT INTO card_to_subcategory (id_card, id_subcategory) VALUES ({card_id}, {subcategory['id']});"
            )
    
    return sql_queries

def main():
    # Leer JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cards = data if isinstance(data, list) else data.get("data", [])

    # Escribir las consultas SQL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for card in cards:
            sql_queries = parse_card(card)
            for query in sql_queries:
                f.write(query + "\n")

    print(f"✅ Archivo CSV generado correctamente: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()