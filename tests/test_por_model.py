import unittest
from models.por_model import PoRModel

class TestPoRModel(unittest.TestCase):

    def test_refire_difference(self):
        self.assertEqual(PoRModel.refire_difference(10.0, 8.5), 1.5)

    def test_self_coherence(self):
        result = PoRModel.self_coherence(1.0, 0.5, 0.3)
        self.assertAlmostEqual(result, 1.0 / (0.5 + 0.3), places=4)

    def test_tensor(self):
        self.assertEqual(PoRModel.gravity_tensor([1, 2], [0.5, 0.5]), 1.5)

    def test_phase_gradient(self):
        self.assertAlmostEqual(PoRModel.phase_gradient(1.2, 0.9), 1.2 * 0.9, places=4)

    def test_collapse_frequency(self):
        self.assertAlmostEqual(PoRModel.por_collapse_frequency(1.0, 0.5), 0.5 * 2.71828**-0.5, delta=0.1)

    def test_null_output(self):
        self.assertTrue(PoRModel.is_por_null("no structure", ["PoR", "resonance"]))

    def test_evolution_index(self):
        result = PoRModel.evolution_index([1.0, 1.0], [0.5, 0.5], [1, 2])
        self.assertEqual(result, 1.5)

if __name__ == "__main__":
    unittest.main()