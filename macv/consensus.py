class ConsensusMechanism:
    """Aggregates agent outputs to make a final decision."""
    def decide(self, fca_results: dict, dsv_results: dict, ats_results: dict) -> tuple:
        # Simple rule-based consensus for demonstration
        
        if dsv_results and not dsv_results.get("is_valid", True):
            return "REJECT", dsv_results.get("reasoning", "Domain-specific validation failed.")
            
        if ats_results and ats_results.get("has_issues", False):
            return "REJECT", ats_results.get("reasoning", "Adversarial test failed.")

        unsupported_claims = 0
        if fca_results:
            for claim, result in fca_results.items():
                if isinstance(result, dict) and result.get("verification") == "not supported":
                    unsupported_claims += 1
        
        if unsupported_claims > 0:
            return "REJECT", f"Found {unsupported_claims} unsupported claims."

        return "ACCEPT", "Consensus"