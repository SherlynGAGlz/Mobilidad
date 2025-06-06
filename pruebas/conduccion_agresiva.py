import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir las variables de entrada
aceleracion = ctrl.Antecedent(np.arange(0, 10, 0.1), 'aceleracion')
frenado = ctrl.Antecedent(np.arange(0, 10, 0.1), 'frenado')
velocidad_variacion = ctrl.Antecedent(np.arange(0, 20, 0.5), 'velocidad_variacion')
vibraciones = ctrl.Antecedent(np.arange(0, 10, 0.1), 'vibraciones')

# Variable de salida
conduccion_agresiva = ctrl.Consequent(np.arange(0, 10, 0.1), 'conduccion_agresiva')

# Definir funciones de pertenencia
aceleracion['baja'] = fuzz.trimf(aceleracion.universe, [0, 1, 3])
aceleracion['moderada'] = fuzz.trimf(aceleracion.universe, [2, 4, 6])
aceleracion['alta'] = fuzz.trimf(aceleracion.universe, [5, 7, 10])

frenado['suave'] = fuzz.trimf(frenado.universe, [0, 1, 3])
frenado['moderado'] = fuzz.trimf(frenado.universe, [2, 4, 6])
frenado['brusco'] = fuzz.trimf(frenado.universe, [5, 7, 10])

velocidad_variacion['estable'] = fuzz.trimf(velocidad_variacion.universe, [0, 2, 5])
velocidad_variacion['moderada'] = fuzz.trimf(velocidad_variacion.universe, [4, 7, 12])
velocidad_variacion['brusca'] = fuzz.trimf(velocidad_variacion.universe, [10, 15, 20])

vibraciones['bajas'] = fuzz.trimf(vibraciones.universe, [0, 2, 4])
vibraciones['moderadas'] = fuzz.trimf(vibraciones.universe, [3, 5, 7])
vibraciones['altas'] = fuzz.trimf(vibraciones.universe, [6, 8, 10])

conduccion_agresiva['baja'] = fuzz.trimf(conduccion_agresiva.universe, [0, 2, 4])
conduccion_agresiva['moderada'] = fuzz.trimf(conduccion_agresiva.universe, [3, 5, 7])
conduccion_agresiva['alta'] = fuzz.trimf(conduccion_agresiva.universe, [6, 8, 10])

# Definir reglas difusas
regla1 = ctrl.Rule(aceleracion['alta'] | frenado['brusco'] | velocidad_variacion['brusca'] | vibraciones['altas'], conduccion_agresiva['alta'])
regla2 = ctrl.Rule(aceleracion['moderada'] | frenado['moderado'] | velocidad_variacion['moderada'] | vibraciones['moderadas'], conduccion_agresiva['moderada'])
regla3 = ctrl.Rule(aceleracion['baja'] & frenado['suave'] & velocidad_variacion['estable'] & vibraciones['bajas'], conduccion_agresiva['baja'])

# Crear el sistema de control
sistema_control_agresiva = ctrl.ControlSystem([regla1, regla2, regla3])
simulacion_agresiva = ctrl.ControlSystemSimulation(sistema_control_agresiva)

# Simulación con datos de ejemplo
simulacion_agresiva.input['aceleracion'] = 6
simulacion_agresiva.input['frenado'] = 7
simulacion_agresiva.input['velocidad_variacion'] = 12
simulacion_agresiva.input['vibraciones'] = 5
simulacion_agresiva.compute()

print(f"Nivel de conducción agresiva: {simulacion_agresiva.output['conduccion_agresiva']:.2f} (0-10)")
