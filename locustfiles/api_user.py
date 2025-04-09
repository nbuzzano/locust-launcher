from locust import HttpUser, task, between, constant

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
            if response.text != "Success":
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Request took too long")


    @task(1)
    def create_order(self):

        with self.client.post(
            "/posts",
            json={"title": "foo","body": "bar","userId": 1},
            headers={"Content-Type": "application/json; charset=UTF-8"},
            catch_response=True
        ) as response:
            if response.text != "Success":
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Request took too long")
            else:
                response.success()

