# Plano de Refatoração - Problema da Mochila

## Problemas Identificados no Código Original

### 1. **Código Duplicado (Code Duplication)**

#### **ANTES** - Função duplicada em 4 arquivos:

```python
# Em algGeneticos.py
def gerar_instancia_aleatoria(n_itens, max_peso=10, max_valor=20):
    pesos = [random.randint(1, max_peso) for _ in range(n_itens)]
    valores = [random.randint(1, max_valor) for _ in range(n_itens)]
    capacidade = random.randint(int(sum(pesos) * 0.3), int(sum(pesos) * 0.6))
    return pesos, valores, capacidade

# Em algEnxParticulas.py (com variação)
def gerar_dados(n_itens):
    pesos = [random.randint(1, 10) for _ in range(n_itens)]
    valores = [random.randint(1, 10) for _ in range(n_itens)]
    capacidade = int(0.2 * sum(pesos))  # Diferente!
    return pesos, valores, capacidade
```

#### **DEPOIS** - Centralizada em uma classe:

```python
# knapsack/core/data_generator.py
class DataGenerator:
    def generate_random_instance(self, num_items: int,
                                max_weight: int = DataGenerationConstants.DEFAULT_MAX_WEIGHT,
                                max_value: int = DataGenerationConstants.DEFAULT_MAX_VALUE) -> KnapsackProblem:
        weights = [random.randint(1, max_weight) for _ in range(num_items)]
        values = [random.randint(1, max_value) for _ in range(num_items)]

        total_weight = sum(weights)
        min_capacity = int(total_weight * DataGenerationConstants.MIN_CAPACITY_RATIO)
        max_capacity = int(total_weight * DataGenerationConstants.MAX_CAPACITY_RATIO)
        capacity = random.randint(min_capacity, max_capacity)

        return KnapsackProblem(weights, values, capacity)
```

### 2. **Falta de Coesão (Low Cohesion)**

#### **ANTES** - Tudo misturado em um arquivo:

```python
# algGeneticos.py - 88 linhas misturando tudo
import random
import time
import pandas as pd

def gerar_instancia_aleatoria(n_itens, max_peso=10, max_valor=20):
    # Geração de dados

def gerar_individuo(n_itens):
    # Lógica do algoritmo

def avaliar_individuo(individuo, pesos, valores, capacidade):
    # Avaliação

def algoritmo_genetico(pesos, valores, capacidade, tam_populacao=20, taxa_mutacao=0.1, n_geracoes=50):
    # Algoritmo principal com 30+ linhas

def main():
    # Execução e relatórios
```

#### **DEPOIS** - Separado por responsabilidades:

```
knapsack/
├── core/
│   ├── problem.py          # KnapsackProblem, KnapsackSolution
│   ├── evaluator.py        # KnapsackEvaluator
│   └── data_generator.py   # DataGenerator
├── algorithms/
│   ├── base.py            # BioinspiredAlgorithm (abstract)
│   └── genetic.py         # GeneticAlgorithm (apenas lógica do algoritmo)
├── config/
│   └── algorithm_configs.py # GeneticAlgorithmConfig
└── benchmarks/
    └── benchmark_runner.py # Execução e relatórios
```

### 3. **Acoplamento Excessivo (High Coupling)**

#### **ANTES** - Parâmetros espalhados:

```python
def algoritmo_genetico(pesos, valores, capacidade, tam_populacao=20, taxa_mutacao=0.1, n_geracoes=50):
    # Algoritmo acoplado aos dados específicos
    n_itens = len(pesos)
    populacao = [gerar_individuo(n_itens) for _ in range(tam_populacao)]
    # ... resto da implementação
```

#### **DEPOIS** - Desacoplado com objetos:

```python
class GeneticAlgorithm(PopulationBasedAlgorithm):
    def __init__(self, config: GeneticAlgorithmConfig,
                 evaluator: KnapsackEvaluator = None):
        super().__init__(
            population_size=config.population_size,
            evaluator=evaluator,
            name=AlgorithmNames.GENETIC
        )
        self._config = config

    def solve(self, problem: KnapsackProblem) -> KnapsackSolution:
        # Algoritmo trabalha com abstrações
```

### 4. **Magic Numbers (Números Mágicos)**

#### **ANTES** - Valores hardcoded:

```python
# Em algGeneticos.py
def avaliar_individuo(individuo, pesos, valores, capacidade):
    if peso_total > capacidade:
        excesso = peso_total - capacidade
        return valor_total - excesso * 2  # Magic number!

# Em algEnxParticulas.py
n_particulas = 30      # Magic number!
n_iteracoes = 100      # Magic number!
c1 = 1.5              # Magic number!
c2 = 1.5              # Magic number!
w = 0.8               # Magic number!
limite_velocidade = 4  # Magic number!
```

#### **DEPOIS** - Constantes nomeadas:

```python
# knapsack/utils/constants.py
class AlgorithmConstants:
    # Algoritmo Genético
    DEFAULT_POPULATION_SIZE: Final[int] = 20
    DEFAULT_MUTATION_RATE: Final[float] = 0.1
    DEFAULT_GENERATIONS: Final[int] = 50
    PENALTY_MULTIPLIER: Final[int] = 2

    # PSO
    DEFAULT_PARTICLES: Final[int] = 30
    DEFAULT_ITERATIONS: Final[int] = 100
    COGNITIVE_COEFFICIENT: Final[float] = 1.5  # c1
    SOCIAL_COEFFICIENT: Final[float] = 1.5     # c2
    INERTIA_WEIGHT: Final[float] = 0.8         # w
    VELOCITY_LIMIT: Final[int] = 4

# knapsack/core/evaluator.py
def evaluate_with_penalty(self, solution: KnapsackSolution) -> float:
    if solution.is_feasible:
        return float(solution.total_value)

    penalty = solution.weight_excess * AlgorithmConstants.PENALTY_MULTIPLIER
    return float(solution.total_value) - penalty
```

### 5. **Long Methods (Métodos Longos)**

#### **ANTES** - Método de 30+ linhas:

```python
def algoritmo_genetico(pesos, valores, capacidade, tam_populacao=20, taxa_mutacao=0.1, n_geracoes=50):
    n_itens = len(pesos)
    populacao = [gerar_individuo(n_itens) for _ in range(tam_populacao)]
    melhor_solucao = None
    melhor_valor = 0

    for _ in range(n_geracoes):
        nova_populacao = []
        for _ in range(tam_populacao // 2):
            pai1, pai2 = selecao(populacao, pesos, valores, capacidade)
            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])
        populacao = nova_populacao

        for individuo in populacao:
            valor = avaliar_individuo(individuo, pesos, valores, capacidade)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_solucao = individuo

        return melhor_solucao, melhor_valor
```

#### **DEPOIS** - Métodos pequenos e focados:

```python
class GeneticAlgorithm(PopulationBasedAlgorithm):
    def _iterate(self) -> bool:
        """Executa uma geração do algoritmo genético."""
        self._generation += 1
        new_population = []

        if self._config.elitism:
            elite = self._select_elite()
            new_population.extend(elite)

        while len(new_population) < self._config.population_size:
            offspring = self._reproduce()
            new_population.extend(offspring)

        self._population = new_population[:self._config.population_size]
        return self._generation < self._config.generations

    def _reproduce(self) -> List[KnapsackSolution]:
        """Executa um ciclo de reprodução."""
        parent1 = self._tournament_selection()
        parent2 = self._tournament_selection()

        if random.random() < self._config.crossover_rate:
            offspring1, offspring2 = self._crossover(parent1, parent2)
        else:
            offspring1, offspring2 = parent1.copy(), parent2.copy()

        offspring1 = self._mutate(offspring1)
        offspring2 = self._mutate(offspring2)

        return [offspring1, offspring2]
```

### 6. **Falta de Validação e Tratamento de Erros**

#### **ANTES** - Sem validação:

```python
def avaliar_individuo(individuo, pesos, valores, capacidade):
    peso_total = sum(p * i for p, i in zip(pesos, individuo))
    valor_total = sum(v * i for v, i in zip(valores, individuo))
    # Sem validação se listas têm mesmo tamanho!
```

#### **DEPOIS** - Com validação robusta:

```python
@dataclass(frozen=True)
class KnapsackProblem:
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
```

### 7. **Nomeação Inadequada (Poor Naming)**

#### **ANTES** - Nomes genéricos:

```python
def main():
    testes = []
    for i, n in enumerate([5, 1000, 10000], start=1):  # n, i genéricos
        pesos, valores, capacidade = gerar_instancia_aleatoria(n)
        inicio = time.time()
        solucao, valor = algoritmo_genetico(pesos, valores, capacidade)
        fim = time.time()
        # ...

    df = pd.DataFrame(testes)  # df genérico
```

#### **DEPOIS** - Nomes descritivos:

```python
class BenchmarkRunner:
    def run_algorithm_benchmark(self, algorithm: BioinspiredAlgorithm,
                               test_sizes: List[int]) -> pd.DataFrame:
        benchmark_results = []

        for problem_size in test_sizes:
            problem = self._data_generator.generate_random_instance(problem_size)
            start_time = time.time()
            solution = algorithm.solve(problem)
            end_time = time.time()

            execution_time = end_time - start_time
            # ...

        return pd.DataFrame(benchmark_results)
```

## Técnicas de Refatoração Aplicadas (Martin Fowler)

### 1. **Extract Method** - Quebrar métodos longos

**Aplicado em:** Todos os algoritmos principais

- `algoritmo_genetico()` → `_iterate()`, `_reproduce()`, `_tournament_selection()`, etc.
- `pso()` → `_update_particles()`, `_update_global_best()`, etc.

### 2. **Extract Class** - Criar classes especializadas

**Classes criadas:**

- `KnapsackProblem`: Representa o problema
- `KnapsackSolution`: Representa uma solução
- `KnapsackEvaluator`: Avalia soluções
- `DataGenerator`: Gera instâncias do problema
- `GeneticAlgorithmConfig`: Configuração do AG

### 3. **Replace Parameter with Object** - Agrupar parâmetros

**ANTES:**

```python
def algoritmo_genetico(pesos, valores, capacidade, tam_populacao=20, taxa_mutacao=0.1, n_geracoes=50):
```

**DEPOIS:**

```python
def solve(self, problem: KnapsackProblem) -> KnapsackSolution:
    # Configuração encapsulada em self._config
```

### 4. **Replace Magic Number with Named Constant**

**ANTES:** `excesso * 2`, `c1 = 1.5`, `w = 0.8`
**DEPOIS:** `AlgorithmConstants.PENALTY_MULTIPLIER`, `AlgorithmConstants.COGNITIVE_COEFFICIENT`

### 5. **Extract Superclass** - Hierarquia de classes

```python
class BioinspiredAlgorithm(ABC):
    @abstractmethod
    def solve(self, problem: KnapsackProblem) -> KnapsackSolution:
        pass

class PopulationBasedAlgorithm(BioinspiredAlgorithm):
    # Funcionalidade comum para algoritmos populacionais

class GeneticAlgorithm(PopulationBasedAlgorithm):
    # Implementação específica do AG
```

### 6. **Introduce Parameter Object** - Simplificar assinaturas

**Configurações encapsuladas:**

```python
@dataclass
class GeneticAlgorithmConfig:
    population_size: int = 20
    mutation_rate: float = 0.1
    generations: int = 50
    tournament_size: int = 3
    crossover_rate: float = 1.0
    elitism: bool = True
```

## Estrutura Final Implementada

```
knapsack/
├── core/
│   ├── __init__.py
│   ├── problem.py          # KnapsackProblem, KnapsackSolution
│   ├── evaluator.py        # KnapsackEvaluator
│   └── data_generator.py   # DataGenerator
├── algorithms/
│   ├── __init__.py
│   ├── base.py            # BioinspiredAlgorithm (abstract)
│   ├── genetic.py         # GeneticAlgorithm
│   ├── pso.py            # ParticleSwarmOptimization
│   ├── aco.py            # AntColonyOptimization
│   ├── cuckoo.py         # CuckooSearch
│   └── bee.py            # BeeAlgorithm
├── config/
│   ├── __init__.py
│   └── algorithm_configs.py # Configurações dos algoritmos
├── utils/
│   ├── __init__.py
│   └── constants.py       # Constantes do sistema
├── tests/
│   ├── __init__.py
│   ├── test_algorithms.py
│   ├── test_evaluator.py
│   └── test_problem.py
├── benchmarks/
│   ├── __init__.py
│   └── benchmark_runner.py # Execução de benchmarks
└── main.py               # Ponto de entrada
```
