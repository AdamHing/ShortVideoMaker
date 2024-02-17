# 1337.to
# movie name and add mkv look through 

#FROM python:3.10 
# FROM python:3.10.11-slim
# WORKDIR /src
# COPY . /src

# # RUN apt-get update && apt-get install -y python3-opencv
# # RUN apt-get update && apt-get install -y python3-opencv
# RUN pip install opencv-python

# RUN apt-get update && apt-get install -y \
#     libmagickwand-dev \
#     --no-install-recommends
    
# #RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# RUN pip install -r requirements.txt

# #entry point
# CMD ["python", "lambda_function.py"]


#============================================================================


# FROM python:3.10.11-slim AS base

# COPY . ./

# RUN apt-get update && apt-get install -y python3-opencv

# RUN pip install opencv-python

# RUN apt-get update && apt-get install -y \
#     libmagickwand-dev \
#     --no-install-recommends

# RUN pip install -r requirements.txt


# #FROM python:3.10.11-alpine
# FROM python:3.10.11-slim


# COPY --from=base . /src
# WORKDIR /src



# #entry point
# CMD ["python", "lambda_function.py"]
# # # CMD ["python", "gui.py"]




#============================================================================



# FROM python:3.10.11-slim
# WORKDIR /src
# COPY . /src

# RUN pip install opencv-python

# RUN apt-get update && apt-get install -y \
#     libmagickwand-dev \
#     --no-install-recommends

# RUN pip install -r requirements.txt

# #entry point
# CMD ["lambda_function.lambda_handler"]

#===================================================

# FROM python:3.10.11-slim

# WORKDIR /src
# COPY . /src
# # Install system dependencies
# RUN apt-get -y update && apt-get install -y 
# #apt-transport-https\
#     # libmagickwand-dev \
#     # --no-install-recommends \
#     # && rm -rf /var/lib/apt/lists/*
    
# # Install Python dependencies
# RUN pip install -r requirements.txt \
#     && rm -rf /var/lib/apt/lists/*
# # Entry point
# CMD ["lambda_function.lambda_handler"]

#=================================================

FROM public.ecr.aws/lambda/python:3.10

WORKDIR /src
COPY . /src
# Install system dependencies
RUN yum -y update && yum -y install python-pip
#apt-transport-https\
    # libmagickwand-dev \
    # --no-install-recommends \
    # && rm -rf /var/lib/apt/lists/*
    
# Install Python dependencies
RUN pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*
# Entry point
CMD ["lambda_function.lambda_handler"]