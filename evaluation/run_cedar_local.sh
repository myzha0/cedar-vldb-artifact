#!/bin/bash

# Note, we provide the exact stats and config files produced by the optimizer on our setup in order to enable reproducibility.
# To generate new profiling stats and re-run the optimizer, use the --run_profiling and --generate_plan flags in eval_ember.py
# Replace the stats and optimizer-produced config in the following commands

# cv-torch
python eval_ember.py --dataset_file pipelines/simclrv2/ember_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_stats.yaml --master_feature_config pipelines/simclrv2/configs/eval_ember_local.yaml

# cv-tf
python eval_ember.py --dataset_file pipelines/simclrv2/ember_tf_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_tf_stats.yaml --master_feature_config pipelines/simclrv2/configs/eval_ember_local_tf.yaml

# nlp-torch
python eval_ember.py --dataset_file pipelines/wikitext103/ember_dataset.py --profiled_stats pipelines/wikitext103/stats/ember.yaml --master_feature_config pipelines/wikitext103/configs/eval_local.yaml  --num_total_samples 100000

# nlp-hf-tf
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_dataset.py --profiled_stats pipelines/wikitext103/stats/tf.yaml --master_feature_config pipelines/wikitext103/configs/eval_local_tf.yaml --num_total_samples 100000

# nlp-tf
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_service_dataset.py --profiled_stats pipelines/wikitext103/stats/tf_service.yaml --master_feature_config pipelines/wikitext103/configs/eval_local_tf_service.yaml --num_total_samples 200000

# asr
python eval_ember.py --dataset_file pipelines/commonvoice/ember_dataset.py --profiled_stats pipelines/commonvoice/stats/ember.yaml --master_feature_config pipelines/commonvoice/configs/eval_local.yaml --num_total_samples 10000
