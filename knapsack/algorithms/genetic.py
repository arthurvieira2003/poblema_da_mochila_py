"""
Algoritmo Genético refatorado para o problema da mochila.

Este módulo implementa uma versão refatorada do algoritmo genético original,
aplicando múltiplas técnicas de Martin Fowler para melhorar a estrutura,
legibilidade e manutenibilidade do código.
"""

import random
from typing import List, Tuple
from ..core.problem import KnapsackProblem, KnapsackSolution
from ..core.evaluator import KnapsackEvaluator
from ..core.data_generator import DataGenerator
from ..config.algorithm_configs import GeneticAlgorithmConfig, ConfigFactory
from ..utils.constants import AlgorithmNames
from .base import PopulationBasedAlgorithm


class GeneticAlgorithm(PopulationBasedAlgorithm):
    """
    Algoritmo Genético refatorado para o problema da mochila.
    
    Esta implementação aplica as seguintes técnicas de refatoração:
    - Extract Method: Métodos pequenos e focados
    - Replace Parameter with Object: Uso de GeneticAlgorithmConfig
    - Extract Class: Separação de responsabilidades
    - Replace Magic Number with Named Constant: Uso de constantes
    """
    
    def __init__(self, config: GeneticAlgorithmConfig, 
                 evaluator: KnapsackEvaluator = None,
                 data_generator: DataGenerator = None):
        """
        Inicializa o Algoritmo Genético.
        
        Args:
            config: Configuração do algoritmo
            evaluator: Avaliador de soluções
            data_generator: Gerador de dados
        """
        super().__init__(
            population_size=config.population_size,
            evaluator=evaluator,
            name=AlgorithmNames.GENETIC
        )
        
        self._config = config
        self._data_generator = data_generator or DataGenerator()
        self._generation = 0
    
    def _get_default_max_iterations(self) -> int:
        """Retorna o número padrão de gerações."""
        return self._config.generations
    
    def _initialize_population(self, problem: KnapsackProblem) -> List[KnapsackSolution]:
        """
        Inicializa a população com soluções aleatórias.
        
        Args:
            problem: Problema da mochila
            
        Returns:
            População inicial
        """
        return self._data_generator.generate_population(
            problem, 
            self._config.population_size
        )
    
    def _iterate(self) -> bool:
        """
        Executa uma geração do algoritmo genético.
        
        Returns:
            True para continuar, False para parar
        """
        self._generation += 1
        
        # Criar nova população
        new_population = []
        
        # Aplicar elitismo se configurado
        if self._config.elitism:
            elite = self._select_elite()
            new_population.extend(elite)
        
        # Gerar resto da população através de reprodução
        while len(new_population) < self._config.population_size:
            offspring = self._reproduce()
            new_population.extend(offspring)
        
        # Truncar para o tamanho correto
        self._population = new_population[:self._config.population_size]
        
        return self._generation < self._config.generations
    
    def _select_elite(self) -> List[KnapsackSolution]:
        """
        Seleciona os melhores indivíduos para elitismo.
        
        Returns:
            Lista dos melhores indivíduos
        """
        ranked_solutions = self._evaluator.rank_solutions(self._population)
        elite_size = min(self._config.elitism_size, len(self._population))
        
        return [solution for solution, _ in ranked_solutions[:elite_size]]
    
    def _reproduce(self) -> List[KnapsackSolution]:
        """
        Executa um ciclo de reprodução (seleção, crossover, mutação).
        
        Returns:
            Lista de descendentes
        """
        # Seleção de pais
        parent1 = self._tournament_selection()
        parent2 = self._tournament_selection()
        
        # Crossover
        if random.random() < self._config.crossover_rate:
            offspring1, offspring2 = self._crossover(parent1, parent2)
        else:
            offspring1, offspring2 = parent1.copy(), parent2.copy()
        
        # Mutação
        offspring1 = self._mutate(offspring1)
        offspring2 = self._mutate(offspring2)
        
        return [offspring1, offspring2]
    
    def _tournament_selection(self) -> KnapsackSolution:
        """
        Seleciona um indivíduo através de seleção por torneio.
        
        Returns:
            Indivíduo selecionado
        """
        tournament_size = min(self._config.tournament_size, len(self._population))
        tournament = random.sample(self._population, tournament_size)
        
        return self._evaluator.get_best_solution(tournament)
    
    def _crossover(self, parent1: KnapsackSolution, 
                   parent2: KnapsackSolution) -> Tuple[KnapsackSolution, KnapsackSolution]:
        """
        Executa crossover de um ponto entre dois pais.
        
        Args:
            parent1: Primeiro pai
            parent2: Segundo pai
            
        Returns:
            Tupla com dois descendentes
        """
        solution1 = parent1.binary_solution
        solution2 = parent2.binary_solution
        
        # Escolher ponto de crossover
        crossover_point = random.randint(1, len(solution1) - 1)
        
        # Criar descendentes
        offspring1_binary = solution1[:crossover_point] + solution2[crossover_point:]
        offspring2_binary = solution2[:crossover_point] + solution1[crossover_point:]
        
        offspring1 = self._create_solution(offspring1_binary)
        offspring2 = self._create_solution(offspring2_binary)
        
        return offspring1, offspring2
    
    def _mutate(self, individual: KnapsackSolution) -> KnapsackSolution:
        """
        Aplica mutação bit-flip em um indivíduo.
        
        Args:
            individual: Indivíduo a ser mutado
            
        Returns:
            Indivíduo mutado
        """
        binary_solution = individual.binary_solution
        
        for i in range(len(binary_solution)):
            if random.random() < self._config.mutation_rate:
                binary_solution[i] = 1 - binary_solution[i]
        
        return self._create_solution(binary_solution)
    
    def _get_additional_metrics(self) -> dict:
        """Retorna métricas específicas do algoritmo genético."""
        base_metrics = super()._get_additional_metrics()
        
        genetic_metrics = {
            "generation": self._generation,
            "mutation_rate": self._config.mutation_rate,
            "crossover_rate": self._config.crossover_rate,
            "tournament_size": self._config.tournament_size,
            "elitism": self._config.elitism
        }
        
        return {**base_metrics, **genetic_metrics}


class AdaptiveGeneticAlgorithm(GeneticAlgorithm):
    """
    Versão adaptativa do Algoritmo Genético.
    
    Esta classe estende o algoritmo básico com capacidades adaptativas,
    como ajuste automático da taxa de mutação baseado na diversidade
    da população.
    """
    
    def __init__(self, config: GeneticAlgorithmConfig,
                 evaluator: KnapsackEvaluator = None,
                 data_generator: DataGenerator = None,
                 adaptation_rate: float = 0.1):
        """
        Inicializa o Algoritmo Genético Adaptativo.
        
        Args:
            config: Configuração do algoritmo
            evaluator: Avaliador de soluções
            data_generator: Gerador de dados
            adaptation_rate: Taxa de adaptação dos parâmetros
        """
        super().__init__(config, evaluator, data_generator)
        self._adaptation_rate = adaptation_rate
        self._initial_mutation_rate = config.mutation_rate
        self._diversity_history = []
    
    def _iterate(self) -> bool:
        """Executa uma geração com adaptação de parâmetros."""
        # Calcular diversidade atual
        diversity = self._calculate_population_diversity()
        self._diversity_history.append(diversity)
        
        # Adaptar taxa de mutação
        self._adapt_mutation_rate(diversity)
        
        # Executar geração normal
        return super()._iterate()
    
    def _calculate_population_diversity(self) -> float:
        """
        Calcula a diversidade da população.
        
        Returns:
            Valor de diversidade (0-1)
        """
        if len(self._population) < 2:
            return 1.0
        
        total_differences = 0
        comparisons = 0
        
        for i in range(len(self._population)):
            for j in range(i + 1, len(self._population)):
                sol1 = self._population[i].binary_solution
                sol2 = self._population[j].binary_solution
                
                differences = sum(1 for a, b in zip(sol1, sol2) if a != b)
                total_differences += differences
                comparisons += 1
        
        if comparisons == 0:
            return 1.0
        
        max_possible_differences = len(self._population[0].binary_solution)
        average_differences = total_differences / comparisons
        
        return average_differences / max_possible_differences
    
    def _adapt_mutation_rate(self, diversity: float):
        """
        Adapta a taxa de mutação baseada na diversidade.
        
        Args:
            diversity: Diversidade atual da população
        """
        # Se diversidade é baixa, aumentar mutação
        # Se diversidade é alta, diminuir mutação
        target_diversity = 0.5
        diversity_error = target_diversity - diversity
        
        adjustment = diversity_error * self._adaptation_rate
        new_rate = self._config.mutation_rate + adjustment
        
        # Manter dentro de limites razoáveis
        self._config.mutation_rate = max(0.01, min(0.5, new_rate))
    
    def _get_additional_metrics(self) -> dict:
        """Retorna métricas incluindo adaptação."""
        base_metrics = super()._get_additional_metrics()
        
        adaptive_metrics = {
            "current_diversity": self._diversity_history[-1] if self._diversity_history else 0,
            "adapted_mutation_rate": self._config.mutation_rate,
            "initial_mutation_rate": self._initial_mutation_rate
        }
        
        return {**base_metrics, **adaptive_metrics}


def create_genetic_algorithm(problem_size: int, 
                           adaptive: bool = False) -> GeneticAlgorithm:
    """
    Factory function para criar algoritmos genéticos.
    
    Args:
        problem_size: Tamanho do problema
        adaptive: Se deve usar versão adaptativa
        
    Returns:
        Instância do algoritmo genético
    """
    config = ConfigFactory.create_genetic_config(problem_size)
    
    if adaptive:
        return AdaptiveGeneticAlgorithm(config)
    else:
        return GeneticAlgorithm(config) 