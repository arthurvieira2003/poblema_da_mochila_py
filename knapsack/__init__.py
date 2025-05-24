"""
Pacote para resolução do Problema da Mochila usando algoritmos bio-inspirados.

Este pacote implementa uma versão refatorada e bem estruturada de algoritmos
bio-inspirados para resolver o problema da mochila 0/1.
"""

__version__ = "1.0.0"
__author__ = "Gabriel D. Kasten, Gustavo Henrique Costa, Lucas Mendes Israel"

from .core.problem import KnapsackProblem, KnapsackSolution
from .core.evaluator import KnapsackEvaluator
from .core.data_generator import DataGenerator

__all__ = [
    "KnapsackProblem",
    "KnapsackSolution", 
    "KnapsackEvaluator",
    "DataGenerator"
] 