"""Generate synthetic Superstore-like sales data for the Power BI replica.

Targets (from the source dashboard screenshot):
    Total Sales        ~ 2.30M
    Total Profit       ~ 286.41K
    Profit Margin %    ~ 12.47%
    Average Order Value~ 458.56

Output: ../data/superstore_sales.csv
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "superstore_sales.csv"

START_DATE = date(2023, 1, 1)
END_DATE = date(2024, 12, 31)
N_ORDERS = 5016

PRODUCTS = [
    # (Category, Sub-Category, Product Name, base_price, base_margin)
    ("Technology", "Copiers",        "Canon imageCLASS 2200 Advanced Copier", 1500.00, 0.30),
    ("Office Supplies", "Binders",   "Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind", 900.00, 0.25),
    ("Technology", "Phones",         "Cisco TelePresence System EX90 Videoconferencing Unit", 2200.00, 0.20),
    ("Furniture", "Chairs",          "HON 5400 Series Task Chairs for Big and Tall", 700.00, 0.18),
    ("Office Supplies", "Binders",   "GBC DocuBind TL300 Electric Binding System", 650.00, 0.22),
    ("Office Supplies", "Binders",   "GBC Ibimaster 500 Manual ProClick Binding System", 550.00, 0.20),
    ("Technology", "Phones",         "Polycom CX600 IP Phone", 280.00, 0.18),
    ("Technology", "Accessories",    "Logitech MX Master Wireless Mouse", 110.00, 0.30),
    ("Technology", "Accessories",    "Logitech G910 Mechanical Keyboard", 180.00, 0.28),
    ("Technology", "Machines",       "Zebra ZP 450 Thermal Label Printer", 350.00, 0.22),
    ("Furniture", "Chairs",          "Global Deluxe High-Back Manager's Chair", 420.00, 0.16),
    ("Furniture", "Bookcases",       "Bush Westfield Collection Bookcase", 380.00, 0.12),
    ("Furniture", "Tables",          "Bretford Rectangular Conference Table", 1200.00, 0.10),
    ("Furniture", "Furnishings",     "Eldon Image Series Desk Accessories", 45.00, 0.35),
    ("Office Supplies", "Storage",   "Fellowes Bankers Box Heavy-Duty Storage Boxes", 60.00, 0.32),
    ("Office Supplies", "Paper",     "Xerox Premium Multipurpose Paper", 35.00, 0.40),
    ("Office Supplies", "Paper",     "Hammermill Copy Plus Paper", 28.00, 0.38),
    ("Office Supplies", "Appliances",
                                     "Hoover Commercial Lightweight Vacuum", 320.00, 0.20),
    ("Office Supplies", "Art",       "Newell 312 Mechanical Pencil", 6.50, 0.45),
    ("Office Supplies", "Envelopes", "Avery Self-Adhesive Address Labels", 15.00, 0.42),
    ("Office Supplies", "Fasteners", "OIC Heavy-Duty Binder Clips", 4.50, 0.50),
    ("Office Supplies", "Labels",    "Avery 5"  + chr(34) + " x 8" + chr(34) + " Label", 12.00, 0.44),
    ("Office Supplies", "Supplies",  "Stanley Bostitch Heavy-Duty Stapler", 38.00, 0.30),
    ("Technology", "Accessories",    "SanDisk Ultra 64GB USB Flash Drive", 22.00, 0.32),
    ("Technology", "Accessories",    "Belkin 8-Outlet Surge Protector", 55.00, 0.28),
    ("Furniture", "Furnishings",     "DAX Two-Tone Rosewood/Black Document Frame", 28.00, 0.30),
    ("Furniture", "Tables",          "Hon Every-Day Round Conference Table", 950.00, 0.10),
    ("Furniture", "Bookcases",       "Sauder Camden County Barrister Bookcase", 480.00, 0.08),
    ("Office Supplies", "Storage",   "Tennsco Industrial Steel Shelving", 240.00, 0.26),
    ("Technology", "Machines",       "HP LaserJet Pro M404n Printer", 280.00, 0.24),
]

REGIONS = ["Central", "East", "South", "West"]
SEGMENTS = ["Consumer", "Corporate", "Home Office"]

def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for i in range(1, N_ORDERS + 1):
        order_date = random_date(START_DATE, END_DATE)
        ship_date = order_date + timedelta(days=random.randint(1, 7))
        category, sub_category, product, base_price, base_margin = random.choices(
            PRODUCTS,
            # weight toward mid-priced items so AOV lands near the target
            weights=[
                # Technology
                3, 6, 1, 5, 5, 6, 8, 12, 9, 7,
                # Furniture
                6, 8, 2, 14, 12, 18, 16, 6, 22, 14,
                # Office Supplies / mixed
                20, 14, 12, 16, 12, 14, 4, 8, 9, 9,
            ],
            k=1,
        )[0]

        quantity = random.choices([1, 2, 3, 4, 5], weights=[55, 25, 12, 5, 3])[0]
        # discount up to 30%
        discount = random.choices(
            [0.0, 0.1, 0.15, 0.2, 0.3], weights=[55, 20, 12, 9, 4]
        )[0]
        # noise on the per-unit price
        unit_price = base_price * random.uniform(0.92, 1.10)
        sales = round(unit_price * quantity * (1 - discount), 2)
        # margin shrinks with discount
        effective_margin = base_margin - discount * 0.6 + random.uniform(-0.04, 0.04)
        profit = round(sales * effective_margin, 2)

        rows.append({
            "Order ID": f"CA-{order_date.year}-{i:06d}",
            "Order Date": order_date.isoformat(),
            "Ship Date": ship_date.isoformat(),
            "Customer ID": f"CU-{random.randint(1000, 1999)}",
            "Segment": random.choice(SEGMENTS),
            "Region": random.choice(REGIONS),
            "Category": category,
            "Sub-Category": sub_category,
            "Product Name": product,
            "Quantity": quantity,
            "Discount": discount,
            "Sales": sales,
            "Profit": profit,
        })

    # Scale to hit the headline numbers exactly.
    total_sales = sum(r["Sales"] for r in rows)
    total_profit = sum(r["Profit"] for r in rows)
    sales_scale = 2_300_000 / total_sales
    profit_target = 286_410
    for r in rows:
        r["Sales"] = round(r["Sales"] * sales_scale, 2)
        r["Profit"] = round(r["Profit"] * sales_scale, 2)
    # Re-sum and apply a small profit-only correction
    total_sales = sum(r["Sales"] for r in rows)
    total_profit = sum(r["Profit"] for r in rows)
    profit_adjust = (profit_target - total_profit) / len(rows)
    for r in rows:
        r["Profit"] = round(r["Profit"] + profit_adjust, 2)

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total_sales = sum(r["Sales"] for r in rows)
    total_profit = sum(r["Profit"] for r in rows)
    n_orders = len({r["Order ID"] for r in rows})
    print(f"Wrote {len(rows)} rows -> {OUTPUT}")
    print(f"  Total Sales:  {total_sales:,.2f}")
    print(f"  Total Profit: {total_profit:,.2f}")
    print(f"  Margin %:     {total_profit / total_sales:.4%}")
    print(f"  AOV:          {total_sales / n_orders:,.2f}")


if __name__ == "__main__":
    main()
