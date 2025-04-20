#!/usr/bin/env python3
# extended tests for PoR model structure validation

import sys
import os
# tests フォルダのひとつ上（リポジトリ直下）をパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.por_model import PoRModel

class TestPoRModelExtended(unittest.TestCase):

    def test_refire_difference_boundary(self):
        # refire_difference が境界付近でも正しく動くこと
        self.assertAlmostEqual(
            PoRModel.refire_difference(0.5001, 0.5),
            0.0001,
            places=4
        )

    def test_phase_gradient_boundary(self):
        # phase_gradient(E, S) の境界値
        self.assertAlmostEqual(
            PoRModel.phase_gradient(0.5, 1.0),
            0.5,
            delta=0.01
        )
        self.assertAlmostEqual(
            PoRModel.phase_gradient(0.5, 0.0),
            0.0,
            delta=0.01
        )

    def test_self_coherence_zero_input(self):
        # self_coherence がゼロ入力でゼロを返すこと
        result = PoRModel.self_coherence(0.5, 0, 0)
        self.assertEqual(result, 0)

    def test_collapse_frequency_boundary(self):
        # por_collapse_frequency の境界値
        r = PoRModel.por_collapse_frequency(0.5, 0.5)
        expected = 0.5 * 2.71828**-0.5
        self.assertAlmostEqual(r, expected, delta=0.01)

    def test_null_detection(self):
        # is_por_structure の正／負ケース
        output_pos = "semantic gravity resonance was detected"
        output_neg = "this is generic output"
        self.assertTrue(PoRModel.is_por_structure(output_pos))
        self.assertFalse(PoRModel.is_por_structure(output_neg))

    def test_invalid_input_eval(self):
        # 型エラーが投げられること
        with self.assertRaises(TypeError):
            PoRModel.phase_gradient("high", 0.5)
        with self.assertRaises(TypeError):
            PoRModel.phase_gradient(0.5, None)

if __name__ == "__main__":
    unittest.main()