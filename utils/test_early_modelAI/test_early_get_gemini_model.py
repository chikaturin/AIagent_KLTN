# tests/test_utils_modelAI.py

import os
import pytest
from unittest import mock

# Absolute import of the function under test
from utils.modelAI import get_gemini_model


class TestGetGeminiModel:
    """Unit tests for the get_gemini_model function in utils/modelAI.py"""

    @pytest.fixture(autouse=True)
    def patch_env_and_genai(self):
        """
        Fixture to patch os.getenv and google.generativeai for all tests.
        """
        with mock.patch("utils.modelAI.os") as mock_os, mock.patch(
            "utils.modelAI.genai"
        ) as mock_genai:
            yield mock_os, mock_genai

    # ------------------- Happy Path Tests -------------------

    @pytest.mark.happy
    def test_returns_generative_model_instance(self, patch_env_and_genai):
        """
        Test that get_gemini_model returns the expected GenerativeModel instance
        when AI_API_KEY is set and genai behaves as expected.
        """
        mock_os, mock_genai = patch_env_and_genai
        mock_os.getenv.return_value = "dummy-key"
        mock_model_instance = mock.Mock(name="GenerativeModelInstance")
        mock_genai.GenerativeModel.return_value = mock_model_instance

        result = get_gemini_model()

        mock_os.getenv.assert_called_once_with("AI_API_KEY")
        mock_genai.configure.assert_called_once_with(api_key="dummy-key")
        mock_genai.GenerativeModel.assert_called_once_with("gemini-2.0-flash")
        assert result is mock_model_instance

    @pytest.mark.happy
    def test_multiple_calls_configure_and_model_called_each_time(
        self, patch_env_and_genai
    ):
        """
        Test that multiple calls to get_gemini_model call configure and GenerativeModel each time.
        """
        mock_os, mock_genai = patch_env_and_genai
        mock_os.getenv.return_value = "another-key"
        mock_model_instance = mock.Mock(name="GenerativeModelInstance")
        mock_genai.GenerativeModel.return_value = mock_model_instance

        for _ in range(3):
            result = get_gemini_model()
            assert result is mock_model_instance

        assert mock_os.getenv.call_count == 3
        assert mock_genai.configure.call_count == 3
        assert mock_genai.GenerativeModel.call_count == 3

    # ------------------- Edge Case Tests -------------------

    @pytest.mark.edge
    def test_ai_api_key_env_var_missing(self, patch_env_and_genai):
        """
        Test behavior when AI_API_KEY environment variable is missing (None).
        Should still call configure with api_key=None.
        """
        mock_os, mock_genai = patch_env_and_genai
        mock_os.getenv.return_value = None
        mock_model_instance = mock.Mock(name="GenerativeModelInstance")
        mock_genai.GenerativeModel.return_value = mock_model_instance

        result = get_gemini_model()

        mock_os.getenv.assert_called_once_with("AI_API_KEY")
        mock_genai.configure.assert_called_once_with(api_key=None)
        mock_genai.GenerativeModel.assert_called_once_with("gemini-2.0-flash")
        assert result is mock_model_instance

    @pytest.mark.edge
    def test_ai_api_key_env_var_empty_string(self, patch_env_and_genai):
        """
        Test behavior when AI_API_KEY environment variable is set to an empty string.
        Should call configure with api_key="".
        """
        mock_os, mock_genai = patch_env_and_genai
        mock_os.getenv.return_value = ""
        mock_model_instance = mock.Mock(name="GenerativeModelInstance")
        mock_genai.GenerativeModel.return_value = mock_model_instance

        result = get_gemini_model()

        mock_os.getenv.assert_called_once_with("AI_API_KEY")
        mock_genai.configure.assert_called_once_with(api_key="")
        mock_genai.GenerativeModel.assert_called_once_with("gemini-2.0-flash")
        assert result is mock_model_instance

    @pytest.mark.edge
    def test_genai_configure_raises_exception(self, patch_env_and_genai):
        """
        Test that if genai.configure raises an exception, it propagates.
        """
        mock_os, mock_genai = patch_env_and_genai
        mock_os.getenv.return_value = "key"
        mock_genai.configure.side_effect = RuntimeError("Config error")

        with pytest.raises(RuntimeError, match="Config error"):
            get_gemini_model()

        mock_os.getenv.assert_called_once_with("AI_API_KEY")
        mock_genai.configure.assert_called_once_with(api_key="key")
        mock_genai.GenerativeModel.assert_not_called()

    @pytest.mark.edge
    def test_generative_model_raises_exception(self, patch_env_and_genai):
        """
        Test that if genai.GenerativeModel raises an exception, it propagates.
        """
        mock_os, mock_genai = patch_env_and_genai
        mock_os.getenv.return_value = "key"
        mock_genai.GenerativeModel.side_effect = ValueError("Model error")

        with pytest.raises(ValueError, match="Model error"):
            get_gemini_model()

        mock_os.getenv.assert_called_once_with("AI_API_KEY")
        mock_genai.configure.assert_called_once_with(api_key="key")
        mock_genai.GenerativeModel.assert_called_once_with("gemini-2.0-flash")
