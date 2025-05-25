from openai import (
    AsyncOpenAI,
    APIError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError,
)

from src.core.config import AIConfig


class DeepseekClient:
    def __init__(
        self,
        model: str = "deepseek/deepseek-chat-v3-0324:free",
        base_url: str = "https://openrouter.ai/api/v1",
    ):
        self.client = AsyncOpenAI(
            api_key=AIConfig.DEEPSEEK_TOKEN,
            base_url=base_url,
        )
        self.model = model

    async def create_chat_completion(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content

        except AuthenticationError:
            raise Exception("Ошибка аутентификации: неверный API ключ")
        except RateLimitError:
            raise Exception("Превышен лимит запросов")
        except APIConnectionError:
            raise Exception("Ошибка соединения с API")
        except APIError as e:
            raise Exception(f"Ошибка API: {e}")

    async def ask(
        self,
        prompt: str,
        system_message: str = "You are a personal psychologist",
        **kwargs,
    ) -> str:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ]
        return await self.create_chat_completion(messages, **kwargs)
