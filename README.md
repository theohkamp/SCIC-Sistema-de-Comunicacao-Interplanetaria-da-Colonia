# SCIC - Sistema de Comunicação Interplanetária da Colônia

> **Projeto Aurora Siger - Fase 6**
>
> *Core Cognitivo, Análise de Telemetria e Priorização Dinâmica de Enlaces*

**Vídeo de apresentação:** https://youtu.be/S3k99MLbHa8

**Integrantes:** Pedro Matteo Benta dos Santos Simplicio (RM573133), Christian Theodor Heisterkamp (RM571998), Samuel Gissi Nogueira Gonçalves (RM568867) e Matheus Freitas da Silva Santos (RM574003)

---

## Sumário

* [Visão Geral e Objetivos](#visão-geral-e-objetivos)
* [Arquitetura e Módulos do Sistema](#arquitetura-e-módulos-do-sistema)
* [Estrutura de Arquivos](#estrutura-de-arquivos)
* [Pré-requisitos e Dependências](#pré-requisitos-e-dependências)
* [Como Executar](#como-executar)
* [Exemplos de Execução](#exemplos-de-execução)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Considerações Éticas e Sustentáveis](#considerações-éticas-e-sustentáveis)

---

## Visão Geral e Objetivos

O **Sistema de Comunicação Interplanetária da Colônia (SCIC)** foi projetado para operar como o núcleo de processamento e gerenciamento de rede da colônia simulada **Aurora Siger**. Em ambientes espaciais críticos como Marte, o monitoramento contínuo de dados operacionais, a predição de latências de enlace e a triagem instantânea de alertas de emergência são vitais para a sobrevivência humana e a eficiência dos módulos operacionais.

Os principais objetivos do sistema incluem:

1. **Estruturação de Dados Operacionais:** Organização e manipulação eficiente do status e consumo dos módulos da colônia.
2. **Análise Numérica e Ponto Flutuante:** Avaliação de erros de latência e monitoramento do drift numérico no padrão IEEE 754.
3. **Predição de Latência:** Treinamento de modelo estatístico para identificar variações na rede de telemetria.
4. **Priorização de Alertas:** Estruturação de **Max-Heap** para respostas imediatas a eventos críticos.
5. **Busca Rápida por Prefixo:** Implementação de árvore **Trie** para localização instantânea de módulos (por nome ou ID) e de sensores (pelo código).
6. **Eletricidade e Hardware:** Cálculo da corrente pela relação de potência (I = P / V), da resistência equivalente pela Lei de Ohm (R = V / I) e conversão do código hexadecimal dos sensores para decimal e binário.
7. **Análise Final e Gerenciamento Inteligente:** Consolidação dos indicadores, classificação dos módulos pela tolerância de erro e recomendações de operação.

---

## Arquitetura e Módulos do Sistema

O arquivo `codigo_fonte.py` atua como o **menu principal interativo** do sistema, orquestrando a chamada para os submódulos organizados na pasta `modulos/`:

* **`modulos/modulo_1_1_dados.py` (1.1 & 1.5 - Dados e Trie):**
  * Manipulação de dados estruturados e buscas rápidas por prefixo via árvore Trie O(m), indexando nome, ID e código do sensor.
* **`modulos/modulo_1_2_erros.py` (1.2 - Análise Numérica):**
  * Cálculo de erro absoluto e erro relativo (%) — com a latência observada como valor de referência —, simulação de acúmulo de ponto flutuante e de degradação do Suporte Médico.
* **`modulos/modulo_1_3_modelo.py` (1.3 - Predição Estatística):**
  * Modelo de Regressão Linear Múltipla para predição de latências com avaliação via MAE, MSE, RMSE e R².
* **`modulos/modulo_1_4_heap.py` (1.4 - Max-Heap de Alertas):**
  * Fila de prioridade para triagem de alertas críticos: inserção e extração em O(log n), consulta do mais urgente em O(1).
* **`modulos/modulo_1_6_hardware.py` (1.6 - Eletricidade e Bases Numéricas):**
  * Conversão do código hexadecimal dos sensores (ex.: `SEN-0x3C` → 60 → `0b111100`), corrente pela relação de potência (I = P / V) conferida com o medidor, e resistência da carga pela Lei de Ohm (R = V / I).
* **`modulos/modulo_1_7_analise_final.py` (1.7 - Análise Final e Gerenciamento Inteligente):**
  * Resumo dos indicadores de latência, módulos fora da tolerância, métricas do modelo, alerta mais urgente, consumo total e recomendações de operação.

---

## Estrutura de Arquivos

A entrega do projeto é organizada conforme a estrutura de diretórios abaixo:

```text
SCIC_Fase6/
├── modulos/
│   ├── modulo_1_1_dados.py    # Carregamento do JSON, Pandas e Árvore Trie
│   ├── modulo_1_2_erros.py    # Análise de erro, drift e degradação
│   ├── modulo_1_3_modelo.py   # Regressão Linear Múltipla e métricas
│   ├── modulo_1_4_heap.py     # Estrutura e gerenciamento do Max-Heap
│   ├── modulo_1_6_hardware.py # Bases numéricas, potência e Lei de Ohm
│   └── modulo_1_7_analise_final.py # Análise final e recomendações
├── codigo_fonte.py            # Script principal (menu interativo)
├── dados_aurora_siger.json    # Base de dados estruturada dos módulos
├── link_video.txt             # Link para o vídeo
├── README.md                  # Documentação completa do projeto
├── relatorio_tecnico.pdf      # Relatório técnico completo do projeto
└── requirements.txt           # Dependências e bibliotecas do projeto
```

---

## Pré-requisitos e Dependências

Para executar o sistema, é necessário ter instalado o **Python 3.12** ou superior (a versão 2.5.3 do NumPy não é distribuída para Python 3.10 ou 3.11).

As dependências do projeto estão listadas no arquivo `requirements.txt`:

```text
numpy == 2.5.3
pandas == 3.0.6
scikit-learn == 1.9.1
```

---

## Como Executar

### 1. Clonar ou Extrair o Projeto

Navegue até a pasta raiz do projeto:

```bash
cd SCIC_Fase6
```
### 2. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Sistema SCIC

Execute o arquivo principal que exibe o menu do sistema:

```bash
python codigo_fonte.py
```

---

## Exemplos de Execução

| Opção | O que digitar | Resultado esperado |
| --- | --- | --- |
| 1 | `Y` | Tabela com os 6 módulos da colônia |
| 1 | `N` e depois `Hab` | Busca na Trie retorna o MOD-01 (Habitação) |
| 1 | `N` e depois `SEN-0x3` | Busca na Trie pelo código do sensor retorna o MOD-03 |
| 2 | `MOD-03` e depois `5` | Erros por módulo (MOD-03: 400,4 ms, 76,94%), drift de ponto flutuante e latência projetada até 771,2 ms |
| 3 | `500` | 3.000 amostras; MAE 104,049 ms, RMSE 118,296 ms, R² 0,2738 |
| 4 | — | Alertas atendidos na ordem ALT-01 (nota 10), ALT-02 (nota 9), ALT-03 (nota 2) |
| 5 | — | Por módulo: corrente (ex.: 1500 W / 240 V = 6,25 A), resistência (38,40 Ω) e sensor em hex, decimal e binário |
| 6 | — | Análise final: MOD-03 fora da tolerância, alerta mais urgente, consumo total (7500 W, 31,25 A) e recomendações |

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Estruturas de Dados:** Árvore Trie (Customizada), Max-Heap (Customizada)
* **Análise e Tratamento de Dados:** Pandas, NumPy (Análise numérica, cálculo de Erro Absoluto, Erro Relativo e simulação de Ponto Flutuante IEEE 754)
* **Machine Learning & Métricas:** Scikit-Learn (Regressão Linear Múltipla, train_test_split, avaliação com MAE, MSE, RMSE e R²)
* **Formatos de Arquivos:** JSON, PDF, Markdown, Python, TXT

---

## Considerações Éticas e Sustentáveis

O projeto SCIC integra princípios éticos e socioambientais fundamentais em seu desenvolvimento:

* **Sustentabilidade:** Controle e dimensionamento da corrente e potência elétrica nos módulos operacionais, e uso da banda priorizado para o que é crítico.
* **Diversidade & Vieses:** Algoritmos desenvolvidos com olhar plural para evitar interpretações preconceituosas contra minorias.
* **Supervisão Humana:** Garantia de controle humano permanente sobre decisões automatizadas de IA e modelos de predição.
