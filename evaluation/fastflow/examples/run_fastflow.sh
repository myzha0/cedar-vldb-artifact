#!/bin/bash

#cv-tf
python eval_app_runner.py simclr_app.py simclr ff config.yaml
#nlp-tf
python eval_app_runner.py nlp_app.py nlp ff config.yaml