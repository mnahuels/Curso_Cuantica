import numpy as np
from spinqit import Circuit, X, H, Z, CX, RX, draw
from spinqit import get_compiler, get_basic_simulator, BasicSimulatorConfig

engine = get_basic_simulator()
config = BasicSimulatorConfig()
config.configure_shots(1000)
compilador = get_compiler("native")


# 1 Superposición Uniforme Hadamard

circ1 = Circuit()
q1 = circ1.allocateQubits(3)
for i in range(3):
    circ1 << (H, q1[i])

ir1 = compilador.compile(circ1, 0)
draw(ir1, "circuito_1_superposicion.png")
config.configure_measure_qubits([q1[0], q1[1], q1[2]])
result1 = engine.execute(ir1, config)

print("--- Circuito 1: Superposición 3 Cúbits ---")
print("Counts:", result1.counts)
print("Probabilities:", result1.probabilities, "\n")



# 2 Estado de Bell Entrelazamiento

circ2 = Circuit()
q2 = circ2.allocateQubits(2)
circ2 << (H, q2[0])
circ2 << (CX, (q2[0], q2[1]))

ir2 = compilador.compile(circ2, 0)
draw(ir2, "circuito_2_bell.png")
config.configure_measure_qubits([q2[0], q2[1]])
result2 = engine.execute(ir2, config)

print("--- Circuito 2: Estado de Bell ---")
print("Counts:", result2.counts)
print("Probabilities:", result2.probabilities, "\n")



# 3 Operador de Inversión de Fase 

circ3 = Circuit()
q3 = circ3.allocateQubits(1)
circ3 << (H, q3[0])
circ3 << (Z, q3[0])
circ3 << (H, q3[0])

ir3 = compilador.compile(circ3, 0)
draw(ir3, "circuito_3_fase.png")
config.configure_measure_qubits([q3[0]])
result3 = engine.execute(ir3, config)

print("--- Circuito 3: Inversión de Fase ---")
print("Counts:", result3.counts)
print("Probabilities:", result3.probabilities, "\n")



# 4 Estado GHZ de 3 cúbits

circ4 = Circuit()
q4 = circ4.allocateQubits(3)
circ4 << (H, q4[0])
circ4 << (CX, (q4[0], q4[1]))
circ4 << (CX, (q4[1], q4[2]))

ir4 = compilador.compile(circ4, 0)
draw(ir4, "circuito_4_ghz.png")
config.configure_measure_qubits([q4[0], q4[1], q4[2]])
result4 = engine.execute(ir4, config)

print("--- Circuito 4: Estado GHZ ---")
print("Counts:", result4.counts)
print("Probabilities:", result4.probabilities, "\n")



# 5 RX

circ5 = Circuit()
q5 = circ5.allocateQubits(1)
circ5 << (RX(np.pi / 2), q5[0])

ir5 = compilador.compile(circ5, 0)
draw(ir5, "circuito_5_rx.png")
config.configure_measure_qubits([q5[0]])
result5 = engine.execute(ir5, config)

print("--- Circuito 5: Rotación RX ---")
print("Counts:", result5.counts)
print("Probabilities:", result5.probabilities, "\n")



# 6 Teleportación Cuántica

circ6 = Circuit()
q6 = circ6.allocateQubits(3)
circ6 << (H, q6[0])
circ6 << (H, q6[1])
circ6 << (CX, (q6[1], q6[2]))

ir6 = compilador.compile(circ6, 0)
draw(ir6, "circuito_6_teleport_prep.png")
config.configure_measure_qubits([q6[0], q6[1], q6[2]])
result6 = engine.execute(ir6, config)

print("--- Circuito 6: Teleportación (Preparación) ---")
print("Counts:", result6.counts)
print("Probabilities:", result6.probabilities, "\n")



# interferencia Cuántica Deutsch

circ7 = Circuit()
q7 = circ7.allocateQubits(2)
circ7 << (X, q7[1])
circ7 << (H, q7[0])
circ7 << (H, q7[1])
circ7 << (CX, (q7[0], q7[1]))
circ7 << (H, q7[0])

ir7 = compilador.compile(circ7, 0)
draw(ir7, "circuito_7_interferencia.png")
config.configure_measure_qubits([q7[0]])
result7 = engine.execute(ir7, config)

print("--- Circuito 7: Interferencia Cuántica ---")
print("Counts:", result7.counts)
print("Probabilities:", result7.probabilities, "\n")