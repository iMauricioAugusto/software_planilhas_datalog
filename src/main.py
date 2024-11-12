import os
from tkinter import Tk

from view.interface_grafica import InterfaceGrafica

# Verificar atualizações antes de iniciar o aplicativo
os.system("python updater.py")


# Função principal que inicia a interface gráfica
def main():
    janela_princial = Tk()
    app = InterfaceGrafica(janela_princial)
    janela_princial.mainloop()


# Executa a função principal quando o script é executado
if __name__ == "__main__":
    main()
