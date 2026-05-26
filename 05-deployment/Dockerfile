FROM agrigorev/zoomcamp-model:2025
RUN pip install uv
WORKDIR /app
COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked
COPY 05-deployment/ ./
EXPOSE 1515
ENTRYPOINT ["uv", "run", "uvicorn", "Homework5:app", "--host", "0.0.0.0", "--port", "1111"]


