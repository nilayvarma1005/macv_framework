import openai
from macv.config import OPENAI_API_KEY

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_llm_response(prompt: str, model: str = "gpt-4-turbo", temperature: float = 0.1) -> str:
    """
    Fetches a response from the specified OpenAI model.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return ""