#!/bin/bash

#cv-torch
# baseline
python eval_ember.py --dataset_file pipelines/simclrv2/ember_remote_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_remote.yaml --master_feature_config pipelines/simclrv2/configs/ablation_baseline.yaml --use_ray --ray_ip 10.138.0.8
#p
python eval_ember.py --dataset_file pipelines/simclrv2/ember_remote_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_remote.yaml --master_feature_config pipelines/simclrv2/configs/ablation_p.yaml --use_ray --ray_ip 10.138.0.8
#pr
python eval_ember.py --dataset_file pipelines/simclrv2/ember_remote_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_remote.yaml --master_feature_config pipelines/simclrv2/configs/ablation_p_r.yaml --use_ray --ray_ip 10.138.0.8
#pro
python eval_ember.py --dataset_file pipelines/simclrv2/ember_remote_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_remote.yaml --master_feature_config pipelines/simclrv2/configs/ablation_p_r_o.yaml --use_ray --ray_ip 10.138.0.8
#prof
python eval_ember.py --dataset_file pipelines/simclrv2/ember_remote_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_remote.yaml --master_feature_config pipelines/simclrv2/configs/eval_ember_remote.yaml --use_ray --ray_ip 10.138.0.8

# cv-tf
#baseline
python eval_ember.py --dataset_file pipelines/simclrv2/ember_tf_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_tf_stats.yaml --master_feature_config pipelines/simclrv2/configs/ablation_tf_baseline.yaml --use_ray --ray_ip 10.138.0.8
#p
python eval_ember.py --dataset_file pipelines/simclrv2/ember_tf_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_tf_stats.yaml --master_feature_config pipelines/simclrv2/configs/ablation_tf_p.yaml --use_ray --ray_ip 10.138.0.8
#pr
python eval_ember.py --dataset_file pipelines/simclrv2/ember_tf_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_tf_stats.yaml --master_feature_config pipelines/simclrv2/configs/ablation_tf_p_r.yaml --use_ray --ray_ip 10.138.0.8
#pro
python eval_ember.py --dataset_file pipelines/simclrv2/ember_tf_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_tf_stats.yaml --master_feature_config pipelines/simclrv2/configs/ablation_tf_p_r_o.yaml --use_ray --ray_ip 10.138.0.8
#prof
python eval_ember.py --dataset_file pipelines/simclrv2/ember_tf_dataset.py --profiled_stats pipelines/simclrv2/stats/ember_tf_stats.yaml --master_feature_config pipelines/simclrv2/configs/eval_ember_remote_tf.yaml --use_ray --ray_ip 10.138.0.8

# nlp-torch
python eval_ember.py --dataset_file pipelines/wikitext103/ember_dataset.py --profiled_stats pipelines/wikitext103/stats/ember.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000 --master_feature_config pipelines/wikitext103/configs/ablation_baseline.yaml
python eval_ember.py --dataset_file pipelines/wikitext103/ember_dataset.py --profiled_stats pipelines/wikitext103/stats/ember.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000 --master_feature_config pipelines/wikitext103/configs/ablation_p.yaml
python eval_ember.py --dataset_file pipelines/wikitext103/ember_dataset.py --profiled_stats pipelines/wikitext103/stats/ember.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000 --master_feature_config pipelines/wikitext103/configs/ablation_p_r.yaml
python eval_ember.py --dataset_file pipelines/wikitext103/ember_dataset.py --profiled_stats pipelines/wikitext103/stats/ember.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000 --master_feature_config pipelines/wikitext103/configs/ablation_p_r_o.yaml
python eval_ember.py --dataset_file pipelines/wikitext103/ember_dataset.py --profiled_stats pipelines/wikitext103/stats/ember.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000 --master_feature_config pipelines/wikitext103/configs/eval_remote.yaml

# nlp-hf-tf
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_dataset.py --profiled_stats pipelines/wikitext103/stats/tf.yaml --master_feature_config pipelines/wikitext103/configs/ablation_tf_baseline.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_dataset.py --profiled_stats pipelines/wikitext103/stats/tf.yaml --master_feature_config pipelines/wikitext103/configs/ablation_tf_p.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_dataset.py --profiled_stats pipelines/wikitext103/stats/tf.yaml --master_feature_config pipelines/wikitext103/configs/ablation_tf_p_r.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_dataset.py --profiled_stats pipelines/wikitext103/stats/tf.yaml --master_feature_config pipelines/wikitext103/configs/ablation_tf_p_r_o.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_dataset.py --profiled_stats pipelines/wikitext103/stats/tf.yaml --master_feature_config pipelines/wikitext103/configs/eval_remote_tf.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 100000
# nlp-tf
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_service_dataset.py --profiled_stats pipelines/wikitext103/stats/tf_service.yaml --master_feature_config pipelines/wikitext103/configs/ablation_baseline.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 200000
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_service_dataset.py --profiled_stats pipelines/wikitext103/stats/tf_service.yaml --master_feature_config pipelines/wikitext103/configs/ablation_p.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 200000
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_service_dataset.py --profiled_stats pipelines/wikitext103/stats/tf_service.yaml --master_feature_config pipelines/wikitext103/configs/ablation_p_r.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 200000
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_service_dataset.py --profiled_stats pipelines/wikitext103/stats/tf_service.yaml --master_feature_config pipelines/wikitext103/configs/ablation_p_r_o.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 200000
python eval_ember.py --dataset_file pipelines/wikitext103/ember_tf_service_dataset.py --profiled_stats pipelines/wikitext103/stats/tf_service.yaml --master_feature_config pipelines/wikitext103/configs/eval_remote_tf_service.yaml --use_ray --ray_ip 10.138.0.8 --num_total_samples 200000
# asr
python eval_ember.py --dataset_file pipelines/commonvoice/ember_dataset.py --profiled_stats pipelines/commonvoice/stats/ember.yaml --master_feature_config pipelines/commonvoice/configs/ablation_baseline.yaml --num_total_samples 10000
python eval_ember.py --dataset_file pipelines/commonvoice/ember_dataset.py --profiled_stats pipelines/commonvoice/stats/ember.yaml --master_feature_config pipelines/commonvoice/configs/ablation_p.yaml --num_total_samples 10000
python eval_ember.py --dataset_file pipelines/commonvoice/ember_dataset.py --profiled_stats pipelines/commonvoice/stats/ember.yaml --master_feature_config pipelines/commonvoice/configs/ablation_p_r.yaml --num_total_samples 10000
python eval_ember.py --dataset_file pipelines/commonvoice/ember_dataset.py --profiled_stats pipelines/commonvoice/stats/ember.yaml --master_feature_config pipelines/commonvoice/configs/ablation_p_r_o.yaml --num_total_samples 10000
python eval_ember.py --dataset_file pipelines/commonvoice/ember_dataset.py --profiled_stats pipelines/commonvoice/stats/ember.yaml --master_feature_config pipelines/commonvoice/configs/eval_remote.yaml --num_total_samples 10000