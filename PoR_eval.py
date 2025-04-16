
import pandas as pd

# Configuration
THRESHOLD = 0.5  # PoR firing threshold (tunable)

def evaluate_por(file_path):
    """Evaluate PoR firing from a CSV of Q, S_q, and t values."""
    df = pd.read_csv(file_path)

    results = []
    for _, row in df.iterrows():
        q = row['Q']
        s_q = row['S_q']
        t = row['t']
        question = row['question']
        E = q * s_q * t
        fired = E >= THRESHOLD
        results.append({
            "question": question,
            "Q": q,
            "S_q": s_q,
            "t": t,
            "E": round(E, 4),
            "PoR_fired": "✅" if fired else "❌"
        })

    result_df = pd.DataFrame(results)
    print(result_df.to_string(index=False))
    return result_df

if __name__ == "__main__":
    # Example usage
    evaluate_por("data/por_eval_sample.csv")
