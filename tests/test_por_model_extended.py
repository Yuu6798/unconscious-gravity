
#!/usr/bin/env python3
# extended tests for PoR model structure validation

import unittest
from models.por_model import PoRModel

 class TestPoRModelExtended(unittest.TestCase):
     def test_refire_difference_boundary(self):
         self.assertAlmostEqual(PoRModel.refire_difference(0.5001, 0.5), 0.0001, places=4)
     ...

class TestPoRModelExtended(unittest.TestCase):

    def test_refire_difference_boundary(self):
        self.assertAlmostEqual(PoRModel.refire_difference(0.5001, 0.5), 0.0001, places=4)

    def test_phase_gradient_boundary(self):
        self.assertAlmostEqual(PoRModel.phase_gradient(0.5, 1.0), 0.5, delta=0.01)
        self.assertAlmostEqual(PoRModel.phase_gradient(0.5, 0.0), 0.0, delta=0.01)

    def test_self_coherence_zero_input(self):
        result = PoRModel.self_coherence(0.5, 0, 0)
        self.assertEqual(result, 0)

    def test_collapse_frequency_boundary(self):
        r = PoRModel.por_collapse_frequency(0.5, 0.5)
        expected = 0.5 * 2.71828**-0.5
        self.assertAlmostEqual(r, expected, delta=0.01)

    def test_null_detection(self):
        output_pos = "semantic gravity resonance was detected"
        output_neg = "this is generic output"
        self.assertTrue(PoRModel.is_por_structure(output_pos))
        self.assertFalse(PoRModel.is_por_structure(output_neg))

    def test_invalid_input_eval(self):
        with self.assertRaises(TypeError):
            PoRModel.phase_gradient("high", 0.5)
        with self.assertRaises(TypeError):
            PoRModel.phase_gradient(0.5, None)

if __name__ == "__main__":
    unittest.main()