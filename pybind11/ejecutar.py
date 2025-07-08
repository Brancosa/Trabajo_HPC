import subprocess
import time
import re

valores_infectados = [30000000,40000000,50000000]
repeticiones = 4

def extraer_tiempo(salida):
    match = re.search(r"Tiempo total: ([\d\.]+) segundos\.?", salida)
    if match:
        return float(match.group(1))
    return None

for infected in valores_infectados:
    print(f"\n🔁 Ejecutando {repeticiones} simulaciones con initial_infected={infected}...\n")
    tiempos = []

    for i in range(repeticiones):
        print(f"  ▶️ Ejecución {i+1}/{repeticiones}")
        resultado = subprocess.run(["python", "epidemiapybind.py", str(infected)], capture_output=True, text=True)

        tiempo = extraer_tiempo(resultado.stdout)
        if tiempo is not None:
            tiempos.append(tiempo)
            print(f"    ✅ Tiempo total: {tiempo:.2f} segundos")
        else:
            print("    ⚠️ No se pudo extraer el tiempo.")
            print("Salida completa:")
            print(resultado.stdout)

        time.sleep(2)  # Pequeño delay entre ejecuciones

    if tiempos:
        promedio = sum(tiempos) / len(tiempos)
        print(f"\n📊 Promedio para initial_infected={infected}: {promedio:.2f} segundos\n")
    else:
        print(f"\n❌ No se pudo calcular el promedio para initial_infected={infected}\n")

    print("⏳ Esperando 5 segundos antes del siguiente M...\n")
    time.sleep(5)
