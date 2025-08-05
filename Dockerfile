FROM python:3.9-slim

WORKDIR /app

EXPOSE 8087

RUN pip install streamlit

COPY app.py . 

CMD ["streamlit", "run", "app.py","--server.port=8087", "--server.address=0.0.0.0"]

