#!/bin/bash

# Caminho para o Python e o script
PYTHON_PATH="/opt/homebrew/bin/python3"
SCRIPT_PATH="/Users/ruicampos/.gemini/antigravity/scratch/acido_ace/auto_commit.py"
LOG_PATH="/Users/ruicampos/.gemini/antigravity/scratch/acido_ace/cron.log"

# A expressão cron para cada 6 horas
CRON_JOB="0 */6 * * * $PYTHON_PATH $SCRIPT_PATH >> $LOG_PATH 2>&1"

# Verificar se já existe no crontab
(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH") || (
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job configurado com sucesso: cada 6 horas."
)
