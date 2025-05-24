"""
Configurações para algoritmos bio-inspirados.

Este módulo implementa classes de configuração para cada algoritmo,
aplicando a técnica "Introduce Parameter Object" de Martin Fowler
para simplificar assinaturas de métodos e agrupar parâmetros relacionados.
"""

from dataclasses import dataclass
from typing import Optional
from ..utils.constants import AlgorithmConstants


@dataclass
class GeneticAlgorithmConfig:
    """Configuração para o Algoritmo Genético."""
    
    population_size: int = AlgorithmConstants.DEFAULT_POPULATION_SIZE
    mutation_rate: float = AlgorithmConstants.DEFAULT_MUTATION_RATE
    generations: int = AlgorithmConstants.DEFAULT_GENERATIONS
    tournament_size: int = AlgorithmConstants.TOURNAMENT_SIZE
    crossover_rate: float = 1.0
    elitism: bool = True
    elitism_size: int = 2
    
    def __post_init__(self):
        """Valida a configuração."""
        if self.population_size <= 0:
            raise ValueError("Tamanho da população deve ser positivo")
        if not 0 <= self.mutation_rate <= 1:
            raise ValueError("Taxa de mutação deve estar entre 0 e 1")
        if self.generations <= 0:
            raise ValueError("Número de gerações deve ser positivo")
        if self.tournament_size <= 0:
            raise ValueError("Tamanho do torneio deve ser positivo")
        if not 0 <= self.crossover_rate <= 1:
            raise ValueError("Taxa de crossover deve estar entre 0 e 1")


@dataclass
class PSOConfig:
    """Configuração para Particle Swarm Optimization."""
    
    num_particles: int = AlgorithmConstants.DEFAULT_PARTICLES
    max_iterations: int = AlgorithmConstants.DEFAULT_ITERATIONS
    cognitive_coefficient: float = AlgorithmConstants.COGNITIVE_COEFFICIENT  # c1
    social_coefficient: float = AlgorithmConstants.SOCIAL_COEFFICIENT        # c2
    inertia_weight: float = AlgorithmConstants.INERTIA_WEIGHT               # w
    velocity_limit: float = AlgorithmConstants.VELOCITY_LIMIT
    sigmoid_threshold: float = AlgorithmConstants.SIGMOID_THRESHOLD
    
    def __post_init__(self):
        """Valida a configuração."""
        if self.num_particles <= 0:
            raise ValueError("Número de partículas deve ser positivo")
        if self.max_iterations <= 0:
            raise ValueError("Número de iterações deve ser positivo")
        if self.cognitive_coefficient < 0:
            raise ValueError("Coeficiente cognitivo deve ser não-negativo")
        if self.social_coefficient < 0:
            raise ValueError("Coeficiente social deve ser não-negativo")
        if self.inertia_weight < 0:
            raise ValueError("Peso de inércia deve ser não-negativo")
        if self.velocity_limit <= 0:
            raise ValueError("Limite de velocidade deve ser positivo")


@dataclass
class ACOConfig:
    """Configuração para Ant Colony Optimization."""
    
    num_ants: int = AlgorithmConstants.DEFAULT_ANTS
    max_iterations: int = AlgorithmConstants.DEFAULT_ITERATIONS
    alpha: float = AlgorithmConstants.ALPHA          # Influência do feromônio
    beta: float = AlgorithmConstants.BETA            # Influência da heurística
    rho: float = AlgorithmConstants.RHO              # Taxa de evaporação
    Q: float = AlgorithmConstants.Q                  # Quantidade de feromônio
    initial_pheromone: float = 1.0
    
    def __post_init__(self):
        """Valida a configuração."""
        if self.num_ants <= 0:
            raise ValueError("Número de formigas deve ser positivo")
        if self.max_iterations <= 0:
            raise ValueError("Número de iterações deve ser positivo")
        if self.alpha < 0:
            raise ValueError("Alpha deve ser não-negativo")
        if self.beta < 0:
            raise ValueError("Beta deve ser não-negativo")
        if not 0 <= self.rho <= 1:
            raise ValueError("Rho deve estar entre 0 e 1")
        if self.Q <= 0:
            raise ValueError("Q deve ser positivo")


@dataclass
class CuckooSearchConfig:
    """Configuração para Cuckoo Search."""
    
    num_nests: int = AlgorithmConstants.DEFAULT_NESTS
    max_iterations: int = AlgorithmConstants.DEFAULT_ITERATIONS
    abandonment_probability: float = AlgorithmConstants.ABANDONMENT_PROBABILITY  # pa
    levy_flight_probability: float = AlgorithmConstants.LEVY_FLIGHT_PROBABILITY
    step_size: float = 1.0
    
    def __post_init__(self):
        """Valida a configuração."""
        if self.num_nests <= 0:
            raise ValueError("Número de ninhos deve ser positivo")
        if self.max_iterations <= 0:
            raise ValueError("Número de iterações deve ser positivo")
        if not 0 <= self.abandonment_probability <= 1:
            raise ValueError("Probabilidade de abandono deve estar entre 0 e 1")
        if not 0 <= self.levy_flight_probability <= 1:
            raise ValueError("Probabilidade de voo de Lévy deve estar entre 0 e 1")


@dataclass
class BeeAlgorithmConfig:
    """Configuração para Bee Algorithm."""
    
    num_bees: int = AlgorithmConstants.DEFAULT_BEES
    max_iterations: int = AlgorithmConstants.DEFAULT_ITERATIONS
    elite_sites: int = AlgorithmConstants.ELITE_SITES
    neighbors_per_site: int = AlgorithmConstants.NEIGHBORS_PER_SITE
    scout_bees_ratio: float = 0.3
    local_search_iterations: int = 5
    
    def __post_init__(self):
        """Valida a configuração."""
        if self.num_bees <= 0:
            raise ValueError("Número de abelhas deve ser positivo")
        if self.max_iterations <= 0:
            raise ValueError("Número de iterações deve ser positivo")
        if self.elite_sites <= 0:
            raise ValueError("Número de sítios elite deve ser positivo")
        if self.elite_sites > self.num_bees:
            raise ValueError("Sítios elite não pode exceder número de abelhas")
        if self.neighbors_per_site <= 0:
            raise ValueError("Vizinhos por sítio deve ser positivo")
        if not 0 <= self.scout_bees_ratio <= 1:
            raise ValueError("Ratio de abelhas exploradoras deve estar entre 0 e 1")


class ConfigFactory:
    """
    Factory para criar configurações padrão dos algoritmos.
    
    Esta classe aplica o padrão Factory para simplificar a criação
    de configurações com valores padrão apropriados.
    """
    
    @staticmethod
    def create_genetic_config(problem_size: int) -> GeneticAlgorithmConfig:
        """
        Cria configuração adaptada para o Algoritmo Genético.
        
        Args:
            problem_size: Tamanho do problema
            
        Returns:
            Configuração otimizada
        """
        # Ajustar parâmetros baseado no tamanho do problema
        if problem_size <= 50:
            return GeneticAlgorithmConfig(
                population_size=20,
                generations=100,
                mutation_rate=0.1
            )
        elif problem_size <= 1000:
            return GeneticAlgorithmConfig(
                population_size=50,
                generations=200,
                mutation_rate=0.05
            )
        else:
            return GeneticAlgorithmConfig(
                population_size=100,
                generations=500,
                mutation_rate=0.02
            )
    
    @staticmethod
    def create_pso_config(problem_size: int) -> PSOConfig:
        """
        Cria configuração adaptada para PSO.
        
        Args:
            problem_size: Tamanho do problema
            
        Returns:
            Configuração otimizada
        """
        if problem_size <= 50:
            return PSOConfig(
                num_particles=20,
                max_iterations=100
            )
        elif problem_size <= 1000:
            return PSOConfig(
                num_particles=30,
                max_iterations=200
            )
        else:
            return PSOConfig(
                num_particles=50,
                max_iterations=300
            )
    
    @staticmethod
    def create_aco_config(problem_size: int) -> ACOConfig:
        """
        Cria configuração adaptada para ACO.
        
        Args:
            problem_size: Tamanho do problema
            
        Returns:
            Configuração otimizada
        """
        if problem_size <= 50:
            return ACOConfig(
                num_ants=20,
                max_iterations=100
            )
        elif problem_size <= 1000:
            return ACOConfig(
                num_ants=50,
                max_iterations=150
            )
        else:
            return ACOConfig(
                num_ants=100,
                max_iterations=200
            )
    
    @staticmethod
    def create_cuckoo_config(problem_size: int) -> CuckooSearchConfig:
        """
        Cria configuração adaptada para Cuckoo Search.
        
        Args:
            problem_size: Tamanho do problema
            
        Returns:
            Configuração otimizada
        """
        if problem_size <= 50:
            return CuckooSearchConfig(
                num_nests=15,
                max_iterations=100
            )
        elif problem_size <= 1000:
            return CuckooSearchConfig(
                num_nests=25,
                max_iterations=150
            )
        else:
            return CuckooSearchConfig(
                num_nests=40,
                max_iterations=200
            )
    
    @staticmethod
    def create_bee_config(problem_size: int) -> BeeAlgorithmConfig:
        """
        Cria configuração adaptada para Bee Algorithm.
        
        Args:
            problem_size: Tamanho do problema
            
        Returns:
            Configuração otimizada
        """
        if problem_size <= 50:
            return BeeAlgorithmConfig(
                num_bees=20,
                max_iterations=100,
                elite_sites=5
            )
        elif problem_size <= 1000:
            return BeeAlgorithmConfig(
                num_bees=30,
                max_iterations=150,
                elite_sites=8
            )
        else:
            return BeeAlgorithmConfig(
                num_bees=50,
                max_iterations=200,
                elite_sites=12
            ) 