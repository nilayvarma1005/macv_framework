from concurrent.futures import ThreadPoolExecutor
from macv.agents import (
    PrimaryResponseGenerator,
    FactCheckingAgent,
    DomainSpecificValidator,
    AdversarialTester,
)
from macv.consensus import ConsensusMechanism
from macv.llm_provider import get_llm_response
from macv.config import AGENT_MODEL, FAST_MODEL, GENERATOR_MODEL
import json

class Orchestrator:
    """Manages the MACV workflow."""

    def __init__(self, use_fcs=True, use_dsv=True, use_ats=True):
        self.prg = PrimaryResponseGenerator()
        self.fca = FactCheckingAgent() if use_fcs else None
        self.dsv = DomainSpecificValidator() if use_dsv else None
        self.ats = AdversarialTester() if use_ats else None
        self.consensus = ConsensusMechanism()

    def _extract_claims(self, response: str) -> list:
        """Extracts factual claims from a response."""
        prompt = f"""
        Extract the key factual claims from the following text. Return them as a JSON list.
        Text: "{response}"
        """
        claims_response = get_llm_response(prompt, model=FAST_MODEL)
        try:
            return json.loads(claims_response)
        except json.JSONDecodeError:
            return [response] # Fallback to the whole response

    def execute(self, prompt: str, domain: str) -> tuple:
        """Runs the full MACV pipeline."""
        initial_response = self.prg.generate(prompt, model=GENERATOR_MODEL)
        claims = self._extract_claims(initial_response)

        fca_results, dsv_results, ats_results = {}, {}, {}

        with ThreadPoolExecutor() as executor:
            futures = {}
            if self.fca:
                futures[executor.submit(self.fca.verify, claims, prompt)] = "fca"
            if self.dsv:
                futures[executor.submit(self.dsv.validate, initial_response, domain)] = "dsv"
            if self.ats:
                futures[executor.submit(self.ats.test, initial_response)] = "ats"

            for future in futures:
                agent_name = futures[future]
                try:
                    result = future.result()
                    if agent_name == "fca":
                        fca_results = result
                    elif agent_name == "dsv":
                        dsv_results = result
                    elif agent_name == "ats":
                        ats_results = result
                except Exception as e:
                    print(f"Agent {agent_name} failed: {e}")

        decision, reason = self.consensus.decide(fca_results, dsv_results, ats_results)

        if decision == "ACCEPT":
            return initial_response, decision, reason
        else:
            return "Abstaining due to verification failure.", decision, reason