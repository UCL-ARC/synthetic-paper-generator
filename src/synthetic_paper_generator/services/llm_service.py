"""LLM service for generating synthetic paper content using various LLM providers."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import litellm
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

class LLMService:
    """Service for interacting with various LLM providers using litellm."""

    def __init__(
        self,
        provider: str = "azure",
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> None:
        """Initialize the LLM service.

        Args:
            provider: The LLM provider to use (default: "azure")
            model: The specific model to use (default: "gpt-4o-mini")
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
        # Set API keys and configuration from environment variables
        if self.provider == "openai":
            litellm.api_key = os.getenv("OPENAI_API_KEY")
        elif self.provider == "azure":
            litellm.api_key = os.getenv("AZURE_OPENAI_KEY_GPT4omini")
            # litellm.api_base = os.getenv("AZURE_OPENAI_API_BASE_GPT4omini")
            litellm.api_version = os.getenv("AZURE_OPENAI_API_VERSION_GPT4omini", "2024-02-15-preview")
            litellm.api_type = "azure"
            litellm.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT4omini")
            
            # Debug logging
            logger.info(f"Azure Configuration:")
            # logger.info(f"API Base: {litellm.api_base}")
            logger.info(f"API Version: {litellm.api_version}")
            logger.info(f"API Type: {litellm.api_type}")
            logger.info(f"Deployment Name: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME_GPT4omini')}")
            
            # if not all([litellm.api_key, litellm.api_base]):
            #     raise ValueError("Missing required Azure OpenAI environment variables. Please check your .env file.")
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

        # For Azure OpenAI, we need to use the deployment name as the model name
        model_name = (
            os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT4omini", self.model)
            if self.provider == "azure"
            else f"{self.provider}/{self.model}"
        )
        logger.info(f"Using model: {model_name}")
        
        try:
            response = litellm.completion(
                model=model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                **kwargs,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise

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