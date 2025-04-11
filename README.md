# Locust Launcher

- Launcher pensado para crear API test de forma simple y rápida con Locust. 

# HOW TO USE

Solamente hay que agregar en: 
- [pyproject.toml](pyproject.toml): el host de la API que se desea probar. i.e.: `host = "https://jsonplaceholder.typicode.com"`
- [locustfiles/](locustfiles/): un file por el API test que se desea probar.
- [configs/](configs/): un file donde unificamos nuestro API test + la simulación del comportamiento que queremos probar. Este archivo tiene la siguiente estructura:

```
# configs/api_user_rampup.yml

test:
  locustfile: locustfiles/api_user.py
  shape: shapes/ramp_up_shape.py

env:
  STEP_TIME: 5
  STEP_LOAD: 10
  SPAWN_RATE: 3
  MAX_USERS: 50
```

Donde:
- `locustfile`: es el API test que queremos ejecutar. 
- `shape`: indicamos de que forma queremos estresar a la API. i.e: Stress test, Peak test, Wave test, etc. La idea es que estos shapes sean reutilizables entre los distintos API tests.
- `env`: son las variables de entorno que se usan en el shape. (podria no usar ninguna)

# RUN & REPORTS

### CLI

Una vez configurado el launcher, solo hay que ejecutar `python launcher.py` y se creara la carpeta de resultados en la carpeta `reports/`. Donde se va a guardar por cada corrida, el reporte de Locust junto al archivo de configuración usado en ese momento.

Como opcional se puede especificar el parametro --configs_path para indicar la carpeta donde se encuentran los archivos de configuración. Esto puede ser util en caso de que no quieras ejecutar todos los API test, si solo quieres probar unos pocos en particular.

### UI
Si se desea se pude levantar la UI de Locust ejecutando `python launcher.py --enable_ui`. Se va a levantar en el puerto 8089. 

Esta opcional es solo para hacer pruebas basicas y validar como funcionan los shapes ya que al ejecutar `--enable_ui` no va a leer los [configs/](configs/) files si no que levanta directamente los API tests. 

# Shapes

Los shapes disponibles se encuentran en la carpeta `shapes/`. Simulan los siguientes comportamientos:

Custom Shapes:
- RampUpShape: "Sube de a pocos usuarios cada X segundos, ideal para ver cómo responde la API mientras aumenta la carga."
- SpikeShape: "Simula un pico repentino (ideal para eventos tipo Black Friday o campañas)."
- WaveShape: "Simula picos horarios. Aumenta y disminuye en ciclos como un flujo de usuarios durante el día."
- StepByStepShape: "Ideal para simular sesiones conocidas: login → navegación → checkout"

En la carpeta [resources/](resources/) se pueden encontrar algunos screenshots de como se comportan los shapes.

# Last comments

Hacer pruebas con Locust y obtener resultados es solo la primer parte de la solución al problema. La segunda parte es poder interpretar esos resultados.

Dejo algunas lecturas que pueden ser de utilidad:
- [closed-vs-open-workload-models](https://www.locust.cloud/blog/closed-vs-open-workload-models)
- [your-load-generator-is-probably-lying-to-you](https://highscalability.com/your-load-generator-is-probably-lying-to-you-take-the-red-pi/)