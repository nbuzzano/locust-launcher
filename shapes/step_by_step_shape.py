from locust import LoadTestShape
import math, os

class WaveShape(LoadTestShape):
    "Simula picos horarios. Aumenta y disminuye en ciclos como un flujo de usuarios durante el día."
    cycle_duration = int(os.getenv("CYCLE_DURATION", 60))
    spawn_rate = int(os.getenv("SPAWN_RATE", 5))
    max_users = int(os.getenv("MAX_USERS", 100))
    time_limit = int(os.getenv("TIME_LIMIT", 60))

    def tick(self):

        if run_time >= self.time_limit:
            print("🚀 Finalizando test")
            return None
        
        run_time = self.get_run_time()
        wave = (math.sin(run_time / self.cycle_duration * 2 * math.pi) + 1) / 2
        users = int(wave * self.max_users)
        return (users, self.spawn_rate)
