import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

df = pd.read_csv("data/cleaned_evidence_table.csv")


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



# COMMON PLOTTING FUNCTIONS 

# 1. Apply a consistent style to all graphs

def clean_ax(ax):
    # Remove unnecessary borders (splines)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)

    # Remove tick marks 
    ax.tick_params(length=0)

    # Set axis label color
    ax.xaxis.label.set_color("dimgrey")
    ax.yaxis.label.set_color("dimgrey")


# 2. Add value labels to end of each bar for simple bar charts
# (If the chart is horizontal, place labels to the right of each bar
# Otherwise, place labels above each vertical bar)

def add_bar_labels(ax, values, horizontal=True):
    for bar, val in zip(ax.patches, values):

        # Position of labels for horizontal bars
        if horizontal:
            x = bar.get_width() + 0.15
            y = bar.get_y() + bar.get_height() / 2
            ax.text(x, y, str(int(val)), va="center", ha="left",
                    fontsize=8, color="dimgrey")
        
        # Position labels for vertical bars
        else:
            x = bar.get_x() + bar.get_width() / 2
            y = bar.get_height() + 0.05
            ax.text(x, y, str(int(val)), va="bottom", ha="center",
                    fontsize=8, color="dimgrey")

# FUNCTIONS FOR PLOTS

# 1. INTERVENTION FREQUENCY PLOT

def plot_intervention_frequency(df, ax=None):

    # Count number of studies reporting each intervention
    counts = (df[interventions] == "Yes").sum()

    # Replace long intervention names with short labels
    counts.index = [short_interventions[i] for i in counts.index]

    # Sort interventions from least to most frequent
    counts = counts.sort_values(ascending=True)

    # Create new figure if no axis exists
    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(8, 5))

    # CREATE A HORIZONTAL BAR CHART

    bars = ax.barh(counts.index, counts.values,
                   color="steelblue", height=0.6)

    # Add numerical labels to each bar
    add_bar_labels(ax, counts.values, horizontal=True)

    # Set x-axis range
    ax.set_xlim(0, len(df) + 3)

    # Add axis labels and title
    ax.set_xlabel(f"Number of studies (total n = {len(df)})", fontsize=9)
    ax.set_title("Intervention frequency across studies", fontsize=11, pad=10)

    # Set label size
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=9)

    # Apply common formatting
    clean_ax(ax) 

    # Add left reference line at zero
    ax.axvline(0, color="lightgrey", linewidth=0.8)

    # Return the figure when created inside the function
    if own_fig:
        fig.tight_layout()
        return fig
    return None


# 2. OUTCOME EFFECTS PLOT

def plot_outcome_effects(df, ax=None):

    # Define outcome categories, associate colors  and shortened labels
    levels=["Improved", "No effect", "Not reported"]
    colors=["green", "darkgrey", "lightgrey"]
    labels=[short_outcomes[o] for o in outcomes]

    # Count how many studies fall into each category
    counts_dict= {}
    for outcome in outcomes:
        category_counts=df[outcome].value_counts()
        category_counts=category_counts.reindex(levels,fill_value=0)
        counts_dict[outcome]=category_counts

    # Convert the counts dictionary into a dataframe
    counts=pd.DataFrame(counts_dict).T

    # Create new figure if no axis exists
    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(9, 5))

    # CREATE A STACKED HORIZONTAL BAR CHART

    # Create an array of zeros for each outcome
    # Denotes starting position of each bar
    left = np.zeros(len(counts))

    # Plot one section for each outcome category
    for level, color in zip(levels, colors):
        # Get number of studies in current level
        vals = counts[level].values
        bars = ax.barh(labels, vals, left=left,
                       color=color, edgecolor="white", linewidth=0.8, height=0.6)
        # Add values inside each bar
        for bar, val in zip(bars, vals):
            if val >=1:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    str(int(val)),
                    ha="center", va="center",
                    fontsize=8,
                    color="white" if color == "green" else "dimgrey")
                
        # Move the starting position for the next stacked section
        left += vals

    # Set x-axis label and title
    ax.set_xlabel("Number of studies", fontsize=9)
    ax.set_title("Outcome effects across studies", fontsize=11, pad=10)

    # Set tick label sizes
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=9)

    # Apply common formatting
    clean_ax(ax)

    # Add vertical reference line at zero
    ax.axvline(0, color="lightgrey", linewidth=0.8)

    # Create and add legend
    legend_patches = [
        mpatches.Patch(facecolor="green", edgecolor="white", label="Improved"),
        mpatches.Patch(facecolor="darkgrey", edgecolor="white", label="No effect"),
        mpatches.Patch(facecolor="lightgrey", edgecolor="white", label="Not reported"),
    ]
    ax.legend(handles=legend_patches, fontsize=8, frameon=False, loc="upper right")

    # Return the figure when created inside the function
    if own_fig:
        fig.tight_layout()
        return fig
    return None

# 3. SAMPLE SIZE AND DROPOUTS

def plot_sample_size_dropouts(df, ax=None):
    plot_df = df[["Author", "Year", "n_enrolled", "n_dropouts"]].copy()
    plot_df["Study"] = plot_df["Author"] + " (" + plot_df["Year"].astype(int).astype(str) + ")"
    plot_df = plot_df.sort_values("n_enrolled", ascending=True)

    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(9, 8))

    ax.barh(
        plot_df["Study"],
        plot_df["n_enrolled"],
        color="steelblue",
        height=0.6,
        label="Total sample size"
    )

    ax.barh(
        plot_df["Study"],
        plot_df["n_dropouts"],
        color="darkgrey",
        height=0.6,
        label="Dropouts"
    )

    ax.set_xlabel("Number of participants", fontsize=9)
    ax.set_title("Sample size and dropouts by study", fontsize=11, pad=10)
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=9)
    clean_ax(ax)
    ax.axvline(0, color="lightgrey", linewidth=0.8)
    ax.legend(frameon=False, fontsize=8, loc="lower right")

    if own_fig:
        fig.tight_layout()
        return fig
    return None


# 4. DURATION OF INTERVENTION (HISTOGRAM)

def plot_duration_histogram(df, ax=None):

    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(7, 4))

    ax.hist(
        df["Duration_weeks"].dropna(),
        bins=8,
        color="steelblue",
        edgecolor="white",
        linewidth=0.8)

    ax.set_xlabel("Intervention duration (weeks)", fontsize=9)
    ax.set_ylabel("Number of studies", fontsize=9)
    ax.set_title("Distribution of intervention duration", fontsize=11, pad=10)

    ax.tick_params(axis="x", labelsize=9)
    ax.tick_params(axis="y", labelsize=9)

    clean_ax(ax)
  
    ax.axhline(0, color="lightgrey", linewidth=0.8)

    if own_fig:
        fig.tight_layout()
        return fig
    return None

if __name__ == "__main__":
    plot_intervention_frequency(df).savefig("figures/intervention_frequency.png", dpi=200, bbox_inches="tight")
    plot_outcome_effects(df).savefig("figures/outcome_effects.png", dpi=200, bbox_inches="tight")
    plot_sample_size_dropouts(df).savefig("figures/sample_size_dropouts.png", dpi=200, bbox_inches="tight")
    plot_duration_histogram(df).savefig("figures/duration_of_intervention.png", dpi=200, bbox_inches="tight")
    plt.show()
