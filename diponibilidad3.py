import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import datetime
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

# Función para organizar mantenimiento permitiendo solo un camión por día
def organizar_mantenimiento(camiones):
    plan_mantenimiento = []
    fecha_actual = datetime.date.today()
    
    # Obtener las fechas de mantenimiento estimadas
    camiones_con_fechas = []
    for camion in camiones:
        vida_util, piezas_criticas = predecir_mantenimiento(camion)
        fecha_mantenimiento = fecha_actual + datetime.timedelta(weeks=vida_util)
        camiones_con_fechas.append((camion['id'], fecha_mantenimiento, piezas_criticas))
    
    # Ordenar por fecha estimada
    camiones_con_fechas.sort(key=lambda x: x[1])
    
    # Asignar fechas asegurando solo un camión por día
    fechas_ocupadas = set()
    for camion_id, fecha, piezas in camiones_con_fechas:
        while fecha in fechas_ocupadas:
            fecha += datetime.timedelta(days=7)  # Mover al siguiente día disponible
        fechas_ocupadas.add(fecha)
        plan_mantenimiento.append((camion_id, fecha, piezas))
    
    print("\n📅 Plan de mantenimiento organizado:")
    for camion_id, fecha, piezas in plan_mantenimiento:
        print(f"- Camión {camion_id}: Mantenimiento programado para {fecha}")
        if piezas:
            print(f"  ⚠️ Piezas críticas a revisar: {', '.join(piezas.keys())}")
    
    return plan_mantenimiento

# Simulación con datos de prueba
if __name__ == "__main__":
    camiones_prueba = [
        {"id": 1, "kilometraje": 300000, "temperatura_motor": 90, "horas_operacion": 2500, "historial_eventos": 2, "rpm": 1500, "masas_homocineticas": 5, "desgaste_frenos": 4},
        {"id": 2, "kilometraje": 1505500, "temperatura_motor": 15, "horas_operacion": 400, "historial_eventos": 9, "rpm": 87000, "masas_homocineticas": 4, "desgaste_frenos": 9},
        {"id": 3, "kilometraje": 900000, "temperatura_motor": 95, "horas_operacion": 4000, "historial_eventos": 5, "rpm": 3000, "masas_homocineticas": 8, "desgaste_frenos": 9},
    ]
    
    organizar_mantenimiento(camiones_prueba)