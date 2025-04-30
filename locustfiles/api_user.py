import uuid
import datetime
import json
import logging

from locust import HttpUser, task, between, constant

logging.basicConfig(level=logging.INFO)

def store(payload: dict):
    timestamp = datetime.datetime.utcnow().isoformat()
    request_id = str(uuid.uuid4())
    payload["request_id"] = request_id
    payload["timestamp"] = timestamp
    
    with open("requests_sent.jsonl", "a") as f:
        f.write(json.dumps(payload) + "\n")

    logging.info(f"📦 Evento guardado con ID {payload['request_id']}")

# A user class represents one type of user/scenario for your system. 
# When you do a test run you specify the number of concurrent users you want to
# simulate and Locust will create an instance per user. 
class APIUser(HttpUser):
    wait_time = constant(1) # between(1, 3)  
    # wait_time will make the simulated users wait between 1 and 5 seconds after each task.
    # https://docs.locust.io/en/stable/writing-a-locustfile.html#wait-time

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})

    @classmethod
    def json(self):
        return {
            "host": self.host,
            "some_custom_arg": "example"
        }
    
    # Methods decorated with @task are the core of your locust file. For every running User, 
    # Locust creates a greenlet (a coroutine or “micro-thread”), that will call those methods.
    @task(2)
    def get_products(self):
        with self.client.post("/posts", catch_response=True) as response:
            
            if response.text == "Err":
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 5:
                response.failure("Request took too long")


    @task(1)
    def create_order(self):

        payload = {"title": "foo","body": "bar","userId": 1}
        store(payload, task="create_order")
        
        with self.client.post(
            "/posts",
            json=payload,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            catch_response=True
        ) as response:
            if response.text == "Err":
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 5:
                response.failure("Request took too long")
            else:
                response.success()

