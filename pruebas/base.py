import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir las variables de entrada
kilometraje = ctrl.Antecedent(np.arange(0, 500000, 1000), 'kilometraje')
condicion_camino = ctrl.Antecedent(np.arange(0, 10, 1), 'condicion_camino') # 0 = excelente, 10 = pésima
frecuencia_mantenimiento = ctrl.Antecedent(np.arange(0, 12, 1), 'frecuencia_mantenimiento')

# Definir las variables de salida
riesgo_fallo = ctrl.Consequent(np.arange(0, 100, 1), 'riesgo_fallo')
tiempo_restante_mantenimiento = ctrl.Consequent(np.arange(0, 12, 1), 'tiempo_restante_mantenimiento')

# Definir las funciones de pertenencia
kilometraje.automf(3)
condicion_camino.automf(3)
frecuencia_mantenimiento.automf(3)

riesgo_fallo['bajo'] = fuzz.trimf(riesgo_fallo.universe, [0, 25, 50])
riesgo_fallo['medio'] = fuzz.trimf(riesgo_fallo.universe, [25, 50, 75])
riesgo_fallo['alto'] = fuzz.trimf(riesgo_fallo.universe, [50, 75, 100])

tiempo_restante_mantenimiento['corto'] = fuzz.trimf(tiempo_restante_mantenimiento.universe, [0, 3, 6])
tiempo_restante_mantenimiento['medio'] = fuzz.trimf(tiempo_restante_mantenimiento.universe, [3, 6, 9])
tiempo_restante_mantenimiento['largo'] = fuzz.trimf(tiempo_restante_mantenimiento.universe, [6, 9, 12])

# Definir las reglas difusas
regla1 = ctrl.Rule(kilometraje['poor'] & condicion_camino['good'], riesgo_fallo['bajo'])
regla2 = ctrl.Rule(kilometraje['average'] & condicion_camino['average'], riesgo_fallo['medio'])
regla3 = ctrl.Rule(kilometraje['good'] & condicion_camino['poor'], riesgo_fallo['alto'])

# Sistema de control
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3])
simulacion = ctrl.ControlSystemSimulation(sistema_control)

# Simulación con datos de entrada
simulacion.input['kilometraje'] = 200000
simulacion.input['condicion_camino'] = 7
simulacion.compute()

print(f"Riesgo de fallo estimado: {simulacion.output['riesgo_fallo']:.2f}%")
