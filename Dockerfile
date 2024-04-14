FROM python:3.10.12

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
RUN pip3 install pipx
RUN pipx install poetry==1.8.2
RUN pipx ensurepath
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --without dev

COPY app.py README.md ./
COPY src/ ./src/
COPY model/ ./model/
COPY data/ ./data/

RUN ls

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
