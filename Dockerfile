#Use ubuntu as the base image 
FROM ubuntu:22.04

#Install system dependencies
RUN apt update && apt install -y curl python3 python3-pip

#Install Ollama
RUN curl -fsSl https://ollama.com/install.sh | sh

#Start Ollama in the background
RUN ollama serve &

#Set the working directory inside the container
WORKDIR /app

#Copy dependencies file and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy the application code 
COPY . .


#Expose port 8000 for FAST API
EXPOSE 8000

#Start the FASTAPI server when the container runs
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
