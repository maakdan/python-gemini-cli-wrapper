import asyncio
from my_gemini import GeminiClient
from my_gemini.models import ChatMessage

async def main():
    client = GeminiClient()
    # client = GeminiClient(cmd=r"C:\Users\user\AppData\Roaming\npm\gemini.cmd") for Windows
    answer = await client.generate(
        messages=[
            ChatMessage(role="user", content="Hello World!")
        ],
        model="gemini-2.5-pro"
    )
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())