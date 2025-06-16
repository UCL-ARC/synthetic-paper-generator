"""LLM service for generating synthetic paper content using various LLM providers."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import litellm
from dotenv import load_dotenv


class LLMService:
    """Service for interacting with various LLM providers using litellm."""

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> None:
        """Initialize the LLM service.

        Args:
            provider: The LLM provider to use (default: "openai")
            model: The specific model to use (default: "gpt-4-turbo-preview")
            temperature: Controls randomness in generation (default: 0.7)
            max_tokens: Maximum tokens in the response (default: 2000)
        """
        load_dotenv()
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._configure_litellm()

    def _configure_litellm(self) -> None:
        """Configure litellm with environment variables."""
        # Set API keys from environment variables
        if self.provider == "openai":
            litellm.api_key = os.getenv("OPENAI_API_KEY")
        elif self.provider == "anthropic":
            litellm.api_key = os.getenv("ANTHROPIC_API_KEY")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Generate text using the configured LLM.

        Args:
            prompt: The main prompt for text generation
            system_prompt: Optional system prompt to guide the model
            **kwargs: Additional arguments to pass to the LLM

        Returns:
            The generated text
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = litellm.completion(
            model=f"{self.provider}/{self.model}",
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs,
        )

        return response.choices[0].message.content

    def generate_section(
        self,
        section_name: str,
        template_vars: Dict[str, str],
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate a specific section of the paper using a template.

        Args:
            section_name: Name of the section to generate (e.g., "abstract", "introduction")
            template_vars: Variables to fill in the template
            system_prompt: Optional system prompt to guide the model

        Returns:
            The generated section text
        """
        # Load the appropriate template
        template_path = Path(__file__).parent.parent / "prompts" / f"{section_name}.txt"
        if not template_path.exists():
            raise ValueError(f"Template not found for section: {section_name}")

        with open(template_path) as f:
            template = f.read()

        # Fill in the template
        prompt = template.format(**template_vars)
        return self.generate_text(prompt, system_prompt) 