import json
from random import randint
from time import time
from uuid import uuid4

import httpx
from faker import Faker

END = True
print("Time can be incorrect because my PC is bad and cant delete fast")

# создание экземпляра httpx.Client
client = httpx.Client(base_url="http://server:8000")

start_time = time()
count = 0


def generate():
    fake = Faker()

    text = fake.lexify(text="?" * 16)

    uuid_user = uuid4().hex
    # print(uuid_user)
    return json.dumps({"uuid": uuid_user, "text": text})


def big_gen():
    for i in range(randint(10, 100)):
        yield generate()


def handler(response):
    # обработка ответа
    if response.status_code == 200:
        data = response.json()
        # print(data)
    else:
        print("Error:", response.status_code)


while END:
    # отправка GET-запроса на эндпоинт /{uuid}
    # response = client.get("/123e4567-e89b-12d3-a456-426655440000")

    end_time = time()
    elapsed_time = end_time - start_time
    if elapsed_time >= 10:
        start_time = time()
        print(f"deleted: {count} ")

    # update
    try:
        for gen in big_gen():
            response = client.post("/new", data=gen)
            # обработка ответа
            handler(response)

        # delete
        response = client.get("/count/10")
        for elem in response.json():
            client.delete(f'{elem["uuid"]}')
        # print(response.json())

        count += 10

    except httpx.ConnectError as e:
        # print("connection failed", e)
        continue

    # отправка GET-запроса на эндпоинт /items/limit/
    # response = client.get("/items/limit/", params={"count": 2})
    # handler(response)

# закрытие экземпляра httpx.Client
client.close()
