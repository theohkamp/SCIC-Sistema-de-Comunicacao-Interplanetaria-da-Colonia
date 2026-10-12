def converter_codigo_sensor(codigo_sensor):
    """
    Interpreta o código hexadecimal do sensor (ex.: 'SEN-0x1A') como identificador numérico.
    Retorna o valor em decimal, a representação hexadecimal e a binária.
    """
    # Separa o prefixo 'SEN-' e converte a parte hexadecimal (base 16) para inteiro (base 10)
    parte_hex = codigo_sensor.split('-')[1]          # '0x1A'
    valor_decimal = int(parte_hex, 16)               # 26
    valor_hex = f"0x{valor_decimal:X}"               # '0x1A'
    valor_bin = f"0b{valor_decimal:b}"               # '0b11010'
    return valor_decimal, valor_hex, valor_bin


def processar_eletricidade(modulo):
    # A tensão de operação vem da própria base de dados (campo 'tensao_v' do JSON)
    tensao_v = modulo['tensao_v']
    potencia_w = modulo['potencia_w']

    # Relação de potência: P = V x I  ->  I = P / V
    corrente_a = potencia_w / tensao_v

    # Lei de Ohm: V = R x I  ->  R = V / I (resistência equivalente da carga do módulo)
    resistencia_ohm = tensao_v / corrente_a

    # Conferência com a corrente registrada pelo medidor na base (tolerância de 0,01 A por arredondamento)
    corrente_registrada = modulo['corrente_a']
    confere = abs(corrente_a - corrente_registrada) <= 0.01

    # Conversão de bases numéricas a partir do código hexadecimal do sensor
    decimal, hexadecimal, binario = converter_codigo_sensor(modulo['codigo_sensor'])

    print(f"\n[{modulo['id']}] {modulo['nome'].upper()}")
    print("-" * 55)
    print(f"Potência Registrada  : {potencia_w} W")
    print(f"Tensão Operacional   : {tensao_v:.0f} V")
    print(f"Corrente Calculada   : {corrente_a:.2f} A  (Potência: I = P / V)")
    print(f"Corrente do Medidor  : {corrente_registrada:.2f} A  ->  {'confere' if confere else 'DIVERGENTE'}")
    print(f"Resistência da Carga : {resistencia_ohm:.2f} Ω  (Lei de Ohm: R = V / I)")
    print(f"Sensor {modulo['codigo_sensor']:<9}   : HEX: {hexadecimal} | DECIMAL: {decimal} | BIN: {binario}")


def executar(df_modulos):
    print("\n--- RELATÓRIO ELÉTRICO E BASES NUMÉRICAS (1.6) ---")
    print("Entrada: sensores/medidores simulados | Saída: terminal e relatórios | Interfaces: rede, USB, Wi-Fi, Bluetooth (conceitual)")

    for _, mod in df_modulos.iterrows():
        processar_eletricidade(mod.to_dict())

    # Totais da colônia: a corrente total ajuda a dimensionar a infraestrutura elétrica compartilhada
    potencia_total = df_modulos['potencia_w'].sum()
    tensao = df_modulos['tensao_v'].iloc[0]
    print("\n--- TOTAIS DA COLÔNIA ---")
    print(f"Potência total: {potencia_total:.1f} W | Corrente total a {tensao:.0f} V: {potencia_total / tensao:.2f} A")
