import unittest
from unittest.mock import patch
from macv.orchestrator import Orchestrator

class TestMACVFramework(unittest.TestCase):

    @patch('macv.llm_provider.get_llm_response')
    def test_orchestrator_accept(self, mock_get_llm):
        # Mock the responses from all agents to simulate an "ACCEPT" scenario
        mock_get_llm.side_effect = [
            "The sky is blue.",  # PRG response
            '["The sky is blue."]',  # Claim extraction
            '{"claim_1": {"verification": "fully supported"}}',  # FCA
            '{"is_valid": true, "reasoning": "Looks good."}',  # DSV
            '{"has_issues": false, "reasoning": "No issues found."}'  # ATS
        ]
        
        orchestrator = Orchestrator()
        response, decision, reason = orchestrator.execute("Why is the sky blue?", "science")
        
        self.assertEqual(decision, "ACCEPT")
        self.assertEqual(response, "The sky is blue.")

    @patch('macv.llm_provider.get_llm_response')
    def test_orchestrator_reject_fca(self, mock_get_llm):
        # Mock the FCA to find an unsupported claim
        mock_get_llm.side_effect = [
            "The sky is green.",
            '["The sky is green."]',
            '{"claim_1": {"verification": "not supported", "reasoning": "Evidence says it is blue."}}',
            '{"is_valid": true, "reasoning": "Plausible but needs checking."}',
            '{"has_issues": false, "reasoning": "No logical issues."}'
        ]
        
        orchestrator = Orchestrator()
        response, decision, reason = orchestrator.execute("Why is the sky green?", "science")
        
        self.assertEqual(decision, "REJECT")
        self.assertIn("unsupported claims", reason)

if __name__ == '__main__':
    unittest.main()