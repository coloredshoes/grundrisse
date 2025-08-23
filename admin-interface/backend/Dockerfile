FROM python:3.12-slim

WORKDIR /app

# Install uv for faster dependency management
RUN pip install uv

# Copy project files
COPY ../../pyproject.toml ../../uv.lock* ./

# Install dependencies
RUN uv pip install --system -e .

# Copy backend source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]