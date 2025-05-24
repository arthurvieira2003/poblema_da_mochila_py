"""
Constantes utilizadas pelos algoritmos bio-inspirados.

Este módulo centraliza todas as constantes mágicas encontradas no código original,
aplicando a técnica "Replace Magic Number with Named Constant" de Martin Fowler.
"""

from dataclasses import dataclass
from typing import Final


# Constantes de geração de dados
class DataGenerationConstants:
    """Constantes para geração de instâncias do problema."""
    
    DEFAULT_MAX_WEIGHT: Final[int] = 10
    DEFAULT_MAX_VALUE: Final[int] = 20
    MIN_CAPACITY_RATIO: Final[float] = 0.3
    MAX_CAPACITY_RATIO: Final[float] = 0.6


# Constantes dos algoritmos
class AlgorithmConstants:
    """Constantes padrão para os algoritmos bio-inspirados."""
    
    # Algoritmo Genético
    DEFAULT_POPULATION_SIZE: Final[int] = 20
    DEFAULT_MUTATION_RATE: Final[float] = 0.1
    DEFAULT_GENERATIONS: Final[int] = 50
    TOURNAMENT_SIZE: Final[int] = 3
    PENALTY_MULTIPLIER: Final[int] = 2
    
    # PSO (Particle Swarm Optimization)
    DEFAULT_PARTICLES: Final[int] = 30
    DEFAULT_ITERATIONS: Final[int] = 100
    COGNITIVE_COEFFICIENT: Final[float] = 1.5  # c1
    SOCIAL_COEFFICIENT: Final[float] = 1.5     # c2
    INERTIA_WEIGHT: Final[float] = 0.8         # w
    VELOCITY_LIMIT: Final[int] = 4
    SIGMOID_THRESHOLD: Final[float] = 0.5
    
    # ACO (Ant Colony Optimization)
    DEFAULT_ANTS: Final[int] = 50
    ALPHA: Final[float] = 1.0  # Influência do feromônio
    BETA: Final[float] = 2.0   # Influência da heurística
    RHO: Final[float] = 0.1    # Taxa de evaporação
    Q: Final[int] = 100        # Quantidade de feromônio
    
    # Cuckoo Search
    DEFAULT_NESTS: Final[int] = 25
    ABANDONMENT_PROBABILITY: Final[float] = 0.25  # pa
    LEVY_FLIGHT_PROBABILITY: Final[float] = 0.5
    
    # Bee Algorithm
    DEFAULT_BEES: Final[int] = 30
    ELITE_SITES: Final[int] = 10
    NEIGHBORS_PER_SITE: Final[int] = 2


# Constantes de teste e benchmark
class TestConstants:
    """Constantes para testes e benchmarks."""
    
    SMALL_INSTANCE_SIZE: Final[int] = 5
    MEDIUM_INSTANCE_SIZE: Final[int] = 1000
    LARGE_INSTANCE_SIZE: Final[int] = 10000
    
    DEFAULT_TEST_SIZES: Final[tuple] = (
        SMALL_INSTANCE_SIZE,
        MEDIUM_INSTANCE_SIZE,
        LARGE_INSTANCE_SIZE
    )
    
    PRECISION_DIGITS: Final[int] = 5


@dataclass(frozen=True)
class AlgorithmNames:
    """Nomes padronizados dos algoritmos para relatórios."""
    
    GENETIC: str = "Algoritmo Genético"
    PSO: str = "PSO"
    ACO: str = "Algoritmo ACO"
    CUCKOO: str = "Cuckoo Search"
    BEE: str = "Bee Algorithm" 