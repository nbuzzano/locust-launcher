import os
import subprocess
import yaml
import time
from glob import glob
from datetime import datetime as dt
from pathlib import Path
import shutil
import argparse

CONFIG_DIR = "configs"

def parse_args():
    parser = argparse.ArgumentParser(description="Locust launcher")
    parser.add_argument(
        "--configs_path", type=str, help="Path donde se encuentran los archivos de configuración", default=CONFIG_DIR
    )
    return parser.parse_args()

def load_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def export_env_vars(env):
    for key, val in env.items():
        os.environ[key] = str(val)

def build_locust_command(locustfile, shape, options):
    _now = dt.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"reports/{Path(locustfile).stem}/{Path(shape).stem}/{_now}/"
    os.makedirs(os.path.dirname(output_dir), exist_ok=True)  # crea carpeta si no existe

    cmd = [
        "locust",
        "-f", f"{locustfile},{shape}",
        "--csv", f"{output_dir}/results",
        "--only-summary", # Disable periodic printing of request stats during --headless run
        "--reset-stats" # Reset statistics once spawning has been completed.
    ]

    if options.get("headless"):
        cmd.append("--headless") # Disable the web interface, and start the test immediately.

    # if "users" in options:
    #     cmd += ["-u", str(options["users"])]
    # if "spawn_rate" in options:
    #     cmd += ["-r", str(options["spawn_rate"])]
    # if "run_time" in options:
    #     cmd += ["-t", str(options["run_time"])]

    return output_dir, cmd

def run(cmd, config_file, output_dir):
    
    # Copiar el archivo YML al mismo folder de resultados
    shutil.copy(config_file, os.path.join(output_dir, os.path.basename(config_file)))

    print(f"🚀 Ejecutando test: {os.path.basename(config_file)}")
    print("   ➤ Comando:", " ".join(cmd))
    subprocess.run(cmd)

def run_all_configs(configs_path=CONFIG_DIR):
    config_files = sorted(glob(os.path.join(configs_path, "*.yml")))

    if not config_files:
        print("⚠️  No se encontraron archivos de configuración en 'configs/'")
        return

    for config_file in config_files:
        print(f"\n📄 Cargando config: {config_file}")
        config = load_config(config_file)

        locustfile = config["test"]["locustfile"]
        shape = config["test"]["shape"]
        env = config.get("env", {})
        options = config.get("options", {})

        export_env_vars(env)
        output_dir, cmd = build_locust_command(locustfile, shape, options)

        run(cmd, config_file, output_dir)

        print("⏱ Esperando 5 segundos antes del siguiente test...\n")
        time.sleep(5)


if __name__ == "__main__":
    args = parse_args()
    run_all_configs(args.configs_path)
