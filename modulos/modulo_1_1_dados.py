import json
import os
import pandas as pd

# Caminho do JSON relativo à pasta do projeto: funciona mesmo executando de outra pasta
CAMINHO_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados_aurora_siger.json")

# Implementação da Estrutura Trie para a busca por prefixo (Req. 1.5)
class NodoTrie:
    def __init__(self):
        self.filhos = {}
        self.is_fim_palavra = False
        self.dados_modulo = None

class TrieBuscaModulos:
    def __init__(self):
        self.raiz = NodoTrie()

    def inserir(self, chave, dados):
        nodo = self.raiz
        for char in chave.lower():
            if char not in nodo.filhos:
                nodo.filhos[char] = NodoTrie()
            nodo = nodo.filhos[char]
        nodo.is_fim_palavra = True
        nodo.dados_modulo = dados

    def buscar_prefixo(self, prefixo):
        nodo = self.raiz
        for char in prefixo.lower():
            if char not in nodo.filhos:
                return []
            nodo = nodo.filhos[char]
        
        resultados = []
        self._coletar(nodo, resultados)
        return resultados

    def _coletar(self, nodo, resultados):
        if nodo.is_fim_palavra:
            resultados.append(nodo.dados_modulo)
        for _, filho in nodo.filhos.items():
            self._coletar(filho, resultados)

def carregar_dados(exibir_tela=False):
    # Leitura utilizando Pandas para alimentar as análises
    with open(CAMINHO_DADOS, "r", encoding="utf-8") as dados:
        dados_carregados = json.load(dados)

    df_modulos = pd.DataFrame(dados_carregados["modulos_colonia"])
    
    # Colunas padrão para manter a mesma identidade visual em tabela
    colunas_tabela = [
        "id",
        "nome",
        "prioridade",
        "proibido_desligar",
        "codigo_sensor",
        "potencia_w",
        "latencia_observada_ms"
    ]

    if exibir_tela:
        while True:
            print("\n--- MÓDULO DE DADOS DA AURORA SIGER ---")
            escolha = input("Deseja exibir todos os módulos cadastrados? (Y/N): ").strip().upper()
            
            if escolha == 'Y':
                print("\n[EXIBIÇÃO COMPLETA - DataFrame Pandas]:")
                print(df_modulos[colunas_tabela])
                break
            elif escolha == 'N':
                # Inicializa e popula a Trie com os dados dos módulos
                trie = TrieBuscaModulos()
                # Cada módulo é indexado por três chaves: nome, ID e código do sensor
                for _, mod in df_modulos.iterrows():
                    trie.inserir(mod['nome'], mod.to_dict())
                    trie.inserir(mod['id'], mod.to_dict())
                    trie.inserir(mod['codigo_sensor'], mod.to_dict())

                prefixo = input("\nDigite o prefixo para busca com Trie (ex: 'Hab', 'MOD-0', 'lab', 'SEN-0x3'): ").strip()
                encontrados = trie.buscar_prefixo(prefixo)
                
                if encontrados:
                    # Remove duplicatas caso a chave case simultaneamente com nome e ID
                    ids_vistos = set()
                    encontrados_unicos = []
                    for m in encontrados:
                        if m['id'] not in ids_vistos:
                            encontrados_unicos.append(m)
                            ids_vistos.add(m['id'])
                    
                    # Converte o resultado filtrado em DataFrame para manter o layout tabular
                    df_filtrado = pd.DataFrame(encontrados_unicos)
                    print(f"\n[BUSCA POR PREFIXO '{prefixo}' - Estrutura Trie]:")
                    print(df_filtrado[colunas_tabela])
                    break
                else:
                    print(f"\nNenhum registro encontrado na Trie com o prefixo '{prefixo}'.")
            else:
                print("Opção inválida. Por favor, digite 'Y' ou 'N'.")
                continue
    
    return df_modulos, dados_carregados