import asyncio
import base64
import uuid
import os
import logging
from typing import List
from .models import ChatMessage

logger = logging.getLogger("my_gemini")

class GeminiClient:
    def __init__(self, cmd: str = "gemini", timeout: float = 60):
        self.cmd = cmd
        self.timeout = timeout

    # ---------- public ----------
    async def generate(self, messages: List[ChatMessage],
                       model: str = "gemini-2.5-pro") -> str:
        """
        Generate a response from Gemini based on the given messages and model.

        Args:
            messages (List[ChatMessage]): A list of messages to generate the response from.
            model (str): The model to use for generation. Defaults to "gemini-2.5-pro".

        Returns:
            str: The generated response from Gemini.

        Raises:
            RuntimeError: If Gemini CLI fails to execute.
        """
        prompt, tmp_files = self._build_prompt(messages)
        try:
            return await self._call_gemini(prompt, model)
        finally:
            for f in tmp_files:
                if os.path.exists(f):
                    os.unlink(f)

    # ---------- private ----------
    def _build_prompt(self, messages: List[ChatMessage]):
        """
        Build a prompt from a list of messages.

        Args:
            messages (List[ChatMessage]): A list of messages to build the prompt from

        Returns:
            Tuple[str, List[str]]: A tuple containing the built prompt and a list of temporary image files
        """
        tmp_files = []
        parts = []
        for m in messages:
            if isinstance(m.content, str):
                parts.append(f"{m.role}: {m.content}")
            else:
                txt = ""
                for seg in m.content:
                    if seg.type == "text":
                        txt += seg.text or ""
                    elif seg.type == "image_url":
                        url = seg.image_url["url"] # type: ignore
                        if url.startswith("data:"):
                            path = self._save_b64(url)
                            tmp_files.append(path)
                            txt += f" @{path}"
                        else:
                            txt += f" <image>{url}</image>"
                parts.append(f"{m.role}: {txt}")
        return "\n".join(parts), tmp_files

    def _save_b64(self, data_url: str) -> str:
        """
        Save a base64-encoded image to a temporary file.

        Args:
            data_url (str): A base64-encoded image URL

        Returns:
            str: The path to the saved file
        """
        header, data = data_url.split(",", 1)
        ext = ".png" if "png" in header else ".jpg"
        fname = f".gemini_tmp/{uuid.uuid4().hex[:8]}{ext}"
        os.makedirs(".gemini_tmp", exist_ok=True)
        with open(fname, "wb") as f:
            f.write(base64.b64decode(data))
        return fname

    async def _call_gemini(self, prompt: str, model: str) -> str:
        """
        Call Gemini CLI with the given prompt and model.

        Args:
            prompt (str): The prompt to pass to Gemini.
            model (str): The model to use.

        Returns:
            str: The response from Gemini.

        Raises:
            RuntimeError: If Gemini CLI fails to execute.
        """
        args = [self.cmd, "-m", model, "-p", prompt]
        # args += ["--sandbox"]
        logger.debug("exec: %s", " ".join(args))

        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=self.timeout
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Gemini CLI failed ({proc.returncode}): {stderr.decode().strip()}")
        return stdout.decode().strip()