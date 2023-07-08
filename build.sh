#!/bin/sh
pip install -r requirements.txt
nltk.download('punkt')
python backend/train.py