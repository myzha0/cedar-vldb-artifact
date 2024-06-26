from ember.compose.constants import RAY_SUBMIT_BATCH_SIZE

RAY_PROFILE_N_ACTORS = 8
RAY_PROFILE_INFLIGHT = 100
RAY_PROFILE_PREFETCH = 100
RAY_PROFILE_SUBMIT_BATCH_SIZE = 10
CONTROLLER_PERIOD_SEC = 3
MAX_HISTORY = CONTROLLER_PERIOD_SEC * 10
THROUGHPUT_LOG_TIME_SEC = 1
SCALE_ATTEMPTS = 3
THROUGHPUT_THRESHOLD = 1.01
EMPTY_BUFFER_THRESHOLD = RAY_SUBMIT_BATCH_SIZE * 1.5
AVAILABLE_RAY_SCALE = 32
SMP_PROFILE_N_PROCS = 8
SMP_TASKSET_MASK = 0xFF  # should match the taskset cpu mask of smp n_procs
SMP_PROFILE_INFLIGHT = 100
SMP_PROFILE_PREFETCH = 100
