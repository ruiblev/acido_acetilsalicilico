import subprocess
import os
from datetime import datetime

# Configurações
REPO_PATH = "/Users/ruicampos/.gemini/antigravity/scratch/acido_ace"
LOG_FILE = os.path.join(REPO_PATH, "auto_commit.log")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE, "a") as f:
        f.write(full_message + "\n")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log(f"Erro ao executar comando: {command}")
        log(f"Erro output: {e.stderr}")
        return None

def auto_commit():
    if not os.path.exists(REPO_PATH):
        print(f"Erro: O repositório em {REPO_PATH} não existe.")
        return

    os.chdir(REPO_PATH)
    
    # Verificar se há alterações
    status = run_command("git status --porcelain")
    if not status:
        log("Sem alterações para commit.")
        return

    log("Alterações detetadas. A preparar commit e push...")
    
    # Adicionar alterações
    run_command("git add .")
    
    # Mensagem de commit
    commit_msg = f"Auto-commit diário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Commit
    res_commit = run_command(f'git commit -m "{commit_msg}"')
    if res_commit:
        log(f"Commit realizado: {commit_msg}")
        
        # Push
        res_push = run_command("git push origin main")
        if res_push is not None:
            log("Push realizado com sucesso para o GitHub.")
        else:
            log("Erro ao realizar o Push.")
    else:
        log("Falha ao realizar o Commit.")

if __name__ == "__main__":
    auto_commit()
