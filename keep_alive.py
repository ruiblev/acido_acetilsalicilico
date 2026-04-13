"""
keep_alive.py
─────────────────────────────────────────────────────────────────────────────
Script executado pelo GitHub Actions para manter a app Streamlit sempre ativa.

Estratégia:
  - Regista um timestamp no ficheiro keep_alive_log.txt
  - O GitHub Actions faz commit desse ficheiro periodicamente
  - O Streamlit Cloud deteta atividade no repositório e mantém a app ativa
─────────────────────────────────────────────────────────────────────────────
"""

from datetime import datetime, timezone
import os

LOG_FILE = "keep_alive_log.txt"
MAX_ENTRIES = 100  # Mantém apenas as últimas 100 entradas no log

def main():
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"[{timestamp}] ✅ App ativa - ping automático\n"

    # Ler entradas existentes
    existing_lines = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()

    # Manter apenas as últimas MAX_ENTRIES entradas (+ header)
    header_lines = [l for l in existing_lines if l.startswith("#")]
    log_lines = [l for l in existing_lines if not l.startswith("#")]
    log_lines = log_lines[-(MAX_ENTRIES - 1):]  # Guarda espaço para a nova entrada

    # Escrever ficheiro atualizado
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        if not header_lines:
            f.write("# Keep-Alive Log — Simulador Ácido Acetilsalicílico\n")
            f.write("# Este ficheiro é atualizado automaticamente pelo GitHub Actions\n")
            f.write("# para manter a app Streamlit sempre ativa.\n\n")
        else:
            f.writelines(header_lines)
            f.write("\n")
        f.writelines(log_lines)
        f.write(entry)

    print(f"Ping registado: {timestamp}")

if __name__ == "__main__":
    main()
