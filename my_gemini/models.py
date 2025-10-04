from typing import List, Optional, Union, Dict, Literal
from pydantic import BaseModel

class ChatContentPart(BaseModel):
    type: Literal["text", "image_url"]
    text: Optional[str] = None
    image_url: Optional[Dict[str, str]] = None

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: Union[str, List[ChatContentPart]]