# moondream-tfg-robot
Servidor moondream para robot centrado en la detección de globos

## 1. moondream-local-prueba-inicial.py
Es el codigo inicial de prueba del modelo

## 2. \servidores
Aqui estan los servidores creados para comunicar moondream con el robot

### \servidores\servidor-mcp-temporal.py
Este a su vez, es un servidor temporal creado para en caso de tener tiempo al final de este tfg, implementar la comunicación entre el servidor mooondream y Claude, a través de otro servidor intermedio (ya que a momento de crear este programa, el mcp de Claude debe estar en local los servidores para ejecutarse sus tools en Claude Desktop).

Como nota, actualmente pone que se le pasa una imagen en base64, pero se modificará a simplemente el nombre (ubicación fisica de esta para poder asi usarse) ya que sino, no se podrá hacer nada con el limite de tamaño de los prompts.