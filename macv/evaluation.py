import pandas as pd
from datasets import load_dataset
from tqdm import tqdm
from macv.config import DATASETS, NUM_SAMPLES_PER_DATASET
from macv.orchestrator import Orchestrator

def run_evaluation():
    """Runs the full evaluation across all datasets and models."""
    results = []
    
    for name, config in DATASETS.items():
        dataset = load_dataset(config["path"], split=config["split"])
        samples = dataset.select(range(NUM_SAMPLES_PER_DATASET))
        
        for item in tqdm(samples, desc=f"Evaluating {name}"):
            prompt = item[config["question_col"]]
            
            # Run MACV (Full)
            orchestrator = Orchestrator(use_fcs=True, use_dsv=True, use_ats=True)
            response, decision, reason = orchestrator.execute(prompt, config["domain"])
            
            # This is a simplified result structure.
            # The original script had more models (RAG, Self-Correction) which can be added here.
            results.append({
                "dataset": name,
                "prompt": prompt,
                "macv_response": response,
                "macv_decision": decision,
                "macv_reason": reason,
            })

    df = pd.DataFrame(results)
    return df