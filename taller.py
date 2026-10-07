"""Funciones auxiliares del Taller de Programación Cuántica - Escuela CACIC 2026.

Uso:
    from taller import simular, ejecutar_en_triangulum

    resultado = simular(circuito)                                  # todos los qubits
    resultado = simular(circuito, qubits=[0], imagen="c.png")      # solo q[0]
    resultado = ejecutar_en_triangulum(circuito, [0, 1], "Bell_PC07")
"""

from spinqit import BasicSimulatorBackend, BasicSimulatorConfig, get_compiler, draw
from spinqit.backend import NMRConfig, get_nmr

# ------------------------------------------------------------------
# Datos de conexión con la SpinQ Triangulum (los completa el docente)
# ------------------------------------------------------------------
IP_TRIANGULUM = ""
PUERTO = 
USUARIO = ""
CONTRASENA = ""



def _compilar(circuito, imagen=None):
    """Compila el circuito y, si se pide, guarda su dibujo en un archivo."""
    ir = get_compiler("native").compile(circuito, 0)
    if imagen is not None:
        draw(ir, imagen)
    return ir


def simular(circuito, qubits=None, imagen=None, shots=1024):
    """Ejecuta el circuito en el simulador ideal.

    qubits: lista de qubits a medir (por ejemplo [0] o [0, 1]).
            Si no se indica, se miden todos.
    """
    ir = _compilar(circuito, imagen)
    config = BasicSimulatorConfig()
    config.configure_shots(shots)
    if qubits is not None:
        config.configure_measure_qubits(qubits)
    return BasicSimulatorBackend().execute(ir, config)


def ejecutar_en_triangulum(circuito, qubits, tarea="UlisesElRapa", descripcion="Taller CACIC 2026",
                           shots=1024, imagen=None):
    """Envía el circuito a la SpinQ Triangulum y espera el resultado.

    tarea: nombre único de la tarea, por ejemplo "Bell_PC07".
    """
    ir = _compilar(circuito, imagen)
    config = NMRConfig()
    config.configure_ip(IP_TRIANGULUM)
    config.configure_port(PUERTO)
    config.configure_account(USUARIO, CONTRASENA)
    config.configure_task(tarea, descripcion)
    config.configure_shots(shots)
    config.configure_measure_qubits(qubits)
    print("Enviando", tarea, "a la Triangulum... (puede demorar)")
    return get_nmr().execute(ir, config)





