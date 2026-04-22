"""Shared chat model factory for QCA CLI and server."""

from __future__ import annotations

import os
from typing import Any

DEFAULT_MODEL_FALLBACK = "nvidia:nvidia/nemotron-3-nano-30b-a3b"
DASHSCOPE_BASE_URL_FALLBACK = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def get_default_model() -> str:
    """Return the configured default chat model."""
    return os.environ.get("QCA_MODEL", DEFAULT_MODEL_FALLBACK)


def create_chat_model(model_name: str) -> tuple[Any, bool]:
    """Create a chat model and report whether streaming is supported.

    Supported model spec forms:
    - ``nvidia:<model>``
    - ``dashscope:<model>`` or ``qwen:<model>``
    - ``openai:<model>``
    - bare ``nvidia/...`` or ``qwen...`` model ids
    - any other spec supported by ``langchain.chat_models.init_chat_model``
    """
    provider, resolved_name = _split_model_spec(model_name)

    if provider == "nvidia":
        from langchain_nvidia_ai_endpoints import ChatNVIDIA

        return (
            ChatNVIDIA(
                model=resolved_name,
                api_key=os.environ.get("NVIDIA_API_KEY"),
                disable_streaming=True,
            ),
            False,
        )

    if provider == "dashscope":
        chat_model = _build_chat_openai(
            model=resolved_name,
            api_key=os.environ.get("DASHSCOPE_API_KEY")
            or os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get(
                "DASHSCOPE_BASE_URL", DASHSCOPE_BASE_URL_FALLBACK
            ),
            extra_body={
                "enable_thinking": _get_bool_env(
                    "DASHSCOPE_ENABLE_THINKING", default=False
                )
            },
            use_responses_api=False,
        )
        return chat_model, True

    if provider == "openai":
        base_url = os.environ.get("OPENAI_BASE_URL")
        kwargs = {"use_responses_api": False}
        if base_url:
            kwargs["base_url"] = base_url
        chat_model = _build_chat_openai(
            model=resolved_name,
            api_key=os.environ.get("OPENAI_API_KEY"),
            **kwargs,
        )
        return chat_model, True

    from langchain.chat_models import init_chat_model

    if provider == "anthropic":
        return init_chat_model(resolved_name, model_provider="anthropic"), True

    return init_chat_model(model_name), True


def _build_chat_openai(model: str, api_key: str | None, **kwargs: Any) -> Any:
    """Create a ChatOpenAI-compatible model with a helpful import error."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise RuntimeError(
            "langchain-openai is required for DashScope/OpenAI chat models. "
            "Install dependencies with: pip install -e ."
        ) from exc

    return ChatOpenAI(model=model, api_key=api_key, **kwargs)


def _split_model_spec(model_name: str) -> tuple[str | None, str]:
    """Infer the provider from a prefixed or bare model spec."""
    if ":" in model_name:
        provider, resolved_name = model_name.split(":", 1)
        provider = provider.lower()
        if provider == "qwen":
            provider = "dashscope"
        return provider, resolved_name

    lowered = model_name.lower()
    if model_name.startswith("nvidia/"):
        return "nvidia", model_name
    if lowered.startswith("qwen"):
        return "dashscope", model_name

    return None, model_name


def _get_bool_env(name: str, default: bool) -> bool:
    """Parse an optional boolean environment variable."""
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default

    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False

    raise ValueError(
        f"Environment variable {name} must be one of: 1, 0, true, false, yes, no, on, off"
    )
