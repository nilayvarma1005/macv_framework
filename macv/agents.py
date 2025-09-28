import json
from tavily import TavilyClient
from macv.config import TAVILY_API_KEY, AGENT_MODEL
from macv.llm_provider import get_llm_response

class PrimaryResponseGenerator:
    """Generates the initial response to a prompt."""
    def generate(self, prompt: str, model: str) -> str:
        return get_llm_response(prompt, model=model)

class FactCheckingAgent:
    """Verifies factual claims using external sources."""
    def __init__(self):
        self.tavily = TavilyClient(api_key=TAVILY_API_KEY)

    def verify(self, claims: list, prompt: str) -> dict:
        search_results = self.tavily.qna_search(query=prompt)
        
        verification_prompt = f"""
        Prompt: "{prompt}"
        Claims: {json.dumps(claims)}
        Search Results: "{search_results}"
        
        Review the search results and verify each claim. For each claim, determine if it is "fully supported", "partially supported", or "not supported". Provide a brief reasoning.
        
        Return a JSON object with a key for each claim.
        """
        
        response = get_llm_response(verification_prompt, model=AGENT_MODEL)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse verification response."}

class DomainSpecificValidator:
    """Validates information against a domain-specific knowledge base."""
    def validate(self, response: str, domain: str) -> dict:
        # In a real-world scenario, this would query a structured database or API.
        # Here, we simulate it with an LLM call for demonstration.
        prompt = f"""
        The following response is from the "{domain}" domain:
        "{response}"
        
        Does this response seem plausible and accurate based on your knowledge of the {domain} domain?
        Return a JSON object with "is_valid" (boolean) and "reasoning" (string).
        """
        response = get_llm_response(prompt, model=AGENT_MODEL)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"is_valid": False, "reasoning": "Failed to parse validation."}

class AdversarialTester:
    """Probes the response for logical contradictions and weaknesses."""
    def test(self, response: str) -> dict:
        prompt = f"""
        Analyze the following response for logical contradictions, inconsistencies, or flawed reasoning:
        "{response}"
        
        Are there any issues?
        Return a JSON object with "has_issues" (boolean) and "reasoning" (string).
        """
        response = get_llm_response(prompt, model=AGENT_MODEL)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"has_issues": True, "reasoning": "Failed to parse adversarial test."}