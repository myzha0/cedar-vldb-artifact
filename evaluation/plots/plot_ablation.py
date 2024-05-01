import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = "~/ember/evaluation/plots/ablation.csv"
data = pd.read_csv(file_path)

rename_dict = {
    "Baseline": "Baseline",
    "plus parallelism": "+P",
    "plus reorder": "+PR",
    "plus offload": "+PRO",
    "plus fusion": "+PROF",
}
data["Setup"] = data["Setup"].map(rename_dict)


# Normalize the 'Average' for 'ember-remote' in each 'Pipeline' group
normalization_factors = data[data["Setup"] == "Baseline"].set_index(
    "Pipeline"
)["Runtime"]
data["Normalized Runtime"] = data.apply(
    lambda row: row["Runtime"] / normalization_factors.get(row["Pipeline"], 1),
    axis=1,
)
print(data)

# Create the plot with normalized values
f = plt.figure(figsize=(3.33, 1.8), dpi=600)
sns.set_style("whitegrid")
ax = sns.barplot(
    x="Pipeline",
    y="Normalized Runtime",
    hue="Setup",
    data=data,
    palette="viridis",
    linewidth=0,
    hue_order=["Baseline", "+P", "+PR", "+PRO", "+PROF"],
)

# Adding vertical lines and red "X" for missing values
pipeline_labels = data["Pipeline"].unique()  # Get unique pipeline labels

# Set x-ticks
# Adding vertical lines to mark ranges of each x category
for i in range(len(pipeline_labels) - 1):
    ax.axvline(
        x=i + 0.5, color="grey", linestyle="-", linewidth=0.5
    )  # End of group

plt.xticks(rotation=30, ha="right", fontsize=6)
plt.yticks((0, 0.5, 1), fontsize=6)
ax.set_ylim((0, 1.3))
ax.tick_params(axis="both", which="major", pad=0)
ax.set_ylabel("Normalized Execution Time", fontsize=6)
ax.set_xlabel("")
ax.tick_params(axis="x", direction="out", length=6, color="black")

ax.legend(fontsize=5, title_fontsize="6", ncol=5)

# Display the plot
plt.tight_layout()
# ax.legend(fontsize=6, title_fontsize='6')
f.savefig("ablation.png")
