import tkinter.messagebox as tkm
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory, asksaveasfilename
import tkinter as tk
from tkinter import messagebox
import configparser

from models.planilhas import Planilha


class InterfaceGrafica:
    def __init__(self, janela_principal):

        self.janela_principal = janela_principal

        self.janela_principal.title("Criador de Planilhas Datalogs")

        self.janela_principal.configure(bg="#f5f5f5")

        self.janela_principal.state("zoomed")

        self.configurar_janela()

        self.planilha = Planilha()

        self.opcao_temperatura = BooleanVar()

        self.opcao_umidade = BooleanVar()

        self.estilo_checkbuton()

        self.criar_widgets()

    def criar_widgets(self):

        Label(
            self.janela_principal,
            text="Criador de Planilhas Datalogs",
            font="Arial 20",
            fg="white",
            bg="#3B5999",
        ).grid(row=0, column=0, columnspan=8, sticky="NSEW")

        Label(
            self.janela_principal,
            text="Selecionar Tabelas:",
            font="Arial 14 bold",
            bg="#f5f5f5",
            justify=LEFT,
        ).grid(row=2, column=0, padx=10)

        Label(
            self.janela_principal,
            text="Selecione a Unidade:",
            font="Arial 14 bold",
            bg="#f5f5f5",
            justify=LEFT,
        ).grid(row=1, column=0, padx=10)

        Label(
            self.janela_principal,
            text="Selecione a Data de Medição:",
            font="Arial 14 bold",
            bg="#f5f5f5",
        ).grid(row=1, column=3, padx=10)

        Label(
            self.janela_principal,
            text="De",
            fg="#3B5999",
            font="Arial 10 bold",
            bg="#f5f5f5",
        ).grid(row=1, column=4, padx=5)

        Label(
            self.janela_principal,
            text="Até",
            fg="#3B5999",
            font="Arial 10 bold",
            bg="#f5f5f5",
        ).grid(row=1, column=6, padx=5)

        Label(
            self.janela_principal,
            text="Selecione o Intervalo de Medição:",
            font="Arial 14 bold",
            bg="#f5f5f5",
        ).grid(row=2, column=3, padx=10)

        Label(
            self.janela_principal,
            text="De",
            fg="#3B5999",
            font="Arial 10 bold",
            bg="#f5f5f5",
        ).grid(row=2, column=4, padx=5)

        Label(
            self.janela_principal,
            text="Até",
            fg="#3B5999",
            font="Arial 10 bold",
            bg="#f5f5f5",
        ).grid(row=2, column=6, padx=5)

        Label(
            self.janela_principal,
            text="Criado por Maurício Augusto \n \n Trescal RJ",
            font="Arial 12 italic",
            bg="#f5f5f5",
            justify=CENTER,
        ).grid(row=4, column=7)

        self.data_inicial_entry = Entry(
            self.janela_principal, font="Arial 12", justify=CENTER
        )
        self.data_inicial_entry.grid(row=1, column=5, padx=20)

        self.data_final_entry = Entry(
            self.janela_principal, font="Arial 12", justify=CENTER
        )
        self.data_final_entry.grid(row=1, column=7, padx=20)

        self.tempo_inicial_entry = Entry(
            self.janela_principal, font="Arial 12", justify=CENTER
        )
        self.tempo_inicial_entry.grid(row=2, column=5, padx=20)

        self.tempo_final_entry = Entry(
            self.janela_principal, font="Arial 12", justify=CENTER
        )
        self.tempo_final_entry.grid(row=2, column=7, padx=20)

        ttk.Checkbutton(
            self.janela_principal,
            text="Temperatura",
            variable=self.opcao_temperatura,
            onvalue=True,
            offvalue=False,
            style="Mauricio.TCheckbutton",
        ).grid(row=1, column=1, padx=10, pady=5, sticky="W")

        ttk.Checkbutton(
            self.janela_principal,
            text="Umidade",
            variable=self.opcao_umidade,
            onvalue=True,
            offvalue=False,
            style="Mauricio.TCheckbutton",
        ).grid(row=1, column=2, padx=10, pady=5, sticky="W")

        Button(
            self.janela_principal,
            text="Selecionar",
            font="Arial 14",
            justify=RIGHT,
            command=self.selecionar_tabelas,
        ).grid(
            row=2,
            column=1,
        )

        Button(
            self.janela_principal,
            text="Criar",
            font="Arial 14",
            command=self.criar_planilha,
        ).grid(row=5, column=0, columnspan=8, padx=20, pady=5, sticky="SEW")

        Button(
            self.janela_principal,
            text="Sair",
            font="Arial 14",
            command=self.janela_principal.destroy,
        ).grid(row=6, column=0, columnspan=8, padx=20, pady=5, sticky="NSEW")

        for i in range(5):

            self.janela_principal.grid_rowconfigure(i, weight=1)

        for i in range(5):

            self.janela_principal.grid_columnconfigure(i, weight=1)

    def configurar_janela(self):

        largura_janela = 450

        altura_janela = 300

        largura_tela = self.janela_principal.winfo_screenwidth()

        altura_tela = self.janela_principal.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura_janela // 2)

        pos_y = (altura_tela // 2) - (altura_janela // 2)

        self.janela_principal.geometry(
            f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}"
        )

    def estilo_checkbuton(self):

        style = ttk.Style()

        style.configure("Mauricio.TCheckbutton", background="#f5f5f5")

    def selecionar_tabelas(self):

        pasta = askdirectory(title="Selecione uma Pasta")

        if pasta:
            opcao_temperatura = self.opcao_temperatura.get()

            opcao_umidade = self.opcao_umidade.get()

            self.planilha.selecionar_tabelas(pasta, opcao_temperatura, opcao_umidade)

    def criar_planilha(self):

        data_inicial = self.data_inicial_entry.get()

        data_final = self.data_final_entry.get()

        # Validar datas
        def validar_data(data):
            try:
                datetime.strptime(data, "%Y-%m-%d")
                return True
            except ValueError:
                return False

        if not validar_data(data_inicial):
            tkm.showerror("Erro", "A data de Medição deve estar no formato YYYY-MM-DD")
            return

        if not validar_data(data_final):
            tkm.showerror("Erro", "A data de Medição deve estar no formato YYYY-MM-DD")
            return

        tempo_inicial = self.tempo_inicial_entry.get()

        tempo_final = self.tempo_final_entry.get()

        def validar_tempo(tempo):
            try:
                datetime.strptime(tempo, "%H:%M:%S")
                return True
            except ValueError:
                return False

        # Validação dos tempos
        if not validar_tempo(tempo_inicial):
            tkm.showerror("Erro", "O tempo inicial deve estar no formato HH:MM:SS")
            return

        if not validar_tempo(tempo_final):
            tkm.showerror("Erro", "O tempo final deve estar no formato HH:MM:SS")
            return

        self.planilha.filtrar_planilha(
            data_inicial, data_final, tempo_inicial, tempo_final
        )

        caminho = asksaveasfilename(
            title="Selecionar Local de Salvamento",
            defaultextension="xls",
            filetypes=(("Arquivos Excel", ".xls"), ("Arquivos de texto", ".txt")),
        )

        if caminho:

            self.planilha.salvar_planilha(caminho)
