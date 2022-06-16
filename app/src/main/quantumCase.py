from lambeq import BobcatParser
from discopy import grammar
from lambeq import Rewriter
import sampleSentences

testSentence = sampleSentences.ADS_ISSUED

# Convert to string diagram
parser = BobcatParser(verbose='text')
diagram = parser.sentence2diagram(testSentence)  # syntax-based, not bag-of-words
grammar.draw(diagram, title='h', figsize=(14, 3), fontsize=12)

# Rewrite string diagram, to reduce performance costs / training time
rewriter = Rewriter(['prepositional_phrase', 'determiner'])  # lower tensor count on prepositions
prep_reduced_diagram = rewriter(diagram).normal_form()
prep_reduced_diagram.draw(figsize=(9, 4), fontsize=13)

curry_functor = Rewriter(['curry'])  # reduce number of cups
curried_diagram = curry_functor(prep_reduced_diagram).normal_form()
curried_diagram.draw(figsize=(5, 4), fontsize=13)


# from lambeq import AtomicType, IQPAnsatz
#
# # Define atomic types
# N = AtomicType.NOUN
# S = AtomicType.SENTENCE
#
# # Convert string diagram to quantum circuit
# ansatz = IQPAnsatz({N: 1, S: 1}, n_layers=2)
# discopy_circuit = ansatz(diagram)
# #discopy_circuit.draw(figsize=(15,10))
#
# from pytket.circuit.display import render_circuit_jupyter
#
# tket_circuit = discopy_circuit.to_tk()
#
# render_circuit_jupyter(tket_circuit)
