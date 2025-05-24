# Plano de Refatoração - Problema da Mochila

## Problemas Identificados

### 1. **Código Duplicado (Code Duplication)**

- **Função `gerar_instancia_aleatoria`**: Duplicada em 4 arquivos com pequenas variações
- **Função `avaliar`**: Implementada de forma similar em todos os algoritmos
- **Estrutura `main()`**: Padrão repetitivo em todos os arquivos
- **Geração de dados de teste**: Lógica similar espalhada por todos os algoritmos

### 2. **Falta de Coesão (Low Cohesion)**

- Cada arquivo mistura responsabilidades: geração de dados, algoritmo, avaliação e execução
- Funções utilitárias misturadas com lógica específica do algoritmo
- Parâmetros hardcoded espalhados pelo código

### 3. **Acoplamento Excessivo (High Coupling)**

- Algoritmos dependem diretamente da estrutura de dados específica
- Funções de avaliação acopladas à implementação específica de cada algoritmo
- Dificuldade para trocar estratégias de avaliação ou geração de dados

### 4. **Falta de Testes (No Tests)**

- Nenhum teste unitário implementado
- Validação manual através de execução direta
- Impossibilidade de verificar regressões

### 5. **Nomeação Inadequada (Poor Naming)**

- Variáveis com nomes genéricos: `n`, `i`, `df`
- Funções com nomes pouco descritivos: `avaliar`, `main`
- Inconsistência na nomenclatura entre arquivos

### 6. **Problemas de Estrutura e Lógica**

- **Magic Numbers**: Valores hardcoded sem explicação
- **Long Methods**: Funções muito longas (ex: `pso()`, `algoritmo_genetico()`)
- **Feature Envy**: Algoritmos acessando diretamente dados que não deveriam
- **Data Clumps**: Grupos de parâmetros sempre passados juntos

## Plano de Refatoração (Baseado em Martin Fowler)

### Fase 1: Extract Method e Extract Class

#### 1.1 **Extract Method** - Quebrar métodos longos

```python
# Antes: algoritmo_genetico() com 30+ linhas
# Depois: Dividir em métodos menores
def algoritmo_genetico():
    populacao = inicializar_populacao()
    for geracao in range(n_geracoes):
        populacao = evoluir_populacao(populacao)
    return obter_melhor_solucao(populacao)
```

#### 1.2 **Extract Class** - Criar classes especializadas

- `KnapsackProblem`: Representa o problema da mochila
- `KnapsackSolution`: Representa uma solução
- `KnapsackEvaluator`: Avalia soluções
- `DataGenerator`: Gera instâncias do problema

### Fase 2: Move Method e Replace Parameter with Object

#### 2.1 **Move Method** - Mover métodos para classes apropriadas

```python
# Mover avaliar() para KnapsackEvaluator
# Mover gerar_instancia() para DataGenerator
```

#### 2.2 **Replace Parameter with Object** - Agrupar parâmetros relacionados

```python
# Antes: def algoritmo(pesos, valores, capacidade, param1, param2...)
# Depois: def algoritmo(problem: KnapsackProblem, config: AlgorithmConfig)
```

### Fase 3: Extract Superclass e Strategy Pattern

#### 3.1 **Extract Superclass** - Criar classe base para algoritmos

```python
class BioinspiredAlgorithm(ABC):
    @abstractmethod
    def solve(self, problem: KnapsackProblem) -> KnapsackSolution:
        pass
```

#### 3.2 **Strategy Pattern** - Permitir troca de estratégias

- Estratégias de avaliação
- Estratégias de geração de dados
- Estratégias de seleção/mutação

### Fase 4: Replace Magic Number with Named Constant

#### 4.1 **Criar constantes nomeadas**

```python
class AlgorithmConstants:
    DEFAULT_POPULATION_SIZE = 20
    DEFAULT_MUTATION_RATE = 0.1
    DEFAULT_GENERATIONS = 50
    PENALTY_MULTIPLIER = 2
```

### Fase 5: Introduce Parameter Object e Extract Interface

#### 5.1 **Parameter Objects** para configurações

```python
@dataclass
class GeneticAlgorithmConfig:
    population_size: int = 20
    mutation_rate: float = 0.1
    generations: int = 50
```

#### 5.2 **Extract Interface** para contratos

```python
class ProblemEvaluator(Protocol):
    def evaluate(self, solution: Solution) -> float:
        ...
```

## Estrutura Final Proposta

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

## Benefícios Esperados

1. **Manutenibilidade**: Código mais fácil de modificar e estender
2. **Testabilidade**: Componentes isolados e testáveis
3. **Reutilização**: Componentes podem ser reutilizados em outros contextos
4. **Legibilidade**: Código mais claro e autodocumentado
5. **Flexibilidade**: Fácil adição de novos algoritmos ou estratégias
6. **Robustez**: Validação através de testes automatizados

## Técnicas de Fowler Aplicadas

1. **Extract Method**: Quebrar métodos longos
2. **Extract Class**: Criar classes com responsabilidades específicas
3. **Move Method**: Mover métodos para classes apropriadas
4. **Replace Parameter with Object**: Agrupar parâmetros relacionados
5. **Extract Superclass**: Criar hierarquia de classes
6. **Replace Magic Number with Named Constant**: Eliminar números mágicos
7. **Introduce Parameter Object**: Simplificar assinaturas de métodos
8. **Extract Interface**: Definir contratos claros

## Ordem de Execução

1. **Semana 1**: Extract Method e Replace Magic Numbers
2. **Semana 2**: Extract Class (core classes)
3. **Semana 3**: Move Method e Extract Superclass
4. **Semana 4**: Strategy Pattern e Parameter Objects
5. **Semana 5**: Testes e validação
6. **Semana 6**: Documentação e benchmarks
