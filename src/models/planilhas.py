import glob
import os
import tkinter.messagebox as tkm
from pathlib import Path

import pandas as pd


class Planilha:
    def __init__(self):
        self.df_final = pd.DataFrame()
        self.df_final_formatada = pd.DataFrame()

    # Função responsável pela filtragem da planilha pela data, hora de início e hora final.
    def filtrar_planilha(self, data_inicial, data_final, tempo_inicial, tempo_final):

        print("Filtrando tabela...")

        # Conversão da coluna "Time" para datetime, permitindo que o Pandas infira o formato
        self.df_final["Time"] = pd.to_datetime(self.df_final["Time"], errors="coerce")

        # Conversão de data_inicial e data_final para datetime, inferindo o formato
        data_inicial = pd.to_datetime(data_inicial, errors="coerce")
        data_final = pd.to_datetime(data_final, errors="coerce")

        if pd.isna(data_inicial) or pd.isna(data_final):
            raise ValueError("Formato inválido para data_inicial ou data_final")

        # Filtrando por data
        filtro_data = (self.df_final["Time"].dt.date >= data_inicial.date()) & (
            self.df_final["Time"].dt.date <= data_final.date()
        )
        self.df_final_formatada = self.df_final[filtro_data].copy()

        # Conversão de tempos
        tempo_inicial = pd.to_datetime(
            tempo_inicial, format="%H:%M:%S", errors="coerce"
        ).time()
        tempo_final = pd.to_datetime(
            tempo_final, format="%H:%M:%S", errors="coerce"
        ).time()

        if pd.isna(tempo_inicial) or pd.isna(tempo_final):
            raise ValueError("Formato inválido para tempo_inicial ou tempo_final")

        # Caso o intervalo de tempo passe para o dia seguinte
        if tempo_final <= tempo_inicial:
            # Filtro para o tempo inicial no primeiro dia
            filtro_tempo_inicial = (
                self.df_final_formatada["Time"].dt.time >= tempo_inicial
            )

            # Filtro para o tempo final no segundo dia
            filtro_tempo_final = self.df_final_formatada["Time"].dt.time <= tempo_final

            # Filtro para dados no primeiro dia e no segundo dia
            filtro_dia_inicial = (
                self.df_final_formatada["Time"].dt.date == data_inicial.date()
            )
            filtro_dia_final = (
                self.df_final_formatada["Time"].dt.date == data_final.date()
            )

            # Aplicando os filtros para o intervalo de 24 horas
            self.df_final_formatada = self.df_final_formatada[
                (filtro_dia_inicial & filtro_tempo_inicial)
                | (filtro_dia_final & filtro_tempo_final)
            ]
        else:
            # Filtrando quando tempo_inicial <= tempo_final no mesmo dia
            filtro_tempo = (
                self.df_final_formatada["Time"].dt.time >= tempo_inicial
            ) & (self.df_final_formatada["Time"].dt.time <= tempo_final)
            self.df_final_formatada = self.df_final_formatada[filtro_tempo]

        # Formatação da coluna "Time" no formato %H:%M:%S
        self.df_final_formatada["Time"] = self.df_final_formatada["Time"].dt.strftime(
            "%H:%M:%S"
        )

        print(self.df_final_formatada)
        return self.df_final_formatada

    # Função responsável por salvar a planilha
    def salvar_planilha(self, caminho):

        self.df_final_formatada.to_excel(Path(caminho), index=False)

        tkm.showinfo(title="Salvo", message="Planilha salva com sucesso.")

    # Função responsável por selecionar a planilha no computador do usuário
    def selecionar_tabelas(self, pasta, opcao_temperatura, opcao_umidade):

        padrao_arquivos_xls = os.path.join(pasta, "*.xls")

        arquivos_xls = glob.glob(padrao_arquivos_xls)

        i = 1

        if arquivos_xls:
            arquivos = [os.path.join(pasta, arquivo) for arquivo in os.listdir(pasta)]

            primeiro_arquivo = arquivos[0]

            try:
                # Tenta ler o arquivo normalmente
                df_data = pd.read_excel(primeiro_arquivo, sheet_name="Lista", header=0)

                if "Tempo" not in df_data.columns:
                    # Se "Tempo" não existe, lê a linha 27 como cabeçalho
                    df_data = pd.read_excel(
                        primeiro_arquivo, sheet_name="Lista", header=26
                    )

                if "Tempo" in df_data.columns:
                    self.df_final["Time"] = df_data["Tempo"]
                else:
                    tkm.showerror(
                        title="ERRO", message="Coluna 'Tempo' não encontrada."
                    )
                    return None

            except Exception as e:
                tkm.showerror(title="ERRO", message=f"Erro ao ler o arquivo: {e}")
                return None

            # Lê temperatura ou umidade dependendo da opção escolhida
            if opcao_temperatura:
                try:
                    for arquivo in arquivos:

                        df = pd.read_excel(arquivo, sheet_name="Lista", header=0)

                        if "Temperatura°C" not in df.columns:
                            df = pd.read_excel(arquivo, sheet_name="Lista", header=26)

                        if "Temperatura°C" in df.columns:
                            self.df_final[i] = df["Temperatura°C"]
                            i += 1
                        else:
                            tkm.showerror(
                                title="ERRO",
                                message="Coluna 'Temperatura°C' não encontrada.",
                            )
                            return None
                    print(self.df_final)
                    return self.df_final

                except Exception as e:
                    tkm.showerror(title="ERRO", message=f"Erro ao ler o arquivo: {e}")
                    return None

            elif opcao_umidade:
                try:
                    for arquivo in arquivos:

                        df = pd.read_excel(arquivo, sheet_name="Lista", header=0)

                        if "Umidade%" not in df.columns:
                            df = pd.read_excel(arquivo, sheet_name="Lista", header=26)

                        if "Umidade%" in df.columns:
                            self.df_final[i] = df["Umidade%"]
                            i += 1
                        else:
                            tkm.showerror(
                                title="ERRO",
                                message="Coluna 'Umidade%' não encontrada.",
                            )
                            return None

                    print(self.df_final)
                    return self.df_final

                except Exception as e:
                    tkm.showerror(title="ERRO", message=f"Erro ao ler o arquivo: {e}")
                    return None
        else:
            tkm.showerror(title="ERRO", message="Nenhuma planilha excel encontrada.")
            return None
