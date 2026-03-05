#Hoja de trabajo 5 Algoritmos y Estructuras de Datos
# Diego Chun - 
# Nicoll Díaz - 251695
import simpy
import random
import numpy as np 
import matplotlib.pyplot as plt

#Son los parametros 
RANDOM_SEED = 42 
RAM_CAPACITY = 100
NUM_CPUS = 1 #Cantidad de CPUs disponibles
INSTRUCCIONES_POR_PROCESO = 10 #Cantidad de instrucciones por proceso
INTERVALO = 10 #Intervalo de tiempo entre la creación de procesos

def proceso(env, nombre, RAM, CPU, tiempo):
    """Ciclo de vida completo de un proceso: NEW -> READY -> RUNNING -> WAITING -> TERMINATED"""
tiempo_llegada = env.now
memoria = random.randint(1, 10) #Es la memoria que necesita el proceso
instrucciones = random.randint(1, 10) #total de instruccciones del proceso
yield RAM.get(memoria) #esto espera a que el proceso tenga la memoria suficiente para poder ejecutarse

while instrucciones > 0:
    with CPU.request() as req:
        yield req 
        turno = min(instrucciones, INSTRUCCIONES_POR_PROCESO)
        yield env.timeout(1)
        instrucciones -= turno
        if instrucciones <= 0: 
            break 
        evento = random.randint(1, 21)
        if evento = 1:
            yield env.timeout(1) #Espera de 1 unidad de tiempo 

            RAM.put(memoria)
            tiempos.append(env.now - tiempo_llegada)
        
def generar_procesos(env, numero_procesos, intervalo, RAM, CPU):
    """Genera procesos con llegadas siguiendo distribución exponencial"""
    for i in range(numero_procesos):
        env.process(proceso(env, f'Proceso-{i}', RAM, CPU, tiempos
        yield env.timeout(random.expovariate(1.0 / intervalo))
        
def run_simulacion (numero_procesos, intervalo, ram = 100, numero_cpus = 1, instrucciones_por_proceso = 3):
    """Ejecuta la simulación y devuelve promedio y desviación estándar"""
    global INSTRUCCIONES_POR_PROCESO
    INSTRUCCIONES_POR_PROCESO = instrucciones_por_proceso

    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    RAM = simpy.Container(env, init=ram, capacity=ram)
    CPU = simpy.Resource(env, capacity=numero_cpus)
    tiempos = []

    env.process(generar_procesos(env, numero_procesos, intervalo, RAM, CPU, tiempos))
    env.run()
    return np.mean(tiempos), np.std(tiempos)
    





class SistemaOperativo:
    def __init__(self, env):
        self.env = env
