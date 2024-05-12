from fastapi import FastAPI
import uvicorn
from sqlmodel import Session, select
from dotenv import load_dotenv
load_dotenv()
from .config.db import create_tables, engine
from .models.todos import Todo, updateTodo

app = FastAPI()

# connection_string = 'DB_URI'
# connection = create_engine(connection_string)

# class Burhan(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     age: int | None = None
#     is_active: bool



@app.get("/get_Todo")
def get_Todo():
    with Session(engine) as session:
        statement = select(Todo)
        results = session.exec(statement)
        data = results.all()
        print (data)
        return data
    
@app.put("/update_Todo/ {id}")
def update_Todo(todo:updateTodo):
    with Session(engine) as session:
        db_todo = session.get(Todo,id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo    



@app.post("/create_todo")
def create_todo(todo:Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return {"status":200, "message":"todo create successfully"}
# Code above omitted 👆

@app.delete("/delete_todo/ {todo_id}")
def delete_todo(todo_id):
    with Session(engine) as session:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(db_todo)
        session.commit()
        session.refresh()
        return {"status":200, "message":"todo deleted successfully"}

# Code below omitted 👇

# students=[{
#     "username":"Burhan",
#     "rollno":1234},
#           {
#     "username":"Hadi",
#     "rollno":5678
#           }]
# @app.get("/students")
# def getStudents():
#     return students
# @app.get("/getTodos/{id}")
# def getTodos (id):
#     print("get todos called",id)
#     return "helloworld",id
# @app.get("/getName")
# def getName ():
#     print ("getName")
#     return
# @app.get("/getSingleTodos")
# def getSingleTodos (username:str,rollno:str):
#     print("getSingleTodos called",username,rollno)
#     return "getSingleTodos called",username,rollno
# @app.put("/putTodos")
# def putTodos():
#     return"putTodos called"
# @app.post("/postTodos")
# def postTodos ():
#     return "postTodos called"



def start():
    create_tables()
    uvicorn.run("todos.main:app" ,host="127.0.0.1", port=8080, reload=True)

