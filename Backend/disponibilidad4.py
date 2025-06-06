import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import datetime
from basechida import predecir_mantenimiento  # Importamos la IA de mantenimiento

# Definimos las variables difusas con 6 niveles en vez de 3
cantidad_camiones = ctrl.Antecedent(np.arange(0, 101, 1), 'cantidad_camiones')
congestion = ctrl.Antecedent(np.arange(0, 101, 1), 'congestion')
mantenimiento_pendiente = ctrl.Antecedent(np.arange(0, 101, 1), 'mantenimiento_pendiente')
orden_mantenimiento = ctrl.Consequent(np.arange(0, 101, 1), 'orden_mantenimiento')

# Definir 6 etiquetas de membresía para cada variable
etiquetas = ['muy_bajo', 'bajo', 'medio_bajo', 'medio_alto', 'alto', 'muy_alto']
cantidad_camiones.automf(names=etiquetas)
congestion.automf(names=etiquetas)
mantenimiento_pendiente.automf(names=etiquetas)
orden_mantenimiento.automf(names=etiquetas)

# Reglas difusas ampliadas
reglas = [
    ctrl.Rule(mantenimiento_pendiente['muy_bajo'] & congestion['muy_bajo'], orden_mantenimiento['muy_bajo']),
    ctrl.Rule(mantenimiento_pendiente['bajo'] & congestion['bajo'], orden_mantenimiento['bajo']),
    ctrl.Rule(mantenimiento_pendiente['medio_bajo'] & congestion['medio_bajo'], orden_mantenimiento['medio_bajo']),
    ctrl.Rule(mantenimiento_pendiente['medio_alto'] & congestion['medio_alto'], orden_mantenimiento['medio_alto']),
    ctrl.Rule(mantenimiento_pendiente['alto'] & congestion['alto'], orden_mantenimiento['alto']),
    ctrl.Rule(mantenimiento_pendiente['muy_alto'] & congestion['muy_alto'], orden_mantenimiento['muy_alto']),
]

sistema_ctrl = ctrl.ControlSystem(reglas)
simulador_mantenimiento = ctrl.ControlSystemSimulation(sistema_ctrl)

# Función para organizar mantenimiento con restricción de un camión por día
def organizar_mantenimiento(camiones):
    plan_mantenimiento = []
    fecha_actual = datetime.date.today()
    
    camiones_con_fechas = []
    for camion in camiones:
        vida_util, piezas_criticas = predecir_mantenimiento(camion)
        fecha_mantenimiento = fecha_actual + datetime.timedelta(weeks=vida_util)
        camiones_con_fechas.append((camion['id'], fecha_mantenimiento, piezas_criticas))
    
    camiones_con_fechas.sort(key=lambda x: x[1])
    
    fechas_ocupadas = set()
    for camion_id, fecha, piezas in camiones_con_fechas:
        while fecha in fechas_ocupadas:
            fecha += datetime.timedelta(days=1)
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