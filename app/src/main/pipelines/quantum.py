import os
import webbrowser

from discopy import grammar
from lambeq import BobcatParser, Rewriter, AtomicType, IQPAnsatz
from matplotlib import pyplot
from pytket.circuit.display import render_circuit_as_html
from pytket.extensions.qiskit import tk_to_qiskit

from app.src.main.constants import sample_sentences
from settings import GEN_PATH


def quantum_compute(sentence):
    # Convert to string diagram
    parser = BobcatParser(verbose='text')
    diagram = parser.sentence2diagram(test_sentence)  # syntax-based, not bag-of-words
    grammar.draw(diagram, title='h', figsize=(14, 3), fontsize=12)

    # Rewrite string diagram, to reduce performance costs / training time
    rewriter = Rewriter(['prepositional_phrase', 'determiner'])  # lower tensor count on prepositions
    prep_reduced_diagram = rewriter(diagram).normal_form()
    prep_reduced_diagram.draw(figsize=(9, 4), fontsize=13)

    curry_functor = Rewriter(['curry'])  # reduce number of cups
    curried_diagram = curry_functor(prep_reduced_diagram).normal_form()
    curried_diagram.draw(figsize=(5, 4), fontsize=13)

    # Parameterize: convert abstract string diagram to concrete quantum circuit
    N = AtomicType.NOUN
    S = AtomicType.SENTENCE
    P = AtomicType.PREPOSITIONAL_PHRASE
    C = AtomicType.CONJUNCTION
    ansatz = IQPAnsatz({N: 1, S: 1, P: 1, C: 1}, n_layers=4)

    discopy_circuit = ansatz(diagram)   # Quantum circuit, DisCoPy format
    discopy_circuit.draw(figsize=(15, 10))

    tket_circuit = discopy_circuit.to_tk()  # Quantum circuit, pytket format
    save_path = os.path.join(GEN_PATH, 'tket_circuit.html')
    with open(save_path, "w") as file:
        file.write(render_circuit_as_html(tket_circuit, False))
    webbrowser.open_new(save_path)

    qiskit_circuit = tk_to_qiskit(tket_circuit)  # qiskit format
    qiskit_circuit.draw(output='mpl')
    pyplot.show()

    # Todo: Training


test_sentence = sample_sentences.BASIC_TEST
print(f"Input string: {test_sentence}")
quantum_compute(test_sentence)
