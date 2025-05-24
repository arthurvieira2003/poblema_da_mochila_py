"""
Classes para representar o problema da mochila e suas soluções.

Este módulo implementa as classes principais que representam o problema da mochila
e suas soluções, aplicando a técnica "Extract Class" de Martin Fowler.
"""

from dataclasses import dataclass
from typing import List, Optional
import copy


@dataclass(frozen=True)
class KnapsackProblem:
    """
    Representa uma instância do problema da mochila 0/1.
    
    Esta classe encapsula todos os dados necessários para definir um problema
    da mochila, incluindo pesos, valores e capacidade.
    
    Attributes:
        weights: Lista de pesos dos itens
        values: Lista de valores dos itens  
        capacity: Capacidade máxima da mochila
        num_items: Número de itens (calculado automaticamente)
    """
    
    weights: List[int]
    values: List[int]
    capacity: int
    
    def __post_init__(self):
        """Valida os dados do problema após inicialização."""
        if len(self.weights) != len(self.values):
            raise ValueError("Número de pesos deve ser igual ao número de valores")
        
        if len(self.weights) == 0:
            raise ValueError("Problema deve ter pelo menos um item")
            
        if self.capacity <= 0:
            raise ValueError("Capacidade deve ser positiva")
            
        if any(w <= 0 for w in self.weights):
            raise ValueError("Todos os pesos devem ser positivos")
            
        if any(v <= 0 for v in self.values):
            raise ValueError("Todos os valores devem ser positivos")
    
    @property
    def num_items(self) -> int:
        """Retorna o número de itens no problema."""
        return len(self.weights)
    
    @property
    def total_weight(self) -> int:
        """Retorna o peso total de todos os itens."""
        return sum(self.weights)
    
    @property
    def total_value(self) -> int:
        """Retorna o valor total de todos os itens."""
        return sum(self.values)
    
    @property
    def value_to_weight_ratios(self) -> List[float]:
        """Retorna a relação valor/peso para cada item."""
        return [v / w for v, w in zip(self.values, self.weights)]
    
    def get_item_info(self, index: int) -> tuple[int, int, float]:
        """
        Retorna informações de um item específico.
        
        Args:
            index: Índice do item
            
        Returns:
            Tupla (peso, valor, ratio_valor_peso)
        """
        if not 0 <= index < self.num_items:
            raise IndexError(f"Índice {index} fora do intervalo válido")
            
        weight = self.weights[index]
        value = self.values[index]
        ratio = value / weight
        
        return weight, value, ratio


class KnapsackSolution:
    """
    Representa uma solução para o problema da mochila.
    
    Esta classe encapsula uma solução binária e fornece métodos para
    calcular suas propriedades e validar sua viabilidade.
    """
    
    def __init__(self, binary_solution: List[int], problem: KnapsackProblem):
        """
        Inicializa uma solução da mochila.
        
        Args:
            binary_solution: Lista binária indicando quais itens estão selecionados
            problem: Instância do problema da mochila
        """
        if len(binary_solution) != problem.num_items:
            raise ValueError("Tamanho da solução deve ser igual ao número de itens")
            
        if not all(bit in [0, 1] for bit in binary_solution):
            raise ValueError("Solução deve ser binária (apenas 0s e 1s)")
            
        self._binary_solution = binary_solution.copy()
        self._problem = problem
        self._total_weight: Optional[int] = None
        self._total_value: Optional[int] = None
    
    @property
    def binary_solution(self) -> List[int]:
        """Retorna uma cópia da solução binária."""
        return self._binary_solution.copy()
    
    @property
    def problem(self) -> KnapsackProblem:
        """Retorna o problema associado à solução."""
        return self._problem
    
    @property
    def selected_items(self) -> List[int]:
        """Retorna os índices dos itens selecionados."""
        return [i for i, bit in enumerate(self._binary_solution) if bit == 1]
    
    @property
    def total_weight(self) -> int:
        """Calcula e retorna o peso total da solução."""
        if self._total_weight is None:
            self._total_weight = sum(
                weight * bit 
                for weight, bit in zip(self._problem.weights, self._binary_solution)
            )
        return self._total_weight
    
    @property
    def total_value(self) -> int:
        """Calcula e retorna o valor total da solução."""
        if self._total_value is None:
            self._total_value = sum(
                value * bit 
                for value, bit in zip(self._problem.values, self._binary_solution)
            )
        return self._total_value
    
    @property
    def is_feasible(self) -> bool:
        """Verifica se a solução é viável (não excede a capacidade)."""
        return self.total_weight <= self._problem.capacity
    
    @property
    def weight_excess(self) -> int:
        """Retorna o excesso de peso (0 se viável)."""
        return max(0, self.total_weight - self._problem.capacity)
    
    @property
    def capacity_utilization(self) -> float:
        """Retorna a utilização da capacidade como percentual."""
        return self.total_weight / self._problem.capacity
    
    def flip_item(self, index: int) -> 'KnapsackSolution':
        """
        Cria uma nova solução com um item invertido.
        
        Args:
            index: Índice do item a ser invertido
            
        Returns:
            Nova solução com o item invertido
        """
        if not 0 <= index < len(self._binary_solution):
            raise IndexError(f"Índice {index} fora do intervalo válido")
            
        new_solution = self._binary_solution.copy()
        new_solution[index] = 1 - new_solution[index]
        
        return KnapsackSolution(new_solution, self._problem)
    
    def copy(self) -> 'KnapsackSolution':
        """Cria uma cópia da solução."""
        return KnapsackSolution(self._binary_solution, self._problem)
    
    def __str__(self) -> str:
        """Representação em string da solução."""
        return (f"KnapsackSolution(value={self.total_value}, "
                f"weight={self.total_weight}/{self._problem.capacity}, "
                f"feasible={self.is_feasible})")
    
    def __repr__(self) -> str:
        """Representação detalhada da solução."""
        return (f"KnapsackSolution(binary={self._binary_solution}, "
                f"value={self.total_value}, weight={self.total_weight}, "
                f"capacity={self._problem.capacity})")
    
    def __eq__(self, other) -> bool:
        """Compara duas soluções."""
        if not isinstance(other, KnapsackSolution):
            return False
        return (self._binary_solution == other._binary_solution and 
                self._problem == other._problem) 