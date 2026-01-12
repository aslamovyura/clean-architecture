FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src:$PYTHONPATH

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY uv.lock pyproject.toml /app/

# Copy config files (if they exist in your project)
COPY config /config/

RUN uv pip install --system -r pyproject.toml
COPY src /app/



EXPOSE 8000

# Default command
CMD ["uvicorn", "app.entrypoints.api.main:app", "--host", "0.0.0.0", "--port", "8000"]