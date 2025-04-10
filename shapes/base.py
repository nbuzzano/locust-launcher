from locust import LoadTestShape
import os

class BaseLoadTestShape(LoadTestShape):
    
    time_limit = int(os.getenv("TIME_LIMIT", 60))

    def should_stop_run(self):
        run_time = self.get_run_time()
        if run_time >= self.time_limit:
            print(f"🚀 Finalizando test por TIME_LIMIT: {self.time_limit}")
            return True
        
    def tick(self):
        "Override in child classes"
        pass