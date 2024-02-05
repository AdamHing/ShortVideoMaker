# # set base image (host OS)
# FROM python:3.10

# # set the working directory in the container
# WORKDIR /app
# # copy all files to working directory
# COPY . /app

# # set env vars
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # install dependencies
# RUN pip install -r requirements.txt

# # Expose the port that the application listens on.
# EXPOSE 8000

# # Run the application.
# CMD ["python", "gui.py"]




FROM python:3.10

WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt


CMD ["python", "./lambda_function.py"]
