#!/bin/bash
# Запустить Flask-приложение и ngrok туннель.
# В одном терминале выполните:
#   python3 app.py
# В другом терминале выполните:
#   ./ngrok http 5000
# После этого ngrok выведет публичный URL, который можно отправить тестерам.

if [ "$1" = "help" ] || [ "$1" = "-h" ]; then
  echo "Usage: ./run_tunnel.sh"
  echo "Run Flask locally in one terminal and ngrok in another."
  exit 0
fi

echo "This script only documents the tunnel workflow."
echo "1. In terminal A: python3 app.py"
echo "2. In terminal B: ./ngrok http 5000"
echo "Then copy the https://... URL from ngrok output."
