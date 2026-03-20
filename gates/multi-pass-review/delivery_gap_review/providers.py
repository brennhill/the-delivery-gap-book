"""LLM provider adapters."""

import sys


def review_with_anthropic(diff: str, perspective: dict, model: str) -> dict:
    try:
        import anthropic
    except ImportError:
        print("pip install anthropic", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"{perspective['prompt']}\n\n---\n\nDiff to review:\n\n{diff}",
            }
        ],
    )
    return {
        "perspective": perspective["name"],
        "result": response.content[0].text,
        "cost": None,
    }


def review_with_openai(diff: str, perspective: dict, model: str) -> dict:
    try:
        import openai
    except ImportError:
        print("pip install openai", file=sys.stderr)
        sys.exit(1)

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"{perspective['prompt']}\n\n---\n\nDiff to review:\n\n{diff}",
            }
        ],
    )
    return {
        "perspective": perspective["name"],
        "result": response.choices[0].message.content,
        "cost": None,
    }


def review_with_litellm(diff: str, perspective: dict, model: str) -> dict:
    """Use LiteLLM as a unified proxy — supports 100+ providers and tracks costs."""
    try:
        import litellm
    except ImportError:
        print("pip install litellm", file=sys.stderr)
        sys.exit(1)

    response = litellm.completion(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"{perspective['prompt']}\n\n---\n\nDiff to review:\n\n{diff}",
            }
        ],
    )
    cost = getattr(response, "_hidden_params", {}).get("response_cost", None)
    return {
        "perspective": perspective["name"],
        "result": response.choices[0].message.content,
        "cost": cost,
    }


PROVIDERS = {
    "anthropic": review_with_anthropic,
    "openai": review_with_openai,
    "litellm": review_with_litellm,
}
