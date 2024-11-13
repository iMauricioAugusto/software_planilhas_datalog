import os
import shutil
import sys
import tkinter as tk
import zipfile
from tkinter import messagebox

import requests

# URLS do servidor
VERSION_URL = "https://github.com/iMauricioAugusto/software_planilhas_datalog/raw/refs/heads/main/src/version.json"
# Função para obter a versão atual do aplicativo

def get_current_version():
    try:
        with open("version.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
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

def download_update(download_url):
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        with open("update.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return True
    except requests.RequestException:
        print("Erro ao baixar a atualização.")
        return False

def apply_update():
    try:
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove("update.zip")
    except zipfile.BadZipFile:
        print("Erro ao extrair o arquivo zip.")

def check_for_updates():
    current_version = get_current_version()
    latest_version = get_latest_version()

    if not latest_version:
        print("Não foi possível obter as informações de atualização.")
        return


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
        janela = messagebox.askyesno(
            "Atualização Disponível",
            "Uma nova versão está disponível.\nDeseja baixar e atualizar agora?",
        )
        # Botão para verificar atualização
        if janela:
            if download_update():
                apply_update()
                print("Atualização concluída com sucesso!")
                # Reiniciar o aplicativo após a atualização
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                print("Falha na atualização.")
        else:
            messagebox.showinfo("Atualização", "Você optou por não atualizar agora.")
            janela.destroy()

        # Iniciar o loop principal da interface
        janela.mainloop()


if __name__ == "__main__":
    check_for_updates()
