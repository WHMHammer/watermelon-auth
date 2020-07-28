#!/bin/sh
python3 -m venv test_back_end_venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 test/auth.py
rm -rf test_back_end_venv
