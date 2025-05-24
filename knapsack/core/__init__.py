"""Módulo core com as classes fundamentais do problema da mochila."""

from .problem import KnapsackProblem, KnapsackSolution
from .evaluator import KnapsackEvaluator, ConstraintViolationEvaluator, MultiObjectiveEvaluator
from .data_generator import DataGenerator, GenerationConfig, SpecializedDataGenerator

__all__ = [
    "KnapsackProblem",
    "KnapsackSolution",
    "KnapsackEvaluator",
    "ConstraintViolationEvaluator", 
    "MultiObjectiveEvaluator",
    "DataGenerator",
    "GenerationConfig",
    "SpecializedDataGenerator"
] 