# Para pruebas:
# mcp dev servidor-mcp-temporal.py 

from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import os


UPLOAD_FOLDER = "uploads"
# Nota no hace falta un token de acceso ya que este programa se ejecuta manualmente (python programa.py)

# Create a server instance
server = Server("example-server")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="example-prompt",
            description="An example prompt template",
            arguments=[
                types.PromptArgument(
                    name="arg1",
                    description="Example argument",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str,
    arguments: dict[str, str] | None
) -> types.GetPromptResult:
    if name != "example-prompt":
        raise ValueError(f"Unknown prompt: {name}")

    return types.GetPromptResult(
        description="Example prompt",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text="Example prompt text"
                )
            )
        ]
    )

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools related to the image upload process.
    """
    return [
        types.Tool(
            name="upload-image",
            description="Upload an image to the server",
            inputSchema={
                "type": "object",
                "properties": {
                    "image": {"type": "string", "description": "Base64-encoded image content"},
                },
                "required": ["image"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle the image upload process using MCP tool execution.
    """
    if name == "upload-image":
        image_data = arguments.get("image")
        if not image_data:
            raise ValueError("No image provided.")
        
        # Guardar la imagen como un archivo
        image_path = os.path.join(UPLOAD_FOLDER, "uploaded_image.png")  # Usamos un nombre fijo por ahora
        with open(image_path, "wb") as img_file:
            img_file.write(image_data.encode())  # Suponemos que la imagen está codificada en base64

        return [types.TextContent(type="text", text=f"Imagen recibida y guardada en: {image_path}")]
    
    raise ValueError(f"Unknown tool: {name}")


async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())