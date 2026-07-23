import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Interventions and outcomes

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

# Short labels for plotting

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


# Load data

df = pd.read_csv("data/cleaned_evidence_table.csv")


# Compute study counts and % improved per cell

bubble_records = []

for intervention in interventions:
    component_studies = df[df[intervention] == "Yes"]

    for outcome in outcomes:
        reported_studies = component_studies[component_studies[outcome] != "Not reported"]
        total_reported = len(reported_studies)
        improved_count = (reported_studies[outcome] == "Improved").sum()

        percentage_improved = (
            (improved_count / total_reported) * 100 if total_reported > 0 else np.nan
        )

        bubble_records.append({
            "intervention": intervention,
            "outcome": outcome,
            "total_reported": total_reported,
            "improved_count": improved_count,
            "percentage_improved": percentage_improved,
        })

bubble_df = pd.DataFrame(bubble_records)

# Assign grid coordinates

outcome_positions = {outcome: i for i, outcome in enumerate(outcomes)}
intervention_positions = {intervention: i for i, intervention in enumerate(interventions)}

bubble_df["x"] = bubble_df["outcome"].map(outcome_positions)
bubble_df["y"] = bubble_df["intervention"].map(intervention_positions)


# Plot the bubble chart

fig, ax = plt.subplots(figsize=(15, 9), facecolor="white")
ax.set_facecolor("whitesmoke")

size_scale = 90


# Draw evidence map bubbles

scatter = ax.scatter(
    bubble_df["x"], bubble_df["y"],
    s=bubble_df["total_reported"] * size_scale,
    c=bubble_df["percentage_improved"],
    cmap="RdYlGn",
    vmin=0, vmax=100,
    edgecolor="darkslategray",
    linewidth=0.9,
    alpha=0.88,
    zorder=3,
)

# Study count labels inside bubbles (white on dark, black on light)

for index, row in bubble_df.iterrows():
    text_color = "white" if (row["percentage_improved"] < 25 or row["percentage_improved"] > 75) else "black"
    ax.text(
        row["x"], row["y"], str(int(row["total_reported"])),
        ha="center", va="center", fontsize=9.5, fontweight="bold",
        color=text_color, zorder=4,
    )


# Axes formatting

ax.set_xticks(range(len(outcomes)))
ax.set_xticklabels([short_outcomes[o] for o in outcomes], fontsize=10.5)

ax.set_yticks(range(len(interventions)))
ax.set_yticklabels([short_interventions[i] for i in interventions], fontsize=11)

ax.invert_yaxis()

ax.set_xlabel("Reported outcomes", fontsize=13, labelpad=15, fontweight="medium")
ax.set_ylabel(
    "Intervention components included within multimodal programmes",
    fontsize=13, labelpad=15, fontweight="medium",
)
ax.set_title(
    "Evidence map of intervention components and reported outcomes",
    fontsize=17, pad=20, fontweight="bold",
)

# Plot formatting

ax.set_xticks(np.arange(-0.5, len(outcomes), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(interventions), 1), minor=True)
ax.grid(which="minor", color="gainsboro", linewidth=0.9, alpha=0.6)
ax.tick_params(which="minor", bottom=False, left=False)
ax.tick_params(which="major", bottom=False, left=False)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_xlim(-0.5, len(outcomes) - 0.5)
ax.set_ylim(len(interventions) - 0.5, -0.5)


# Colour bar

colour_bar = fig.colorbar(scatter, ax=ax, pad=0.03, shrink=0.85)
colour_bar.set_label("Percentage of studies reporting improvement among studies reporting the outcome", 
                     fontsize=11, labelpad=12)
colour_bar.set_ticks([0, 20, 40, 60, 80, 100])
colour_bar.set_ticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
colour_bar.outline.set_visible(False)


# Bubble-size legend (scaled to the data's actual range)

max_count = int(bubble_df["total_reported"].max())
raw_steps = np.array([1, 5, 10, 15, 20, 25, 30])
size_values = [v for v in raw_steps if v <= max_count]
if not size_values or size_values[-1] != max_count:
    size_values.append(max_count)

size_handles = [
    ax.scatter([], [], s=v * size_scale, facecolor="gainsboro",
                edgecolor="darkslategray", alpha=0.9, label=str(v))
    for v in size_values
]

legend = ax.legend(
    handles=size_handles, title="Number of studies\nreporting outcome",
    bbox_to_anchor=(1.2, 0.78), loc="upper left",
    frameon=False, labelspacing=1.6, handletextpad=2.0, title_fontsize=10.5, fontsize=9.5,
)


plt.tight_layout()
plt.savefig("figures/evidence_map_bubble_chart.png", dpi=300, bbox_inches="tight")
