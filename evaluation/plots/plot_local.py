import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = "~/ember/evaluation/plots/local_data.csv"
data = pd.read_csv(file_path)


# Normalize the 'Average' for 'ember-remote' in each 'Pipeline' group
normalization_factors = data[data["System"] == "ember-local"].set_index(
    "Pipeline"
)["Average"]
data["Normalized Average"] = data.apply(
    lambda row: row["Average"] / normalization_factors.get(row["Pipeline"], 1),
    axis=1,
)
data.drop(columns="Command")
print(data)

# Rename
data["System"] = data["System"].replace("ember-local", "cedar-local")

# Create the plot with normalized values
f = plt.figure(figsize=(3.33, 1.8), dpi=600)
sns.set_style("whitegrid")
systems = ["tf", "plumber", "ray-local", "torch", "cedar-local"]
ax = sns.barplot(
    x="Pipeline",
    y="Normalized Average",
    hue="System",
    data=data,
    palette="viridis",
    linewidth=0,
    hue_order=systems,
)

bar_width = 0.175
# Adding vertical lines and red "X" for missing values
pipeline_labels = data["Pipeline"].unique()  # Get unique pipeline labels
for i, pipeline in enumerate(pipeline_labels):
    for j, system in enumerate(systems):
        if not (
            (data["Pipeline"] == pipeline) & (data["System"] == system)
        ).any():
            # Draw red "X" where the bar is missing
            # ax.text(i + j*0.2 - 0.45, 0.02, "X", color='red', fontsize=6, ha='center')
            # Calculate the center of the position where the bar would have been
            x_position = i + j * bar_width - (0.44 - bar_width / 2)
            # Draw red "X" where the bar is missing
            ax.text(
                x_position, 0.02, "X", color="red", fontsize=6, ha="center"
            )


# Set x-ticks
# Adding vertical lines to mark ranges of each x category
for i in range(len(pipeline_labels) - 1):
    ax.axvline(
        x=i + 0.5, color="grey", linestyle="-", linewidth=0.5
    )  # End of group

plt.xticks(rotation=30, ha="right", fontsize=6)
plt.yticks((0, 1, 2, 3, 4, 5, 6), fontsize=6)
ax.tick_params(axis="both", which="major", pad=0)
ax.set_ylabel("Normalized Execution Time", fontsize=6)
ax.set_xlabel("")
ax.tick_params(axis="x", direction="out", length=6, color="black")
ax.legend(fontsize=6, title_fontsize="6", ncols=2)

# Display the plot
plt.tight_layout()
# ax.legend(fontsize=6, title_fontsize='6')
f.savefig("local.png")
