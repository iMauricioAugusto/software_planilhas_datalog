import os
import shutil
import sys
import tkinter as tk
import zipfile
from tkinter import messagebox

import requests

DOWNLOAD_URL = "https://download1325.mediafire.com/xvmvq04h9frgASBd76wlML9RM78GzED8-8fyNZOySp0235-Y8JlzVU7WSP-0H51saRW8qbZOufKGunL0g17jTINlo0f5bMdsrdtpm3EGd1VGfXo__xdDJ-QYtPS9MySp0Y3vEZAE6Cbgok0CQ7IW4-kHdQlvkJmHp1ajzzvE4yPb/l2cbj5w0m0thd4a/software_planilha_datalog.zip"


# Função para baixar a nova versão
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

# Configuração da interface Tkinter
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

# Iniciar o loop principal da interface
janela.mainloop()
