"""Tests for shared chat model factory."""

import types
from unittest.mock import MagicMock, patch

import pytest

from core.chat_models import (
    DASHSCOPE_BASE_URL_FALLBACK,
    DEFAULT_MODEL_FALLBACK,
    _get_bool_env,
    create_chat_model,
    get_default_model,
)


def _module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    return module


class TestGetDefaultModel:
    def test_uses_env_override(self, monkeypatch):
        monkeypatch.setenv("QCA_MODEL", "dashscope:qwen3.6-plus")
        assert get_default_model() == "dashscope:qwen3.6-plus"

    def test_uses_fallback(self, monkeypatch):
        monkeypatch.delenv("QCA_MODEL", raising=False)
        assert get_default_model() == DEFAULT_MODEL_FALLBACK


class TestCreateChatModel:
    def test_dashscope_prefixed_model(self, monkeypatch):
        monkeypatch.setenv("DASHSCOPE_API_KEY", "dash-key")

        mock_chat_cls = MagicMock(return_value="dashscope-model")
        mock_module = _module("langchain_openai", ChatOpenAI=mock_chat_cls)

        with patch.dict("sys.modules", {"langchain_openai": mock_module}):
            model, supports_streaming = create_chat_model(
                "dashscope:qwen3.6-plus"
            )

        assert model == "dashscope-model"
        assert supports_streaming is True
        kwargs = mock_chat_cls.call_args.kwargs
        assert kwargs["model"] == "qwen3.6-plus"
        assert kwargs["api_key"] == "dash-key"
        assert kwargs["base_url"] == DASHSCOPE_BASE_URL_FALLBACK
        assert kwargs["extra_body"] == {"enable_thinking": False}
        assert kwargs["use_responses_api"] is False

    def test_bare_qwen_model_uses_dashscope(self, monkeypatch):
        monkeypatch.setenv("DASHSCOPE_API_KEY", "dash-key")
        monkeypatch.setenv("DASHSCOPE_ENABLE_THINKING", "true")

        mock_chat_cls = MagicMock(return_value="dashscope-model")
        mock_module = _module("langchain_openai", ChatOpenAI=mock_chat_cls)

        with patch.dict("sys.modules", {"langchain_openai": mock_module}):
            model, supports_streaming = create_chat_model("qwen3.6-plus")

        assert model == "dashscope-model"
        assert supports_streaming is True
        assert (
            mock_chat_cls.call_args.kwargs["extra_body"]["enable_thinking"] is True
        )

    def test_openai_model_uses_optional_base_url(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
        monkeypatch.setenv("OPENAI_BASE_URL", "https://example.com/v1")

        mock_chat_cls = MagicMock(return_value="openai-model")
        mock_module = _module("langchain_openai", ChatOpenAI=mock_chat_cls)

        with patch.dict("sys.modules", {"langchain_openai": mock_module}):
            model, supports_streaming = create_chat_model("openai:gpt-4o")

        assert model == "openai-model"
        assert supports_streaming is True
        kwargs = mock_chat_cls.call_args.kwargs
        assert kwargs["base_url"] == "https://example.com/v1"
        assert kwargs["use_responses_api"] is False

    def test_nvidia_bare_model_disables_streaming(self, monkeypatch):
        monkeypatch.setenv("NVIDIA_API_KEY", "nv-key")

        mock_chat_cls = MagicMock(return_value="nvidia-model")
        mock_module = _module(
            "langchain_nvidia_ai_endpoints", ChatNVIDIA=mock_chat_cls
        )

        with patch.dict(
            "sys.modules", {"langchain_nvidia_ai_endpoints": mock_module}
        ):
            model, supports_streaming = create_chat_model(
                "nvidia/nemotron-3-nano-30b-a3b"
            )

        assert model == "nvidia-model"
        assert supports_streaming is False
        kwargs = mock_chat_cls.call_args.kwargs
        assert kwargs["model"] == "nvidia/nemotron-3-nano-30b-a3b"
        assert kwargs["disable_streaming"] is True

    def test_fallback_model_uses_init_chat_model(self):
        mock_init = MagicMock(return_value="fallback-model")
        langchain_module = _module("langchain")
        chat_models_module = _module("langchain.chat_models", init_chat_model=mock_init)

        with patch.dict(
            "sys.modules",
            {
                "langchain": langchain_module,
                "langchain.chat_models": chat_models_module,
            },
        ):
            model, supports_streaming = create_chat_model("claude-sonnet-4-6")

        assert model == "fallback-model"
        assert supports_streaming is True
        mock_init.assert_called_once_with("claude-sonnet-4-6")


class TestGetBoolEnv:
    def test_invalid_value_raises(self, monkeypatch):
        monkeypatch.setenv("DASHSCOPE_ENABLE_THINKING", "sometimes")

        with pytest.raises(ValueError, match="DASHSCOPE_ENABLE_THINKING"):
            _get_bool_env("DASHSCOPE_ENABLE_THINKING", default=False)
