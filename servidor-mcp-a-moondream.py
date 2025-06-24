# proxy_mcp_to_flask.py
"""
Proxy MCP → Flask que **solo acepta la ruta del archivo de imagen**.
Se elimina la conversión base‑64: el agente debe pasar la ruta local
(file://… o ruta absoluta) y el proxy leerá los bytes y los enviará al
endpoint /balloon_colour.
"""

import asyncio
import httpx
from pathlib import Path
from urllib.parse import urlparse
import mcp.server.stdio
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types

# ────────────────────────── CONFIG ──────────────────────────
FLASK_URL = "http://localhost:5000/balloon_colour"
API_KEY = "tu_token_secreto_12345"
server = Server("balloon-proxy")

# ────────────────────────── HELPERS ─────────────────────────


def read_image(path_or_uri: str) -> bytes:
    """Lee bytes de una ruta local o de un URI file:// …"""
    if path_or_uri.startswith("file://"):
        path = urlparse(path_or_uri).path
    else:
        path = path_or_uri  # ruta absoluta o relativa en disco
    return Path(path).read_bytes()


# ────────────────────────── TOOL DEF ────────────────────────


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="balloon-colour",
            description="Devuelve si hay globos y sus colores",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": (
                            "Ruta de la imagen en disco. Puede ser:\n"
                            "• Una ruta absoluta o relativa (p. ej. C:/imgs/foto.png)\n"
                            "• Un URI file://… (Claude lo envía al adjuntar un PNG)"
                        ),
                    }
                },
                "required": ["image_path"],
            },
        )
    ]


# ──────────────────────── TOOL HANDLER ──────────────────────


@server.call_tool()
async def call_tool(name: str, args: dict | None):
    if name != "balloon-colour":
        raise ValueError(f"Herramienta desconocida: {name}")

    path = args["image_path"]
    img_bytes = read_image(path)

    files = {"image": ("img.png", img_bytes, "image/png")}
    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with httpx.AsyncClient() as client:
        r = await client.post(FLASK_URL, files=files, headers=headers, timeout=50)
        r.raise_for_status()
        data = r.json()

    return [types.TextContent(type="text", text=str(data))]


# ────────────────────────── MAIN LOOP ───────────────────────


async def run():
    async with mcp.server.stdio.stdio_server() as (rx, tx):
        await server.run(
            rx,
            tx,
            InitializationOptions(
                server_name="balloon-proxy",
                server_version="0.4.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())
