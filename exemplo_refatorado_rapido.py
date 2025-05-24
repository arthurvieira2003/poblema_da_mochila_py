"""
Exemplo RÁPIDO da versão refatorada do problema da mochila.

Esta versão otimizada executa rapidamente para demonstração,
usando tamanhos menores e menos iterações.
"""

import pandas as pd
from knapsack.core.data_generator import DataGenerator, GenerationConfig
from knapsack.core.evaluator import KnapsackEvaluator
from knapsack.algorithms.genetic import GeneticAlgorithm, create_genetic_algorithm
from knapsack.config.algorithm_configs import ConfigFactory


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
    
    # 2. Criar e configurar algoritmo genético (versão rápida)
    genetic_config = ConfigFactory.create_genetic_config(problem.num_items)
    # Reduzir gerações para execução mais rápida
    genetic_config.generations = 30
    
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


def comparar_tamanhos_rapido():
    """Compara diferentes tamanhos com execução rápida."""
    print("=== Comparação de Tamanhos (Versão Rápida) ===\n")
    
    # Usar tamanhos menores para execução rápida
    tamanhos_rapidos = [5, 20, 50, 100]
    generator = DataGenerator(seed=42)
    results = []
    
    for size in tamanhos_rapidos:
        print(f"Testando com {size} itens...")
        
        # Gerar problema
        config = GenerationConfig(num_items=size, seed=42 + size)
        problem = generator.generate_random_instance(config)
        
        # Criar algoritmo com configuração rápida
        algorithm = create_genetic_algorithm(size, adaptive=False)
        
        # Reduzir iterações para execução mais rápida
        max_iterations = min(50, size)  # Máximo 50 iterações
        
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
    
    # Criar problema pequeno para execução rápida
    generator = DataGenerator(seed=42)
    config = GenerationConfig(num_items=15)
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
        result = algorithm.solve(problem, max_iterations=25)  # Reduzido para 25
        
        print(f"  {name:12}: Valor={result.best_solution.total_value:3d}, "
              f"Viável={str(result.best_solution.is_feasible):5}, "
              f"Tempo={result.execution_time:.4f}s")
    
    print()
    
    # Testar algoritmo adaptativo vs normal
    print("Comparando algoritmo normal vs adaptativo:")
    
    normal_alg = create_genetic_algorithm(problem.num_items, adaptive=False)
    adaptive_alg = create_genetic_algorithm(problem.num_items, adaptive=True)
    
    normal_result = normal_alg.solve(problem, max_iterations=30)  # Reduzido
    adaptive_result = adaptive_alg.solve(problem, max_iterations=30)  # Reduzido
    
    print(f"  Normal    : Valor={normal_result.best_solution.total_value:3d}, "
          f"Tempo={normal_result.execution_time:.4f}s")
    print(f"  Adaptativo: Valor={adaptive_result.best_solution.total_value:3d}, "
          f"Tempo={adaptive_result.execution_time:.4f}s")
    print()


def demonstrar_metricas_detalhadas():
    """Demonstra as métricas detalhadas disponíveis."""
    print("=== Métricas Detalhadas ===\n")
    
    # Criar problema pequeno
    generator = DataGenerator(seed=42)
    config = GenerationConfig(num_items=12)
    problem = generator.generate_random_instance(config)
    
    algorithm = create_genetic_algorithm(problem.num_items, adaptive=True)
    result = algorithm.solve(problem, max_iterations=25)  # Reduzido
    
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


def benchmark_rapido():
    """Executa um benchmark rápido para demonstrar performance."""
    print("=== Benchmark Rápido ===\n")
    
    generator = DataGenerator(seed=42)
    tamanhos = [10, 25, 50]
    
    print("Testando performance com diferentes tamanhos:")
    print(f"{'Tamanho':>8} {'Tempo (s)':>10} {'Valor':>8} {'Viável':>8}")
    print("-" * 40)
    
    for size in tamanhos:
        config = GenerationConfig(num_items=size, seed=42 + size)
        problem = generator.generate_random_instance(config)
        
        algorithm = create_genetic_algorithm(size, adaptive=False)
        result = algorithm.solve(problem, max_iterations=20)  # Muito reduzido
        
        print(f"{size:>8} {result.execution_time:>10.4f} {result.best_solution.total_value:>8} "
              f"{str(result.best_solution.is_feasible):>8}")
    
    print()


def main():
    """Função principal com execução rápida."""
    print("Demonstração RÁPIDA da Versão Refatorada do Problema da Mochila")
    print("=" * 70)
    print("(Versão otimizada para execução rápida)")
    print()
    
    try:
        demonstrar_uso_basico()
        comparar_tamanhos_rapido()
        demonstrar_flexibilidade()
        benchmark_rapido()
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
        
        print(f"\n💡 Para testes mais extensos, use: python exemplo_refatorado.py")
        print(f"💡 Para testes rápidos, use: python exemplo_refatorado_rapido.py")
        
    except Exception as e:
        print(f"Erro durante execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 