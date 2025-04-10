from base import BaseLoadTestShape
import os

class RampUpShape(BaseLoadTestShape):
    "Sube de a pocos usuarios cada X segundos, ideal para ver cómo responde la API mientras aumenta la carga."
    step_time = int(os.getenv("STEP_TIME", 10))
    step_load = int(os.getenv("STEP_LOAD", 10))
    spawn_rate = int(os.getenv("SPAWN_RATE", 5))
    max_users = int(os.getenv("MAX_USERS", 100))

    def tick(self):
        if self.should_stop_run():
            return None
        
        run_time = self.get_run_time()
        current_step = run_time // self.step_time
        users = min(self.step_load * (current_step + 1), self.max_users)
        
        if users >= self.max_users:
            print("🚀 Finalizando test")
            return None
        
        return (users, self.spawn_rate)