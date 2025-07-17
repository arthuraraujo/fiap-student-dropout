# Estágio 1: Instalar dependências
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala o uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copia os arquivos de dependência e cria o ambiente virtual
COPY pyproject.toml uv.lock* ./
RUN uv venv /opt/venv && \
    uv sync --no-cache --python /opt/venv/bin/python

# Estágio 2: Imagem final de produção
FROM python:3.12-slim AS production

WORKDIR /app

# Copia apenas o ambiente virtual com as dependências do estágio anterior
COPY --from=builder /opt/venv /opt/venv

# Adiciona o venv ao PATH para que os executáveis sejam encontrados
ENV PATH="/opt/venv/bin:$PATH"

# Cria um usuário não-root para segurança
RUN useradd --create-home app
USER app

# Copia os artefatos e o código-fonte da aplicação
COPY --chown=app:app src/ ./src/
COPY --chown=app:app artifacts/ ./artifacts/
COPY --chown=app:app data/ ./data/
COPY --chown=app:app models/ ./models/

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]