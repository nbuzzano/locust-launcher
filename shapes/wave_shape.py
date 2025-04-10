from locust import LoadTestShape
import os
class StepByStepShape(LoadTestShape):
    "Ideal para simular sesiones conocidas: login → navegación → checkout"

    time_limit = int(os.getenv("TIME_LIMIT", 60))

    def tick(self):
        run_time = self.get_run_time()

        if run_time >= self.time_limit:
            print("🚀 Finalizando test")
            return None
        
        if run_time < 60:
            return (10, 5)
        elif run_time < 120:
            return (50, 10)
        elif run_time < 150:
            return (100, 20)
        elif run_time < 180:
            return (20, 10)
        else:
            print("🚀 Finalizando test")
            return None