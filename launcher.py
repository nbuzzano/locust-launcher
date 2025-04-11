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
    parser.add_argument(
        "--enable_ui", action="store_true", help="Ejecutar Locust UI"
    )
    parser.add_argument(
        "--latest", action="store_true", help="Guardar en latest/ el reporte mas reciente"
    )
    return parser.parse_args()

def load_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def export_env_vars(env):
    for key, val in env.items():
        print(f"🚀 Exportando variable de entorno: {key}={val}")
        os.environ[key] = str(val)

def build_locust_command(locustfile, shape, options={}, latest=False):
    dir = dt.now().strftime('%Y%m%d_%H%M%S')
    if latest:
        dir = "latest"
        
    output_dir = f"reports/{Path(locustfile).stem}/{Path(shape).stem}/{dir}/"
    os.makedirs(os.path.dirname(output_dir), exist_ok=True)  # crea carpeta si no existe

    cmd = [
        "locust",
        "-f", f"{locustfile},{shape}",
        "--csv", f"{output_dir}/results",
        "--html", f"{output_dir}/charts.html",
        "--only-summary", # Disable periodic printing of request stats during --headless run
    ]

    if options.get("headless", True):
        cmd.append("--headless") # Disable the web interface, and start the test immediately.
    else:
        cmd.append("--class-picker")

    return output_dir, cmd

def run(cmd, config_file):

    print(f"🚀 Ejecutando test: {os.path.basename(config_file)}")
    print("   ➤ Comando:", " ".join(cmd))
    subprocess.run(cmd)

def run_all_configs(configs_path=CONFIG_DIR, enable_ui=False, latest=False):
    config_files = sorted(glob(os.path.join(configs_path, "*.yml")))

    if not config_files:
        print("⚠️  No se encontraron archivos de configuración en 'configs/'")
        return

    if enable_ui:
        print(f"\n📄 enable_ui: {enable_ui}")
        options = {"headless": False}
        _, cmd = build_locust_command("locustfiles/", "shapes/", options, latest)
        run(cmd, "configs/")
    else:
        config_files_len = len(config_files)
        print(f"📄 Se encontraron {config_files_len} archivos de configuración.")
        i = 0
        for config_file in config_files:
            i += 1
            print(f"\n📄 Cargando config ({i}/{config_files_len}): {config_file}")
            config = load_config(config_file)

            locustfile = config["test"]["locustfile"]
            shape = config["test"]["shape"]
            env = config.get("env", {})

            export_env_vars(env)
            output_dir, cmd = build_locust_command(locustfile, shape, latest=latest)

            # Copiar el archivo YML al mismo folder de resultados
            shutil.copy(config_file, os.path.join(output_dir, os.path.basename(config_file)))

            run(cmd, config_file)

            print("⏱ Esperando 5 segundos antes del siguiente test...\n")
            time.sleep(5)


if __name__ == "__main__":
    args = parse_args()
    run_all_configs(args.configs_path, args.enable_ui, args.latest)
