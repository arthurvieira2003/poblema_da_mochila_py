"""
Testes unitários para as classes do problema da mochila.

Este módulo implementa testes abrangentes para validar o comportamento
das classes KnapsackProblem e KnapsackSolution, garantindo que a
refatoração não introduziu regressões.
"""

import unittest
from knapsack.core.problem import KnapsackProblem, KnapsackSolution


class TestKnapsackProblem(unittest.TestCase):
    """Testes para a classe KnapsackProblem."""
    
    def setUp(self):
        """Configura dados de teste."""
        self.weights = [2, 3, 4, 5, 1]
        self.values = [3, 4, 5, 6, 2]
        self.capacity = 5
        self.problem = KnapsackProblem(self.weights, self.values, self.capacity)
    
    def test_valid_problem_creation(self):
        """Testa criação de problema válido."""
        self.assertEqual(self.problem.weights, self.weights)
        self.assertEqual(self.problem.values, self.values)
        self.assertEqual(self.problem.capacity, self.capacity)
        self.assertEqual(self.problem.num_items, 5)
    
    def test_invalid_problem_creation(self):
        """Testa validação na criação de problemas inválidos."""
        # Tamanhos diferentes
        with self.assertRaises(ValueError):
            KnapsackProblem([1, 2], [1, 2, 3], 5)
        
        # Lista vazia
        with self.assertRaises(ValueError):
            KnapsackProblem([], [], 5)
        
        # Capacidade inválida
        with self.assertRaises(ValueError):
            KnapsackProblem([1, 2], [1, 2], 0)
        
        # Pesos inválidos
        with self.assertRaises(ValueError):
            KnapsackProblem([0, 2], [1, 2], 5)
        
        # Valores inválidos
        with self.assertRaises(ValueError):
            KnapsackProblem([1, 2], [0, 2], 5)
    
    def test_properties(self):
        """Testa propriedades calculadas."""
        self.assertEqual(self.problem.total_weight, 15)
        self.assertEqual(self.problem.total_value, 20)
        
        expected_ratios = [1.5, 4/3, 1.25, 1.2, 2.0]
        self.assertEqual(self.problem.value_to_weight_ratios, expected_ratios)
    
    def test_get_item_info(self):
        """Testa obtenção de informações de itens."""
        weight, value, ratio = self.problem.get_item_info(0)
        self.assertEqual(weight, 2)
        self.assertEqual(value, 3)
        self.assertEqual(ratio, 1.5)
        
        # Índice inválido
        with self.assertRaises(IndexError):
            self.problem.get_item_info(10)


class TestKnapsackSolution(unittest.TestCase):
    """Testes para a classe KnapsackSolution."""
    
    def setUp(self):
        """Configura dados de teste."""
        self.weights = [2, 3, 4, 5, 1]
        self.values = [3, 4, 5, 6, 2]
        self.capacity = 5
        self.problem = KnapsackProblem(self.weights, self.values, self.capacity)
        
        # Solução viável: itens 0 e 4 (peso=3, valor=5)
        self.feasible_solution = KnapsackSolution([1, 0, 0, 0, 1], self.problem)
        
        # Solução inviável: todos os itens (peso=15, valor=20)
        self.infeasible_solution = KnapsackSolution([1, 1, 1, 1, 1], self.problem)
    
    def test_valid_solution_creation(self):
        """Testa criação de solução válida."""
        binary = [1, 0, 1, 0, 0]
        solution = KnapsackSolution(binary, self.problem)
        
        self.assertEqual(solution.binary_solution, binary)
        self.assertEqual(solution.problem, self.problem)
    
    def test_invalid_solution_creation(self):
        """Testa validação na criação de soluções inválidas."""
        # Tamanho incorreto
        with self.assertRaises(ValueError):
            KnapsackSolution([1, 0], self.problem)
        
        # Valores não binários
        with self.assertRaises(ValueError):
            KnapsackSolution([1, 0, 2, 0, 1], self.problem)
    
    def test_feasible_solution_properties(self):
        """Testa propriedades de solução viável."""
        self.assertEqual(self.feasible_solution.total_weight, 3)
        self.assertEqual(self.feasible_solution.total_value, 5)
        self.assertTrue(self.feasible_solution.is_feasible)
        self.assertEqual(self.feasible_solution.weight_excess, 0)
        self.assertEqual(self.feasible_solution.selected_items, [0, 4])
        self.assertAlmostEqual(self.feasible_solution.capacity_utilization, 0.6)
    
    def test_infeasible_solution_properties(self):
        """Testa propriedades de solução inviável."""
        self.assertEqual(self.infeasible_solution.total_weight, 15)
        self.assertEqual(self.infeasible_solution.total_value, 20)
        self.assertFalse(self.infeasible_solution.is_feasible)
        self.assertEqual(self.infeasible_solution.weight_excess, 10)
        self.assertEqual(self.infeasible_solution.selected_items, [0, 1, 2, 3, 4])
        self.assertEqual(self.infeasible_solution.capacity_utilization, 3.0)
    
    def test_flip_item(self):
        """Testa inversão de itens."""
        original = [1, 0, 0, 0, 1]
        solution = KnapsackSolution(original, self.problem)
        
        # Inverter item 1
        new_solution = solution.flip_item(1)
        expected = [1, 1, 0, 0, 1]
        
        self.assertEqual(new_solution.binary_solution, expected)
        self.assertEqual(solution.binary_solution, original)  # Original não mudou
        
        # Índice inválido
        with self.assertRaises(IndexError):
            solution.flip_item(10)
    
    def test_copy(self):
        """Testa cópia de solução."""
        copy_solution = self.feasible_solution.copy()
        
        self.assertEqual(copy_solution.binary_solution, self.feasible_solution.binary_solution)
        self.assertEqual(copy_solution.problem, self.feasible_solution.problem)
        self.assertIsNot(copy_solution, self.feasible_solution)
    
    def test_equality(self):
        """Testa comparação de soluções."""
        solution1 = KnapsackSolution([1, 0, 0, 0, 1], self.problem)
        solution2 = KnapsackSolution([1, 0, 0, 0, 1], self.problem)
        solution3 = KnapsackSolution([0, 1, 0, 0, 1], self.problem)
        
        self.assertEqual(solution1, solution2)
        self.assertNotEqual(solution1, solution3)
        self.assertNotEqual(solution1, "not a solution")
    
    def test_string_representations(self):
        """Testa representações em string."""
        str_repr = str(self.feasible_solution)
        self.assertIn("value=5", str_repr)
        self.assertIn("weight=3/5", str_repr)
        self.assertIn("feasible=True", str_repr)
        
        repr_str = repr(self.feasible_solution)
        self.assertIn("binary=[1, 0, 0, 0, 1]", repr_str)
        self.assertIn("value=5", repr_str)


if __name__ == '__main__':
    unittest.main() 