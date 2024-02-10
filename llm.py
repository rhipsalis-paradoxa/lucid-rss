from os import environ as env
import asyncio
import openai_async


async def get_response(prompt):
    response = await openai_async.chat_complete(
        env['OPENAI_API_KEY'],
        timeout=2,
        payload={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
        },
    )

    return response.json()["choices"][0]["message"]


response = asyncio.run(get_response("Hello there!"))
print(response)

