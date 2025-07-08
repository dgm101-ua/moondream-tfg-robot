> **Important Notice**  
> All code, models, and documentation in this repository are provided **without any license**.  
> You have **no permission** to copy, modify, distribute, or use any part of the content unless the author gives explicit written consent.

# moondream-tfg-robot
Servidor Moondream para robot centrado en la detección de globos

## 1. `moondream-local-prueba-inicial.py`
Código inicial de prueba del modelo.

## 2. `\servidores`
Contiene los servidores creados para comunicar Moondream con el robot.

### `\servidores\servidor-mcp-temporal.py`
Servidor temporal pensado, si el tiempo lo permite, para enlazar el servidor Moondream con Claude a través de un endpoint intermedio (en la fecha de creación, el MCP de Claude debe ejecutarse en local dentro de Claude Desktop para usar sus tools).

**Nota:** Actualmente el script espera recibir la imagen en base64, pero se cambiará a enviar solo la ruta del archivo (ubicación física) para evitar superar el límite de tamaño de los prompts.
