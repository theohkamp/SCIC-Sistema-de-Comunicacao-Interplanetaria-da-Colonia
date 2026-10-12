from modulos import modulo_1_2_erros, modulo_1_3_modelo, modulo_1_4_heap

# Tolerância de erro relativo por tipo de módulo (mesmo critério discutido na opção 2)
TOLERANCIA_ESSENCIAL_PCT = 5.0       # módulos proibidos de desligar (ex.: Suporte Médico)
TOLERANCIA_PERIFERICO_PCT = 15.0     # demais módulos (ex.: Laboratório)


def classificar_modulo(linha):
    # Define a tolerância conforme o módulo seja essencial ou periférico
    tolerancia = TOLERANCIA_ESSENCIAL_PCT if linha["proibido_desligar"] else TOLERANCIA_PERIFERICO_PCT
    situacao = "CRÍTICO" if linha["erro_relativo_pct"] > tolerancia else "aceitável"
    return tolerancia, situacao


def executar(df_modulos, dados_brutos):
    print("\n=== ANÁLISE FINAL DOS RESULTADOS - SCIC (1.7) ===")

    # 1. Indicadores de comunicação: latência acima do previsto e erro relativo vs tolerância
    df = modulo_1_2_erros.calcular_erros(df_modulos)
    acima = df[df["latencia_observada_ms"] > df["latencia_prevista_ms"]]
    print("\n[1] INDICADORES DE COMUNICAÇÃO")
    print(f"Latência média prevista : {df['latencia_prevista_ms'].mean():.1f} ms")
    print(f"Latência média observada: {df['latencia_observada_ms'].mean():.1f} ms")
    print(f"Módulos com latência acima do previsto: {len(acima)} de {len(df)}")

    criticos = []
    for _, linha in df.iterrows():
        tolerancia, situacao = classificar_modulo(linha)
        print(f"  {linha['id']} {linha['nome']:<17} erro {linha['erro_relativo_pct']:>6.2f}% "
              f"(tolerância {tolerancia:.0f}%) -> {situacao}")
        if situacao == "CRÍTICO":
            criticos.append(linha)

    # 2. Desempenho do modelo de previsão (mesma configuração do relatório: 500 ciclos)
    m = modulo_1_3_modelo.treinar_e_avaliar(df_modulos, ciclos=500)
    print("\n[2] MODELO DE PREVISÃO (500 ciclos simulados)")
    print(f"MAE {m['mae']:.1f} ms | RMSE {m['rmse']:.1f} ms | R² {m['r2']:.2f}")
    print("Leitura: o modelo serve de referência; desvios grandes indicam anomalia a investigar.")

    # 3. Alerta mais urgente, consultado na raiz do Max-Heap
    heap = modulo_1_4_heap.MaxHeapAlertas()
    for alerta in dados_brutos.get("alertas_operacionais", []):
        heap.inserir(alerta)
    urgente = heap.consultar_mais_urgente()
    print("\n[3] ALERTA MAIS URGENTE (raiz do Max-Heap)")
    if urgente:
        print(f"[{urgente['id_alerta']}] {urgente['unidade']} - {urgente['situacao']} (nota {urgente['prioridade_nota']})")

    # 4. Energia: potência e corrente totais (relação de potência I = P / V)
    potencia_total = df_modulos["potencia_w"].sum()
    tensao = df_modulos["tensao_v"].iloc[0]
    print("\n[4] ENERGIA")
    print(f"Potência total: {potencia_total:.1f} W | Corrente total a {tensao:.0f} V: {potencia_total / tensao:.2f} A")

    # 5. Gerenciamento inteligente: recomendações derivadas dos próprios resultados
    print("\n[5] GERENCIAMENTO INTELIGENTE - RECOMENDAÇÕES")
    if criticos:
        for linha in criticos:
            print(f"- {linha['id']} ({linha['nome']}): reservar banda prioritária e acionar enlace redundante;")
            print(f"  agendar manutenção preditiva do sensor {linha['codigo_sensor']} antes de nova degradação.")
    else:
        print("- Nenhum módulo fora da tolerância: manter monitoramento contínuo.")
    print("- Monitoramento contínuo: recalcular erros a cada ciclo para detectar anomalias cedo.")
    print("- Supervisão humana: a equipe valida cada alerta antes de qualquer ação automática.")
