"""Main module for generating synthetic scientific papers."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
from faker import Faker
import argparse
from .services.llm_service import LLMService


class PaperGenerator:
    """Generator for synthetic scientific papers."""

    def __init__(
        self,
        config_path: Optional[Path] = None,
        llm_provider: str = "azure",
        llm_model: str = "gpt-4o-mini",
        use_llm: bool = True,
    ) -> None:
        """Initialize the paper generator.

        Args:
            config_path: Path to the configuration file
            llm_provider: LLM provider to use for content generation
            llm_model: Specific LLM model to use
            use_llm: Whether to use LLM for content generation
        """
        self.fake = Faker()
        self.config = self._load_config(config_path)
        self.use_llm = use_llm
        if self.use_llm:
            self.llm_service = LLMService(provider=llm_provider, model=llm_model)
        else:
            self.llm_service = None

    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to the configuration file

        Returns:
            Configuration dictionary
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        with open(config_path) as f:
            return yaml.safe_load(f)

    def generate_paper_metadata(self) -> Dict[str, str]:
        """Generate metadata for the paper.

        Returns:
            Dictionary containing paper metadata
        """
        return {
            "title": self.fake.catch_phrase(),
            "authors": [self.fake.name() for _ in range(3)],
            "institution": f"{self.fake.company()} University",
            "field": self.fake.random_element(self.config["fields"]),
            "topics": self.fake.random_elements(
                self.config["topics"],
                length=self.fake.random_int(2, 4),
                unique=True
            ),
        }

    def generate_paper_content(self, metadata: Dict[str, str]) -> Dict[str, str]:
        """Generate the content of the paper.

        Args:
            metadata: Paper metadata dictionary

        Returns:
            Dictionary containing paper sections
        """
        if self.use_llm and self.llm_service:
            # Generate abstract
            abstract = self.llm_service.generate_section(
                "abstract",
                {
                    "title": metadata["title"],
                    "field": metadata["field"],
                    "topics": ", ".join(metadata["topics"]),
                }
            )

            # Generate introduction
            introduction = self.llm_service.generate_section(
                "introduction",
                {
                    "title": metadata["title"],
                    "field": metadata["field"],
                    "topics": ", ".join(metadata["topics"]),
                    "objectives": "To investigate " + ", ".join(metadata["topics"]),
                }
            )
        else:
            # Use Faker to generate synthetic content
            abstract = " ".join(self.fake.sentences(nb=5))
            introduction = self.fake.paragraph(nb_sentences=7)

        return {
            "abstract": abstract,
            "introduction": introduction,
            # Add more sections as needed
        }

    def generate_paper(self) -> Dict[str, Any]:
        """Generate a complete synthetic paper.

        Returns:
            Dictionary containing the complete paper
        """
        metadata = self.generate_paper_metadata()
        content = self.generate_paper_content(metadata)
        
        return {
            "metadata": metadata,
            "content": content,
        }


def main() -> None:
    """Main function to generate a synthetic paper."""
    parser = argparse.ArgumentParser(description="Generate a synthetic scientific paper.")
    parser.add_argument(
        "--use-llm",
        type=str,
        default="false",
        help="Whether to use LLM for content generation (true/false). Default: false",
    )
    args = parser.parse_args()
    use_llm = args.use_llm.lower() == "true"

    generator = PaperGenerator(use_llm=use_llm)
    paper = generator.generate_paper()
    
    # Print the generated paper
    print("\n=== Generated Paper ===\n")
    print(f"Title: {paper['metadata']['title']}")
    print(f"Authors: {', '.join(paper['metadata']['authors'])}")
    print(f"Institution: {paper['metadata']['institution']}")
    print(f"Field: {paper['metadata']['field']}")
    print(f"Topics: {', '.join(paper['metadata']['topics'])}")
    print("\n=== Abstract ===\n")
    print(paper['content']['abstract'])
    print("\n=== Introduction ===\n")
    print(paper['content']['introduction'])


if __name__ == "__main__":
    main()