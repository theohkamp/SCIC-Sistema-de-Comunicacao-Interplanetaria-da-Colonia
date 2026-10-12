class MaxHeapAlertas:
    """
    Estrutura de dados Max-Heap para gerenciar e priorizar alertas operacionais
    com base na nota de urgência (prioridade_nota).
    """
    def __init__(self):
        # Inicializa a lista vazia que armazenará os nós da heap
        self.heap = []

    def pai(self, i):
        # Retorna o índice do nó pai dado o índice i de um nó filho
        return (i - 1) // 2

    def filho_esquerdo(self, i):
        # Retorna o índice do filho esquerdo dado o índice i de um nó pai
        return 2 * i + 1

    def filho_direito(self, i):
        # Retorna o índice do filho direito dado o índice i de um nó pai
        return 2 * i + 2

    def inserir(self, alerta):
        # Adiciona o novo alerta ao final da heap e reorganiza a estrutura subindo o elemento
        self.heap.append(alerta)
        self.heapify_up(len(self.heap) - 1)

    def consultar_mais_urgente(self):
        # Consulta a raiz sem removê-la: o alerta mais urgente está sempre no índice 0 -> O(1)
        return self.heap[0] if self.heap else None

    def extrair_mais_urgente(self):
        # Remove e retorna o elemento de maior prioridade (a raiz da Max-Heap)
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        raiz = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        return raiz

    def heapify_up(self, i):
        # Max-Heap: flutua o elemento para cima se a prioridade_nota for MAIOR que a do pai
        while i != 0 and self.heap[self.pai(i)]['prioridade_nota'] < self.heap[i]['prioridade_nota']:
            self.heap[i], self.heap[self.pai(i)] = self.heap[self.pai(i)], self.heap[i]
            i = self.pai(i)

    def heapify_down(self, i):
        # Restaura a propriedade de Max-Heap movendo o elemento para baixo caso seja menor que seus filhos
        maior = i
        esq = self.filho_esquerdo(i)
        dir = self.filho_direito(i)

        # Verifica se o filho esquerdo possui prioridade maior que o atual maior
        if esq < len(self.heap) and self.heap[esq]['prioridade_nota'] > self.heap[maior]['prioridade_nota']:
            maior = esq

        # Verifica se o filho direito possui prioridade maior que o atual maior
        if dir < len(self.heap) and self.heap[dir]['prioridade_nota'] > self.heap[maior]['prioridade_nota']:
            maior = dir

        # Se o maior não for o nó atual, realiza a troca e continua o processo recursivamente
        if maior != i:
            self.heap[i], self.heap[maior] = self.heap[maior], self.heap[i]
            self.heapify_down(maior)

def executar(dados_brutos):
    print("\n--- PRIORIZAÇÃO DE ALERTAS CRÍTICOS COM HEAP (1.4) ---")
    
    # Extrai os alertas operacionais do JSON bruto
    alertas = dados_brutos.get("alertas_operacionais", [])

    # Valida se existem alertas cadastrados antes de iniciar o processamento
    if not alertas:
        print("Nenhum alerta operacional cadastrado na base.")
        return

    heap_alertas = MaxHeapAlertas()

    print("Inserindo alertas no Max-Heap com base na 'prioridade_nota':")

    # Itera sobre cada alerta da base e o insere na estrutura de heap
    for alt in alertas:
        heap_alertas.inserir(alt)
        print(f" -> Inserido: [{alt['id_alerta']}] {alt['unidade']} (Nota de Urgência: {alt['prioridade_nota']})")

    # A raiz do Max-Heap é sempre o alerta de maior nota: consulta direta em O(1)
    raiz = heap_alertas.consultar_mais_urgente()
    print(f"\nRaiz do heap (consulta O(1)): [{raiz['id_alerta']}] {raiz['unidade']} - nota {raiz['prioridade_nota']}")
    print("Ordem interna da lista do heap:", [a['id_alerta'] for a in heap_alertas.heap])

    print("\n--- FILA DE ATENDIMENTO DE ALERTAS (Extração Ordenada por Urgência) ---")
    
    # Extrai iterativamente da heap os alertas em ordem decrescente de urgência
    while len(heap_alertas.heap) > 0:
        urgente = heap_alertas.extrair_mais_urgente()
        print(f" [ALERTA ATENDIDO] ID: {urgente['id_alerta']} | Unidade: {urgente['unidade']} | Nível: {urgente['nivel']} | Situação: {urgente['situacao']}")