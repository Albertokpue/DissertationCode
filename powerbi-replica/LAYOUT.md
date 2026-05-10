# Layout spec — Sales Overview page

Page size: 1280 × 720. Background: light teal (`#CFE4E8` ≈ source). Text: dark
navy (`#0B2A3A`). Card chart background: dark navy (`#0B2A3A`) with white text
for the YTD-vs-LY line chart and the right-hand projected cards.

The page has 12 visuals, arranged in three rows. Coordinates are page-relative
(top-left origin, in pixels).

## Row 1 — KPI strip (y ≈ 110)

Four `Card` visuals sized 196×96.

| # | Position (x, y) | Field            | Format               | Title          |
|---|-----------------|------------------|----------------------|----------------|
| 1 | (40, 110)       | `[Total Sales]`         | `$#,0.00,,"M"` → 2.30M       | Total Sales         |
| 2 | (240, 110)      | `[Total Profit]`        | `$#,0,"K"` → 286.41K         | Total Profit        |
| 3 | (440, 110)      | `[Profit Margin %]`     | `0.00%` → 12.47%             | Profit Margin %     |
| 4 | (640, 110)      | `[Average Order Value]` | `$#,0.00` → 458.56           | Average Order Value |

## Row 2 — Charts (y ≈ 220, height 260)

### Sales by Category (clustered bar)
- Position: (40, 220), 540 × 260
- Y-axis: `Sales[Category]`
- X-axis: `[Total Sales]`
- Sort by `[Total Sales]` descending
- Data labels off; gridlines off

### Sales YTD vs Last Year (line chart, dark theme)
- Position: (600, 220), 640 × 260
- X-axis: `DateTable[Month]` (sorted by `Month Number`)
- Y-axis values: `[Sales YTD]` (cyan) and `[Sales LY YTD]` (red)
- Title: "Sales YTD vs Last Year"
- Legend: top right, "Sales YTD" / "Sales LY"

## Row 3 — Product table + slicers + projection cards (y ≈ 500, height 200)

### Product table
- Position: (40, 500), 540 × 200
- Visual type: `Table`
- Columns: `Product Name`, `[Total Sales]`, `[ABC Classification]`, `[Product Sales Rank]`
- Sort by `[Product Sales Rank]` ascending
- Renamed column headers: "Total Sales", "ABC Classification", "Product Sales Rank"
- Total row: sum of `[Total Sales]`, label "Total"

### Category slicer
- Position: (600, 220 - swap with row 2 if you want it above the line chart) — in the source it sits between the two row-2 charts; place at (600, 170), 200 × 40 if matching the source exactly.
- Field: `Sales[Category]`
- Style: dropdown

### Year slicer
- Position: (820, 170), 200 × 40
- Field: `DateTable[Year]`
- Style: dropdown

### Growth Rate % slicer (What-If)
- Position: (600, 500), 200 × 40
- Field: `'Growth Rate %'[Growth Rate %]`
- Style: single-value slider (set min −20%, max 50%, step 1%, default 0%)

### Projected Sales card
- Position: (820, 540), 200 × 100
- Field: `[Total Sales]` (top label) and `[Projected Sales]` (bottom)
- In the source, the "left" projection card actually shows `Total Sales` (2.30M)
  for comparison and the middle shows `Projected Sales`.
- Format: `$#,0.00,,"M"`

### Projected Sales (projection)
- Position: (1020, 540), 100 × 100
- Field: `[Projected Sales]`
- Format: `$#,0.00,,"M"`

### Projected Profit card
- Position: (1140, 540), 100 × 100
- Field: `[Projected Profit]`
- Format: `$#,0,"K"`

## Theme

The closest built-in theme to the source is **Innovate** with its dark cards on
a pale teal canvas. To match more precisely:

1. **View → Themes → Customize current theme**.
2. Page background: `#CFE4E8`.
3. Visual background (cards/charts on the dark stripe): `#0B2A3A`, foreground
   text white.
4. Data colors: `#19B5BC` (primary cyan), `#E84E4E` (LY red), `#1F4E5F` (secondary).
5. Save as **Sales Overview Theme** for reuse.

## Build order (fastest path)

1. Drop the four KPI cards across the top.
2. Drop `Sales by Category` bar chart.
3. Drop `Sales YTD vs Last Year` line chart, format dark theme.
4. Drop the product table, sort by rank.
5. Add the three slicers (Category, Year, Growth Rate %).
6. Add the three bottom cards (Total / Projected Sales / Projected Profit).
7. Apply the theme tweaks above.

Total build time after the model is loaded: ~15 minutes.
