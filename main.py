from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MultiplyRequest(BaseModel):
    a: float
    b: float

@app.post("/multiply")
def get_multiplication(data: MultiplyRequest):
    result = data.a * data.b
    return {
        "a": data.a,
        "b": data.b,
        "result": result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
