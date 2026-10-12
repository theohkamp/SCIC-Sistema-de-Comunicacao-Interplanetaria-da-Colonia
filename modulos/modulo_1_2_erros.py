import pandas as pd

def simular_acumulo_buffer(latencia_inicial, ciclos=5):
    """
    Simulação iterativa simples (progressão numérica).
    Fórmula: L(t+1) = L(t) * 1.10 + 2.0
    Simula o atraso aumentando 10% a cada ciclo devido ao congestionamento,
    mais 2ms fixos de tempo de processamento.
    """
    latencias = [latencia_inicial]
    
    for _ in range(ciclos - 1):
        nova_latencia = latencias[-1] * 1.10 + 2.0
        # Arredondamos para 2 casas decimais para simular a leitura do sensor
        latencias.append(round(nova_latencia, 2))
        
    return latencias

def calcular_erros(df_modulos):
    """
    Calcula o erro absoluto e o erro relativo (%) de cada módulo.
    A latência observada (medida) é o valor de referência e a prevista é a aproximação:
    erro relativo = |observada - prevista| / observada.
    """
    df = df_modulos.copy()
    df["erro_absoluto_ms"] = (df["latencia_observada_ms"] - df["latencia_prevista_ms"]).abs()
    df["erro_relativo_pct"] = ((df["erro_absoluto_ms"] / df["latencia_observada_ms"]) * 100).round(2)
    return df

def executar(df_modulos):

    # Cálculo de Erros (Absoluto e Relativo)
    df = calcular_erros(df_modulos)

    print("\n--- TABELA DE ERROS NUMÉRICOS POR MÓDULO ---")
    print("Referência: latência observada (medida). Aproximação: latência prevista.")
    print(df[["id", "nome", "latencia_prevista_ms", "latencia_observada_ms", "erro_absoluto_ms", "erro_relativo_pct"]].to_string(index=False))

    # Análise de Ponto Flutuante e Acúmulo de Erro (IEEE 754)
    passo_ciclo = 0.1
    drift_acumulado = 0.0
    
    for _ in range(1000): 
        drift_acumulado += passo_ciclo
        
    erro_ponto_flutuante = drift_acumulado - 100.0

    print("\n--- ANÁLISE DE PONTO FLUTUANTE (IEEE 754) ---")
    print("Demonstração da imprecisão do Python ao somar 0.1 mil vezes:")
    print(f"Valor Esperado:      100.0000000000000000 ms")
    print(f"Drift Acumulado:     {drift_acumulado:.16f} ms")
    print(f"Erro Residual de PF: {erro_ponto_flutuante:.16e} ms")

    # Simulação Iterativa Simples da Evolução da Latência
    while True:
        mod_escolhido = input("\nDigite o ID do módulo que deseja simular (ex: MOD-03): ").strip().upper()

        if mod_escolhido in df['id'].values:
            mod_0x = df[df['id'] == mod_escolhido].iloc[0] # Pegando o módulo escolhido
            break
        else:
            print("ID de módulo inválido. Certifique-se de digitar um ID de módulo existente (ex: MOD-01, MOD-02...)")
            
    while True:
        try:
            ciclos_simulacao = int(input("Quantos ciclos de simulação você deseja realizar? "))
            break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    latencias_futuras = simular_acumulo_buffer(mod_0x['latencia_observada_ms'], ciclos=ciclos_simulacao)
    
    print(f"\n--- SIMULAÇÃO ITERATIVA: DEGRADAÇÃO DO SINAL NO {mod_0x['id']} ---")
    print("Cenário: O módulo sofre sobrecarga e a latência aumenta a cada ciclo.")
    for ciclo, latencia in enumerate(latencias_futuras, start=1):
        print(f"  Ciclo {ciclo}: Latência Projetada = {latencia} ms")
        
    print("\n--- DISCUSSÃO DE ACEITABILIDADE ---")
    print("No contexto da Aurora Siger, erros relativos acima de 5% no MOD-03 (Suporte Médico)")
    print("são críticos e inaceitáveis, pois atrasam a telemetria de sinais vitais.")
    print("Já erros de até 15% no MOD-06 (Laboratório) podem ser tolerados pela baixa prioridade.")