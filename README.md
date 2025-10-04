# Gemini CLI Python Wrapper

A Python wrapper for Google's [Gemini CLI](https://github.com/google-gemini/gemini-cli) with async support and multimodal capabilities.

## Features

- 🚀 Async/await support with asyncio
- 🖼️ Multimodal input (text and images)
- 📦 Type-safe with Pydantic models
- 🔄 Support for base64-encoded images and image URLs

## Prerequisites

- Python 3.7+
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) installed and configured

### Installing Gemini CLI

```bash
npm install -g @google/generative-ai-cli
```

Make sure the CLI is accessible in your PATH or note its installation location.


## Usage

### Basic Example

```python
import asyncio
from my_gemini import GeminiClient
from my_gemini.models import ChatMessage

async def main():
    client = GeminiClient()
    
    answer = await client.generate(
        messages=[
            ChatMessage(role="user", content="Hello World!")
        ],
        model="gemini-2.5-pro"
    )
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
```

### On Windows

If you're on Windows, specify the full path to the Gemini CLI:

```python
client = GeminiClient(cmd=r"C:\Users\YOUR-USER-NAME\AppData\Roaming\npm\gemini.cmd")
```

### Multimodal Example (with Images)

```python
from my_gemini.models import ChatMessage, ChatContentPart

# Using image URL
message = ChatMessage(
    role="user",
    content=[
        ChatContentPart(type="text", text="What's in this image?"),
        ChatContentPart(
            type="image_url",
            image_url={"url": "https://example.com/image.jpg"}
        )
    ]
)

# Using base64-encoded image
message = ChatMessage(
    role="user",
    content=[
        ChatContentPart(type="text", text="Describe this image"),
        ChatContentPart(
            type="image_url",
            image_url={"url": "data:image/png;base64,iVBORw0KGgo..."}
        )
    ]
)

answer = await client.generate(messages=[message])
```

### Custom Timeout

```python
client = GeminiClient(timeout=120)  # 120 seconds timeout
```

## Reference

### `GeminiClient`

#### Constructor

```python
GeminiClient(cmd: str = "gemini", timeout: float = 60)
```

- `cmd`: Path to the Gemini CLI executable (default: "gemini")
- `timeout`: Timeout for CLI execution in seconds (default: 60)

#### Methods

##### `generate()`

```python
async def generate(
    messages: List[ChatMessage],
    model: str = "gemini-2.5-pro"
) -> str
```

Generate a response from Gemini.

**Parameters:**
- `messages`: List of chat messages
- `model`: Model to use (default: "gemini-2.5-pro")

**Returns:** Generated response as a string

**Raises:** `RuntimeError` if CLI execution fails

### `ChatMessage`

```python
ChatMessage(
    role: Literal["system", "user", "assistant"],
    content: Union[str, List[ChatContentPart]]
)
```

### `ChatContentPart`

```python
ChatContentPart(
    type: Literal["text", "image_url"],
    text: Optional[str] = None,
    image_url: Optional[Dict[str, str]] = None
)
```

## Project Structure

```
.
├── my_gemini/
│   ├── __init__.py
│   ├── client.py      # Main client implementation
│   └── models.py      # Pydantic models
├── main.py            # Example usage
└── README.md
```

## Error Handling

The wrapper raises a `RuntimeError` if the Gemini CLI fails:

```python
try:
    answer = await client.generate(messages=[...])
except RuntimeError as e:
    print(f"Error: {e}")
```

## Logging

Enable debug logging to see CLI execution details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Acknowledgments

- [Google Gemini CLI](https://github.com/google-gemini/gemini-cli)
- Built with Python and Pydantic
