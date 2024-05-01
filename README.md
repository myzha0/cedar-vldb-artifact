# cedar-vldb-artifact

cedar (referred to as ember in this artifact) is an optimized and unified programming framework for ML input data pipelines.
This repository holds the artifact for cedar for its submission to PVLDB vol. 18.

## Setup
To setup cedar and its dependencies, begin by making sure that you have Python>=3.9 installed, as well as `pip` and `venv`.

We suggest first creating an virtual environment.
Then, simply `pip install` the `requirements.txt` file.

```bash
cd <PATH_TO_REPO>
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Finally, install cedar as a package using pip.
```bash
pip install -e .
```

In the setup instructions below, we refer to the node that you run the main data loading process on as the `local` node, and any distributed workers as `remote` nodes. The instructions assume that you execute commands on the `local` node unless otherwise specified.

### Downloading Datasets
We provide scripts to download datasets for each set of evaluation pipelines.
Simply execute the following scripts.

- `CV`: `python <PATH_TO_REPO>/evaluation/pipelines/simclrv2/download.py`
- `NLP`: `python <PATH_TO_REPO>/evaluation/pipelines/wikitext103/download.py`
- `ASR`: Mozilla requires you to manually register and download the CommonVoice dataset via their website (https://commonvoice.mozilla.org/en/datasets). Specifically, we used the `cv-corpus-15.0-delta-2023-09-08` set. Once you have downloaded the dataset, save all of the raw MP3s locally at `<PATH_TO_REPO>/evaluation/datasets/commonvoice/cv-corpus-15.0-delta-2023-09-08/en/clips`. 

### Distributed Processing
cedar uses Ray Core to distribute preprocessing. To use Ray, you first need
to set up the appropriate permissions and settings on GCP (or whichever cloud provider you use), as detailed
[here](https://docs.ray.io/en/latest/cluster/vms/getting-started.html#vm-cluster-quick-start).

Once Ray is setup, you will have to first create a machine image that Ray can automatically create a cluster with.
Since Ray requires that the same environment is used between nodes in the Ray cluster, the easiest way to do so is to simply clone the VM that you already installed dependencies and downloaded datasets on.

Once you have an image with all dependencies installed, update the respective field in `configs/ray.yaml` (specifically, the `node_config`) to point to your appropriate image.

Additionally, you will need to update the `setup_commands` to point to your respective home directory.

Once the config is setup, you can simply create the Ray Cluster by running the following.

```bash
ray up -y configs/ray.yaml
```

Once you are done with Ray, **REMEMBER TO DESTROY THE CLUSTER**

```bash
ray down -y configs/ray.yaml
```

### Setting up Baselines
cedar compares against multiple baselines, including PyTorch DataLoaders, tf.data, tf.data service, Ray DataSets, FastFlow, and Plumber.
The above pip installation installs PyTorch DataLoaders, and tf.data.
We provide setup instructions for the other following baselines below.

#### tf.data service
tf.data is already installed using the above commands.
To use tf.data service, you must create another VM with all dependencies and datasets already installed (as mentioned above for setting up Ray).

Prior to running tf.data service benchmarks, you must manually start up the other VM (we used an `n2-standard-32`), source your `venv`, and then run `python <PATH_TO_REPO>/evaluation/run_tf_service.py --ip_addr <IP_ADDR>` to launch the tf.data service worker process.
The process must be continuously running when you run tf.data service benchmarks on your local node (we used an `n2-standard-8`).

#### Ray Data
To use Ray Data, first create a Ray Cluster using the `ray up` command as mentioned above.
This will create a remote VM that Ray Data will use for processing.
However, to ensure that Ray can run tasks on both the remote and local VM, connect your local VM by executing the following on your local VM.

`ray start --address='10.138.0.79:6379’`

Note that the address should be the one that is provided to you after you run the `ray up` command.

Remember to run `ray stop` and `ray down -y configs/ray.yaml` when you are done.

#### FastFlow
Follow the instructions at https://github.com/SamsungLabs/FastFlow to install FastFlow.
It is recommended that you do this in a separate venv, as FastFlow must build a custom version of TensorFlow from scratch.

After installation, follow the instructions for tf.data service to clone a new VM and launch the remote worker for processing (with the same `run_tf_service.py` script).
Note that you must use the environment that has FastFlow installed when running the worker process on the remote node.

#### Plumber
Follow the instructions at https://github.com/mkuchnik/PlumberApp to install Plumber.
As with FastFlow, this requires a custom TensorFlow installation, so be sure to do this in a separate environment.

You must also install the following package in the Plumber environment.
`pip install tensorflow-addons==0.16.1`

## Running Experiments

#### Baseline Comparison
Once all dependencies and datasets are installed/downloaded, you are ready to run experiments.
Note that `cedar-remote`, Ray Data, tf.data service, and FastFlow require a running remote VM (n2-standard-32), as specified in the setup instructions above.
It is recommended to run experiments for one framework at a time, since each requires different setup steps and potentially different environments.

We provide all scripts to run experiments and generate plots in `<PATH_TO_REPO>/evaluation`.
Note that these commands should be run on the local VM (n2-standard-8).

- cedar_local: `run_cedar_local.sh`
- torch: `run_torch.sh`
- ray_local: `run_ray_local.sh`
- tf: `run_tf.sh`
- plumber: `plumber/simclr/run_plumber.sh`

- cedar_remote: `run_cedar_remote.sh` (note, requires Ray cluster running. You must first manually update the IP address for the ray head node in the script).
- ray remote: `run_ray_remote.sh` (note, requires Ray Data setup as detailed above)
- tf.data service: `run_tf_service.sh` (note, requires tf.data service worker setup. You must also manually update the worker IP address in the script)
- fastflow: `fastflow/examples/run_fastflow.sh` (note, requires FastFlow worker setup. You must also manually update the worker IP in the `config.yaml` file in the fastflow directory)

Each script will run all pipelines back to back. After running each pipeline, the evaluation script will report the execution time.
To generate the plots, first update the results file with the reported runtimes (`local_data.csv` for local experiments, `remote_data.csv` for remote experiments). Then, run the following scripts.
- `python plot_local.py`: Figure 9
- `python plot_remote.py`: Figure 10

#### Auto-tuning
To generate auto-tuning results, run `run_autotuning.sh` (with the Ray cluster set up).
Each command will run the auto-tuner and report results for a different row in Table 4.

#### Ablation
To run ablation experiments, run `run_ablation.sh` (with the Ray cluster set up).
As with the baseline experiments, each command will run a separate job and report execution times.
To generate the ablation plot, update the corresponding reported execution times (plots/ablation.csv) and run `python plots/plot_ablation.py`.

#### Caching
To run caching experiments, run `run_cache.sh` (with the Ray cluster set up).
As with the baseline experiments, each command will run a separate job, one with caching and one without caching, for the three pipelines in Table 5.
Table 5 reports the cache throughput normalized to the throughput without caching.


## Troubleshooting
* Connecting to the head node: Make sure that your firewall rules allows incoming connections to
the head node (likely at port 10001).

* Permission issues performing `ray up`: Make sure your VM has necessary API permissions.


