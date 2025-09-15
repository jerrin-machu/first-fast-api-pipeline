#use official python image
FROM python:3.12
#set work directory
WORKDIR /app
#install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# copy app code from localmachine to docker image

COPY ./app ./app
# Run FastApi with Uvicorn # what command to run when the docker starts.
#"--host","0.0.0.0" Makes the app accessible from outside container, "--port","8000"=>runs the app on port 8000"--reload" enable auto-reload on code changes.
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]