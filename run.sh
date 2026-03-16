#!/bin/bash
# Script para iniciar o simulador de Síntese de Ácido Acetilsalicílico

# Verificar se o Streamlit está instalado
if ! command -v streamlit &> /dev/null
then
    echo "Streamlit não encontrado. A instalar dependências..."
    pip install -r requirements.txt
fi

echo "A iniciar o simulador..."
streamlit run app.py
