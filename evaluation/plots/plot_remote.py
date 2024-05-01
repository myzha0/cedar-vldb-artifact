import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = "~/ember/evaluation/plots/remote_data.csv"
data = pd.read_csv(file_path)

rename_dict = {
    "ember-remote": "ember-remote",
    "ray-remote": "ray-remote",
    "tfdata-service": "tf-service",
    "fastflow": "fastflow",
}
data["System"] = data["System"].map(rename_dict)

# Normalize the 'Average' for 'ember-remote' in each 'Pipeline' group
normalization_factors = data[data["System"] == "ember-remote"].set_index(
    "Pipeline"
)["Average"]
data["Normalized Average"] = data.apply(
    lambda row: row["Average"] / normalization_factors.get(row["Pipeline"], 1),
    axis=1,
)
data.drop(columns="Command")
print(data)

# Rename
data["System"] = data["System"].replace("ember-remote", "cedar-remote")

# Create the plot with normalized values
f = plt.figure(figsize=(3.33, 1.8), dpi=600)
sns.set_style("whitegrid")
systems = ["tf-service", "fastflow", "ray-remote", "cedar-remote"]
ax = sns.barplot(
    x="Pipeline",
    y="Normalized Average",
    hue="System",
    data=data,
    palette="viridis",
    linewidth=0,
    hue_order=systems,
)

# Set x-ticks
pipeline_labels = data["Pipeline"].unique()  # Get unique pipeline labels

# Calculate bar width (default for seaborn barplot is 0.8)
bar_width = 0.8
n_systems = len(systems)
width_per_system = bar_width / n_systems
n_bars_in_group = len(systems)
total_group_width = bar_width  # Total width used by all bars in a group

# Calculate the center position of each bar within its group
bar_positions = [
    i - total_group_width / 2 + width_per_system * (0.5 + j)
    for i in range(len(pipeline_labels))
    for j in range(n_bars_in_group)
]

for i, pipeline in enumerate(pipeline_labels):
    for j, system in enumerate(systems):
        if not (
            (data["Pipeline"] == pipeline) & (data["System"] == system)
        ).any():
            # Draw red "X" where the bar is missing
            position_index = i * n_bars_in_group + j
            bar_position = i + width_per_system * (j - n_systems / 2)
            ax.text(
                bar_positions[position_index],
                0.02,
                "X",
                color="red",
                fontsize=6,
                ha="center",
            )


# Adding vertical lines to mark ranges of each x category
for i in range(len(pipeline_labels) - 1):
    ax.axvline(
        x=i + 0.5, color="grey", linestyle="-", linewidth=0.5
    )  # End of group


plt.xticks(rotation=30, ha="right", fontsize=6)
plt.yticks(fontsize=6)
ax.set_ylabel("Normalized Execution Time", fontsize=6)
ax.set_xlabel("")
ax.legend(fontsize=5, title_fontsize="6", ncols=4)
ax.set_ylim([0, 4.3])
ax.set_yticks([0, 1, 2, 3, 4])
# ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=6)


# Display the plot
plt.tight_layout()
# ax.legend(fontsize=6, title_fontsize='6')
f.savefig("remote.png")
