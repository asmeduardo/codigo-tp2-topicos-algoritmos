# PCVPB: GRASP + Tabu

Este projeto implementa uma abordagem híbrida para resolver o **Problema do Caixeiro Viajante Branco e Preto (PCVPB)**, uma variação NP-difícil do TSP clássico, com restrições de cardinalidade e limite de distância. Os vértices são classificados como centros de distribuição (P) e clientes (B), e o objetivo é construir rotas viáveis de menor custo.

## Base Teórica
Este trabalho foi fundamentado nos conceitos e metodologias apresentadas no artigo:

MACIEL, A. C. M.; MARTINHON, C. A.; OCHI, L. S. Heurísticas e Metaheurísticas para o Problema do Caixeiro Viajante Branco e Preto. In: **Pesquisa Operacional e o Desenvolvimento Sustentável**, Gramado, RS, 27 a 30 de setembro de 2005, p. 1349-1360.

O artigo de referência aborda técnicas de otimização para problemas com restrições de cardinalidade e comprimento, fornecendo a base teórica para as implementações das metaheurísticas GRASP e Busca Tabu utilizadas neste projeto.

## Metodologia

A solução combina:

* **GRASP (Greedy Randomized Adaptive Search Procedure)**: para gerar soluções iniciais diversificadas.
* **Busca Tabu**: para intensificação e refinamento local.

Cada solução é validada quanto às restrições de:

* Até `Q = 4` clientes por rota;
* Máximo de `L = 100` unidades de distância por segmento.

## Execução

O script principal executa:

1. Múltiplas construções GRASP para encontrar a melhor solução inicial viável;
2. Busca Tabu para melhorar essa solução.

A saída inclui a rota, custo total e indicação de viabilidade.

## Requisitos

* Python 3.x
* Bibliotecas: `collections`, `random`

## Como usar

Execute o script diretamente:

```bash
python nome_do_arquivo.py
```

Os parâmetros podem ser ajustados nas variáveis:

* `ITERACOES_GRASP`
* `ALPHA`
* `ITERACOES_TABU`
* `TAMANHO_LISTA_TABU`

## Resultados

O código imprime:

* A melhor solução inicial viável encontrada pelo GRASP;
* A melhor solução final após a Busca Tabu;
* O ganho percentual em relação à solução inicial.
