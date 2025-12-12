from fastapi import FastAPI

app = FastAPI()

@app.post("/multiply")
def get_multiplication(a: float, b: float):
    result = a * b
    return {"a": a, "b": b, "result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
