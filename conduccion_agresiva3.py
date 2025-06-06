import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# Definir las variables de entrada
aceleracion = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'aceleracion')
frenado = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'frenado')
velocidad_variacion = ctrl.Antecedent(np.arange(0, 20.1, 0.5), 'velocidad_variacion')
vibraciones = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'vibraciones')

# Variable de salida
conduccion_agresiva = ctrl.Consequent(np.arange(0, 10.1, 0.1), 'conduccion_agresiva')

# Definir funciones de membresía con más categorías
niveles = ['muy_bajo', 'bajo', 'medio', 'alto', 'muy_alto']

aceleracion.automf(names=niveles)
frenado.automf(names=niveles)
velocidad_variacion.automf(names=niveles)
vibraciones.automf(names=niveles)
conduccion_agresiva.automf(names=niveles)

# Definir reglas difusas mejoradas
reglas = [
    ctrl.Rule(aceleracion['muy_alto'] | frenado['muy_alto'] | velocidad_variacion['muy_alto'] | vibraciones['muy_alto'], conduccion_agresiva['muy_alto']),
    ctrl.Rule(aceleracion['alto'] | frenado['alto'] | velocidad_variacion['alto'] | vibraciones['alto'], conduccion_agresiva['alto']),
    ctrl.Rule(aceleracion['medio'] | frenado['medio'] | velocidad_variacion['medio'] | vibraciones['medio'], conduccion_agresiva['medio']),
    ctrl.Rule(aceleracion['bajo'] & frenado['bajo'] & velocidad_variacion['bajo'] & vibraciones['bajo'], conduccion_agresiva['bajo']),
    ctrl.Rule(aceleracion['muy_bajo'] & frenado['muy_bajo'] & velocidad_variacion['muy_bajo'] & vibraciones['muy_bajo'], conduccion_agresiva['muy_bajo'])
]

# Crear el sistema de control
sistema_control_agresiva = ctrl.ControlSystem(reglas)
simulacion_agresiva = ctrl.ControlSystemSimulation(sistema_control_agresiva)

# Datos de prueba con ID de conductor
datos_prueba = [
    {"id": 1, "aceleracion": 6.5, "frenado": 7.2, "velocidad_variacion": 14, "vibraciones": 6.8},
    {"id": 2, "aceleracion": 3.0, "frenado": 2.5, "velocidad_variacion": 5, "vibraciones": 3.2},
    {"id": 3, "aceleracion": 8.0, "frenado": 8.5, "velocidad_variacion": 17, "vibraciones": 9.0},
    {"id": 4, "aceleracion": 1.5, "frenado": 1.2, "velocidad_variacion": 2, "vibraciones": 1.0},
    {"id": 5, "aceleracion": 9.0, "frenado": 9.5, "velocidad_variacion": 18, "vibraciones": 9.8}
]

# Función para evaluar la conducción agresiva
def evaluar_conduccion(datos):
    simulacion_agresiva.input['aceleracion'] = datos['aceleracion']
    simulacion_agresiva.input['frenado'] = datos['frenado']
    simulacion_agresiva.input['velocidad_variacion'] = datos['velocidad_variacion']
    simulacion_agresiva.input['vibraciones'] = datos['vibraciones']
    simulacion_agresiva.compute()
    nivel_agresivo = simulacion_agresiva.output['conduccion_agresiva']
    
    if nivel_agresivo <= 4:
        estado = "✅ Conducción correcta"
    elif 5 <= nivel_agresivo <= 7:
        estado = "⚠️ Conducción en alerta"
    else:
        estado = "🚨 Conducción muy agresiva"
    
    print(f"ID {datos['id']} - Nivel de conducción agresiva: {nivel_agresivo:.2f} - {estado}")

# Evaluar cada conductor
for datos in datos_prueba:
    evaluar_conduccion(datos)