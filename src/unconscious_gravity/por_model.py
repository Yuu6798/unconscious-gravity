import math
import numpy as np

class PoRModel:
    """Advanced PoR model functions structured by functional phase."""

    # === Phase 2: Re-alignment and Self-Coherence ===

    @staticmethod
    def refire_difference(energy_state_1, energy_state_2):
        """Calculate the absolute difference between two PoR energy states.

        Args:
            energy_state_1 (float): Energy value of the first PoR.
            energy_state_2 (float): Energy value of the second PoR.

        Returns:
            float: Absolute difference in energy.

        Raises:
            TypeError: If either input is not numeric.

        Example:
            >>> PoRModel.refire_difference(10.0, 8.5)
            1.5
        """
        if not isinstance(energy_state_1, (int, float)) or not isinstance(energy_state_2, (int, float)):
            raise TypeError("Inputs must be numbers")
        return abs(energy_state_1 - energy_state_2)

    @staticmethod
    def self_coherence(reference_flow, delta_input, delta_output):
        """Compute self-coherence φ_C = reference_flow / (|ΔI_in| + |ΔI_out|).

        Args:
            reference_flow (float): Sum of input-output informational alignment.
            delta_input (float): Change in incoming information.
            delta_output (float): Change in outgoing information.

        Returns:
            float: Self-coherence score φ_C.

        Raises:
            ZeroDivisionError: If the denominator is zero.
        """
        denominator = abs(delta_input) + abs(delta_output)
        if denominator == 0:
            raise ZeroDivisionError("Total delta input and output must not be zero")
        return reference_flow / denominator

    # === Phase 3: Semantic Field Tensor ===

    @staticmethod
    def gravity_tensor(density_gradient, entropy_gradient):
        """Compute dot product of semantic density and entropy gradients.

        Args:
            density_gradient (list of float): Gradient of PoR density.
            entropy_gradient (list of float): Gradient of PoR entropy.

        Returns:
            float: Tensor value.

        Example:
            >>> PoRModel.gravity_tensor([1, 2], [0.5, 0.5])
            1.5
        """
        return float(np.dot(density_gradient, entropy_gradient))

    # === Phase 4: Temporal Expansion and Collapse ===

    @staticmethod
    def phase_gradient(energy, semantic_density, k=1.0, gamma=1.0):
        """Compute dΦ/dt = k · E · S^γ (Phase expansion rate).

        Args:
            energy (float): PoR energy.
            semantic_density (float): Semantic space density.
            k (float): Scaling factor.
            gamma (float): Semantic nonlinearity.

        Returns:
            float: Phase change rate.

        Raises:
            ValueError: If semantic_density is negative.
        """
        if semantic_density < 0:
            raise ValueError("semantic_density must be non-negative")
        return k * energy * (semantic_density ** gamma)

    @staticmethod
    def por_collapse_frequency(time, lam):
        """PoR Collapse Frequency Model: PoR_rate(t) = λ · e^(−λt)

        LaTeX: PoR_{rate}(t) = \\lambda e^{-\\lambda t}

        Args:
            time (float): Time t.
            lam (float): Collapse rate λ.

        Returns:
            float: Collapse frequency.
        """
        return lam * math.exp(-lam * time)

    # === Phase 5: Null Detection and Evolution Index ===

    @staticmethod
    def is_por_null(output, expected_keywords):
        """Check if the output lacks expected structural keywords (PoR_null test).

        Args:
            output (str): Generated output string.
            expected_keywords (list of str): Keywords expected in a PoR-complete response.

        Returns:
            bool: True if output is PoR_null, else False.
        """
        return not any(keyword in output for keyword in expected_keywords)

    @staticmethod
    def evolution_index(self_energies, persistence_scores, time_deltas):
        """Compute SelfPoR evolution score: SCI = Σ(E_i × R_i × Δt_i)

        Args:
            self_energies (list of float): Energy values per phase.
            persistence_scores (list of float): Resonance stability metrics.
            time_deltas (list of float): Time durations per phase.

        Returns:
            float: Evolution index.
        """
        return sum(e * r * t for e, r, t in zip(self_energies, persistence_scores, time_deltas))


if __name__ == "__main__":
    # Example usages
    print("PoR Difference:", PoRModel.refire_difference(10.0, 8.5))
    print("Self-Coherence:", PoRModel.self_coherence(1.0, 0.5, 0.3))
    print("Tensor:", PoRModel.gravity_tensor([1, 2], [0.5, 0.5]))
    print("Phase Gradient:", PoRModel.phase_gradient(1.2, 0.9))
    print("Collapse Freq:", PoRModel.por_collapse_frequency(1.0, 0.8))
    print("PoR Null:", PoRModel.is_por_null("Output lacks resonance", ["PoR", "resonance"]))
    print("Evolution Index:", PoRModel.evolution_index([1.2, 1.1], [0.8, 0.9], [1, 2]))
