# Como Executar a Aplicação Refatorada

## 🚀 Execução Rápida (Recomendado)

```bash
python exemplo_refatorado_rapido.py
```

**Tempo de execução:** ~30 segundos  
**Testa:** 5, 20, 50, 100 itens com poucas iterações

---

## 📊 Execução Completa (Otimizada)

```bash
python exemplo_refatorado.py
```

**Tempo de execução:** ~20 segundos  
**Testa:** 5, 1000, 10000 itens (10000 usa apenas 20 iterações)

---

## 🧪 Executar Testes

### Método 1 (Direto)

```bash
python knapsack/tests/test_problem.py
```

### Método 2 (Com pytest, se instalado)

```bash
pip install pytest
python -m pytest knapsack/tests/ -v
```

---

## ⚡ Teste Rápido de Funcionamento

Crie um arquivo `teste_simples.py`:

```python
from knapsack.core.data_generator import DataGenerator, GenerationConfig
from knapsack.algorithms.genetic import create_genetic_algorithm

# Problema pequeno
generator = DataGenerator(seed=42)
config = GenerationConfig(num_items=10)
problem = generator.generate_random_instance(config)

# Algoritmo rápido
algorithm = create_genetic_algorithm(problem.num_items)
result = algorithm.solve(problem, max_iterations=20)

# Resultados
print(f"Valor: {result.best_solution.total_value}")
print(f"Tempo: {result.execution_time:.4f}s")
print(f"Viável: {result.best_solution.is_feasible}")
```

Execute:

```bash
python teste_simples.py
```

---

## 🔧 Solução de Problemas

### Erro "ModuleNotFoundError"

```bash
# Certifique-se de estar no diretório correto
# Deve conter a pasta 'knapsack'
dir  # Windows
ls   # Linux/Mac
```

### Verificar Instalação

```bash
python -c "from knapsack.core.problem import KnapsackProblem; print('✅ Funcionando!')"
```

---

## 📈 Comparação de Tempos

| Comando                        | Tempo | Descrição        |
| ------------------------------ | ----- | ---------------- |
| `exemplo_refatorado_rapido.py` | ~30s  | Versão rápida    |
| `exemplo_refatorado.py`        | ~20s  | Versão otimizada |
| `teste_simples.py`             | ~1s   | Teste básico     |

---

## 💡 Dicas

- **Para demonstrações:** Use `exemplo_refatorado_rapido.py`
- **Para análise completa:** Use `exemplo_refatorado.py`
- **Para desenvolvimento:** Use `teste_simples.py`
- **Para validação:** Execute os testes unitários

---

## ✅ Saída Esperada

Quando executar qualquer exemplo, você deve ver:

- ✅ Problemas sendo criados
- ✅ Algoritmos sendo executados
- ✅ Resultados com valores, tempos e viabilidade
- ✅ Métricas detalhadas
- ✅ Lista de vantagens da refatoração

Se algo não funcionar, verifique se está no diretório correto que contém a pasta `knapsack/`.
