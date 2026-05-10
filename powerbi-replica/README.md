# Sales Overview — Power BI replica

A Power BI Project (PBIP) replica of the Sales Overview dashboard from the
reference screenshot. Includes a synthetic Superstore-like dataset, a fully
defined semantic model with all measures, and a layout spec for the report.

## Headline numbers (built into the synthetic data)

| Metric              | Target   | Generated |
|---------------------|---------:|----------:|
| Total Sales         |    2.30M |    2.30M  |
| Total Profit        |  286.41K |  286.41K  |
| Profit Margin %     |   12.47% |   12.45%  |
| Average Order Value |   458.56 |   458.53  |

## Folder layout

```
powerbi-replica/
├── SalesOverview.pbip                      # PBIP entry point — open this in Power BI Desktop
├── SalesOverview.Report/
│   ├── definition.pbir                     # Links the report to the semantic model
│   └── report.json                         # Blank page (build visuals per LAYOUT.md)
├── SalesOverview.SemanticModel/
│   ├── definition.pbism                    # Semantic model entry
│   └── model.bim                           # TMSL: tables, columns, relationships, measures
├── data/
│   └── superstore_sales.csv                # 5,016 generated order rows
├── scripts/
│   └── generate_data.py                    # Regenerate the CSV (seeded for reproducibility)
├── LAYOUT.md                               # Visual-by-visual build spec for the report page
└── README.md
```

## Opening the project

1. Install Power BI Desktop (Windows). PBIP support is on by default in recent
   versions; older builds need it enabled under **File → Options → Preview features
   → Power BI Project (.pbip) save format**.
2. Double-click `SalesOverview.pbip`.
3. The semantic model loads with three tables (`Sales`, `DateTable`, `Growth Rate %`),
   one relationship, and all measures already defined.
4. The report opens to a blank `Sales Overview` page — follow `LAYOUT.md` to drop
   in the visuals. Every measure referenced in the spec already exists, so each
   visual is a drag-and-drop.

If Power BI Desktop reports an issue with `report.json`, delete that file and
reopen — Desktop will write a fresh blank page while preserving the semantic
model. Visuals can then be built per `LAYOUT.md`.

## Regenerating the data

```bash
python3 scripts/generate_data.py
```

The script is deterministic (`random.seed(42)`) so reruns produce identical
output. After regenerating, click **Refresh** in Power BI Desktop.

## Measures included

All measures live on the `Sales` table unless noted.

**KPIs**
- `Total Sales` — `SUM(Sales[Sales])`
- `Total Profit` — `SUM(Sales[Profit])`
- `Profit Margin %` — `DIVIDE([Total Profit], [Total Sales])`
- `Average Order Value` — `DIVIDE([Total Sales], DISTINCTCOUNT(Sales[Order ID]))`

**Time intelligence** (uses `DateTable`)
- `Sales YTD` — `TOTALYTD([Total Sales], DateTable[Date])`
- `Sales LY` — `CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DateTable[Date]))`
- `Sales LY YTD` — YTD of last year, for the YTD-vs-LY comparison line chart

**What-If** (uses `Growth Rate %` parameter table; range −20% to +50%, step 1%)
- `Projected Sales` — `[Total Sales] * (1 + SELECTEDVALUE('Growth Rate %'[Growth Rate % Value], 0))`
- `Projected Profit` — `[Total Profit] * (1 + SELECTEDVALUE('Growth Rate %'[Growth Rate % Value], 0))`

**Product analytics**
- `Product Sales Rank` — dense `RANKX` over `Product Name`
- `ABC Classification` — `A - Top 20%` / `B - Next 30%` / `C - Bottom 50%` by
  cumulative share of total sales

## Notes

- The CSV path in the model's M query is relative (`..\data\superstore_sales.csv`).
  If Power BI Desktop can't resolve it, replace the file path in **Transform data →
  Source** with the absolute path to the CSV on your machine.
- Product names, categories, and sub-categories deliberately match the rows in
  the source screenshot (Canon imageCLASS 2200, Fellowes PB500, Cisco TelePresence
  EX90, HON 5400, GBC DocuBind TL300, GBC Ibimaster 500), so the product table
  in the dashboard reproduces.
