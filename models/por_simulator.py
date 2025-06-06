import random
import numpy as np
import pandas as pd
import logging
from typing import Tuple, Optional, Callable
from tqdm import tqdm
from models.por_formal_models import PoRModel

logger = logging.getLogger(__name__)


class PoRSimulator:
    """Monte Carlo simulator for PoR (Point of Resonance)."""

    def __init__(self, model: PoRModel = PoRModel, seed: Optional[int] = None) -> None:
        """Initialize simulator with a PoR model and optional random seed."""
        self.model = model
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        logger.info("PoRSimulator initialized with seed=%s", seed)

    def validate_range(self, range_tuple: Tuple[float, float], name: str) -> None:
        """Validate that range tuple is valid (min <= max, non-negative)."""
        if range_tuple[0] > range_tuple[1]:
            raise ValueError(f"{name} range min must <= max: {range_tuple}")
        if range_tuple[0] < 0:
            raise ValueError(f"{name} range cannot be negative: {range_tuple}")

    def sample_params(
        self,
        n: int,
        q_range: Tuple[float, float] = (0.0, 1.0),
        s_range: Tuple[float, float] = (0.0, 1.0),
        t_range: Tuple[float, float] = (0.0, 1.0),
        distribution: Callable[[float, float, int], np.ndarray] = np.random.uniform,
    ) -> np.ndarray:
        """Sample random parameters for Q, S_q, and t."""
        self.validate_range(q_range, "Q")
        self.validate_range(s_range, "S_q")
        self.validate_range(t_range, "t")

        try:
            q = distribution(q_range[0], q_range[1], size=n)
            s = distribution(s_range[0], s_range[1], size=n)
            t = distribution(t_range[0], t_range[1], size=n)
            samples = np.vstack([q, s, t]).T
        except TypeError:
            # Fallback to Python loop if distribution signature differs
            samples = np.zeros((n, 3))
            for i in tqdm(range(n), desc="Sampling parameters"):
                samples[i, 0] = distribution(q_range[0], q_range[1])
                samples[i, 1] = distribution(s_range[0], s_range[1])
                samples[i, 2] = distribution(t_range[0], t_range[1])
        return samples

    def run(
        self,
        samples: np.ndarray,
        output_file: Optional[str] = None,
    ) -> np.ndarray:
        """Compute existence scores ``E`` for each sample."""
        n = len(samples)
        results = np.empty(n)
        for i, (q, s, t) in enumerate(tqdm(samples, desc="Computing E")):
            try:
                results[i] = self.model.existence(q, s, t)
            except Exception as e:
                logger.error(
                    "Error at sample %s: Q=%s, S_q=%s, t=%s, error=%s",
                    i,
                    q,
                    s,
                    t,
                    e,
                )
                results[i] = np.nan

        if output_file:
            df = pd.DataFrame({"Q": samples[:, 0], "S_q": samples[:, 1], "t": samples[:, 2], "E": results})
            df.to_csv(output_file, index=False)
            logger.info("Results saved to %s", output_file)

        return results

    def simulate_distribution(
        self,
        n: int = 1000,
        q_range: Tuple[float, float] = (0.0, 1.0),
        s_range: Tuple[float, float] = (0.0, 1.0),
        t_range: Tuple[float, float] = (0.0, 1.0),
        distribution: Callable[[float, float, int], np.ndarray] = np.random.uniform,
        output_file: Optional[str] = None,
    ) -> np.ndarray:
        """Sample parameters and compute the resulting ``E`` distribution."""
        logger.info("Starting simulation: n=%s, output_file=%s", n, output_file)
        samples = self.sample_params(n, q_range, s_range, t_range, distribution)
        results = self.run(samples, output_file)
        logger.info("Simulation completed")
        return results
