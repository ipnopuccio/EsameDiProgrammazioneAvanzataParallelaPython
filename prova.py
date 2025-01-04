from lmc import Assembler, LMC

programma_assembly = """INP
STA 50
INP
ADD 50
OUT
"""

assembler = Assembler()
codice_macchina = assembler.assemble(programma_assembly)
print("Codice macchina:", codice_macchina)

lmc = LMC()
lmc.load_program(codice_macchina)
lmc.set_input([5, 3])

risultato = lmc.run()
print("Risultato:", risultato)