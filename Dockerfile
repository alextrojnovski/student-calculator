FROM ubuntu:20.04

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    python3 \
    bc \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY calculator.sh /app/
COPY calculator.py /app/

# Даем права на выполнение
RUN chmod +x calculator.sh calculator.py

# Устанавливаем команду по умолчанию
CMD ["/bin/bash"]
