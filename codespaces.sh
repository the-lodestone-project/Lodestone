#!/bin/bash

pip install -r requirements.txt
clear
cat config.json
echo ""
echo ""
echo "Please make sure you have configued the config.json file. Otherwise the bot will fail to run."
echo ""
read -p "Press enter to continue "
clear
python3 main.py