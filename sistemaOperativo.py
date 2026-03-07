# Hoja de trabajo 5 Algoritmos y Estructuras de Datos
# Diego Rizzo - 22955
# Nicoll Díaz - 251695
import simpy
import random
import numpy as np 
import matplotlib.pyplot as plt

# Parámetros 
RANDOM_SEED = 42 
RAM_CAPACITY = 100 # Capacidad del RAM
NUM_CPUS = 1 # Cantidad de CPUs disponibles
INSTRUCCIONES_POR_PROCESO = 3 # Cantidad de instrucciones realizadas por cada unidad de tiempo
INTERVALO = 10 # Intervalo de tiempo entre la creación de procesos
NUM_PROCESOS = 25 # Cantidad de procesos a realizar

# Definir la clase SistemaOperativo con un recurso de CPU y un contenedor de memoria
class SistemaOperativo:

    def __init__(self, env):
        self.cpu = simpy.Resource(env, capacity=NUM_CPUS)
        self.ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)

def proceso(env, nombre, sistema, tiempos):
    """Ciclo de vida completo de un proceso: NEW -> READY -> RUNNING -> WAITING -> TERMINATED"""
    tiempo_llegada = env.now
    memoria = random.randint(1, 10) # Es la memoria que necesita el proceso
    instrucciones = random.randint(1, 10) # Total de instruccciones del proceso
    print(f'El {nombre} entra a NEW despues de {tiempo_llegada} unidades de tiempo. Solicita {memoria} unidades de RAM.')

    yield sistema.ram.get(memoria) # Esto espera a que el proceso tenga la memoria suficiente para poder ejecutarse
    print(f'El {nombre} pasa a READY. Tiene {instrucciones} instrucciones a realizar.')

    while instrucciones > 0:
        with sistema.cpu.request() as req: # Solicita acceso al CPU
            yield req # Espera a que el CPU esté disponible
            print(f'El {nombre} pasa a RUNNING.')
            turno = min(instrucciones, INSTRUCCIONES_POR_PROCESO)

            instrucciones -= turno
            yield env.timeout(1) # Se corre una cantidad variable de instrucciones en 1 unidad de tiempo

            if instrucciones <= 0: 
                break 
            else:
                print(f'Al {nombre} le faltan {instrucciones} instrucciones a realizar.')
                evento = random.randint(1, 2)

                if evento == 1:
                    print(f'El {nombre} pasa a WAITING.')
                    yield env.timeout(1) # Espera de 1 unidad de tiempo 
                    print (f'El {nombre} sale de WAITING y regresa a READY.')
                else:
                    print(f'El {nombre} regresa a READY.')

    print(f'El {nombre} ha terminado todas sus instrucciones y pasa a TERMINATED.')
    sistema.ram.put(memoria)
    tiempos.append(env.now - tiempo_llegada)
        
def generar_procesos(env, sistema, tiempos):
    """Genera procesos con llegadas siguiendo distribución exponencial"""
    for i in range(NUM_PROCESOS):
        env.process(proceso(env, f'Proceso-{i+1}', sistema, tiempos))
        yield env.timeout(random.expovariate(1.0 / INTERVALO)) # Se generan numeros al azar para simular la llegada de procesos
        
def run_simulacion ():
    """Ejecuta la simulación y devuelve promedio y desviación estándar"""

    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    sistema = SistemaOperativo(env) # Crear una instancia del Sistema Operativo
    tiempos = []

    env.process(generar_procesos(env, sistema, tiempos)) # Iniciar el generador de procesos
    env.run()
    return np.mean(tiempos), np.std(tiempos)

cantidades = [25, 50, 100, 150, 200]
intervalos = [10, 5, 1]
colores    = ['blue', 'orange', 'red']

print("=" * 60)
print("TAREAS 1 y 2 – Configuración base (RAM=100, 1 CPU, 3 inst/turno)")
print("=" * 60)

plt.figure(figsize=(9, 5))
for intervalo, color in zip(intervalos, colores):
    promedios = []
    print(f"\nIntervalo = {intervalo}")
    for n in cantidades:
        prom, desv = run_simulacion()
        promedios.append(prom)
        print(f"  N={n:3d} → Promedio={prom:7.2f}  Desv.Std={desv:6.2f}")
    plt.plot(cantidades, promedios, marker='o', color=color,
             label=f"Intervalo={intervalo}")

plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio en sistema")
plt.title("Tareas 1 y 2 – Configuración base")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafica_tareas1y2.png", dpi=150)
plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# TAREA 3 – Estrategias de optimización
# ═══════════════════════════════════════════════════════════════════════════════
estrategias = [
    {"label": "Base (RAM=100, 1CPU, 3inst)",  "ram": 100, "cpus": 1, "inst": 3},
    {"label": "a) RAM=200",                   "ram": 200, "cpus": 1, "inst": 3},
    {"label": "b) CPU rápido (6 inst/turno)", "ram": 100, "cpus": 1, "inst": 6},
    {"label": "c) 2 CPUs",                    "ram": 100, "cpus": 2, "inst": 3},
]

for intervalo in intervalos:
    print("\n" + "=" * 60)
    print(f"TAREA 3 – Optimizaciones  |  Intervalo = {intervalo}")
    print("=" * 60)

    plt.figure(figsize=(10, 5))
    for est in estrategias:
        promedios = []
        print(f"\n  {est['label']}")
        for n in cantidades:
            prom, desv = run_simulacion()
            promedios.append(prom)
            print(f"    N={n:3d} → Promedio={prom:7.2f}  Desv.Std={desv:6.2f}")
        plt.plot(cantidades, promedios, marker='o', label=est["label"])

    plt.xlabel("Número de procesos")
    plt.ylabel("Tiempo promedio en sistema")
    plt.title(f"Tarea 3 – Comparación de estrategias  (Intervalo={intervalo})")
    plt.legend(fontsize=8)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"grafica_tarea3_intervalo{intervalo}.png", dpi=150)
    plt.show()

print("\n✓ Simulación completada. Gráficas guardadas como archivos PNG.")



    
