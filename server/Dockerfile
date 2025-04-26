FROM python:3.10-alpine


COPY . /app/
WORKDIR /app/

RUN pip install -r requirements.txt

# HYBRID run mode launches both Game and HTTP servers
# GAME run mode launches game only
# HTTP run mode launches HTTP only
ENV RUN_MODE=HYBRID

ENV PROJECTZ0_HOST=0.0.0.0


EXPOSE 23899
EXPOSE 8080

ENTRYPOINT [ "python3", "/app/app.py" ]