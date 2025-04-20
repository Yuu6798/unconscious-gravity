#!/usr/bin/env python3
import sys
import os
# testsフォルダのひとつ上（リポジトリ直下）をパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.por_model import PoRModel

class TestPoRModelExtended(unittest.TestCase):

    def test_refire_difference_boundary(self):
        """再発火差分の境界チェック"""
        self.assertAlmostEqual(
            PoRModel.refire_difference(0.5001, 0.5),
            0.0001,
            places=4
        )

    def test_phase_gradient_boundary(self):
        """位相勾配の 2 引数版・境界チェック"""
        # signature: phase_gradient(E, S) の場合
        self.assertAlmostEqual(
            PoRModel.phase_gradient(1.0, 0.5, k=None, gamma=None),
            1.0 * 0.5,
            delta=1e-6
        )
        # signature: phase_gradient(k, S) の場合 (k=0.5, S=0.0 → 0.0)
        self.assertAlmostEqual(
            PoRModel.phase_gradient(0.0, 1.0, k=0.5, gamma=None),
            0.0,
            delta=1e-6
        )

    def test_self_coherence_zero_input(self):
        """自己コヒーレンスのゼロ除算エラーを確認"""
        with self.assertRaises(ZeroDivisionError):
            PoRModel.self_coherence(0.5, 0.0, 0.0)

    def test_collapse_frequency_boundary(self):
        """λ=0.5, t=0.5 として λ·e^(−λt)=0.5*e^(−0.25) をチェック"""
        r = PoRModel.por_collapse_frequency(0.5, 0.5)
        expected = 0.5 * 2.71828**(-0.25)
        self.assertAlmostEqual(r, expected, delta=0.01)

    def test_null_detection(self):
        """PoR 構造検出メソッドの正負を確認"""
        output_pos = "semantic gravity resonance was detected"
        output_neg = "this is generic output"
        self.assertTrue(PoRModel.is_por_structure(output_pos))
        self.assertFalse(PoRModel.is_por_structure(output_neg))

    def test_invalid_input_eval(self):
        """位相勾配メソッドの型エラーを確認"""
        with self.assertRaises(TypeError):
            PoRModel.phase_gradient("high", 0.5)
        with self.assertRaises(TypeError):
            PoRModel.phase_gradient(0.5, None)

if __name__ == "__main__":
    unittest.main()