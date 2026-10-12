import os
import subprocess
import pandas as pd
from modulos import modulo_1_1_dados, modulo_1_2_erros, modulo_1_3_modelo, modulo_1_4_heap, modulo_1_6_hardware, modulo_1_7_analise_final

# Exibe todas as colunas das tabelas do Pandas no terminal, sem cortes com "..."
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

def limpar_terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

def voltar_menu():
    input("\nPressione ENTER para voltar ao menu principal...")
    limpar_terminal()

def main():

    # 1. Carregamos o Estado Global (Memória Principal) logo no início
    try:
        df_modulos, dados_brutos = modulo_1_1_dados.carregar_dados()
    except FileNotFoundError:
        print("ERRO: Arquivo 'dados_aurora_siger.json' não encontrado. Certifique-se de que ele está na mesma pasta.")
        return

    # 2. Loop do Menu Interativo
    while True:
        print("\n" + "="*55)
        print(" MENU PRINCIPAL - AURORA SIGER (FASE 6)")
        print("="*55)
        print("1 - Gerenciar Dados dos Módulos & Busca por Prefixo (1.1 & 1.5)")
        print("2 - Analisar Erros Numéricos e Ponto Flutuante (1.2)")
        print("3 - Avaliar Modelo de Previsão de Latência (1.3)")
        print("4 - Priorizar Alertas Críticos via Heap (1.4)")
        print("5 - Hardware, Bases Numéricas e Eletricidade (1.6)")
        print("6 - Análise Final e Gerenciamento Inteligente (1.7)")
        print("0 - Encerrar Sistema")
        
        opcao = input("\nDigite o número da opção desejada: ")

        match opcao:
            case '1':
                # Chama a função do 1.1 novamente só se o usuário quiser rever o log
                limpar_terminal()
                modulo_1_1_dados.carregar_dados(exibir_tela=True)
                voltar_menu()
            
            case '2':
                # Passa o DataFrame para o módulo 1.2
                limpar_terminal()
                modulo_1_2_erros.executar(df_modulos)
                voltar_menu()
            
            case '3':
                # Passa o DataFrame para o módulo 1.3
                limpar_terminal()
                modulo_1_3_modelo.executar(df_modulos)
                voltar_menu()
            
            case '4':
                limpar_terminal()
                modulo_1_4_heap.executar(dados_brutos)
                voltar_menu()
            
            case '5':
                limpar_terminal()
                modulo_1_6_hardware.executar(df_modulos)
                voltar_menu()
            
            
            case '6':
                limpar_terminal()
                modulo_1_7_analise_final.executar(df_modulos, dados_brutos)
                voltar_menu()

            case '0':
                print("Desconectando da Aurora Siger. Sistema encerrado.")
                break
            
            case _:
                print("Opção inválida. Tente novamente.")
                voltar_menu()

if __name__ == "__main__":
    main()