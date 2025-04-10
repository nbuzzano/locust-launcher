from locust import LoadTestShape
import os

class SpikeShape(LoadTestShape):
    "Simula un pico repentino (ideal para eventos tipo Black Friday o campañas)."

    time_limit = int(os.getenv("TIME_LIMIT", 60))

    def tick(self):

        if run_time >= self.time_limit:
            print("🚀 Finalizando test")
            return None
        
        run_time = self.get_run_time()
        if run_time < 30:
            return (10, 2)
        elif run_time < 60:
            return (200, 50)
        elif run_time < 90:
            return (10, 10)
        else:
            print("🚀 Finalizando test")
            return None
        
        