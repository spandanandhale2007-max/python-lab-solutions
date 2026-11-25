"""
Experiment 9 - Question 10: E-commerce Product Catalog Converter

Scenario: An e-commerce platform keeps its inventory in products.csv with
columns such as product_id, name, price and stock. Convert the CSV into JSON
(products.json) for a frontend that displays products dynamically.

Usage:
  python q10_products_csv_to_json.py
  python q10_products_csv_to_json.py --in-stock-only --indent 4
"""

import argparse
import csv
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DEFAULT_CSV = os.path.join(DATA, "products.csv")
DEFAULT_JSON = os.path.join(DATA, "products.json")

LOW_STOCK = 10

SAMPLE_CSV = """product_id,name,category,price,stock,rating
P-1001,Digital Thermometer,Diagnostics,349.00,120,4.4
P-1002,Pulse Oximeter,Diagnostics,1299.00,45,4.6
P-1003,BP Monitor,Diagnostics,2199.00,8,4.3
P-1004,N95 Mask (pack of 10),Protective,499.00,0,4.1
P-1005,Surgical Gloves (box),Protective,650.00,210,4.5
P-1006,Nebulizer,Respiratory,1850.00,6,4.2
P-1007,Wheelchair Foldable,Mobility,7499.00,3,4.0
P-1008,Walking Stick,Mobility,899.00,64,3.9
P-1009,Glucometer Kit,Diagnostics,1099.00,0,4.4
P-1010,First Aid Box,General,1299.00,32,4.7
P-1011,Hot Water Bag,General,299.00,88,3.8
P-1012,Oxygen Concentrator,Respiratory,38999.00,2,4.8
"""


def ensure_sample(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(SAMPLE_CSV)
        print(f"[setup] created sample input {path}")


def to_product(row):
    price = float(row["price"])
    stock = int(row["stock"])
    return {
        "productId": row["product_id"],
        "name": row["name"],
        "category": row["category"],
        "price": price,
        "priceDisplay": f"Rs.{price:,.2f}",
        "stock": stock,
        "inStock": stock > 0,
        "lowStock": 0 < stock <= LOW_STOCK,
        "rating": float(row["rating"]),
        "inventoryValue": round(price * stock, 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a product catalogue CSV into frontend JSON.")
    parser.add_argument("--input", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_JSON)
    parser.add_argument("--indent", type=int, default=2)
    parser.add_argument("--in-stock-only", action="store_true",
                        help="export only products with stock above zero")
    args = parser.parse_args()

    ensure_sample(args.input)

    with open(args.input, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        headers = reader.fieldnames

    print(f"=== read {os.path.basename(args.input)} ===")
    print(f"  columns  : {headers}")
    print(f"  products : {len(rows)}")
    print(f"  size     : {os.path.getsize(args.input)} bytes")

    print("\n=== catalogue ===")
    print(f"  {'id':<9}{'name':<26}{'category':<14}{'price':>11}"
          f"{'stock':>7}{'rating':>8}")
    print("  " + "-" * 76)
    for r in rows:
        print(f"  {r['product_id']:<9}{r['name']:<26}{r['category']:<14}"
              f"{float(r['price']):>11,.2f}{int(r['stock']):>7}"
              f"{float(r['rating']):>8.1f}")

    products = [to_product(r) for r in rows]
    exported = [p for p in products if p["inStock"]] \
        if args.in_stock_only else products

    print("\n=== derived fields added for the frontend ===")
    print(json.dumps(products[0], indent=2))

    categories = defaultdict(list)
    for p in products:
        categories[p["category"]].append(p)

    summary = {
        "totalProducts": len(products),
        "exported": len(exported),
        "inStock": sum(1 for p in products if p["inStock"]),
        "outOfStock": sum(1 for p in products if not p["inStock"]),
        "lowStock": sum(1 for p in products if p["lowStock"]),
        "categories": sorted(categories),
        "priceRange": {"min": min(p["price"] for p in products),
                       "max": max(p["price"] for p in products)},
        "averagePrice": round(sum(p["price"] for p in products) /
                              len(products), 2),
        "inventoryValue": round(sum(p["inventoryValue"] for p in products), 2),
        "averageRating": round(sum(p["rating"] for p in products) /
                               len(products), 2),
    }

    payload = {"summary": summary, "products": exported}

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=args.indent, ensure_ascii=False)

    print(f"\n=== wrote {os.path.basename(args.output)} ===")
    print(f"  size     : {os.path.getsize(args.output)} bytes")
    print(f"  exported : {len(exported)} of {len(products)} product(s)")

    print("\n=== summary block ===")
    print(json.dumps(summary, indent=2))

    print("\n=== category breakdown ===")
    print(f"  {'category':<14}{'items':>6}{'in stock':>10}"
          f"{'avg price':>12}{'inventory value':>18}")
    for cat in sorted(categories):
        group = categories[cat]
        avg = sum(p["price"] for p in group) / len(group)
        value = sum(p["inventoryValue"] for p in group)
        print(f"  {cat:<14}{len(group):>6}"
              f"{sum(1 for p in group if p['inStock']):>10}"
              f"{avg:>12,.2f}{value:>18,.2f}")

    print("\n=== out of stock, hide or mark on the storefront ===")
    for p in products:
        if not p["inStock"]:
            print(f"  {p['productId']}  {p['name']:<26}"
                  f"{p['priceDisplay']:>14}")

    print(f"\n=== low stock (1 to {LOW_STOCK} units), reorder soon ===")
    for p in sorted((p for p in products if p["lowStock"]),
                    key=lambda x: x["stock"]):
        print(f"  {p['productId']}  {p['name']:<26}{p['stock']:>3} left")

    print("\n=== top rated and most valuable stock ===")
    for p in sorted(products, key=lambda x: -x["rating"])[:3]:
        print(f"  rating {p['rating']:.1f}  {p['name']}")
    print()
    for p in sorted(products, key=lambda x: -x["inventoryValue"])[:3]:
        print(f"  Rs.{p['inventoryValue']:>12,.2f} tied up in {p['name']}")

    print("\n=== round-trip check ===")
    with open(args.output, "r", encoding="utf-8") as fh:
        reloaded = json.load(fh)
    print(f"  products reloaded   : {len(reloaded['products'])}")
    print(f"  price is a number   : "
          f"{isinstance(reloaded['products'][0]['price'], float)}")
    print(f"  inStock is a boolean: "
          f"{isinstance(reloaded['products'][0]['inStock'], bool)}")
    print(f"  matches export      : "
          f"{len(reloaded['products']) == len(exported)}")
