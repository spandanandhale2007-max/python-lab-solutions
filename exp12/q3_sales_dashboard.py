"""
Experiment 12 - Question 3: Sales Data Dashboard

Scenario: A data analyst for a retail chain builds a dashboard that visualises
the sales distribution by category.

Rubrics covered:
  * create a DataFrame with product and sales data
  * group and aggregate by category
  * visualise with a pie chart and a bar chart

Requires: pandas, numpy, matplotlib
"""

import pandas as pd

from chart_style import CATEGORICAL, apply_style, label_bars, save
import matplotlib.pyplot as plt


def build_frame():
    return pd.DataFrame([
        ("Paracetamol 500mg", "Medicines", 18400, 1840),
        ("Amoxicillin 250mg", "Medicines", 12600, 420),
        ("Cough Syrup", "Medicines", 7800, 390),
        ("Digital Thermometer", "Devices", 20940, 60),
        ("Pulse Oximeter", "Devices", 38970, 30),
        ("BP Monitor", "Devices", 26388, 12),
        ("N95 Mask (10s)", "Protective", 14970, 30),
        ("Surgical Gloves", "Protective", 19500, 30),
        ("Face Shield", "Protective", 4400, 40),
        ("Multivitamin", "Supplements", 11200, 160),
        ("Protein Powder", "Supplements", 16500, 15),
        ("First Aid Box", "General", 9093, 7),
        ("Hot Water Bag", "General", 5382, 18),
    ], columns=["product", "category", "revenue", "units"])


def main():
    apply_style()
    df = build_frame()

    print("=== product sales DataFrame ===")
    print(df.to_string(index=False))
    print(f"\n  rows {len(df)}, categories "
          f"{df['category'].nunique()}")

    print("\n=== groupby category ===")
    grouped = df.groupby("category").agg(
        products=("product", "count"),
        revenue=("revenue", "sum"),
        units=("units", "sum"),
        avg_revenue=("revenue", "mean"),
        top_product=("revenue", "idxmax"),
    )
    grouped["top_product"] = df.loc[grouped["top_product"], "product"].values
    grouped["share_percent"] = (
        grouped["revenue"] / grouped["revenue"].sum() * 100).round(1)
    grouped["avg_revenue"] = grouped["avg_revenue"].round(0).astype(int)
    grouped = grouped.sort_values("revenue", ascending=False)
    print(grouped.to_string())

    total = df["revenue"].sum()
    print("\n=== headline numbers ===")
    print(f"  total revenue       : Rs.{total:,}")
    print(f"  total units sold    : {df['units'].sum():,}")
    print(f"  products tracked    : {len(df)}")
    print(f"  average revenue per product : "
          f"Rs.{df['revenue'].mean():,.2f}")
    print(f"  biggest category    : {grouped.index[0]} "
          f"(Rs.{grouped['revenue'].iloc[0]:,}, "
          f"{grouped['share_percent'].iloc[0]:.1f}%)")
    print(f"  smallest category   : {grouped.index[-1]} "
          f"(Rs.{grouped['revenue'].iloc[-1]:,})")

    print("\n=== top 5 products by revenue ===")
    print(df.nlargest(5, "revenue")[["product", "category", "revenue",
                                     "units"]].to_string(index=False))

    print("\n=== revenue per unit, by category ===")
    per_unit = (grouped["revenue"] / grouped["units"]).round(2)
    for cat, value in per_unit.sort_values(ascending=False).items():
        print(f"  {cat:<13}Rs.{value:>9,.2f} per unit")
    print("  Devices sell few units at high value; Medicines are the"
          " opposite.")

    print("\n=== pivot: revenue by category and units band ===")
    df["units_band"] = pd.cut(df["units"], bins=[0, 50, 500, 2000],
                              labels=["<=50", "51-500", "500+"])
    pivot = df.pivot_table(index="category", columns="units_band",
                           values="revenue", aggfunc="sum",
                           observed=False).fillna(0).astype(int)
    print(pivot.to_string())

    # ---------------- charts ----------------
    categories = grouped.index.tolist()
    revenues = grouped["revenue"].tolist()
    colours = CATEGORICAL[:len(categories)]

    fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(13, 5.5))

    # pie: share of the whole. Only five slices, each directly labelled.
    wedges, _, autotexts = ax_pie.pie(
        revenues, labels=None, colors=colours, startangle=90,
        counterclock=False,
        autopct=lambda pct: f"{pct:.1f}%",
        pctdistance=0.72,
        wedgeprops=dict(edgecolor="#FCFCFB", linewidth=2))
    for text in autotexts:
        text.set_color("#FFFFFF")
        text.set_fontsize(9)
        text.set_fontweight("bold")
    ax_pie.set_title("Share of revenue by category")
    ax_pie.legend(wedges,
                  [f"{c}  Rs.{r:,}" for c, r in zip(categories, revenues)],
                  loc="center left", bbox_to_anchor=(0.98, 0.5))
    ax_pie.grid(False)

    # bar: the same numbers, read as magnitudes rather than angles
    bars = ax_bar.barh(categories[::-1], revenues[::-1],
                       color=colours[::-1], edgecolor="#FCFCFB",
                       linewidth=2, height=0.68)
    label_bars(ax_bar, bars, revenues[::-1], fmt="Rs.{:,.0f}",
               offset=0.015, horizontal=True)
    ax_bar.set_title("Revenue by category")
    ax_bar.set_xlabel("Revenue (Rs.)")
    ax_bar.set_xlim(0, max(revenues) * 1.22)
    ax_bar.grid(axis="y", visible=False)

    fig.suptitle(f"Retail sales dashboard - Rs.{total:,} across "
                 f"{len(df)} products")
    save(fig, "q3_sales_pie_bar.png")

    # second figure: units vs revenue, since the two tell different stories
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    x = range(len(categories))
    width = 0.38
    rev_scaled = [r / 1000 for r in revenues]
    units = grouped["units"].tolist()
    units_scaled = [u / 10 for u in units]

    b1 = ax2.bar([i - width / 2 for i in x], rev_scaled, width=width,
                 color=CATEGORICAL[0], edgecolor="#FCFCFB", linewidth=2,
                 label="Revenue (Rs. thousands)")
    b2 = ax2.bar([i + width / 2 for i in x], units_scaled, width=width,
                 color=CATEGORICAL[2], edgecolor="#FCFCFB", linewidth=2,
                 label="Units sold (tens)")
    label_bars(ax2, b1, rev_scaled, fmt="{:.0f}k", offset=0.02)
    label_bars(ax2, b2, units_scaled, fmt="{:.0f}", offset=0.02)

    ax2.set_xticks(list(x))
    ax2.set_xticklabels(categories)
    ax2.set_ylabel("Indexed value (see legend)")
    ax2.set_title("Revenue and volume on one common scale, not two y-axes")
    ax2.legend(loc="upper right")
    save(fig2, "q3_revenue_vs_units.png")

    print("\n=== reading the charts ===")
    print("  The pie answers 'what share of revenue?' - five slices only, each")
    print("  labelled with its percentage and rupee value.")
    print("  The bar chart answers 'how much?' - the same figures as lengths,")
    print("  which the eye compares far more accurately than angles.")
    print("  The third chart puts revenue and volume on one indexed scale")
    print("  rather than a dual y-axis, which would let any conclusion be")
    print("  manufactured by rescaling.")


if __name__ == "__main__":
    main()
