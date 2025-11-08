import json
import csv
import argparse
from pathlib import Path

def normalize(s):
    return (s or "").strip()

def resolve_input_path(arg_path: str) -> Path:
    p = Path(arg_path)
    if p.exists():
        return p
    p_cwd = Path.cwd() / arg_path
    if p_cwd.exists():
        return p_cwd
    script_dir = Path(__file__).parent
    p_script = script_dir / arg_path
    if p_script.exists():
        return p_script
    p_parent = script_dir.parent / arg_path
    if p_parent.exists():
        return p_parent
    p_repo = script_dir.parents[1] / arg_path
    if p_repo.exists():
        return p_repo
    raise FileNotFoundError(f"Input file not found (tried several locations): {arg_path}")

def extract_unique_abilities(input_path):
    p = resolve_input_path(input_path)
    text = p.read_text(encoding="utf-8")
    data = json.loads(text)
    cards = data if isinstance(data, list) else data.get("data", [])
    seen = set()
    abilities = []
    for card in cards:
        for ability in (card.get("abilities") or []):
            name = normalize(ability.get("name"))
            txt = normalize(ability.get("text"))
            if not name:
                continue
            key = (name, txt)
            if key in seen:
                continue
            seen.add(key)
            abilities.append({"name": name, "text": txt})
    return abilities

def save_csv(abilities, out_path):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "text"])
        writer.writeheader()
        for a in abilities:
            writer.writerow(a)
    return out.resolve()

def main():
    p = argparse.ArgumentParser(description="Extraer abilities únicas (name,text) desde JSON de cartas")
    p.add_argument("input", nargs="?", default="SV10.json", help="Archivo JSON de cartas")
    p.add_argument("--out-csv", default="unique_abilities.csv", help="CSV de salida (solo name,text)")
    args = p.parse_args()

    try:
        abilities = extract_unique_abilities(args.input)
    except Exception as e:
        print(f"Error: {e}")
        return

    out_file = save_csv(abilities, args.out_csv)
    print(f"Guardadas {len(abilities)} abilities únicas en: {out_file}")

if __name__ == "__main__":
    main()