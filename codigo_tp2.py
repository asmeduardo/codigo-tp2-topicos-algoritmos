import random
import collections

pontos = [
    (0, 0), (300, 200), (100, 300), (400, 100), (200, 400),
    (50, 50), (80, 30), (120, 60), (150, 100), (200, 150),
    (250, 180), (350, 120), (380, 180), (180, 250), (220, 280),
    (60, 280), (140, 320)
]

tipos = ['P', 'P', 'P', 'P', 'P', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']

distancias = [
    [0, 32, 28, 37, 40, 8, 10, 12, 16, 22, 26, 35, 39, 26, 30, 26, 30],
    [32, 0, 20, 9, 20, 28, 26, 24, 20, 16, 6, 5, 7, 9, 10, 22, 18],
    [20, 20, 0, 28, 12, 10, 24, 21, 18, 14, 16, 25, 28, 7, 11, 20, 5],
    [37, 9, 28, 0, 25, 33, 31, 28, 25, 20, 14, 5, 4, 18, 19, 32, 28],
    [40, 20, 12, 25, 0, 22, 30, 28, 25, 20, 20, 20, 25, 4, 3, 20, 12],
    [8, 28, 10, 33, 22, 0, 3, 7, 10, 14, 20, 30, 33, 18, 22, 22, 25],
    [10, 26, 24, 31, 30, 3, 0, 5, 7, 12, 18, 27, 31, 22, 25, 28, 28],
    [12, 24, 21, 28, 28, 7, 5, 0, 4, 9, 14, 22, 26, 18, 20, 25, 24],
    [16, 20, 18, 25, 25, 10, 7, 4, 0, 6, 10, 18, 22, 14, 16, 22, 20],
    [22, 16, 14, 20, 20, 14, 12, 9, 6, 0, 6, 14, 16, 7, 9, 18, 12],
    [26, 6, 16, 14, 20, 20, 18, 14, 10, 6, 0, 10, 12, 9, 9, 20, 16],
    [35, 5, 25, 5, 20, 30, 27, 22, 18, 14, 10, 0, 3, 12, 14, 28, 20],
    [39, 7, 28, 4, 25, 33, 31, 26, 22, 16, 12, 3, 0, 16, 18, 32, 24],
    [26, 9, 7, 18, 4, 18, 22, 18, 14, 7, 9, 12, 16, 0, 4, 12, 9],
    [30, 10, 11, 19, 3, 22, 25, 20, 16, 9, 9, 14, 18, 4, 0, 16, 10],
    [26, 22, 20, 32, 20, 22, 28, 25, 22, 18, 20, 28, 32, 12, 16, 0, 20],
    [30, 18, 5, 28, 12, 25, 28, 24, 20, 12, 16, 20, 24, 9, 10, 20, 0]
]

Q = 4
L = 100

def calcular_custo_e_validar(solucao):
    custo_total = 0
    for i in range(len(solucao) - 1):
        ponto_atual = solucao[i]
        proximo_ponto = solucao[i+1]
        custo_total += distancias[ponto_atual][proximo_ponto]

    segmentos = []
    inicio_segmento = 0
    for i in range(1, len(solucao)):
        if tipos[solucao[i]] == 'P':
            segmentos.append(solucao[inicio_segmento : i + 1])
            inicio_segmento = i

    for seg in segmentos:
        clientes_no_segmento = sum(1 for ponto_idx in seg[1:-1] if tipos[ponto_idx] == 'B')
        if clientes_no_segmento == 0: return float('inf')
        if clientes_no_segmento > Q: return float('inf')
        dist_segmento = sum(distancias[seg[i]][seg[i+1]] for i in range(len(seg)-1))
        if dist_segmento > L: return float('inf')

    return custo_total

def imprimir_solucao(titulo, solucao, custo):
    nomes = [f'C{chr(65+i)}' if t == 'P' else f'Cli{i-4}' for i, t in enumerate(tipos)]
    print(f"\n--- {titulo} ---")
    print(f"Custo Total: {custo:.2f} km")
    print(f"Viável: {'Sim' if custo != float('inf') else 'Não'}")
    print(f"Rota: {' → '.join(nomes[i] for i in solucao)}")

def construcao_grasp(alpha):
    solucao = [0]
    pontos_a_visitar = list(range(1, len(pontos)))

    while pontos_a_visitar:
        ultimo_ponto = solucao[-1]
        candidatos = []
        
        for ponto in pontos_a_visitar:
            custo = distancias[ultimo_ponto][ponto]
            candidatos.append({'ponto': ponto, 'custo': custo})
        
        candidatos.sort(key=lambda x: x['custo'])
        
        custo_minimo = candidatos[0]['custo']
        custo_maximo = candidatos[-1]['custo']
        limite_custo = custo_minimo + alpha * (custo_maximo - custo_minimo)
        
        lcr = [c for c in candidatos if c['custo'] <= limite_custo]
        
        escolhido = random.choice(lcr)
        solucao.append(escolhido['ponto'])
        pontos_a_visitar.remove(escolhido['ponto'])
        
    solucao.append(0)
    return solucao

def busca_tabu(solucao_inicial, max_iteracoes, tamanho_lista_tabu):
    lista_tabu = collections.deque(maxlen=tamanho_lista_tabu)
    
    melhor_solucao_global = solucao_inicial[:]
    custo_melhor_global = calcular_custo_e_validar(melhor_solucao_global)
    
    solucao_atual = solucao_inicial[:]
    custo_atual = custo_melhor_global
    
    for i in range(max_iteracoes):
        melhor_vizinho = None
        melhor_custo_vizinho = float('inf')
        melhor_movimento = None

        for j in range(1, len(solucao_atual) - 3):
            for k in range(j + 2, len(solucao_atual) - 1):
                vizinho = solucao_atual[:]
                segmento_invertido = list(reversed(vizinho[j:k]))
                vizinho[j:k] = segmento_invertido
                
                movimento = tuple(sorted((j, k)))
                custo_vizinho = calcular_custo_e_validar(vizinho)

                criterio_aspiracao = (movimento in lista_tabu) and (custo_vizinho < custo_melhor_global)
                
                if (movimento not in lista_tabu) or criterio_aspiracao:
                    if custo_vizinho < melhor_custo_vizinho:
                        melhor_vizinho = vizinho
                        melhor_custo_vizinho = custo_vizinho
                        melhor_movimento = movimento
        
        if melhor_vizinho:
            solucao_atual = melhor_vizinho
            custo_atual = melhor_custo_vizinho
            
            lista_tabu.append(melhor_movimento)
            
            if custo_atual < custo_melhor_global:
                melhor_solucao_global = solucao_atual
                custo_melhor_global = custo_atual

    return melhor_solucao_global, custo_melhor_global

def executar_grasp_com_busca_tabu(iteracoes_grasp, alpha, iteracoes_tabu, tamanho_lista_tabu):
    print("Executando fase de construção GRASP para encontrar a melhor solução inicial...")
    melhor_solucao_inicial = None
    custo_melhor_inicial = float('inf')

    for i in range(iteracoes_grasp):
        solucao_candidata = None
        custo_candidato = float('inf')
        tentativas = 0
        
        while custo_candidato == float('inf') and tentativas < 100:
            solucao_gerada = construcao_grasp(alpha)
            custo_gerado = calcular_custo_e_validar(solucao_gerada)
            if custo_gerado != float('inf'):
                solucao_candidata = solucao_gerada
                custo_candidato = custo_gerado
            tentativas += 1
        
        if custo_candidato < custo_melhor_inicial:
            custo_melhor_inicial = custo_candidato
            melhor_solucao_inicial = solucao_candidata

    if melhor_solucao_inicial is None:
        return None, float('inf'), None

    imprimir_solucao("MELHOR SOLUÇÃO INICIAL (APÓS GRASP)", melhor_solucao_inicial, custo_melhor_inicial)

    print("\nIniciando Busca Tabu na melhor solução inicial...")
    solucao_final, custo_final = busca_tabu(melhor_solucao_inicial, iteracoes_tabu, tamanho_lista_tabu)
    
    return solucao_final, custo_final, custo_melhor_inicial

if __name__ == "__main__":
    ITERACOES_GRASP = 10
    ALPHA = 0.3
    ITERACOES_TABU = 100
    TAMANHO_LISTA_TABU = 7

    print("=== INICIANDO OTIMIZAÇÃO COM GRASP + BUSCA TABU ===")
    
    solucao_final, custo_final, custo_inicial = executar_grasp_com_busca_tabu(
        iteracoes_grasp=ITERACOES_GRASP,
        alpha=ALPHA,
        iteracoes_tabu=ITERACOES_TABU,
        tamanho_lista_tabu=TAMANHO_LISTA_TABU
    )
    
    if solucao_final:
        imprimir_solucao("MELHOR SOLUÇÃO FINAL ENCONTRADA", solucao_final, custo_final)
        
        print("\n--- RESUMO DA OTIMIZAÇÃO ---")
        if custo_inicial:
             print(f"Custo da Melhor Solução Inicial: {custo_inicial:.2f} km")
        print(f"Custo da Melhor Solução Final:   {custo_final:.2f} km")
        if custo_inicial:
            melhoria = custo_inicial - custo_final
            percentual = (melhoria / custo_inicial) * 100
            print(f"Melhoria Total:                  {melhoria:.2f} km ({percentual:.2f}%)")
    else:
        print("\nNão foi possível encontrar uma solução viável em nenhuma iteração.")
