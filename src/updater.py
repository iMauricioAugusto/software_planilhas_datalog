import os
import shutil
import sys
import zipfile

import requests

# URLS do servidor
VERSION_URL = "https://raw.githubusercontent.com/iMauricioAugusto/software_planilhas_datalog/refs/heads/main/src/version.txt"  # Link para o arquivo version.txt no servidor
DOWNLOAD_URL = "https://github.com/iMauricioAugusto/software_planilhas_datalog/blob/main/software_planilha_datalog.zip"  # Link para o arquivo zip do seu aplicativo


# Função para obter a versão atual do aplicativo
def get_current_version():
    try:
        # Ajuste o caminho do version.txt, se necessário
        current_dir = os.path.dirname(os.path.abspath(__file__))
        version_path = os.path.join(current_dir, "version.txt")
        with open(version_path, "r") as file:
            return file.read().strip()
        print(file.read().strip())
    except FileNotFoundError:
        print("Arquivo version.txt não encontrado.")
        return "0.0.0"

# Função para obter a versão mais recente do servidor
def get_latest_version():
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        print("Erro ao verificar a versão mais recente.")
        return None

# # Função para baixar a nova versão
def download_update():
    try:
        response = requests.get(DOWNLOAD_URL, stream=True)
        response.raise_for_status()
        with open("update.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return True
    except requests.RequestException:
        print("Erro ao baixar a atualização.")
        return False


# Função para aplicar a atualização
def apply_update():
    try:
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove("update.zip")
    except zipfile.BadZipFile:
        print("Erro ao extrair o arquivo zip.")


# Função principal para verificar e aplicar atualizações
def check_for_updates():
    current_version = get_current_version()
    latest_version = get_latest_version()

    if not latest_version:
        print("Não foi possível obter a versão mais recente.")
        return

    print(f"Versão atual: {current_version}")
    print(f"Versão mais recente: {latest_version}")

    if current_version != latest_version:
        print(f"Versão atual: {current_version}")
        print(f"Versão mais recente: {latest_version}")
        print("Nova versão disponível! Atualizando...")
        if download_update():
            apply_update()
            print("Atualização concluída com sucesso!")
            # Reiniciar o aplicativo após a atualização
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            print("Falha na atualização.")
    else:
        print("Você já está usando a versão mais recente.")


if __name__ == "__main__":
    check_for_updates()
