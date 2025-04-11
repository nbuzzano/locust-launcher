from base import BaseLoadTestShape
import os

class StepByStepShape(BaseLoadTestShape):
    """
    Ideal para simular sesiones conocidas: login → navegación → checkout.
    Cada paso del flujo puede ser configurado por env vars.
    """

    # Paso 1: login
    step1_duration = int(os.getenv("STEP1_DURATION", 15))
    step1_users = int(os.getenv("STEP1_USERS", 10))
    step1_spawn = int(os.getenv("STEP1_SPAWN", 5))

    # Paso 2: navegación
    step2_duration = int(os.getenv("STEP2_DURATION", 15))
    step2_users = int(os.getenv("STEP2_USERS", 50))
    step2_spawn = int(os.getenv("STEP2_SPAWN", 10))

    # Paso 3: checkout
    step3_duration = int(os.getenv("STEP3_DURATION", 15))
    step3_users = int(os.getenv("STEP3_USERS", 100))
    step3_spawn = int(os.getenv("STEP3_SPAWN", 20))

    # Paso 4: cleanup / logout
    step4_duration = int(os.getenv("STEP4_DURATION", 15))
    step4_users = int(os.getenv("STEP4_USERS", 20))
    step4_spawn = int(os.getenv("STEP4_SPAWN", 10))

    # Cálculo del tiempo total
    total_duration = (
        step1_duration + step2_duration + step3_duration + step4_duration
    )

    def tick(self):
        if self.should_stop_run():
            return None
        
        run_time = self.get_run_time()

        if run_time < self.step1_duration:
            return (self.step1_users, self.step1_spawn)

        elif run_time < self.step1_duration + self.step2_duration:
            return (self.step2_users, self.step2_spawn)

        elif run_time < self.step1_duration + self.step2_duration + self.step3_duration:
            return (self.step3_users, self.step3_spawn)

        elif run_time < self.total_duration:
            return (self.step4_users, self.step4_spawn)

        else:
            print("🚀 Finalizando test")
            return None
