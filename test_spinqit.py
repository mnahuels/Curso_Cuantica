"""Prueba local de SpinQit para Python 3.9.13 de 64 bits.

Instalacion: py -3.9 -m pip install spinqit
Ejecucion:   py -3.9 test_spinqit.py
Opcional:    py -3.9 test_spinqit.py --repeticiones 5

Sin limites de tiempo: se informan por separado la importacion de SpinQit
y la ejecucion posterior de la prueba.
Para comparar PCs, usar las mismas versiones, opciones y carga del sistema.
Esta prueba usa el simulador local; no necesita un computador cuantico.
API: https://github.com/SpinQTech/SpinQit/blob/main/README.md
"""

import argparse
import math
import os
import platform
import statistics
import struct
import sys
import time
from importlib.metadata import PackageNotFoundError, version

SHOTS = 4096
QUBITS = (2, 8, 16)


def verificar_resultado(conteos, qubits):
    """GHZ debe dar solo todos ceros o todos unos, aproximadamente 50/50."""
    ceros, unos = "0" * qubits, "1" * qubits
    if not conteos or any(
        not isinstance(n, (int, float)) or not math.isfinite(n) or n < 0
        for n in conteos.values()
    ):
        raise ValueError("Conteos vacios o invalidos.")
    if sum(conteos.values()) != SHOTS:
        raise ValueError("La suma de conteos no coincide con los shots.")
    if any(n != 0 for estado, n in conteos.items() if estado not in (ceros, unos)):
        raise ValueError("Aparecieron estados incompatibles con el circuito GHZ.")
    # Tolerancia amplia para evitar falsos fallos si el backend muestrea.
    if any(abs(conteos.get(estado, 0) / SHOTS - 0.5) > 0.10
           for estado in (ceros, unos)):
        raise ValueError("La distribucion no es aproximadamente 50/50.")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repeticiones", type=int, default=3,
                        help="Mediciones por circuito, de 1 a 20 (por defecto: 3).")
    args = parser.parse_args()
    if not 1 <= args.repeticiones <= 20:
        parser.error("--repeticiones debe estar entre 1 y 20.")

    print("=" * 60)
    print("PRUEBA FUNCIONAL Y TIEMPOS DE SPINQIT")
    print("Python:", platform.python_version(), "| Ejecutable:", sys.executable)
    print("Sistema:", platform.platform())
    print("CPU:", platform.processor() or "No disponible")
    print("CPUs logicas:", os.cpu_count(), "| Python bits:", struct.calcsize("P") * 8)
    if sys.version_info[:3] != (3, 9, 13):
        print("AVISO: esta ejecucion no verifica especificamente Python 3.9.13.")
    if struct.calcsize("P") != 8:
        print("ERROR: usar Python de 64 bits para los paquetes binarios de SpinQit.")
        return 1

    try:
        inicio = time.perf_counter()
        from spinqit import (Circuit, H, CX, BasicSimulatorConfig,
                            get_basic_simulator, get_compiler)
        inicio_prueba = time.perf_counter()
        tiempo_importacion = inicio_prueba - inicio
        print("Importacion de SpinQit: {:.6f} s".format(tiempo_importacion))
    except ModuleNotFoundError as exc:
        if exc.name == "spinqit":
            print("ERROR: SpinQit no esta instalado en este interprete.")
            print('Instalar con: "{}" -m pip install spinqit'.format(sys.executable))
        else:
            print("ERROR: falta una dependencia de SpinQit:", exc)
        return 1
    except Exception as exc:
        print("ERROR al cargar SpinQit (API, dependencias o binarios):",
              type(exc).__name__, str(exc))
        return 1

    try:
        print("SpinQit:", version("spinqit"))
    except PackageNotFoundError:
        print("SpinQit: version no disponible (posible instalacion desde codigo).")

    print("Circuitos GHZ:", QUBITS, "| Shots:", SHOTS,
          "| Repeticiones:", args.repeticiones)
    print("Tiempo medido: execute + lectura de counts; sin compilacion ni validacion.")
    print("Cada circuito tiene un calentamiento previo excluido de la mediana.")
    print("Sin referencia de otra PC no existe un tiempo 'normal' universal.")
    try:
        inicio = time.perf_counter()
        compilador = get_compiler("native")
        simulador = get_basic_simulator()
        config = BasicSimulatorConfig()
        config.configure_shots(SHOTS)
        print("Inicializacion: {:.6f} s".format(time.perf_counter() - inicio))

        for n in QUBITS:
            print("\n--- {} qubits ---".format(n), flush=True)
            inicio = time.perf_counter()
            circuito = Circuit()
            q = circuito.allocateQubits(n)
            circuito << (H, q[0])
            for i in range(n - 1):
                circuito << (CX, (q[i], q[i + 1]))
            ejecutable = compilador.compile(circuito, 0)
            print("Construccion + compilacion: {:.6f} s".format(time.perf_counter() - inicio))

            tiempos = []
            for intento in range(args.repeticiones + 1):
                inicio = time.perf_counter()
                resultado = simulador.execute(ejecutable, config)
                conteos = resultado.counts
                segundos = time.perf_counter() - inicio
                verificar_resultado(conteos, n)
                if intento == 0:
                    print("Calentamiento: {:.6f} s | Resultado correcto".format(segundos),
                          flush=True)
                else:
                    tiempos.append(segundos)
                    print("Ejecucion {}: {:.6f} s | Resultado correcto".format(intento, segundos),
                          flush=True)

            mediana = statistics.median(tiempos)
            print("Minimo: {:.6f} s | Mediana: {:.6f} s | Maximo: {:.6f} s".format(
                min(tiempos), mediana, max(tiempos)))

    except Exception as exc:
        print("\nERROR en la prueba:", type(exc).__name__, str(exc))
        return 1

    tiempo_prueba = time.perf_counter() - inicio_prueba
    print("\nOK: SpinQit ejecuto y valido los tres circuitos.")
    print("Tiempo de importacion de SpinQit: {:.6f} s".format(tiempo_importacion))
    print("Tiempo de ejecucion posterior (sin importacion): {:.6f} s".format(tiempo_prueba))
    print("La ejecucion posterior incluye preparacion, compilacion, calentamientos,")
    print("simulaciones, validaciones y mensajes de consola posteriores a la importacion.")
    print("El resultado describe estos circuitos; no predice todos los algoritmos.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())  # 0: correcto; 1: fallo; 2: argumentos invalidos.
    except KeyboardInterrupt:
        print("\nPrueba interrumpida por el usuario.")
        sys.exit(130)

