#!/bin/bash

# compute stats and uploads them
python scores.py

rsync -avz --delete -e 'ssh -p 1892' target/site/* skayafr@skaya.fr:public_html/scores
