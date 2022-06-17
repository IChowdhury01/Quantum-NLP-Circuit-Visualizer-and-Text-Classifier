from lambeq import BobcatParser
from discopy import grammar
from lambeq import Rewriter
import sampleSentences

testSentence = sampleSentences.ADS_ISSUED

# Convert to string diagram
parser = BobcatParser(verbose='text')
diagram = parser.sentence2diagram(sentence)

from lambeq import AtomicType, IQPAnsatz

# Define atomic types
N = AtomicType.NOUN
S = AtomicType.SENTENCE

# Convert string diagram to quantum circuit
ansatz = IQPAnsatz({N: 1, S: 1}, n_layers=2)
discopy_circuit = ansatz(diagram)
#discopy_circuit.draw(figsize=(15,10))

from pytket.circuit.display import render_circuit_as_html

tket_circuit = discopy_circuit.to_tk()

with open("data.html", "w") as file:
  file.write(render_circuit_as_html(tket_circuit, False))