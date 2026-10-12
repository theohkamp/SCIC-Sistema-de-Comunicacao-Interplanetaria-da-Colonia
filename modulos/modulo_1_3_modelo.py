import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def treinar_e_avaliar(df_modulos, ciclos=500):
    """
    Gera 'ciclos' de telemetria simulada, treina a Regressão Linear Múltipla
    e devolve um dicionário com as métricas de avaliação (MAE, MSE, RMSE e R²).
    Também é usada pela Análise Final (opção 6), sem pedir dados ao usuário.
    """
    # Fixando a semente para que os resultados sejam sempre os mesmos a cada execução
    np.random.seed(42)
    registros_expandidos = []

    # Expansão de dados simulando n ciclos de telemetria para obtermos volume de treino (n*6 amostras)
    for _ in range(ciclos): 
        for _, mod in df_modulos.iterrows():
            # Introduzindo ruído aleatório (distribuição normal) para simular flutuações reais de hardware
            ruido_latencia = np.random.normal(0, 15.0)
            ruido_potencia = np.random.normal(0, 20.0)
            
            # Garantindo que latência e potência não sejam negativas
            lat_obs = max(10.0, mod["latencia_observada_ms"] + ruido_latencia)
            pot_w = max(100.0, mod["potencia_w"] + ruido_potencia)
            
            registros_expandidos.append({
                "prioridade": mod["prioridade"],    
                "potencia_w": pot_w,
                "latencia_prevista_ms": mod["latencia_prevista_ms"],
                "latencia_observada_ms": lat_obs
            })

    # Criando o DataFrame de treinamento
    df_treino = pd.DataFrame(registros_expandidos)
    
    # Separando as variáveis independentes (X) da variável dependente (y)
    X = df_treino[["prioridade", "potencia_w", "latencia_prevista_ms"]]
    y = df_treino["latencia_observada_ms"]

    # Divisão: 70% para treino e 30% para teste (validação)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

    # Utilizando Regressão Linear Múltipla Clássica (Nível básico, sem Ridge ou hiperparâmetros)
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Realizando as previsões com os dados de teste
    y_pred = modelo.predict(X_test)

    # Cálculo das métricas de performance
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    return {"ciclos": ciclos, "amostras": len(df_treino), "mae": mae, "mse": mse, "rmse": rmse, "r2": r2}


def executar(df_modulos):
    while True:
        try:
            ciclos = int(input("Quantos ciclos de telemetria você deseja simular para treinar o modelo? (ex: 500) "))
            if ciclos < 2:
                print("Use pelo menos 2 ciclos para haver dados de treino e de teste.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    m = treinar_e_avaliar(df_modulos, ciclos)
    mae, mse, rmse, r2 = m["mae"], m["mse"], m["rmse"], m["r2"]

    print(f"\nAmostras geradas: {m['amostras']} (70% treino / 30% teste)")
    print("\n--- MÉTRICAS DE PERFORMANCE DO MODELO SCIC (REGRESSÃO LINEAR) ---")
    print(f"MAE  (Erro Absoluto Médio):        {mae:.3f} ms")
    print(f"MSE  (Erro Quadrático Médio):      {mse:.3f}")
    print(f"RMSE (Raiz do Erro Quadrático):    {rmse:.3f} ms")
    print(f"R²   (Coeficiente de Determinação): {r2:.4f}")

    # Interpretação: um número sozinho não basta para julgar o modelo
    print("\n--- INTERPRETAÇÃO ---")
    print(f"O R² indica que o modelo explica cerca de {r2*100:.0f}% da variação da latência.")
    print(f"RMSE ({rmse:.1f} ms) maior que o MAE ({mae:.1f} ms) indica alguns erros bem grandes,")
    print("como o salto de latência do MOD-03, que uma relação linear não captura.")
