from base import BaseLoadTestShape
import math, os

class WaveShape(BaseLoadTestShape):
    "Simula picos horarios. Aumenta y disminuye en ciclos como un flujo de usuarios durante el día."
    cycle_duration = int(os.getenv("CYCLE_DURATION", 60))
    spawn_rate = int(os.getenv("SPAWN_RATE", 5))
    max_users = int(os.getenv("MAX_USERS", 100))

    def tick(self):
        if self.should_stop_run():
            return None
        
        run_time = self.get_run_time()
        wave = (math.sin(run_time / self.cycle_duration * 2 * math.pi) + 1) / 2
        users = int(wave * self.max_users)
        return (users, self.spawn_rate)
