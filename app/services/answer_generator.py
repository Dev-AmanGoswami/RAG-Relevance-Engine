from openai import OpenAI
from utils.prompt_extracter import get_prompt
from pathlib import Path
from config import ANSWER_GENERATOR_MODEL

client = OpenAI()
PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "answer_generator.txt"

def generate_answer(
    question: str,
    context: str
) -> str:
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Invalid question input.")
    
    if not isinstance(context, str) or not context.strip():
        return "I could not find enough relevant policy information to answer this question."

    response = client.responses.create(
        model = ANSWER_GENERATOR_MODEL,
        input = [
            {
                "role": "system",
                "content": get_prompt(
                    path = PROMPT_PATH
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question.strip()}\n\n"
                    f"Context:\n{context.strip()}\n"
                )
            }
        ]
    )
    answer = response.output_text

    if not answer or not answer.strip():
        raise RuntimeError(
            "Answer generation returned empty output"
        )

    return answer.strip()