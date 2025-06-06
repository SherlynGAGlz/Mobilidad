import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir las variables de entrada
#A esta ia le hace falta las piezas que son para remplazar,
#el cambio  de aceite, capacitacion de personal para gigante 001
#el chequeo de pasamanos, reguladores, asientos 0
#suspenciones, rampas, asegurar timepos de personas capacitadas para la reparacion de las cosas
#carroceria, espejos, llantas, luces, puertas, señalizacoines internas, validadores de tarjetas, ventanillas y extintores
#desgaste de llantas,
#el cambio de aceite es por kilometraje y se le cambia normalmente a los 300 mil kilomentros 
#Amortiguadores que ees parte de la suspencion tienen su vida util y se le cambian frecuentemente 
#balatas 
#obd ll se tiene que acer periodicamente
# hay gps que te dan consumo de combustible km recorridos,
#a lo mejor se tiene que cambiar por kilometraje en vez de tiempo
#Saber que tanto acite tiene el camion como lo vamos a hacer no lo se en vez de que lo cheque la persona

kilometraje = ctrl.Antecedent(np.arange(0, 500000, 1000), 'kilometraje')
temperatura_motor = ctrl.Antecedent(np.arange(50, 130, 1), 'temperatura_motor')
conduccion_agresiva = ctrl.Antecedent(np.arange(0, 10, 1), 'conduccion_agresiva')#Hacer una ia para detectar la conduccion agresiva
consumo_combustible = ctrl.Antecedent(np.arange(5, 50, 1), 'consumo_combustible')
presion_aceite = ctrl.Antecedent(np.arange(10, 80, 1), 'presion_aceite')
temperatura_ambiental = ctrl.Antecedent(np.arange(-10, 50, 1), 'temperatura_ambiental')
vibraciones_motor = ctrl.Antecedent(np.arange(0, 10, 1), 'vibraciones_motor')
desgaste_frenos = ctrl.Antecedent(np.arange(0, 100, 1), 'desgaste_frenos')

# Definir la variable de salida
tiempo_restante_mantenimiento = ctrl.Consequent(np.arange(0, 12, 1), 'tiempo_restante_mantenimiento')

# Definir las funciones de pertenencia
kilometraje.automf(3)
temperatura_motor['nomal'] = fuzz.trimf(temperatura_motor.universe, [50, 70, 90])
temperatura_motor['alta'] = fuzz.trimf(temperatura_motor.universe, [80, 100, 130])
temperatura_ambiental['fria'] = fuzz.trimf(temperatura_ambiental.universe, [-10, 0, 15])
temperatura_ambiental['moderada'] = fuzz.trimf(temperatura_ambiental.universe, [10, 20, 30])
temperatura_ambiental['caliente'] = fuzz.trimf(temperatura_ambiental.universe, [25, 35, 50])
conduccion_agresiva['baja'] = fuzz.trimf(conduccion_agresiva.universe, [0, 2, 4])
conduccion_agresiva['alta'] = fuzz.trimf(conduccion_agresiva.universe, [5, 7, 10])
consumo_combustible['bajo'] = fuzz.trimf(consumo_combustible.universe, [5, 15, 25])
consumo_combustible['alto'] = fuzz.trimf(consumo_combustible.universe, [20, 35, 50])
presion_aceite['baja'] = fuzz.trimf(presion_aceite.universe, [10, 30, 50])
presion_aceite['alta'] = fuzz.trimf(presion_aceite.universe, [40, 60, 80])
vibraciones_motor['bajas'] = fuzz.trimf(vibraciones_motor.universe, [0, 2, 5])
vibraciones_motor['altas'] = fuzz.trimf(vibraciones_motor.universe, [4, 7, 10])
desgaste_frenos['bajo'] = fuzz.trimf(desgaste_frenos.universe, [0, 20, 40])
desgaste_frenos['alto'] = fuzz.trimf(desgaste_frenos.universe, [60, 80, 100])

tiempo_restante_mantenimiento['corto'] = fuzz.trimf(tiempo_restante_mantenimiento.universe, [0, 3, 6])
tiempo_restante_mantenimiento['medio'] = fuzz.trimf(tiempo_restante_mantenimiento.universe, [3, 6, 9])
tiempo_restante_mantenimiento['largo'] = fuzz.trimf(tiempo_restante_mantenimiento.universe, [6, 9, 12])

# Definir las reglas difusas
regla1 = ctrl.Rule(kilometraje['poor'] & temperatura_motor['alta'], tiempo_restante_mantenimiento['corto'])
regla2 = ctrl.Rule(kilometraje['average'] & conduccion_agresiva['alta'], tiempo_restante_mantenimiento['medio'])
regla3 = ctrl.Rule(kilometraje['good'] & conduccion_agresiva['baja'], tiempo_restante_mantenimiento['largo'])
regla4 = ctrl.Rule(consumo_combustible['alto'] & presion_aceite['baja'], tiempo_restante_mantenimiento['corto'])
regla5 = ctrl.Rule(consumo_combustible['bajo'] & presion_aceite['alta'], tiempo_restante_mantenimiento['largo'])
regla6 = ctrl.Rule(temperatura_ambiental['caliente'] & temperatura_motor['alta'], tiempo_restante_mantenimiento['corto'])
regla7 = ctrl.Rule(vibraciones_motor['altas'], tiempo_restante_mantenimiento['corto'])
regla8 = ctrl.Rule(desgaste_frenos['alto'], tiempo_restante_mantenimiento['corto'])
regla9 = ctrl.Rule(desgaste_frenos['bajo'], tiempo_restante_mantenimiento['largo'])

# Sistema de control
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9])
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
simulacion.compute()

print(f"Tiempo restante estimado para mantenimiento: {simulacion.output['tiempo_restante_mantenimiento']:.2f} meses")
