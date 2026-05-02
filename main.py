from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from typing import Optional
from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    address: str

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

app = FastAPI()


# for simple get data api
@app.get("/")
def say_hello():


    return [
        {   "id": 1,
            "Name": "Surakshya Khatri",
            "Address": "Bardiya"
         },
        {
            "id": 2,
            "Name": "Kranti Pariyar",
            "Address": "Dang"
        }
    ]


# for simple get data api with id
@app.get("/users")
def get_users_details():

    #read data.json file
    with open("data.json", "r") as file:
        data = json.load(file)

        return data


@app.get("/users/search")
def search_users(limit: int = None):
    return {"limit": limit}


@app.get("/users/{user_id}")
def get_user_detail(user_id: int):

    #read data.json file
    with open("data.json", "r") as file:
        data = json.load(file)

        user = next((user for user in data if user["id"] == user_id), None)

        if user is None:
            return JSONResponse(status_code=404, content={"message": "User with id {} does not exist".format(user_id)})
    return user


    #     if user_id > 100:
    #         return JSONResponse(status_code=404, content={"message": "User with id {} does not exist".format(user_id)})
    # return {"id": user_id, "Name": "", "Address": ""}


@app.post("/users")
def create_user(create_user_payload: CreateUserRequest):

    # return "OK"

    # read existing users
    with open("data.json", "r") as file:
        data = json.load(file)

    #create new user object
    new_user = {
        "id": len(data) + 1,
        "name": create_user_payload.name,
        "address": create_user_payload.address,

        # in short using model_dump
        # **create_user_payload.model_dump()
    }

    #append new user
    data.append(new_user)
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

        return {
            "message": "User created successfully",
            "user": new_user,
        }

@app.put("/users/{user_id}")
def update_user(user_id: int, update_user_payload: CreateUserRequest):

    # read existing users
    with open("data.json", "r") as file:
        data = json.load(file)

    # find user
    user = next((user for user in data if user["id"] == user_id), None)

    if user is None:
        return JSONResponse(
            status_code=404,
            content={"message": "User with id {} does not exist".format(user_id)}
        )

    user["name"] = update_user_payload.name
    user["address"] = update_user_payload.address

    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

    return {
        "message": "User updated successfully",
        "user": user
    }


@app.patch("/users/{user_id}")
def patch_user(user_id: int, update_user_payload: UpdateUserRequest):

    # read existing users
    with open("data.json", "r") as file:
        data = json.load(file)

    # find user
    user = next((user for user in data if user["id"] == user_id), None)

    if user is None:
        return JSONResponse(
            status_code=404,
            content={"message": "User with id {} does not exist".format(user_id)}
        )

    if update_user_payload.name is not None:
        user["name"] = update_user_payload.name

    if update_user_payload.address is not None:
        user["address"] = update_user_payload.address

    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

    return {
        "message": "User patched successfully",
        "user": user
    }