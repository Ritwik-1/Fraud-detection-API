FROM python:3.9

WORKDIR /app

COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 

EXPOSE 8000 

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"] 


# docker build -t fraud-api .
# docker run -d -p 8000:8000 fraud-api


# http://localhost:8000/docs 