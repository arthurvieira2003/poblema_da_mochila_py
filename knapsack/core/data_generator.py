"""
Gerador de dados para instâncias do problema da mochila.

Este módulo implementa a geração de instâncias do problema da mochila,
aplicando a técnica "Extract Class" de Martin Fowler para centralizar
a lógica de geração que estava duplicada em todos os algoritmos.
"""

import random
from typing import List, Tuple, Optional
from dataclasses import dataclass
from .problem import KnapsackProblem, KnapsackSolution
from ..utils.constants import DataGenerationConstants, TestConstants


@dataclass
class GenerationConfig:
    """Configuração para geração de instâncias."""
    
    num_items: int
    max_weight: int = DataGenerationConstants.DEFAULT_MAX_WEIGHT
    max_value: int = DataGenerationConstants.DEFAULT_MAX_VALUE
    min_capacity_ratio: float = DataGenerationConstants.MIN_CAPACITY_RATIO
    max_capacity_ratio: float = DataGenerationConstants.MAX_CAPACITY_RATIO
    seed: Optional[int] = None
    
    def __post_init__(self):
        """Valida a configuração."""
        if self.num_items <= 0:
            raise ValueError("Número de itens deve ser positivo")
        if self.max_weight <= 0:
            raise ValueError("Peso máximo deve ser positivo")
        if self.max_value <= 0:
            raise ValueError("Valor máximo deve ser positivo")
        if not 0 < self.min_capacity_ratio < self.max_capacity_ratio < 1:
            raise ValueError("Ratios de capacidade devem estar entre 0 e 1, com min < max")


class DataGenerator:
    """
    Gerador de instâncias do problema da mochila.
    
    Esta classe centraliza toda a lógica de geração de dados que estava
    duplicada nos algoritmos originais, fornecendo métodos consistentes
    para criar instâncias de teste.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa o gerador de dados.
        
        Args:
            seed: Semente para reprodutibilidade (opcional)
        """
        self._seed = seed
        if seed is not None:
            random.seed(seed)
    
    def generate_random_instance(self, config: GenerationConfig) -> KnapsackProblem:
        """
        Gera uma instância aleatória do problema da mochila.
        
        Args:
            config: Configuração para geração
            
        Returns:
            Instância do problema da mochila
        """
        if config.seed is not None:
            random.seed(config.seed)
        
        # Gerar pesos e valores aleatórios
        weights = [
            random.randint(1, config.max_weight) 
            for _ in range(config.num_items)
        ]
        
        values = [
            random.randint(1, config.max_value) 
            for _ in range(config.num_items)
        ]
        
        # Calcular capacidade baseada no peso total
        total_weight = sum(weights)
        min_capacity = int(total_weight * config.min_capacity_ratio)
        max_capacity = int(total_weight * config.max_capacity_ratio)
        
        capacity = random.randint(min_capacity, max_capacity)
        
        return KnapsackProblem(weights, values, capacity)
    
    def generate_correlated_instance(self, config: GenerationConfig, 
                                   correlation: float = 0.8) -> KnapsackProblem:
        """
        Gera uma instância com correlação entre peso e valor.
        
        Args:
            config: Configuração para geração
            correlation: Correlação entre peso e valor (0-1)
            
        Returns:
            Instância do problema da mochila
        """
        if not 0 <= correlation <= 1:
            raise ValueError("Correlação deve estar entre 0 e 1")
        
        if config.seed is not None:
            random.seed(config.seed)
        
        weights = [
            random.randint(1, config.max_weight) 
            for _ in range(config.num_items)
        ]
        
        values = []
        for weight in weights:
            if random.random() < correlation:
                # Valor correlacionado com o peso
                base_value = int(weight * config.max_value / config.max_weight)
                noise = random.randint(-base_value // 4, base_value // 4)
                value = max(1, base_value + noise)
            else:
                # Valor aleatório
                value = random.randint(1, config.max_value)
            values.append(value)
        
        # Calcular capacidade
        total_weight = sum(weights)
        min_capacity = int(total_weight * config.min_capacity_ratio)
        max_capacity = int(total_weight * config.max_capacity_ratio)
        capacity = random.randint(min_capacity, max_capacity)
        
        return KnapsackProblem(weights, values, capacity)
    
    def generate_uncorrelated_instance(self, config: GenerationConfig) -> KnapsackProblem:
        """
        Gera uma instância sem correlação entre peso e valor.
        
        Args:
            config: Configuração para geração
            
        Returns:
            Instância do problema da mochila
        """
        return self.generate_correlated_instance(config, correlation=0.0)
    
    def generate_test_instances(self) -> List[KnapsackProblem]:
        """
        Gera instâncias padrão para testes.
        
        Returns:
            Lista de instâncias de teste
        """
        instances = []
        
        for size in TestConstants.DEFAULT_TEST_SIZES:
            config = GenerationConfig(
                num_items=size,
                seed=42 + size  # Semente determinística para reprodutibilidade
            )
            instance = self.generate_random_instance(config)
            instances.append(instance)
        
        return instances
    
    def generate_benchmark_instances(self, sizes: List[int], 
                                   instances_per_size: int = 5) -> List[KnapsackProblem]:
        """
        Gera instâncias para benchmark.
        
        Args:
            sizes: Lista de tamanhos de instâncias
            instances_per_size: Número de instâncias por tamanho
            
        Returns:
            Lista de instâncias para benchmark
        """
        instances = []
        
        for size in sizes:
            for i in range(instances_per_size):
                config = GenerationConfig(
                    num_items=size,
                    seed=42 + size * 1000 + i  # Semente única para cada instância
                )
                instance = self.generate_random_instance(config)
                instances.append(instance)
        
        return instances
    
    def generate_random_solution(self, problem: KnapsackProblem) -> KnapsackSolution:
        """
        Gera uma solução aleatória para um problema.
        
        Args:
            problem: Problema da mochila
            
        Returns:
            Solução aleatória
        """
        binary_solution = [
            random.randint(0, 1) 
            for _ in range(problem.num_items)
        ]
        
        return KnapsackSolution(binary_solution, problem)
    
    def generate_greedy_solution(self, problem: KnapsackProblem) -> KnapsackSolution:
        """
        Gera uma solução gulosa baseada na relação valor/peso.
        
        Args:
            problem: Problema da mochila
            
        Returns:
            Solução gulosa
        """
        # Criar lista de itens com seus índices e ratios
        items_with_ratio = [
            (i, problem.values[i] / problem.weights[i])
            for i in range(problem.num_items)
        ]
        
        # Ordenar por ratio decrescente
        items_with_ratio.sort(key=lambda x: x[1], reverse=True)
        
        # Construir solução gulosa
        binary_solution = [0] * problem.num_items
        current_weight = 0
        
        for item_index, _ in items_with_ratio:
            if current_weight + problem.weights[item_index] <= problem.capacity:
                binary_solution[item_index] = 1
                current_weight += problem.weights[item_index]
        
        return KnapsackSolution(binary_solution, problem)
    
    def generate_population(self, problem: KnapsackProblem, 
                          population_size: int) -> List[KnapsackSolution]:
        """
        Gera uma população de soluções aleatórias.
        
        Args:
            problem: Problema da mochila
            population_size: Tamanho da população
            
        Returns:
            Lista de soluções aleatórias
        """
        return [
            self.generate_random_solution(problem) 
            for _ in range(population_size)
        ]


class SpecializedDataGenerator(DataGenerator):
    """
    Gerador especializado para casos específicos.
    
    Esta classe estende o gerador básico para criar instâncias
    com características específicas para testes especializados.
    """
    
    def generate_hard_instance(self, num_items: int) -> KnapsackProblem:
        """
        Gera uma instância difícil (alta correlação peso-valor).
        
        Args:
            num_items: Número de itens
            
        Returns:
            Instância difícil do problema
        """
        config = GenerationConfig(
            num_items=num_items,
            max_weight=100,
            max_value=100,
            min_capacity_ratio=0.45,
            max_capacity_ratio=0.55
        )
        
        return self.generate_correlated_instance(config, correlation=0.95)
    
    def generate_easy_instance(self, num_items: int) -> KnapsackProblem:
        """
        Gera uma instância fácil (baixa correlação peso-valor).
        
        Args:
            num_items: Número de itens
            
        Returns:
            Instância fácil do problema
        """
        config = GenerationConfig(
            num_items=num_items,
            max_weight=10,
            max_value=50,
            min_capacity_ratio=0.2,
            max_capacity_ratio=0.8
        )
        
        return self.generate_uncorrelated_instance(config)
    
    def generate_known_optimal_instance(self) -> Tuple[KnapsackProblem, KnapsackSolution]:
        """
        Gera uma instância pequena com solução ótima conhecida.
        
        Returns:
            Tupla (problema, solução_ótima)
        """
        # Instância simples com solução ótima conhecida
        weights = [2, 3, 4, 5, 1]
        values = [3, 4, 5, 6, 2]
        capacity = 5
        
        problem = KnapsackProblem(weights, values, capacity)
        
        # Solução ótima: itens 0 e 4 (peso=3, valor=5)
        optimal_solution = KnapsackSolution([1, 0, 0, 0, 1], problem)
        
        return problem, optimal_solution 