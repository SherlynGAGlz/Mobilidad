import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

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

# Simulación con datos de ejemplo
simulacion_agresiva.input['aceleracion'] = 6.5
simulacion_agresiva.input['frenado'] = 7.2
simulacion_agresiva.input['velocidad_variacion'] = 14
simulacion_agresiva.input['vibraciones'] = 6.8
simulacion_agresiva.compute()

print(f"Nivel de conducción agresiva: {simulacion_agresiva.output['conduccion_agresiva']:.2f} (0-10)")
