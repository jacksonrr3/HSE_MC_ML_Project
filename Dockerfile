FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libsm6 libxext6 libxrender-dev \
    software-properties-common \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 --version
RUN pip3 --version
RUN pip3 install opencv-python-headless
RUN pip3 install openvino
RUN pip3 install streamlit
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


WORKDIR /app

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
