import time
from openai import AsyncOpenAI
from app.config import get_settings

def get_client(provider: str = "meta"):
    s = get_settings()
    if provider == "meta":
        if not s.META_API_KEY: raise ValueError("META_API_KEY not set")
        return AsyncOpenAI(api_key=s.META_API_KEY, base_url=s.META_BASE_URL), s.META_MODEL
    elif provider == "fireworks":
        if not s.FIREWORKS_API_KEY: raise ValueError("FIREWORKS_API_KEY not set")
        return AsyncOpenAI(api_key=s.FIREWORKS_API_KEY, base_url=s.FIREWORKS_BASE_URL), s.FIREWORKS_MODEL
    elif provider == "baseten":
        if not s.BASETEN_API_KEY: raise ValueError("BASETEN_API_KEY not set")
        return AsyncOpenAI(api_key=s.BASETEN_API_KEY, base_url=s.BASETEN_BASE_URL), s.META_MODEL
    raise ValueError(f"Unknown provider: {provider}")

async def stream_ping(provider: str = "meta") -> dict:
    client, model = get_client(provider)
    start = time.perf_counter()
    first_token = None
    ttft_ms = None
    token_count = 0

    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Reply with exactly: OK"}],
        stream=True,
        max_tokens=10,
        temperature=0,
    )

    async for chunk in stream:
        if not chunk.choices: continue
        content = chunk.choices[0].delta.content
        if content:
            if first_token is None:
                first_token = content
                ttft_ms = (time.perf_counter() - start) * 1000
            token_count += 1
            if token_count >= 5:
                break

    total_ms = (time.perf_counter() - start) * 1000
    return {
        "status": "ok" if first_token else "no_tokens_returned",
        "provider": provider,
        "model": model,
        "streaming_verified": first_token is not None,
        "first_token": first_token,
        "time_to_first_token_ms": round(ttft_ms, 2) if ttft_ms else None,
        "total_latency_ms": round(total_ms, 2),
        "tokens_received": token_count,
    }
