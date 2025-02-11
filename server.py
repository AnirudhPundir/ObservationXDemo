from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app import chat_with_ollama
from excelToVectorDB import convertExcelToVDB


app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/generate")
def generate_response(request: QueryRequest):
    try:
        response = chat_with_ollama(request.query)
        # Check if the response structure is as expected
        if "message" in response and "content" in response["message"]:
            print("Response : {response}")
            return {"response": response["message"]["content"]}
        else:
            raise HTTPException(status_code=500, detail="Unexpected response structure")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/convert")
async def convert_execel_to_embeddibngs():
    try:
        convertExcelToVDB()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def health_check():
    return {"status": "RAG Model API is up coming"}

