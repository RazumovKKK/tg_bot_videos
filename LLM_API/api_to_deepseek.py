from fastapi import FastAPI

from sqlalchemy.orm import Session

from LLM_API.llm import request_deepseek

from DB.database import execute_sql_query


app = FastAPI()

@app.get("/sql/{prompt}")
async def get_sql(prompt: str):
    sql_query = await request_deepseek(prompt)
    print(sql_query)
    result = await execute_sql_query(sql_query)
    return result
    



