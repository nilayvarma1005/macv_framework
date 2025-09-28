### `main.py`
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from macv.evaluation import run_evaluation
from macv.config import RESULTS_FILE

def main():
    """Main function to run evaluation and generate plots."""
    
    # Run the evaluation
    # Note: In a real run, you'd merge this with existing results
    # or load from file if it exists.
    print("Running MACV evaluation...")
    results_df = run_evaluation()
    results_df.to_csv(RESULTS_FILE, index=False)
    print(f"Evaluation complete. Results saved to {RESULTS_FILE}")

    # --- Plotting ---
    # This section assumes the CSV has all the data from the user's original file.
    # For this generated repo, it will only have the MACV results.
    # To generate the full plots, you would need to run all models (RAG, etc.)
    # and combine the data. The `evaluation_analysis.ipynb` is better for this.
    
    print("Generating plots (this is a placeholder; see `notebooks/evaluation_analysis.ipynb` for full analysis)...")
    
    # Example of a simple plot:
    if not results_df.empty:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=results_df, x='dataset', hue='macv_decision')
        plt.title('MACV Decisions per Dataset')
        plt.savefig('images/macv_decisions.png')
        print("Saved a sample plot to `images/macv_decisions.png`")

if __name__ == "__main__":
    main()