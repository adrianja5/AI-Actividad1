# syntax=docker/dockerfile:1

FROM python:3.10.2-alpine3.15

WORKDIR /app

COPY requirments.txt requirments.txt
RUN pip3 install -r requirments.txt

COPY . .

RUN touch MAX_PRECIO.json

RUN echo "* * * * * python3 /app/actividad_1.py --fichero-empresas /app/EMPRESAS.txt --fichero-ult-precio /app/MAX_PRECIO.json --chat-id \$CHAT_ID --bot-token \$BOT_TOKEN" | crontab -

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
 
# Run the command on container startup
CMD crontab -l && crond && tail -f /var/log/cron.log
