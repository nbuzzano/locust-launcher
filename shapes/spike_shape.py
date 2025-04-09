from locust import LoadTestShape

class SpikeShape(LoadTestShape):
    "Simula un pico repentino (ideal para eventos tipo Black Friday o campañas)."
    def tick(self):
        run_time = self.get_run_time()
        if run_time < 30:
            return (10, 2)
        elif run_time < 60:
            return (200, 50)
        elif run_time < 90:
            return (10, 10)
        else:
            return None