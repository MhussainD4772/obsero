FROM python:3.11-slim

WORKDIR /app

# Install deps before copying code so rebuilds are faster when only code changes
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# 0.0.0.0 = listen on all interfaces (required inside Docker; localhost alone won't accept outside traffic)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]