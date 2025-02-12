from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app import chat_with_ollama
from excelToVectorDB import convertExcelToVDB
import re
import json


app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/generate")
async def generate_response(request: QueryRequest):
    # try:
    response = chat_with_ollama(request.query)

    json_match = re.search(r'```json\n(.*?)\n```', response["message"]["content"], re.DOTALL)

    if json_match:
        json_string = json_match.group(1)
        json_data = json.loads(json_string)

    return {"data": json_data}
        # 
        # Check if the response structure is as expected
        # if "message" in response and "content" in response["message"]:
        #     print("Response : {message}")
        #     return 
        
        # else:
        #     raise HTTPException(status_code=500, detail="Unexpected response structure")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/convert")
async def convert_execel_to_embeddibngs():
    try:
        convertExcelToVDB()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def health_check():
    return {"status": "RAG Model API is up coming"}

