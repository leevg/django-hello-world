#!/bin/bash

filename=`date +%d_%m_%Y`.dat
python manage.py print_models 2> ${filename}