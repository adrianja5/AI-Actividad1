# Actividad 1 - Agentes de recolección

Saca la cotización de las empresas que se indiquen o las de por defecto en el fichero `EMPRESAS.txt`.

## Pasos

### Automático

Se puede obtener la imagen del contenedor alojada en este repositorio de GitHub con los siguientes pasos:

1.
   ```console
   $ docker pull ghcr.io/adrianja5/ai-actividad1:latest
   ```

2. Ejecutar el contenedor con las empresas por defecto del fichero `EMPRESAS.txt`:
   ```console
   $ docker run -e CHAT_ID=XXX -e BOT_TOKEN=XXX ai-actividad1
   ```
   O con las empresas indicadas en un fichero externo:
   ```console
   $ docker run -e CHAT_ID=XXX -e BOT_TOKEN=XXX -v ruta-local-fichero-empresas:/app/EMPRESAS.txt ai-actividad1
   ```
   Esta última opción permite modificar fácilmente las empresas a las que vigilar por el bot, sin la necesidad de parar el contenedor.

---

### Build manual

Se puede obtener la imagen del contenedor contruyéndola manualmente siguiendo los pasos:

1. 
   ```console
   $ git clone https://github.com/adrianja5/AI-Actividad1
   ```

2.
   ```console
   $ cd AI-Actividad1
   ```

3.
   ```console
   $ docker build --tag ai-actividad1
   ```

4.
   ```console
   $ docker pull ghcr.io/adrianja5/ai-actividad1:latest
   ```

5. Ejecutar el contenedor con las empresas por defecto del fichero `EMPRESAS.txt`:
   ```console
   $ docker run -e CHAT_ID=XXX -e BOT_TOKEN=XXX ai-actividad1
   ```
   O con las empresas indicadas en un fichero externo:
   ```console
   $ docker run -e CHAT_ID=XXX -e BOT_TOKEN=XXX -v ruta-local-fichero-empresas:/app/EMPRESAS.txt ai-actividad1
   ```
   Esta última opción permite modificar fácilmente las empresas a las que vigilar por el bot, sin la necesidad de parar el contenedor.
