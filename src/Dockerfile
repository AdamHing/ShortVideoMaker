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
# 1337.to

# movie name and add mkv look through 

FROM python:3.10

WORKDIR /src

COPY . /src

RUN apt-get update && apt-get install -y \
    libmagickwand-dev \
    --no-install-recommends

RUN pip install -r requirements.txt


<<<<<<< HEAD

CMD ["python", "lambda_function.py"]
=======
CMD ["python", "./lambda_function.py"]

>>>>>>> 74c1cdb0c0c54ffaba5fb1e03e9ba272a2e8e632
