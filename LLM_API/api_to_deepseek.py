from fastapi import FastAPI

from sqlalchemy.orm import Session

from LLM_API.llm import request_deepseek

from DB.database import execute_sql_query


app = FastAPI()

@app.get("/sql/{prompt}")
async def get_sql(prompt: str):
    sql_query = request_deepseek(prompt)
    return execute_sql_query(sql_query)
    

