#!/usr/bin/env bash

python3 run.py ingest
python3 run.py run_model
python3 run.py ingest_result