"""
Classe base para algoritmos bio-inspirados.

Este módulo implementa a classe base abstrata para todos os algoritmos,
aplicando a técnica "Extract Superclass" de Martin Fowler para eliminar
duplicação e estabelecer uma interface comum.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time

from ..core.problem import KnapsackProblem, KnapsackSolution
from ..core.evaluator import KnapsackEvaluator
from ..utils.constants import AlgorithmNames


@dataclass
class AlgorithmResult:
    """
    Resultado da execução de um algoritmo.
    
    Esta classe encapsula todos os resultados de uma execução,
    aplicando "Replace Parameter with Object" para simplificar
    as assinaturas dos métodos.
    """
    
    algorithm_name: str
    best_solution: KnapsackSolution
    best_fitness: float
    execution_time: float
    iterations_completed: int
    problem_size: int
    additional_metrics: Dict[str, Any]
    
    @property
    def summary(self) -> Dict[str, Any]:
        """Retorna um resumo dos resultados."""
        return {
            "algoritmo": self.algorithm_name,
            "n_itens": self.problem_size,
            "capacidade": self.best_solution.problem.capacity,
            "valor_total": self.best_solution.total_value,
            "peso_total": self.best_solution.total_weight,
            "tempo_execucao": round(self.execution_time, 5),
            "iteracoes": self.iterations_completed,
            "viavel": self.best_solution.is_feasible,
            "fitness": self.best_fitness
        }


class BioinspiredAlgorithm(ABC):
    """
    Classe base abstrata para algoritmos bio-inspirados.
    
    Esta classe define a interface comum para todos os algoritmos
    e implementa funcionalidades compartilhadas, eliminando duplicação
    de código entre as implementações específicas.
    """
    
    def __init__(self, evaluator: Optional[KnapsackEvaluator] = None, 
                 name: Optional[str] = None):
        """
        Inicializa o algoritmo.
        
        Args:
            evaluator: Avaliador de soluções (opcional)
            name: Nome do algoritmo (opcional)
        """
        self._evaluator = evaluator or KnapsackEvaluator()
        self._name = name or self.__class__.__name__
        self._current_problem: Optional[KnapsackProblem] = None
        self._execution_stats = {}
        
    @property
    def name(self) -> str:
        """Retorna o nome do algoritmo."""
        return self._name
    
    @property
    def evaluator(self) -> KnapsackEvaluator:
        """Retorna o avaliador de soluções."""
        return self._evaluator
    
    @abstractmethod
    def _initialize(self, problem: KnapsackProblem) -> None:
        """
        Inicializa o algoritmo para um problema específico.
        
        Args:
            problem: Problema da mochila a ser resolvido
        """
        pass
    
    @abstractmethod
    def _iterate(self) -> bool:
        """
        Executa uma iteração do algoritmo.
        
        Returns:
            True se deve continuar, False se deve parar
        """
        pass
    
    @abstractmethod
    def _get_best_solution(self) -> KnapsackSolution:
        """
        Retorna a melhor solução encontrada.
        
        Returns:
            Melhor solução
        """
        pass
    
    def solve(self, problem: KnapsackProblem, max_iterations: Optional[int] = None) -> AlgorithmResult:
        """
        Resolve o problema da mochila.
        
        Args:
            problem: Problema da mochila
            max_iterations: Número máximo de iterações (opcional)
            
        Returns:
            Resultado da execução
        """
        self._current_problem = problem
        start_time = time.time()
        
        # Inicializar algoritmo
        self._initialize(problem)
        
        # Executar iterações
        iterations = 0
        max_iter = max_iterations or self._get_default_max_iterations()
        
        while iterations < max_iter:
            should_continue = self._iterate()
            iterations += 1
            
            if not should_continue:
                break
        
        # Obter resultado
        end_time = time.time()
        execution_time = end_time - start_time
        
        best_solution = self._get_best_solution()
        best_fitness = self._evaluator.evaluate(best_solution)
        
        return AlgorithmResult(
            algorithm_name=self._name,
            best_solution=best_solution,
            best_fitness=best_fitness,
            execution_time=execution_time,
            iterations_completed=iterations,
            problem_size=problem.num_items,
            additional_metrics=self._get_additional_metrics()
        )
    
    def _get_default_max_iterations(self) -> int:
        """Retorna o número padrão de iterações."""
        return 100
    
    def _get_additional_metrics(self) -> Dict[str, Any]:
        """Retorna métricas adicionais específicas do algoritmo."""
        return {}
    
    def _evaluate_solution(self, solution: KnapsackSolution) -> float:
        """
        Avalia uma solução usando o avaliador configurado.
        
        Args:
            solution: Solução a ser avaliada
            
        Returns:
            Fitness da solução
        """
        return self._evaluator.evaluate(solution)
    
    def _evaluate_binary(self, binary_solution: List[int]) -> float:
        """
        Avalia uma solução binária.
        
        Args:
            binary_solution: Lista binária da solução
            
        Returns:
            Fitness da solução
        """
        if self._current_problem is None:
            raise RuntimeError("Problema não foi definido")
        
        solution = KnapsackSolution(binary_solution, self._current_problem)
        return self._evaluate_solution(solution)
    
    def _create_solution(self, binary_solution: List[int]) -> KnapsackSolution:
        """
        Cria uma solução a partir de uma representação binária.
        
        Args:
            binary_solution: Lista binária da solução
            
        Returns:
            Objeto KnapsackSolution
        """
        if self._current_problem is None:
            raise RuntimeError("Problema não foi definido")
        
        return KnapsackSolution(binary_solution, self._current_problem)
    
    def benchmark(self, problems: List[KnapsackProblem], 
                  max_iterations: Optional[int] = None) -> List[AlgorithmResult]:
        """
        Executa benchmark em múltiplos problemas.
        
        Args:
            problems: Lista de problemas
            max_iterations: Número máximo de iterações por problema
            
        Returns:
            Lista de resultados
        """
        results = []
        
        for problem in problems:
            result = self.solve(problem, max_iterations)
            results.append(result)
        
        return results
    
    def __str__(self) -> str:
        """Representação em string do algoritmo."""
        return f"{self._name}(evaluator={type(self._evaluator).__name__})"
    
    def __repr__(self) -> str:
        """Representação detalhada do algoritmo."""
        return (f"{self.__class__.__name__}("
                f"name='{self._name}', "
                f"evaluator={self._evaluator})")


class PopulationBasedAlgorithm(BioinspiredAlgorithm):
    """
    Classe base para algoritmos baseados em população.
    
    Esta classe estende a classe base para algoritmos que trabalham
    com populações de soluções (GA, PSO, etc.).
    """
    
    def __init__(self, population_size: int, evaluator: Optional[KnapsackEvaluator] = None,
                 name: Optional[str] = None):
        """
        Inicializa algoritmo baseado em população.
        
        Args:
            population_size: Tamanho da população
            evaluator: Avaliador de soluções
            name: Nome do algoritmo
        """
        super().__init__(evaluator, name)
        self._population_size = population_size
        self._population: List[KnapsackSolution] = []
    
    @property
    def population_size(self) -> int:
        """Retorna o tamanho da população."""
        return self._population_size
    
    @property
    def population(self) -> List[KnapsackSolution]:
        """Retorna uma cópia da população atual."""
        return self._population.copy()
    
    @abstractmethod
    def _initialize_population(self, problem: KnapsackProblem) -> List[KnapsackSolution]:
        """
        Inicializa a população.
        
        Args:
            problem: Problema da mochila
            
        Returns:
            População inicial
        """
        pass
    
    def _initialize(self, problem: KnapsackProblem) -> None:
        """Inicializa o algoritmo com uma população."""
        self._population = self._initialize_population(problem)
    
    def _get_best_solution(self) -> KnapsackSolution:
        """Retorna a melhor solução da população."""
        return self._evaluator.get_best_solution(self._population)
    
    def _get_additional_metrics(self) -> Dict[str, Any]:
        """Retorna métricas da população."""
        if not self._population:
            return {}
        
        fitnesses = [self._evaluate_solution(sol) for sol in self._population]
        
        return {
            "population_size": len(self._population),
            "best_fitness": max(fitnesses),
            "worst_fitness": min(fitnesses),
            "average_fitness": sum(fitnesses) / len(fitnesses),
            "feasible_solutions": sum(1 for sol in self._population if sol.is_feasible)
        } 