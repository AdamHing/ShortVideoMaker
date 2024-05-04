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

# FROM public.ecr.aws/lambda/python:3.10

# WORKDIR /src
# COPY . /src
# # Install system dependencies
# RUN yum -y update && yum -y install python-pip
# #apt-transport-https\
#     # libmagickwand-dev \
#     # --no-install-recommends \
#     # && rm -rf /var/lib/apt/lists/*
    
# # Install Python dependencies
# RUN pip install -r requirements.txt \
#     && rm -rf /var/lib/apt/lists/*
# # Entry point
# CMD ["lambda_function.lambda_handler"]
#===============================



# #Install Python dependencies
# RUN yum -y update \
#     && yum -y install python-pip \
#     && yum clean all \
#     && pip install --no-cache-dir -r requirements.txt \
#     && rm -rf /var/lib/apt/lists/*

# RUN yum -y update \
#     && yum -y install wget \
#     && yum -y install xz \
#     && yum install -y tar.x86_64 \
#     && wget -O ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz \
#     && tar xvf ffmpeg.tar.xz \
#     && yum -y install python-pip \
#     && yum clean all \
#     && pip install --no-cache-dir -r requirements.txt \
#     && rm -rf /var/lib/apt/lists/*


# RUN yum -y update \
#     && yum -y install python-pip \
#     && yum clean all \
#     && pip install --no-cache-dir -r requirements.txt \
#     && rm -rf /var/lib/apt/lists/*

# RUN yum -y update\
#     && yum -y install python-pip\
#     && pip install --no-cache-dir -r requirements.txt




# FROM public.ecr.aws/lambda/python:3.10
# COPY src/* ${LAMBDA_TASK_ROOT}
# COPY ffmpeg-6.1-amd64-static /usr/local/bin/ffmpeg
# RUN chmod 777 -R /usr/local/bin/ffmpeg

FROM public.ecr.aws/lambda/python:3.10
COPY src/* ${LAMBDA_TASK_ROOT}

#Install Python dependencies
RUN yum -y update \
    && yum -y install tar xz \
    && yum -y install python-pip \
    && yum clean all 
RUN curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz > /tmp/ffmpeg-release.tar.xz && tar xvf /tmp/ffmpeg-release.tar.xz -C /opt && mv /opt/ffmpeg-* /opt/ffmpeg && cd /opt/ffmpeg && mv model /usr/local/share && mv ffmpeg ffprobe qt-faststart /usr/local/bin && rm /tmp/ffmpeg-release.tar.xz
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*


# Entry point
CMD ["lambda_function.lambda_handler"]




