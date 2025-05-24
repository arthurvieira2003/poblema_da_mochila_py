"""
Avaliador de soluções para o problema da mochila.

Este módulo implementa diferentes estratégias de avaliação de soluções,
aplicando a técnica "Move Method" de Martin Fowler para centralizar
a lógica de avaliação que estava espalhada pelos algoritmos.
"""

from abc import ABC, abstractmethod
from typing import Protocol
from .problem import KnapsackProblem, KnapsackSolution
from ..utils.constants import AlgorithmConstants


class SolutionEvaluator(Protocol):
    """Protocol para avaliadores de solução."""
    
    def evaluate(self, solution: KnapsackSolution) -> float:
        """Avalia uma solução e retorna seu fitness."""
        ...


class KnapsackEvaluator:
    """
    Avaliador principal para soluções do problema da mochila.
    
    Esta classe centraliza toda a lógica de avaliação que estava duplicada
    nos algoritmos originais, aplicando diferentes estratégias de penalização
    para soluções inviáveis.
    """
    
    def __init__(self, penalty_strategy: str = "linear"):
        """
        Inicializa o avaliador.
        
        Args:
            penalty_strategy: Estratégia de penalização ("linear", "quadratic", "zero")
        """
        self._penalty_strategy = penalty_strategy
        self._validate_penalty_strategy()
    
    def _validate_penalty_strategy(self):
        """Valida a estratégia de penalização."""
        valid_strategies = ["linear", "quadratic", "zero"]
        if self._penalty_strategy not in valid_strategies:
            raise ValueError(f"Estratégia deve ser uma de: {valid_strategies}")
    
    def evaluate(self, solution: KnapsackSolution) -> float:
        """
        Avalia uma solução do problema da mochila.
        
        Args:
            solution: Solução a ser avaliada
            
        Returns:
            Valor de fitness da solução
        """
        if solution.is_feasible:
            return float(solution.total_value)
        
        return self._apply_penalty(solution)
    
    def _apply_penalty(self, solution: KnapsackSolution) -> float:
        """
        Aplica penalização para soluções inviáveis.
        
        Args:
            solution: Solução inviável
            
        Returns:
            Valor penalizado
        """
        base_value = float(solution.total_value)
        excess_weight = solution.weight_excess
        
        if self._penalty_strategy == "zero":
            return 0.0
        elif self._penalty_strategy == "linear":
            penalty = excess_weight * AlgorithmConstants.PENALTY_MULTIPLIER
            return max(0.0, base_value - penalty)
        elif self._penalty_strategy == "quadratic":
            penalty = (excess_weight ** 2) * AlgorithmConstants.PENALTY_MULTIPLIER
            return max(0.0, base_value - penalty)
        
        return 0.0
    
    def evaluate_binary(self, binary_solution: list[int], problem: KnapsackProblem) -> float:
        """
        Avalia uma solução binária diretamente.
        
        Args:
            binary_solution: Lista binária da solução
            problem: Problema da mochila
            
        Returns:
            Valor de fitness da solução
        """
        solution = KnapsackSolution(binary_solution, problem)
        return self.evaluate(solution)
    
    def compare_solutions(self, solution1: KnapsackSolution, solution2: KnapsackSolution) -> int:
        """
        Compara duas soluções.
        
        Args:
            solution1: Primeira solução
            solution2: Segunda solução
            
        Returns:
            1 se solution1 é melhor, -1 se solution2 é melhor, 0 se iguais
        """
        fitness1 = self.evaluate(solution1)
        fitness2 = self.evaluate(solution2)
        
        if fitness1 > fitness2:
            return 1
        elif fitness1 < fitness2:
            return -1
        else:
            return 0
    
    def get_best_solution(self, solutions: list[KnapsackSolution]) -> KnapsackSolution:
        """
        Retorna a melhor solução de uma lista.
        
        Args:
            solutions: Lista de soluções
            
        Returns:
            Melhor solução
        """
        if not solutions:
            raise ValueError("Lista de soluções não pode estar vazia")
        
        return max(solutions, key=self.evaluate)
    
    def rank_solutions(self, solutions: list[KnapsackSolution]) -> list[tuple[KnapsackSolution, float]]:
        """
        Ordena soluções por fitness.
        
        Args:
            solutions: Lista de soluções
            
        Returns:
            Lista de tuplas (solução, fitness) ordenada por fitness decrescente
        """
        evaluated = [(solution, self.evaluate(solution)) for solution in solutions]
        return sorted(evaluated, key=lambda x: x[1], reverse=True)


class ConstraintViolationEvaluator(KnapsackEvaluator):
    """
    Avaliador que considera violações de restrições.
    
    Esta classe estende o avaliador básico para considerar
    diferentes tipos de violações de restrições.
    """
    
    def __init__(self, weight_penalty: float = 1.0, capacity_penalty: float = 1.0):
        """
        Inicializa o avaliador com penalidades customizadas.
        
        Args:
            weight_penalty: Penalidade por excesso de peso
            capacity_penalty: Penalidade por violação de capacidade
        """
        super().__init__("linear")
        self._weight_penalty = weight_penalty
        self._capacity_penalty = capacity_penalty
    
    def _apply_penalty(self, solution: KnapsackSolution) -> float:
        """Aplica penalidades customizadas."""
        base_value = float(solution.total_value)
        excess_weight = solution.weight_excess
        
        weight_penalty = excess_weight * self._weight_penalty
        capacity_violation = 1 if not solution.is_feasible else 0
        capacity_penalty = capacity_violation * self._capacity_penalty
        
        total_penalty = weight_penalty + capacity_penalty
        return max(0.0, base_value - total_penalty)


class MultiObjectiveEvaluator(KnapsackEvaluator):
    """
    Avaliador multi-objetivo que considera valor e utilização da capacidade.
    
    Esta classe implementa uma avaliação que balanceia o valor total
    com a eficiência de utilização da capacidade.
    """
    
    def __init__(self, value_weight: float = 0.8, efficiency_weight: float = 0.2):
        """
        Inicializa o avaliador multi-objetivo.
        
        Args:
            value_weight: Peso do valor total na avaliação
            efficiency_weight: Peso da eficiência na avaliação
        """
        super().__init__("zero")
        self._value_weight = value_weight
        self._efficiency_weight = efficiency_weight
        
        if abs(value_weight + efficiency_weight - 1.0) > 1e-6:
            raise ValueError("Pesos devem somar 1.0")
    
    def evaluate(self, solution: KnapsackSolution) -> float:
        """Avalia considerando valor e eficiência."""
        if not solution.is_feasible:
            return 0.0
        
        # Normalizar valor pelo valor máximo possível
        max_possible_value = solution.problem.total_value
        normalized_value = solution.total_value / max_possible_value
        
        # Eficiência de utilização da capacidade
        efficiency = solution.capacity_utilization
        
        # Combinar métricas
        combined_score = (self._value_weight * normalized_value + 
                         self._efficiency_weight * efficiency)
        
        return combined_score 