# Usa uma imagem oficial e leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia as dependências primeiro (para otimizar o cache do Docker)
COPY requirements.txt .

# Instala as bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do projeto
COPY . .

# Expõe a porta que o Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação web
CMD ["python", "app.py"]