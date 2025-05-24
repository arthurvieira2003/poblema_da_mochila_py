"""
Exemplo de uso da versão refatorada do problema da mochila.

Este script demonstra como usar a versão refatorada dos algoritmos
bio-inspirados, mostrando as melhorias em estrutura, legibilidade
e facilidade de uso.
"""

import pandas as pd
from knapsack.core.data_generator import DataGenerator, GenerationConfig
from knapsack.core.evaluator import KnapsackEvaluator
from knapsack.algorithms.genetic import GeneticAlgorithm, create_genetic_algorithm
from knapsack.config.algorithm_configs import ConfigFactory
from knapsack.utils.constants import TestConstants


def demonstrar_uso_basico():
    """Demonstra o uso básico da versão refatorada."""
    print("=== Demonstração de Uso Básico ===\n")
    
    # 1. Criar um problema da mochila
    generator = DataGenerator(seed=42)
    config = GenerationConfig(num_items=10, max_weight=10, max_value=20)
    problem = generator.generate_random_instance(config)
    
    print(f"Problema criado:")
    print(f"  - Itens: {problem.num_items}")
    print(f"  - Capacidade: {problem.capacity}")
    print(f"  - Peso total: {problem.total_weight}")
    print(f"  - Valor total: {problem.total_value}")
    print()
    
    # 2. Criar e configurar algoritmo genético
    genetic_config = ConfigFactory.create_genetic_config(problem.num_items)
    evaluator = KnapsackEvaluator(penalty_strategy="linear")
    algorithm = GeneticAlgorithm(genetic_config, evaluator, generator)
    
    print(f"Algoritmo configurado:")
    print(f"  - População: {genetic_config.population_size}")
    print(f"  - Gerações: {genetic_config.generations}")
    print(f"  - Taxa de mutação: {genetic_config.mutation_rate}")
    print()
    
    # 3. Resolver o problema
    print("Executando algoritmo...")
    result = algorithm.solve(problem)
    
    # 4. Exibir resultados
    print(f"\nResultados:")
    print(f"  - Melhor valor: {result.best_solution.total_value}")
    print(f"  - Peso usado: {result.best_solution.total_weight}/{problem.capacity}")
    print(f"  - Solução viável: {result.best_solution.is_feasible}")
    print(f"  - Tempo de execução: {result.execution_time:.4f}s")
    print(f"  - Gerações executadas: {result.iterations_completed}")
    print(f"  - Itens selecionados: {result.best_solution.selected_items}")
    print()


def comparar_com_versao_original():
    """Compara a versão refatorada com a original (OTIMIZADO)."""
    print("=== Comparação com Versão Original (Otimizado) ===\n")
    
    # Usar os mesmos tamanhos de teste da versão original
    generator = DataGenerator(seed=42)
    results = []
    
    for size in TestConstants.DEFAULT_TEST_SIZES:
        print(f"Testando com {size} itens...")
        
        # Gerar problema
        config = GenerationConfig(num_items=size, seed=42 + size)
        problem = generator.generate_random_instance(config)
        
        # Criar algoritmo adaptado ao tamanho
        algorithm = create_genetic_algorithm(size, adaptive=False)
        
        # OTIMIZAÇÃO: Reduzir drasticamente as iterações para problemas grandes
        if size <= 50:
            max_iterations = None  # Usar padrão
        elif size <= 1000:
            max_iterations = 50    # Reduzir para 50
        else:  # 10000 itens
            max_iterations = 20    # Muito reduzido para execução rápida
            print(f"  ⚡ Usando apenas {max_iterations} iterações para execução rápida")
        
        # Resolver
        result = algorithm.solve(problem, max_iterations=max_iterations)
        
        # Armazenar resultado
        results.append(result.summary)
        
        print(f"  - Valor: {result.best_solution.total_value}")
        print(f"  - Tempo: {result.execution_time:.5f}s")
        print(f"  - Viável: {result.best_solution.is_feasible}")
        print(f"  - Iterações: {result.iterations_completed}")
        print()
    
    # Criar DataFrame para comparação
    df = pd.DataFrame(results)
    print("Resumo dos resultados:")
    print(df[['n_itens', 'valor_total', 'tempo_execucao', 'viavel', 'iteracoes']].to_string(index=False))
    print()


def demonstrar_flexibilidade():
    """Demonstra a flexibilidade da versão refatorada."""
    print("=== Demonstração de Flexibilidade ===\n")
    
    # Criar problema
    generator = DataGenerator(seed=42)
    config = GenerationConfig(num_items=20)
    problem = generator.generate_random_instance(config)
    
    # Testar diferentes estratégias de avaliação
    strategies = [
        ("Linear", KnapsackEvaluator("linear")),
        ("Quadrática", KnapsackEvaluator("quadratic")),
        ("Zero", KnapsackEvaluator("zero"))
    ]
    
    genetic_config = ConfigFactory.create_genetic_config(problem.num_items)
    
    print("Comparando estratégias de penalização:")
    for name, evaluator in strategies:
        algorithm = GeneticAlgorithm(genetic_config, evaluator, generator)
        result = algorithm.solve(problem, max_iterations=50)
        
        print(f"  {name:12}: Valor={result.best_solution.total_value:3d}, "
              f"Viável={str(result.best_solution.is_feasible):5}, "
              f"Tempo={result.execution_time:.4f}s")
    
    print()
    
    # Testar algoritmo adaptativo vs normal
    print("Comparando algoritmo normal vs adaptativo:")
    
    normal_alg = create_genetic_algorithm(problem.num_items, adaptive=False)
    adaptive_alg = create_genetic_algorithm(problem.num_items, adaptive=True)
    
    normal_result = normal_alg.solve(problem, max_iterations=100)
    adaptive_result = adaptive_alg.solve(problem, max_iterations=100)
    
    print(f"  Normal    : Valor={normal_result.best_solution.total_value:3d}, "
          f"Tempo={normal_result.execution_time:.4f}s")
    print(f"  Adaptativo: Valor={adaptive_result.best_solution.total_value:3d}, "
          f"Tempo={adaptive_result.execution_time:.4f}s")
    print()


def demonstrar_metricas_detalhadas():
    """Demonstra as métricas detalhadas disponíveis."""
    print("=== Métricas Detalhadas ===\n")
    
    # Criar problema e algoritmo
    generator = DataGenerator(seed=42)
    config = GenerationConfig(num_items=15)
    problem = generator.generate_random_instance(config)
    
    algorithm = create_genetic_algorithm(problem.num_items, adaptive=True)
    result = algorithm.solve(problem, max_iterations=50)
    
    print("Métricas da execução:")
    for key, value in result.additional_metrics.items():
        if isinstance(value, float):
            print(f"  {key:20}: {value:.4f}")
        else:
            print(f"  {key:20}: {value}")
    
    print()
    print("Resumo completo:")
    summary = result.summary
    for key, value in summary.items():
        print(f"  {key:20}: {value}")
    print()


def main():
    """Função principal demonstrando todas as funcionalidades."""
    print("Demonstração da Versão Refatorada do Problema da Mochila")
    print("=" * 60)
    print("(Versão otimizada - teste com 10.000 itens usa apenas 20 iterações)")
    print()
    
    try:
        demonstrar_uso_basico()
        comparar_com_versao_original()
        demonstrar_flexibilidade()
        demonstrar_metricas_detalhadas()
        
        print("=== Vantagens da Refatoração ===")
        print("✓ Código mais limpo e organizado")
        print("✓ Separação clara de responsabilidades")
        print("✓ Facilidade para adicionar novos algoritmos")
        print("✓ Configuração flexível e validada")
        print("✓ Testes automatizados")
        print("✓ Métricas detalhadas")
        print("✓ Reutilização de componentes")
        print("✓ Melhor manutenibilidade")
        print("✓ Performance configurável")
        
        print(f"\n💡 Para execução ainda mais rápida, use: python exemplo_refatorado_rapido.py")
        
    except Exception as e:
        print(f"Erro durante execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 