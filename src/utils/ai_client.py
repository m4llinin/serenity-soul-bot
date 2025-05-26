import json

from openai import (
    AsyncOpenAI,
    APIError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError,
)

from src.core.config import (
    AIConfig,
    RedisConfig,
)
from src.utils.load_lexicon import LoaderLexicon


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
        self.redis_client = RedisConfig().conn

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

    async def get_phrase_of_the_day(
        self,
        user_id: int,
        prompt: str,
        system_message: str,
    ) -> str:
        key = f"deepseek:phrase_of_the_day:{user_id}"
        ttl = 24 * 60 * 60
        cached_phrase = await self.redis_client.get(key)

        if cached_phrase:
            return json.loads(cached_phrase)["phrase"]

        phrase = await self.ask(
            prompt=prompt,
            system_message=system_message,
        )
        await self.redis_client.setex(key, ttl, json.dumps({"phrase": phrase}))

        return phrase
