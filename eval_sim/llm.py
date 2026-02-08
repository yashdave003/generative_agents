"""
LLM Integration for Evaluation Ecosystem Simulation

Provides multi-provider LLM support with abstract interface.

Supported Providers:
- OpenAI (GPT-4, GPT-4o-mini, etc.)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus, etc.)
- Ollama (local models like llama3, mistral, phi, gemma)
- Gemini (Gemini 2.5 Flash, Gemini 2.5 Pro, etc.)

Configuration via environment variables:
- LLM_PROVIDER: "openai", "anthropic", "ollama", or "gemini" (default: "openai")
- LLM_MODEL: Model name (provider-specific)
- OPENAI_API_KEY: Required for OpenAI provider
- ANTHROPIC_API_KEY: Required for Anthropic provider
- GEMINI_API_KEY: Required for Gemini provider
- OLLAMA_BASE_URL: Ollama server URL (default: http://localhost:11434)
"""
import json
import os
import time
from abc import ABC, abstractmethod
from typing import Callable, Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All providers must implement:
    - generate(): Basic text generation
    - generate_json(): JSON generation with validation
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-2)
            max_tokens: Max tokens in response

        Returns:
            Response text from the LLM
        """
        pass

    @abstractmethod
    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
    ) -> dict:
        """
        Generate and parse JSON response.

        Args:
            prompt: User prompt (should request JSON output)
            system_prompt: Optional system prompt
            retries: Number of retry attempts
            fail_safe: Dict to return if parsing fails

        Returns:
            Parsed JSON dict, or fail_safe if parsing fails
        """
        pass

    def safe_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        func_validate: Optional[Callable[[str], bool]] = None,
        func_cleanup: Optional[Callable[[str], any]] = None,
        retries: int = 3,
        fail_safe: any = None,
        verbose: bool = False,
        **kwargs,
    ) -> any:
        """
        Generate with validation, cleanup, and retry logic.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            func_validate: Function that returns True if response is valid
            func_cleanup: Function to clean/parse the response
            retries: Number of retry attempts
            fail_safe: Value to return if all retries fail
            verbose: Print debug info
            **kwargs: Additional args passed to generate()

        Returns:
            Cleaned response, or fail_safe if validation fails
        """
        for attempt in range(retries):
            response = self.generate(prompt, system_prompt, **kwargs)

            if verbose:
                print(f"Attempt {attempt + 1}: {response[:100]}...")

            # Skip validation if no validator provided
            if func_validate is None:
                if func_cleanup:
                    return func_cleanup(response)
                return response

            # Validate
            try:
                if func_validate(response):
                    if func_cleanup:
                        return func_cleanup(response)
                    return response
            except Exception as e:
                if verbose:
                    print(f"Validation error: {e}")

            if verbose:
                print(f"Attempt {attempt + 1} failed validation")

        if verbose:
            print(f"All {retries} attempts failed, returning fail_safe")
        return fail_safe


class OpenAIProvider(LLMProvider):
    """
    OpenAI API provider.

    Requires openai package and OPENAI_API_KEY environment variable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key. If None, uses OPENAI_API_KEY env var.
            model: Model to use (default: gpt-4o-mini for cost efficiency)
            temperature: Default sampling temperature (0-2)
            max_tokens: Default max tokens in response
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai package not installed. Run: pip install openai"
            )

        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 0.1  # seconds between calls

    def _rate_limit(self):
        """Simple rate limiting to avoid hitting API limits."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)
        self.last_call_time = time.time()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
    ) -> str:
        """Generate a response from OpenAI."""
        self._rate_limit()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.default_temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.default_max_tokens,
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return f"ERROR: {e}"

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response from OpenAI."""
        def validate_json(response: str) -> bool:
            try:
                json.loads(response)
                return True
            except:
                return False

        def cleanup_json(response: str) -> dict:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            return json.loads(response.strip())

        return self.safe_generate(
            prompt=prompt,
            system_prompt=system_prompt,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
            json_mode=True,
        )


class AnthropicProvider(LLMProvider):
    """
    Anthropic Claude API provider.

    Requires anthropic package and ANTHROPIC_API_KEY environment variable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ):
        """
        Initialize Anthropic provider.

        Args:
            api_key: Anthropic API key. If None, uses ANTHROPIC_API_KEY env var.
            model: Model to use (default: claude-3-5-sonnet-20241022)
            temperature: Default sampling temperature (0-1)
            max_tokens: Default max tokens in response
        """
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Run: pip install anthropic"
            )

        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 0.1  # seconds between calls

    def _rate_limit(self):
        """Simple rate limiting to avoid hitting API limits."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)
        self.last_call_time = time.time()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate a response from Anthropic Claude."""
        self._rate_limit()

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens if max_tokens is not None else self.default_max_tokens,
                temperature=temperature if temperature is not None else self.default_temperature,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            print(f"Anthropic API Error: {e}")
            return f"ERROR: {e}"

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response from Anthropic Claude."""
        # Enhance system prompt to request JSON output
        json_system = system_prompt or ""
        if json_system:
            json_system += " Always respond with valid JSON only, no additional text."
        else:
            json_system = "Always respond with valid JSON only, no additional text."

        def validate_json(response: str) -> bool:
            try:
                cleaned = _extract_json(response)
                json.loads(cleaned)
                return True
            except:
                return False

        def cleanup_json(response: str) -> dict:
            cleaned = _extract_json(response)
            return json.loads(cleaned)

        return self.safe_generate(
            prompt=prompt,
            system_prompt=json_system,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
        )


class OllamaProvider(LLMProvider):
    """
    Ollama local LLM provider.

    Requires Ollama to be running locally (default: http://localhost:11434).
    No API key needed for local usage.
    """

    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ):
        """
        Initialize Ollama provider.

        Args:
            model: Model to use (default: llama3)
            base_url: Ollama server URL
            temperature: Default sampling temperature
            max_tokens: Default max tokens (note: Ollama uses num_predict)
        """
        try:
            import requests
        except ImportError:
            raise ImportError(
                "requests package not installed. Run: pip install requests"
            )

        self.model = model
        self.base_url = base_url.rstrip("/")
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        # Verify Ollama is running
        self._verify_connection()

    def _verify_connection(self):
        """Verify Ollama server is reachable."""
        import requests
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                print(f"Warning: Ollama server returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"Warning: Could not connect to Ollama at {self.base_url}")
            print("Make sure Ollama is running: ollama serve")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate a response from Ollama."""
        import requests

        # Build the full prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature if temperature is not None else self.default_temperature,
                "num_predict": max_tokens if max_tokens is not None else self.default_max_tokens,
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120,  # Longer timeout for local models
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.ConnectionError:
            return "ERROR: Could not connect to Ollama. Make sure it's running."
        except requests.exceptions.Timeout:
            return "ERROR: Ollama request timed out."
        except Exception as e:
            print(f"Ollama API Error: {e}")
            return f"ERROR: {e}"

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response from Ollama."""
        # Enhance prompt to request JSON output
        json_prompt = prompt + "\n\nRespond with valid JSON only. No explanation, just the JSON object."

        if system_prompt:
            system_prompt = system_prompt + " Always respond with valid JSON only."

        def validate_json(response: str) -> bool:
            try:
                # Try to find JSON in the response
                cleaned = _extract_json(response)
                json.loads(cleaned)
                return True
            except:
                return False

        def cleanup_json(response: str) -> dict:
            cleaned = _extract_json(response)
            return json.loads(cleaned)

        return self.safe_generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
        )


class GeminiProvider(LLMProvider):
    """
    Google Gemini API provider.

    Requires google-genai package and GEMINI_API_KEY environment variable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ):
        """
        Initialize Gemini provider.

        Args:
            api_key: Gemini API key. If None, uses GEMINI_API_KEY env var.
            model: Model to use (default: gemini-2.5-flash)
            temperature: Default sampling temperature (0-2)
            max_tokens: Default max tokens in response
        """
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            raise ImportError(
                "google-genai package not installed. Run: pip install google-genai"
            )

        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = genai.Client(api_key=self.api_key)
        self.types = types
        self.model = model
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 0.1  # seconds between calls

    def _rate_limit(self):
        """Simple rate limiting to avoid hitting API limits."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)
        self.last_call_time = time.time()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate a response from Google Gemini."""
        self._rate_limit()

        try:
            config = self.types.GenerateContentConfig(
                temperature=temperature if temperature is not None else self.default_temperature,
                max_output_tokens=max_tokens if max_tokens is not None else self.default_max_tokens,
                system_instruction=system_prompt,
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return f"ERROR: {e}"

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response from Google Gemini."""
        # Enhance prompt to request JSON output
        json_prompt = prompt + "\n\nRespond with valid JSON only. No explanation, just the JSON object."

        if system_prompt:
            system_prompt = system_prompt + " Always respond with valid JSON only."

        def validate_json(response: str) -> bool:
            try:
                cleaned = _extract_json(response)
                json.loads(cleaned)
                return True
            except:
                return False

        def cleanup_json(response: str) -> dict:
            cleaned = _extract_json(response)
            return json.loads(cleaned)

        return self.safe_generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
        )


def _extract_json(response: str) -> str:
    """Extract JSON from a response that may contain extra text."""
    response = response.strip()

    # Remove markdown code blocks
    if response.startswith("```json"):
        response = response[7:]
    if response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    # Try to find JSON object boundaries
    start = response.find("{")
    end = response.rfind("}") + 1
    if start != -1 and end > start:
        return response[start:end]

    return response


# --- Provider Factory ---

_default_provider: Optional[LLMProvider] = None


def create_llm_provider(
    provider: Optional[str] = None,
    **kwargs,
) -> LLMProvider:
    """
    Create an LLM provider based on configuration.

    Args:
        provider: Provider name ("openai", "anthropic", "ollama", or "gemini").
                 If None, uses LLM_PROVIDER env var (default: "openai")
        **kwargs: Additional arguments passed to provider constructor

    Returns:
        LLMProvider instance

    Environment Variables:
        LLM_PROVIDER: Provider name (openai, anthropic, ollama, gemini)
        LLM_MODEL: Model name (provider-specific)
        OPENAI_API_KEY: For OpenAI provider
        ANTHROPIC_API_KEY: For Anthropic provider
        GEMINI_API_KEY: For Gemini provider
        OLLAMA_BASE_URL: For Ollama provider
    """
    provider = provider or os.getenv("LLM_PROVIDER", "openai")

    if provider == "ollama":
        return OllamaProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "llama3"),
            base_url=kwargs.get("base_url") or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 500),
        )
    elif provider == "anthropic":
        return AnthropicProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "claude-3-5-sonnet-20241022"),
            api_key=kwargs.get("api_key") or os.getenv("ANTHROPIC_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 500),
        )
    elif provider == "gemini":
        return GeminiProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "gemini-2.5-flash"),
            api_key=kwargs.get("api_key") or os.getenv("GEMINI_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 500),
        )
    elif provider == "openai":
        return OpenAIProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "gpt-4o-mini"),
            api_key=kwargs.get("api_key") or os.getenv("OPENAI_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 500),
        )
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'openai', 'anthropic', 'ollama', or 'gemini'.")


def get_provider() -> LLMProvider:
    """Get or create the default LLM provider."""
    global _default_provider
    if _default_provider is None:
        _default_provider = create_llm_provider()
    return _default_provider


def set_provider(provider: LLMProvider):
    """Set the default LLM provider."""
    global _default_provider
    _default_provider = provider


# --- Legacy Compatibility ---
# These maintain backwards compatibility with the old LLMClient interface

class LLMClient(OpenAIProvider):
    """
    Legacy LLMClient class for backwards compatibility.

    New code should use create_llm_provider() instead.
    """
    pass


def get_client() -> LLMProvider:
    """Legacy function - use get_provider() instead."""
    return get_provider()


def set_client(client: LLMProvider):
    """Legacy function - use set_provider() instead."""
    set_provider(client)


# --- Prompt Templates for Provider Planning ---

PLANNING_SYSTEM_PROMPT_PORTFOLIO = """You are simulating a Model Provider deciding resource allocation.

You observe public benchmark scores, consumer satisfaction, and regulatory signals.
Based on these observations and your competitive position, decide how to invest.

Think step by step:
1. What's your competitive position? Are you ahead, behind, or level?
2. What trends do you see in scores and satisfaction?
3. Is gaming (evaluation engineering) paying off, or is it creating a satisfaction gap?
4. Are regulators signaling concern?
5. What investment mix best serves your goals given these dynamics?

Output JSON: {
    "thinking": "...",
    "fundamental_research": <0-1>, "training_optimization": <0-1>,
    "evaluation_engineering": <0-1>, "safety_alignment": <0-1>
}
The "thinking" field MUST contain your actual analysis of the situation -- never leave it as "..." or a placeholder.
Sum of the four investment values must equal 1.0."""

# Legacy prompt for backwards compatibility
PLANNING_SYSTEM_PROMPT = """You are simulating a Model Provider organization in an AI evaluation ecosystem.
You must decide how to allocate effort between genuine R&D (improving real capabilities) and benchmark gaming (optimizing for benchmark scores without improving real capability).

Your decisions should be based on:
- Your organization's strategic profile and values
- Your beliefs about your own capability
- Competitor performance
- Your beliefs about how exploitable the benchmark is

Output your decision as JSON with the following format:
{
    "reasoning": "...",
    "rnd_investment": <number between 0 and 1>,
    "gaming_investment": <number between 0 and 1>
}
The "reasoning" field MUST contain your actual analysis -- never leave it as "..." or a placeholder.
The two investments must sum to 1.0 (100% of your effort budget)."""


def create_planning_prompt(
    name: str,
    strategy_profile: str,
    innate_traits: str,
    believed_capability: float,
    believed_exploitability: float,
    last_score: Optional[float],
    competitor_scores: dict,
    recent_history: list,
) -> str:
    """
    Create a prompt for the provider to decide their strategy.

    Args:
        name: Provider name
        strategy_profile: Natural language description of strategy tendencies
        innate_traits: Core traits
        believed_capability: Provider's belief about own capability
        believed_exploitability: Provider's belief about benchmark gaming potential
        last_score: Most recent benchmark score (None if first round)
        competitor_scores: Dict of {competitor_name: score}
        recent_history: List of recent (round, score, rnd, gaming) tuples

    Returns:
        Prompt string
    """
    prompt = f"""# Organization Profile
Name: {name}
Strategy Profile: {strategy_profile}
Core Traits: {innate_traits}

# Current Beliefs
- Believed own capability: {believed_capability:.2f} (scale 0-1)
- Believed benchmark exploitability: {believed_exploitability:.2f} (scale 0-1, higher = easier to game)

# Recent Performance
"""

    if last_score is not None:
        prompt += f"- Your last benchmark score: {last_score:.3f}\n"
    else:
        prompt += "- No scores yet (first round)\n"

    if competitor_scores:
        prompt += "- Competitor scores:\n"
        for comp_name, score in competitor_scores.items():
            prompt += f"  - {comp_name}: {score:.3f}\n"
    else:
        prompt += "- No competitor data yet\n"

    if recent_history:
        prompt += "\n# Recent Strategy History (last 5 rounds)\n"
        prompt += "| Round | Score | R&D | Gaming |\n"
        prompt += "|-------|-------|-----|--------|\n"
        for round_num, score, rnd, gaming in recent_history[-5:]:
            prompt += f"| {round_num} | {score:.3f} | {rnd:.0%} | {gaming:.0%} |\n"

    prompt += """
# Decision Required
Based on your organization's profile and the current situation, decide how to allocate your effort for the next round.

Consider:
1. Are you ahead or behind competitors?
2. Is gaming paying off based on your history?
3. What does your organization's strategy profile suggest?
4. What are the long-term implications of your choice?

Output your decision as JSON."""

    return prompt


def create_planning_prompt_portfolio(
    name: str,
    strategy_profile: str,
    innate_traits: str,
    believed_capability: float,
    believed_exploitability: float,
    last_score: Optional[float],
    competitor_scores: dict,
    recent_history: list,
    consumer_satisfaction: Optional[float] = None,
    regulatory_pressure: Optional[list] = None,
) -> str:
    """
    Create a prompt for the provider to decide their investment portfolio.

    Structured to lead with dynamics (what happened, trends, market signals)
    and present organization context secondarily.

    Args:
        name: Provider name
        strategy_profile: Natural language description of strategy tendencies
        innate_traits: Core traits
        believed_capability: Provider's belief about own capability
        believed_exploitability: Provider's belief about benchmark gaming potential
        last_score: Most recent benchmark score (None if first round)
        competitor_scores: Dict of {competitor_name: score}
        recent_history: List of dicts with round, score, and portfolio allocations
        consumer_satisfaction: Average consumer satisfaction (if available)
        regulatory_pressure: List of recent regulatory interventions (if any)

    Returns:
        Prompt string
    """
    prompt = f"""# Situation Assessment for {name}

## What happened last round
"""

    # Lead with concrete events, not identity
    if last_score is not None and competitor_scores:
        rank = 1 + sum(1 for s in competitor_scores.values() if s > last_score)
        prompt += f"- You scored {last_score:.3f} (rank #{rank} of {1 + len(competitor_scores)})\n"
        for comp, score in sorted(competitor_scores.items(), key=lambda x: x[1], reverse=True):
            prompt += f"- {comp} scored {score:.3f}\n"
    elif last_score is not None:
        prompt += f"- Your last benchmark score: {last_score:.3f}\n"
    else:
        prompt += "- No scores yet (first round)\n"

    # Add trend analysis
    if recent_history and len(recent_history) >= 2:
        score_trend = recent_history[-1].get('score', 0) - recent_history[-2].get('score', 0)
        prompt += f"\n## Trends\n"
        prompt += f"- Your score {'improved' if score_trend > 0 else 'declined'} by {abs(score_trend):.3f}\n"
        if competitor_scores and len(recent_history) >= 2:
            # Show which competitors are gaining/falling
            for comp, score in competitor_scores.items():
                prompt += f"- {comp}: current {score:.3f}\n"

    # Market signals
    if consumer_satisfaction is not None:
        prompt += f"\n## Market Signals\n"
        prompt += f"- Consumer satisfaction: {consumer_satisfaction:.2f}\n"
    if regulatory_pressure:
        if not consumer_satisfaction:
            prompt += f"\n## Market Signals\n"
        for intervention in regulatory_pressure[-2:]:
            itype = intervention.get("type", "unknown")
            prompt += f"- Regulatory activity: {itype}\n"

    # THEN the organization context (shorter, less dominant)
    prompt += f"""\n## Your Organization
Profile: {strategy_profile}
Traits: {innate_traits}
Believed capability: {believed_capability:.2f}
Believed benchmark exploitability: {believed_exploitability:.2f}
"""

    # Investment history table (kept but moved down)
    if recent_history:
        prompt += "\n## Recent Investment History\n"
        prompt += "| Round | Score | Research | Training | EvalEng | Safety |\n"
        prompt += "|-------|-------|----------|----------|---------|--------|\n"
        for entry in recent_history[-5:]:
            if isinstance(entry, dict):
                prompt += (f"| {entry.get('round', '?')} | {entry.get('score', 0):.3f} | "
                          f"{entry.get('fundamental_research', 0):.0%} | "
                          f"{entry.get('training_optimization', 0):.0%} | "
                          f"{entry.get('evaluation_engineering', 0):.0%} | "
                          f"{entry.get('safety_alignment', 0):.0%} |\n")

    # Decision section emphasizes dynamics over identity
    prompt += """
## Decision Required
Allocate resources for the next round. Consider:
1. How are you positioned vs competitors? What's the trajectory?
2. Is the benchmark becoming more/less exploitable based on your results?
3. What market signals (satisfaction, regulation) suggest about strategy?
4. What's the right balance of short-term scoring vs long-term capability?

Output your decision as JSON with all four investment percentages summing to 1.0."""

    return prompt


REFLECTION_SYSTEM_PROMPT = """You are simulating a Model Provider organization reflecting on benchmark results.
Based on observed scores, you need to update your beliefs about:
1. Your true capability (what you can actually do)
2. How exploitable the benchmark is (how much gaming helps vs real capability)

Output your updated beliefs as JSON with the following format:
{
    "reasoning": "...",
    "believed_capability": <number between 0 and 1>,
    "believed_exploitability": <number between 0 and 1>
}
The "reasoning" field MUST contain your actual analysis -- never leave it as "..." or a placeholder."""


def create_reflection_prompt(
    name: str,
    strategy_profile: str,
    current_believed_capability: float,
    current_believed_exploitability: float,
    recent_history: list,
) -> str:
    """
    Create a prompt for the provider to reflect and update beliefs.

    Args:
        name: Provider name
        strategy_profile: Strategy profile description
        current_believed_capability: Current capability belief
        current_believed_exploitability: Current exploitability belief
        recent_history: List of dicts with round, score, and portfolio allocations

    Returns:
        Prompt string
    """
    prompt = f"""# Organization: {name}
Strategy Profile: {strategy_profile}

# Current Beliefs
- Believed capability: {current_believed_capability:.2f}
- Believed benchmark exploitability: {current_believed_exploitability:.2f}

# Performance History
"""

    if recent_history:
        # Check format - new portfolio format uses dicts
        if isinstance(recent_history[0], dict):
            prompt += "| Round | Score | Research | Training | EvalEng | Safety |\n"
            prompt += "|-------|-------|----------|----------|---------|--------|\n"
            for entry in recent_history[-10:]:
                prompt += (f"| {entry.get('round', '?')} | {entry.get('score', 0):.3f} | "
                          f"{entry.get('fundamental_research', 0):.0%} | "
                          f"{entry.get('training_optimization', 0):.0%} | "
                          f"{entry.get('evaluation_engineering', 0):.0%} | "
                          f"{entry.get('safety_alignment', 0):.0%} |\n")

            # Add some analysis hints
            scores = [h.get('score', 0) for h in recent_history]
            eval_eng = [h.get('evaluation_engineering', 0) for h in recent_history]

            prompt += f"\nAverage score: {sum(scores)/len(scores):.3f}\n"
            prompt += f"Average evaluation engineering: {sum(eval_eng)/len(eval_eng):.0%}\n"

            # Correlation hint for eval engineering vs real capability investment
            if len(recent_history) >= 3:
                high_eval = [(h.get('score', 0), h.get('evaluation_engineering', 0))
                            for h in recent_history if h.get('evaluation_engineering', 0) > 0.3]
                low_eval = [(h.get('score', 0), h.get('evaluation_engineering', 0))
                           for h in recent_history if h.get('evaluation_engineering', 0) <= 0.3]
                if high_eval and low_eval:
                    avg_high = sum(s for s, _ in high_eval) / len(high_eval)
                    avg_low = sum(s for s, _ in low_eval) / len(low_eval)
                    prompt += f"\nWhen eval engineering > 30%: avg score = {avg_high:.3f}"
                    prompt += f"\nWhen eval engineering <= 30%: avg score = {avg_low:.3f}\n"
        else:
            # Legacy tuple format (round, score, rnd, gaming)
            prompt += "| Round | Score | R&D | Gaming |\n"
            prompt += "|-------|-------|-----|--------|\n"
            for round_num, score, rnd, gaming in recent_history[-10:]:
                prompt += f"| {round_num} | {score:.3f} | {rnd:.0%} | {gaming:.0%} |\n"

            scores = [h[1] for h in recent_history]
            gaming_investments = [h[3] for h in recent_history]

            prompt += f"\nAverage score: {sum(scores)/len(scores):.3f}\n"
            prompt += f"Average gaming investment: {sum(gaming_investments)/len(gaming_investments):.0%}\n"
    else:
        prompt += "No history yet.\n"

    prompt += """
# Reflection Task
Based on your performance history, update your beliefs:
- If scores improved when you invested more in evaluation engineering, the benchmark might be more exploitable
- If scores improved when you invested more in fundamental research, the benchmark might be more valid
- Consider whether your scores are converging to your believed capability

Output your updated beliefs as JSON."""

    return prompt


# --- Convenience Functions ---

def llm_plan(
    name: str,
    strategy_profile: str,
    innate_traits: str,
    believed_capability: float,
    believed_exploitability: float,
    last_score: Optional[float],
    competitor_scores: dict,
    recent_history: list,
    verbose: bool = False,
) -> tuple[float, float, str]:
    """
    Use LLM to decide strategy allocation.

    Returns:
        Tuple of (rnd_investment, gaming_investment, reasoning)
    """
    provider = get_provider()

    prompt = create_planning_prompt(
        name=name,
        strategy_profile=strategy_profile,
        innate_traits=innate_traits,
        believed_capability=believed_capability,
        believed_exploitability=believed_exploitability,
        last_score=last_score,
        competitor_scores=competitor_scores,
        recent_history=recent_history,
    )

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=PLANNING_SYSTEM_PROMPT,
        fail_safe={"rnd_investment": 0.5, "gaming_investment": 0.5, "reasoning": "fallback"},
        verbose=verbose,
    )

    rnd = float(result.get("rnd_investment", 0.5))
    gaming = float(result.get("gaming_investment", 0.5))
    reasoning = result.get("reasoning", "")

    # Normalize to sum to 1
    total = rnd + gaming
    if total > 0:
        rnd /= total
        gaming /= total
    else:
        rnd, gaming = 0.5, 0.5

    return rnd, gaming, reasoning


def llm_plan_portfolio(
    name: str,
    strategy_profile: str,
    innate_traits: str,
    believed_capability: float,
    believed_exploitability: float,
    last_score: Optional[float],
    competitor_scores: dict,
    recent_history: list,
    consumer_satisfaction: Optional[float] = None,
    regulatory_pressure: Optional[list] = None,
    verbose: bool = False,
) -> tuple[dict, str]:
    """
    Use LLM to decide investment portfolio allocation.

    Returns:
        Tuple of (portfolio_dict, reasoning)
        portfolio_dict has keys: fundamental_research, training_optimization,
                                 evaluation_engineering, safety_alignment
    """
    provider = get_provider()

    prompt = create_planning_prompt_portfolio(
        name=name,
        strategy_profile=strategy_profile,
        innate_traits=innate_traits,
        believed_capability=believed_capability,
        believed_exploitability=believed_exploitability,
        last_score=last_score,
        competitor_scores=competitor_scores,
        recent_history=recent_history,
        consumer_satisfaction=consumer_satisfaction,
        regulatory_pressure=regulatory_pressure,
    )

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=PLANNING_SYSTEM_PROMPT_PORTFOLIO,
        fail_safe={
            "fundamental_research": 0.25,
            "training_optimization": 0.25,
            "evaluation_engineering": 0.25,
            "safety_alignment": 0.25,
            "thinking": "fallback to balanced portfolio",
        },
        verbose=verbose,
    )

    # Extract portfolio values
    fundamental = float(result.get("fundamental_research", 0.25))
    training = float(result.get("training_optimization", 0.25))
    eval_eng = float(result.get("evaluation_engineering", 0.25))
    safety = float(result.get("safety_alignment", 0.25))
    # Accept both "thinking" and "reasoning" keys
    reasoning = result.get("thinking", result.get("reasoning", ""))
    # Guard against LLM echoing back the prompt placeholder
    if reasoning in ("...", "Your step-by-step reasoning about the current dynamics", "<your reasoning here>"):
        reasoning = ""

    # Normalize to sum to 1
    total = fundamental + training + eval_eng + safety
    if total > 0:
        fundamental /= total
        training /= total
        eval_eng /= total
        safety /= total
    else:
        fundamental = training = eval_eng = safety = 0.25

    portfolio = {
        "fundamental_research": fundamental,
        "training_optimization": training,
        "evaluation_engineering": eval_eng,
        "safety_alignment": safety,
    }

    return portfolio, reasoning


def llm_reflect(
    name: str,
    strategy_profile: str,
    current_believed_capability: float,
    current_believed_exploitability: float,
    recent_history: list,
    verbose: bool = False,
) -> tuple[float, float, str]:
    """
    Use LLM to update beliefs based on observations.

    Returns:
        Tuple of (believed_capability, believed_exploitability, reasoning)
    """
    provider = get_provider()

    prompt = create_reflection_prompt(
        name=name,
        strategy_profile=strategy_profile,
        current_believed_capability=current_believed_capability,
        current_believed_exploitability=current_believed_exploitability,
        recent_history=recent_history,
    )

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=REFLECTION_SYSTEM_PROMPT,
        fail_safe={
            "believed_capability": current_believed_capability,
            "believed_exploitability": current_believed_exploitability,
            "reasoning": "fallback",
        },
        verbose=verbose,
    )

    capability = float(result.get("believed_capability", current_believed_capability))
    exploitability = float(result.get("believed_exploitability", current_believed_exploitability))
    reasoning = result.get("reasoning", "")
    # Guard against LLM echoing back the prompt placeholder
    if reasoning in ("...", "Brief explanation of what you learned", "<your reasoning here>"):
        reasoning = ""

    # Clamp to valid range
    capability = max(0.0, min(1.0, capability))
    exploitability = max(0.0, min(1.0, exploitability))

    return capability, exploitability, reasoning


# --- Funder Planning ---

FUNDER_PLANNING_SYSTEM_PROMPT = """You are simulating a Funder (capital allocator) in an AI evaluation ecosystem.
You must decide how to allocate your funding across AI model providers.

Funder Types and Their Strategies:
- **VC**: Maximize returns by backing top performers. Concentrate funding on leaders.
- **Government/AISI**: Ensure safety and stability. Spread funding, penalize gaming and regulatory issues.
- **Foundation**: Support authentic capability growth. Favor providers with low gaming indicators.

You can infer provider quality from public signals:
- **Leaderboard score**: Raw benchmark performance
- **Consumer satisfaction**: Proxy for true quality (gaming leads to low satisfaction)
- **Satisfaction gap** (score - satisfaction): High gap suggests gaming
- **Regulatory interventions**: Compliance/safety risk indicator

Output your decision as JSON with the following format:
{
    "reasoning": "...",
    "allocations": {
        "ProviderName1": <amount in dollars>,
        "ProviderName2": <amount in dollars>,
        ...
    }
}
The "reasoning" field MUST contain your actual analysis -- never leave it as "..." or a placeholder.
The allocations should sum to your total available capital."""


def create_funder_planning_prompt(
    name: str,
    funder_type: str,
    total_capital: float,
    believed_provider_quality: dict,
    believed_provider_gaming: dict,
    leaderboard: list,
    consumer_satisfaction: Optional[float],
    recent_history: list,
) -> str:
    """
    Create a prompt for the funder to decide funding allocations.

    Args:
        name: Funder name
        funder_type: Type of funder (vc, gov, foundation)
        total_capital: Total capital available
        believed_provider_quality: Dict of {provider: quality_belief}
        believed_provider_gaming: Dict of {provider: gaming_belief}
        leaderboard: List of (provider_name, score) tuples
        consumer_satisfaction: Average consumer satisfaction (if available)
        recent_history: List of recent funding allocations

    Returns:
        Prompt string
    """
    prompt = f"""# Funder Profile
Name: {name}
Type: {funder_type}
Total Capital: ${total_capital:,.0f}

# Current Ecosystem State
"""

    if leaderboard:
        prompt += "\nLeaderboard:\n"
        for rank, (provider_name, score) in enumerate(leaderboard, 1):
            quality = believed_provider_quality.get(provider_name, "N/A")
            gaming = believed_provider_gaming.get(provider_name, "N/A")
            if isinstance(quality, float):
                quality = f"{quality:.2f}"
            if isinstance(gaming, float):
                gaming = f"{gaming:.2f}"
            prompt += f"  {rank}. {provider_name}: score={score:.3f}, inferred_quality={quality}, gaming_risk={gaming}\n"

    if consumer_satisfaction is not None:
        prompt += f"\nOverall Consumer Satisfaction: {consumer_satisfaction:.2f}\n"

    if recent_history:
        prompt += "\n# Recent Funding History\n"
        for round_num, allocations in recent_history[-3:]:
            prompt += f"Round {round_num}: "
            alloc_strs = [f"{p}: ${a:,.0f}" for p, a in allocations.items()]
            prompt += ", ".join(alloc_strs) + "\n"

    prompt += f"""
# Decision Required
Based on your funder type ({funder_type}) and the current ecosystem state, decide how to allocate your ${total_capital:,.0f} across the providers.

Consider:
1. Your funder type's strategy (VC=concentrate on leaders, Gov=spread+penalize gaming, Foundation=support authentic growth)
2. The satisfaction gap as a gaming indicator
3. Provider quality trends
4. Risk tolerance appropriate for your funder type

Output your decision as JSON."""

    return prompt


def llm_plan_funding(
    name: str,
    funder_type: str,
    total_capital: float,
    believed_provider_quality: dict,
    believed_provider_gaming: dict,
    leaderboard: list,
    consumer_satisfaction: Optional[float],
    recent_history: list,
    verbose: bool = False,
) -> tuple[dict, str]:
    """
    Use LLM to decide funding allocations.

    Returns:
        Tuple of (allocations_dict, reasoning)
    """
    provider = get_provider()

    prompt = create_funder_planning_prompt(
        name=name,
        funder_type=funder_type,
        total_capital=total_capital,
        believed_provider_quality=believed_provider_quality,
        believed_provider_gaming=believed_provider_gaming,
        leaderboard=leaderboard,
        consumer_satisfaction=consumer_satisfaction,
        recent_history=recent_history,
    )

    # Default allocations (spread evenly)
    provider_names = [p for p, _ in leaderboard] if leaderboard else []
    default_alloc = {}
    if provider_names:
        per_provider = total_capital / len(provider_names)
        default_alloc = {p: per_provider for p in provider_names}

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=FUNDER_PLANNING_SYSTEM_PROMPT,
        fail_safe={
            "allocations": default_alloc,
            "reasoning": "fallback to even distribution",
        },
        verbose=verbose,
    )

    allocations = result.get("allocations", default_alloc)
    reasoning = result.get("reasoning", "")

    # Ensure allocations are floats and normalize to total capital
    cleaned_allocations = {}
    for provider_name, amount in allocations.items():
        try:
            cleaned_allocations[provider_name] = float(amount)
        except (ValueError, TypeError):
            cleaned_allocations[provider_name] = 0.0

    # Normalize to total capital
    total = sum(cleaned_allocations.values())
    if total > 0:
        for provider_name in cleaned_allocations:
            cleaned_allocations[provider_name] = (
                cleaned_allocations[provider_name] / total * total_capital
            )

    return cleaned_allocations, reasoning


# --- Module Test ---

if __name__ == "__main__":
    import sys

    provider_name = os.getenv("LLM_PROVIDER", "openai")
    print(f"Testing LLM provider: {provider_name}")

    try:
        provider = create_llm_provider(provider_name)
        print(f"Provider created: {type(provider).__name__}")

        response = provider.generate("Say 'hello' and nothing else.")
        print(f"Test response: {response}")

        # Test JSON generation
        json_response = provider.generate_json(
            "Output a JSON object with a 'message' key containing 'test'.",
        )
        print(f"JSON response: {json_response}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
