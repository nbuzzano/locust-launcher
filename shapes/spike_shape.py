from base import BaseLoadTestShape
import os

class SpikeShape(BaseLoadTestShape):
    """
    Simula un pico repentino (ideal para eventos tipo Black Friday o campañas).
    Todo es configurable desde variables de entorno.
    """

    # 🔧 Variables configurables
    pre_spike_users = int(os.getenv("SPIKE_PRE_USERS", 10))
    pre_spike_spawn_rate = int(os.getenv("SPIKE_PRE_SPAWN", 2))
    pre_spike_duration = int(os.getenv("SPIKE_PRE_DURATION", 30))

    spike_users = int(os.getenv("SPIKE_PEAK_USERS", 200))
    spike_spawn_rate = int(os.getenv("SPIKE_PEAK_SPAWN", 50))
    spike_duration = int(os.getenv("SPIKE_PEAK_DURATION", 30))  # desde t=30 a t=60

    post_spike_users = int(os.getenv("SPIKE_POST_USERS", 10))
    post_spike_spawn_rate = int(os.getenv("SPIKE_POST_SPAWN", 10))
    post_spike_duration = int(os.getenv("SPIKE_POST_DURATION", 30))  # desde t=60 a t=90

    total_duration = pre_spike_duration + spike_duration + post_spike_duration

    def tick(self):
        if self.should_stop_run():
            return None
       
        run_time = self.get_run_time()

        if run_time < self.pre_spike_duration:
            return (self.pre_spike_users, self.pre_spike_spawn_rate)

        elif run_time < self.pre_spike_duration + self.spike_duration:
            return (self.spike_users, self.spike_spawn_rate)

        elif run_time < self.total_duration:
            return (self.post_spike_users, self.post_spike_spawn_rate)

        else:
            print("🚀 Finalizando test")
            return None
