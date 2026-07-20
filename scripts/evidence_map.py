import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Intervention and Outcome lists

interventions = [
    "Aerobic exercise",
    "Resistance training",
    "Respiratory Muscle Training",
    "Protein supplementation",
    "Dietary councelling",
    "Complete Oral Nutritional Supplement",
    "Micronutrients supplementation",
    "Psychological interventions",
]

outcomes = [
    "Functional Capacity",
    "Post-operative complications",
    "Length of hospital stay",
    "Nutritional Status/Body composition",
    "Quality of Life",
    "Neoadjuvant chemotherapy adherence",
]

# Create short labels for clear plotting

short_interventions = {
    "Aerobic exercise": "Aerobic exercise",
    "Resistance training": "Resistance training",
    "Respiratory Muscle Training": "Resp. muscle training",
    "Protein supplementation": "Protein supplementation",
    "Dietary councelling": "Dietary counselling",
    "Complete Oral Nutritional Supplement": "Oral nutr. supp. (ONS)",
    "Micronutrients supplementation": "Micronutrients",
    "Psychological interventions": "Psychological",
}

short_outcomes = {
    "Functional Capacity": "Functional\ncapacity",
    "Post-operative complications": "Post-op\ncomplications",
    "Length of hospital stay": "Hospital\nstay",
    "Nutritional Status/Body composition": "Nutritional\nstatus",
    "Quality of Life": "Quality\nof life",
    "Neoadjuvant chemotherapy adherence": "Neoadj. chemo\nadherence",
}

min_studies = 5   #less than 5 studies are noted as insufficient evidence

# BUILD EVIDENCE MATRIX

def build_evidence_matrix(df):
    # count how many studies included each intervention and reported each outcome
    rows = []
    for intervention in interventions:
        for outcome in outcomes:
            eligible_rows = (df[intervention] == "Yes") & (df[outcome] != "Not reported")
            n = int(eligible_rows.sum())
            # Add each intervention-outcome combination and its no of studies as one row if eligible
            rows.append({"Intervention": intervention, "Outcome": outcome, "Studies": n})
    return pd.DataFrame(rows)

# Load cleaned dataset
df = pd.read_csv("data/cleaned_evidence_table.csv")

# Build evidence matrix using cleaned dataset
evidence_matrix = build_evidence_matrix(df)

# Pivot data for plotting
plot_matrix = evidence_matrix.pivot(
    index="Intervention", # denote rows 
    columns="Outcome",
    values="Studies"
).reindex(index=interventions, columns=outcomes)  

# CREATE EVIDENCE GAP MAP

fig, ax = plt.subplots(figsize=(12, 6))
n_rows, n_cols = plot_matrix.shape # no of rows and columns in matrix
max_n = int(plot_matrix.values.max()) # highest study count

# Draw one coloured rectangle per cell and write number of studies on top

for i in range(n_rows):
    for j in range(n_cols):
        n = int(plot_matrix.iloc[i, j])

        if n == 0:
            # True evidence gap (dark grey boxes)
            facecolor = "darkgrey"
            text = "—"
            textcolor = "grey"
            fontweight = "normal"

        elif n < min_studies:
            # Too few studies (light grey boxes)
            facecolor = "lightgrey"
            text = f"n={n}*"
            textcolor = "dimgray"
            fontweight = "normal"

        else:
            # Enough studies (blue boxes), intensity based on number of studies available
            intensity = 0.3 + 0.6 * (n/max_n)
            facecolor = plt.cm.Blues(intensity)
            text = f"n={n}"
            textcolor = "black" if intensity < 0.55 else "white"
            fontweight = "bold"

        # Draw a rounded rectangle for current cell
        # FancyBboxPatch starts at bottom-left corner
        # The rectangle is 0.90 × 0.90, so subtracting half (0.45)
        # so the box is centred at the grid position (j,i)

        rect = mpatches.FancyBboxPatch(
            (j - 0.45, i - 0.45), 0.90, 0.90,
            boxstyle="round,pad=0.03",
            facecolor=facecolor, edgecolor="white", linewidth=2,
            zorder=2)

        # Add the rectangle to the axes
        ax.add_patch(rect)

        # Place study count at center of cell
        ax.text(j, i, text,
            ha="center", va="center",
            fontsize=9, fontweight=fontweight, color=textcolor,
            zorder=3)

# Set axis limits

ax.set_xlim(-0.5, n_cols - 0.5)
ax.set_ylim(n_rows - 0.5, -0.5)    # flip y so row 0 is at the top

# Add labels to x axis

ax.set_xticks(range(n_cols))
ax.set_xticklabels([short_outcomes[o] for o in outcomes], fontsize=9, ha="center", linespacing=1.3)
ax.xaxis.set_tick_params(length=0)

# Add labels to y axis

ax.set_yticks(range(n_rows))
ax.set_yticklabels([short_interventions[iv] for iv in interventions], fontsize=9)
ax.yaxis.set_tick_params(length=0)

# Add white grid lines between cells

for x in np.arange(-0.5, n_cols, 1):
    ax.axvline(x, color="white", linewidth=2.5, zorder=1)
for y in np.arange(-0.5, n_rows, 1):
    ax.axhline(y, color="white", linewidth=2.5, zorder=1)

# Remove axis borders

for spine in ax.spines.values():
    spine.set_visible(False)

# Create legend

# Create custom colored boxes for legend
legend_patches = [
    mpatches.Patch(facecolor="darkgrey", edgecolor="white", label="No studies - evidence gap"),
    mpatches.Patch(facecolor="lightgrey", edgecolor="white", label=f"n < {min_studies} - Insufficient evidence*"),
    mpatches.Patch(facecolor="cornflowerblue", edgecolor="white", label=f"n ≥ {min_studies} - Evidence available (darker blue = more studies)")
]

# Add legend below evidence table
ax.legend(
    handles=legend_patches,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.22),
    ncol=1, fontsize=8.5, frameon=False)

# Add title and axis labels

ax.set_title(
    "Evidence Gap Map: Intervention Components vs Reported Outcomes\n"
    "n = studies that included this component AND reported this outcome  "
    "(descriptive only — no causal inference implied)",
    fontsize=10, fontweight="bold",pad=14, linespacing=1.6)
ax.set_xlabel("Outcome domain", fontsize=9, labelpad=10)
ax.set_ylabel("Intervention component", fontsize=9, labelpad=10)


if __name__ == "__main__":
    plt.savefig("figures/evidence_gap_map.png", dpi=200, bbox_inches="tight")
    fig.tight_layout()