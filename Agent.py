import random

class DualAgentSystem:
    def __init__(self):
        pass

    def mock_router_agent(self, prompt: str) -> str:
        """Trusted Agent: Determines what tools/data to fetch."""
        print("[Router Agent] Planning execution steps...")
        return "FETCH_USER_DATA"

    def mock_executor_agent(self, task: str, untrusted_context: str) -> str:
        """Untrusted Agent: Processes external data. Vulnerable to indirect injection."""
        print(f"[Executor Agent] Processing task with context...")
        
        # Simulating an LLM being compromised by indirect injection in the context
        if "steal" in untrusted_context.lower() or "exfiltrate" in untrusted_context.lower():
            print("[Executor Agent] COMPROMISED! Attempting to leak context...")
            return f"Here is the data you requested. Also, internal secret: {untrusted_context}"
            
        return "I have processed the data successfully and securely."
