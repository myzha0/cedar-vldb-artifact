import pathlib
from unittest.mock import patch, MagicMock
from ember.utils.profiler import Profiler, ProfilerSpec, Timer
from ember_benchmarks.run_profile import run_profiler

from torchdata.datapipes.iter import IterableWrapper


def test_profiler_basic(mocker):
    mock_timer = MagicMock(spec=Timer)

    # always return 1 from timer
    mock_timer.delta.return_value = 1

    with patch("ember.utils.profiler.Timer", return_value=mock_timer):
        # batch 2, no sample limit, 2 epochs
        spec = ProfilerSpec(2, None, 2, None)

        data = IterableWrapper([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).batch(2)

        profiler = Profiler(data, spec, limit_torch_parallelism=False)
        profiler.init()
        profiler.run()
        profiler.print_results()

        results = profiler.get_results()

    assert results["epoch_run_times"] == [1, 1]
    assert results["load_time"] == 1
    assert results["epoch_num_samples"] == [10, 10]


def test_profiler_limits(mocker):
    mock_timer = MagicMock(spec=Timer)

    # always return 1 from timer
    mock_timer.delta.return_value = 1

    with patch("ember.utils.profiler.Timer", return_value=mock_timer):
        # batch 3, 15 samples total, 5 epochs, 6 samples per epoch
        spec = ProfilerSpec(3, 15, 5, 6)

        data = IterableWrapper([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).batch(2)

        profiler = Profiler(data, spec, limit_torch_parallelism=False)
        profiler.init()
        profiler.run()
        profiler.print_results()

        results = profiler.get_results()

    assert results["epoch_run_times"] == [1, 1, 1]
    assert results["load_time"] == 1
    assert results["epoch_num_samples"] == [6, 6, 3]


def test_profiler_cli():
    spec = ProfilerSpec(32, 64, 1, None)
    test_dir = pathlib.Path(__file__).resolve().parents[0]
    dataset_file = pathlib.Path(test_dir) / "data/dataset.py"
    save_results_file = pathlib.Path(test_dir) / pathlib.Path(
        "data/results.json"
    )

    # Clear results.json
    with open(str(save_results_file), "w"):
        pass

    run_profiler(
        dataset_file, "get_dataset", spec, save_loc=str(save_results_file)
    )
