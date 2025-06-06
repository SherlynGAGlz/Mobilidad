import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import datetime
import random
from basechida import predecir_mantenimiento  # Importamos la IA de mantenimiento

# Definimos las variables difusas
cantidad_camiones = ctrl.Antecedent(np.arange(0, 101, 1), 'cantidad_camiones')
congestion = ctrl.Antecedent(np.arange(0, 101, 1), 'congestion')  # % de congestión de rutas
mantenimiento_pendiente = ctrl.Antecedent(np.arange(0, 101, 1), 'mantenimiento_pendiente')  # % de camiones que requieren mantenimiento
orden_mantenimiento = ctrl.Consequent(np.arange(0, 101, 1), 'orden_mantenimiento')

# Funciones de membresía
cantidad_camiones.automf(3)
congestion.automf(3)
mantenimiento_pendiente.automf(3)
orden_mantenimiento.automf(3)

# Reglas difusas para decidir el orden de mantenimiento
reglas = [
    ctrl.Rule(mantenimiento_pendiente['poor'] & congestion['poor'], orden_mantenimiento['poor']),
    ctrl.Rule(mantenimiento_pendiente['average'] & congestion['average'], orden_mantenimiento['average']),
    ctrl.Rule(mantenimiento_pendiente['good'] & congestion['good'], orden_mantenimiento['good']),
    ctrl.Rule(mantenimiento_pendiente['good'] & congestion['average'], orden_mantenimiento['average']),
    ctrl.Rule(mantenimiento_pendiente['average'] & congestion['good'], orden_mantenimiento['average'])
]

sistema_ctrl = ctrl.ControlSystem(reglas)
simulador_mantenimiento = ctrl.ControlSystemSimulation(sistema_ctrl)

# Función para organizar mantenimiento

def organizar_mantenimiento(camiones):
    plan_mantenimiento = []
    fecha_actual = datetime.date.today()
    
    for camion in camiones:
        vida_util, piezas_criticas = predecir_mantenimiento(camion)
        fecha_mantenimiento = fecha_actual + datetime.timedelta(weeks=vida_util)
        plan_mantenimiento.append((camion['id'], fecha_mantenimiento, piezas_criticas))
    
    # Ordenar camiones por fecha de mantenimiento
    plan_mantenimiento.sort(key=lambda x: x[1])
    
    print("\n📅 Plan de mantenimiento organizado:\n")
    for camion_id, fecha, piezas in plan_mantenimiento:
        print(f"Camión {camion_id}: Mantenimiento programado para {fecha}")
        if piezas:
            print(f"  ⚠️ Piezas críticas a revisar: {', '.join(piezas.keys())}")
    
    return plan_mantenimiento

# Simulación con datos de prueba
if __name__ == "__main__":
    camiones_prueba = [
        {"id": 1, "kilometraje": 300000, "temperatura_motor": 90, "horas_operacion": 2500, "historial_eventos": 2, "rpm": 1500, "masas_homocineticas": 5, "desgaste_frenos": 4},
        {"id": 2, "kilometraje": 150000, "temperatura_motor": 85, "horas_operacion": 1000, "historial_eventos": 1, "rpm": 2000, "masas_homocineticas": 2, "desgaste_frenos": 1},
        {"id": 3, "kilometraje": 900000, "temperatura_motor": 95, "horas_operacion": 4000, "historial_eventos": 5, "rpm": 3000, "masas_homocineticas": 8, "desgaste_frenos": 9},
    ]
    
    organizar_mantenimiento(camiones_prueba)
