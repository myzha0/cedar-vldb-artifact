import os
import json
import matplotlib.pyplot as plt

def read_json_file(file_path):
    """Reads a JSON file and returns the data."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_epoch_run_times(file_data):
    """Extracts the last value of epoch_run_times from the JSON data."""
    return file_data['epoch_run_times'][-1]

def process_directory(directory):
    """Processes a single directory to extract caching and no-caching data."""
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    caching_file, no_caching_file = None, None

    for file in files:
        if "no_caching" in file:
            no_caching_file = file
        else:
            caching_file = file

    if not caching_file or not no_caching_file:
        raise ValueError("Required files not found in directory: " + directory)

    caching_data = read_json_file(os.path.join(directory, caching_file))
    no_caching_data = read_json_file(os.path.join(directory, no_caching_file))

    caching_time = get_epoch_run_times(caching_data)
    no_caching_time = get_epoch_run_times(no_caching_data)

    return caching_time, no_caching_time

def compare_results(directories):
    """Compares results across multiple directories and prepares data for plotting."""
    results = []
    for directory in directories:
        caching_time, no_caching_time = process_directory(directory)
        scaled_caching_time = (caching_time / no_caching_time) * 100
        results.append((scaled_caching_time, 100))  # 100 represents the no-caching scaled to itself

    return results

def plot_results(directories, results, names):
    """Plots the comparison results."""
    fig, ax = plt.subplots()
    width = 0.35
    ind = range(len(directories))

    caching_times = [result[0] for result in results]
    no_caching_times = [result[1] for result in results]

    p1 = ax.bar(ind, no_caching_times, width, color="#1f77b4")
    p2 = ax.bar([i + width for i in ind], caching_times, width, color="#ff7f0e")

    ax.set_title('Caching vs No-Caching Performance Comparison')
    ax.set_xticks([i + width / 2 for i in ind])
    ax.set_xticklabels(names)
    ax.legend((p1[0], p2[0]), ('No-Caching', 'Caching'))
    ax.set_ylabel('Performance (% of No-Caching)')

    plt.savefig("caching.png")


def main():
    home_directory = os.path.expanduser("~")
    directory_appendices = ['/ember/evaluation/pipelines/wikitext103/cache_results', '/ember/evaluation/pipelines/simclrv2/cache_results', '/ember/evaluation/pipelines/commonvoice/cache_results']
    directories = []
    for directory_appendix in directory_appendices:
        directories.append(home_directory + directory_appendix)
    results = compare_results(directories)
    names = ["wikitext", "simclr", "commonvoice"]
    print(f"Got following comparison results {results}")
    plot_results(directories, results, names)


if __name__ == '__main__':
    main()
