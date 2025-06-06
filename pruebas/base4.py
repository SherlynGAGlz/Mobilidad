import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir las variables de entrada
kilometraje = ctrl.Antecedent(np.arange(0, 500000, 1000), 'kilometraje')
temperatura_motor = ctrl.Antecedent(np.arange(50, 130, 1), 'temperatura_motor')
conduccion_agresiva = ctrl.Antecedent(np.arange(0, 10, 1), 'conduccion_agresiva')
consumo_combustible = ctrl.Antecedent(np.arange(5, 50, 1), 'consumo_combustible')
presion_aceite = ctrl.Antecedent(np.arange(10, 80, 1), 'presion_aceite')
temperatura_ambiental = ctrl.Antecedent(np.arange(-10, 50, 1), 'temperatura_ambiental')
vibraciones_motor = ctrl.Antecedent(np.arange(0, 10, 1), 'vibraciones_motor')
desgaste_frenos = ctrl.Antecedent(np.arange(0, 100, 1), 'desgaste_frenos')

# Variables adicionales para mantenimiento
cambio_aceite = ctrl.Antecedent(np.arange(0, 10000, 500), 'cambio_aceite')
capacitacion_personal = ctrl.Antecedent(np.arange(0, 12, 1), 'capacitacion_personal')
chequeo_pasamanos = ctrl.Antecedent(np.arange(0, 6, 1), 'chequeo_pasamanos')
suspensiones_rampas = ctrl.Antecedent(np.arange(0, 6, 1), 'suspensiones_rampas')
carroceria = ctrl.Antecedent(np.arange(0, 6, 1), 'carroceria')
llantas = ctrl.Antecedent(np.arange(0, 12, 1), 'llantas')
luces_puertas = ctrl.Antecedent(np.arange(0, 6, 1), 'luces_puertas')
validadores_extintores = ctrl.Antecedent(np.arange(0, 6, 1), 'validadores_extintores')

# Definir la variable de salida
tiempo_restante_mantenimiento = ctrl.Consequent(np.arange(0, 12, 1), 'tiempo_restante_mantenimiento')

# Definir las funciones de pertenencia
kilometraje.automf(3)
temperatura_motor['normal'] = fuzz.trimf(temperatura_motor.universe, [50, 70, 90])
temperatura_motor['alta'] = fuzz.trimf(temperatura_motor.universe, [80, 100, 130])
temperatura_ambiental['fria'] = fuzz.trimf(temperatura_ambiental.universe, [-10, 0, 15])
temperatura_ambiental['moderada'] = fuzz.trimf(temperatura_ambiental.universe, [10, 20, 30])
temperatura_ambiental['caliente'] = fuzz.trimf(temperatura_ambiental.universe, [25, 35, 50])
conduccion_agresiva['baja'] = fuzz.trimf(conduccion_agresiva.universe, [0, 2, 4])
conduccion_agresiva['alta'] = fuzz.trimf(conduccion_agresiva.universe, [5, 7, 10])

# Definir reglas para mantenimiento
regla1 = ctrl.Rule(kilometraje['poor'] & temperatura_motor['alta'], tiempo_restante_mantenimiento['corto'])
regla2 = ctrl.Rule(kilometraje['average'] & conduccion_agresiva['alta'], tiempo_restante_mantenimiento['medio'])
regla3 = ctrl.Rule(kilometraje['good'] & conduccion_agresiva['baja'], tiempo_restante_mantenimiento['largo'])
regla4 = ctrl.Rule(consumo_combustible['alto'] & presion_aceite['baja'], tiempo_restante_mantenimiento['corto'])
regla5 = ctrl.Rule(consumo_combustible['bajo'] & presion_aceite['alta'], tiempo_restante_mantenimiento['largo'])
regla6 = ctrl.Rule(temperatura_ambiental['caliente'] & temperatura_motor['alta'], tiempo_restante_mantenimiento['corto'])
regla7 = ctrl.Rule(vibraciones_motor['altas'], tiempo_restante_mantenimiento['corto'])
regla8 = ctrl.Rule(desgaste_frenos['alto'], tiempo_restante_mantenimiento['corto'])
regla9 = ctrl.Rule(desgaste_frenos['bajo'], tiempo_restante_mantenimiento['largo'])

# Reglas de mantenimiento adicional
regla10 = ctrl.Rule(cambio_aceite['poor'], tiempo_restante_mantenimiento['corto'])
regla11 = ctrl.Rule(capacitacion_personal['poor'], tiempo_restante_mantenimiento['corto'])
regla12 = ctrl.Rule(chequeo_pasamanos['poor'], tiempo_restante_mantenimiento['corto'])
regla13 = ctrl.Rule(llantas['poor'], tiempo_restante_mantenimiento['corto'])
regla14 = ctrl.Rule(validadores_extintores['poor'], tiempo_restante_mantenimiento['corto'])

# Sistema de control
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9, regla10, regla11, regla12, regla13, regla14])
simulacion = ctrl.ControlSystemSimulation(sistema_control)

# Simulación con datos de ejemplo
simulacion.input['kilometraje'] = 200000
simulacion.input['temperatura_motor'] = 95
simulacion.input['conduccion_agresiva'] = 6
simulacion.input['consumo_combustible'] = 30
simulacion.input['presion_aceite'] = 25
simulacion.input['temperatura_ambiental'] = 35
simulacion.input['vibraciones_motor'] = 7
simulacion.input['desgaste_frenos'] = 80
simulacion.input['cambio_aceite'] = 9000
simulacion.input['capacitacion_personal'] = 4
simulacion.input['chequeo_pasamanos'] = 2
simulacion.input['llantas'] = 8
simulacion.input['validadores_extintores'] = 3
simulacion.compute()

print(f"Tiempo restante estimado para mantenimiento: {simulacion.output['tiempo_restante_mantenimiento']:.2f} meses")
