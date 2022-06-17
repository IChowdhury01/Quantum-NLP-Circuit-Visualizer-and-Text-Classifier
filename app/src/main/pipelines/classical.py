from discopy import grammar, Dim
from lambeq import BobcatParser, Rewriter, AtomicType, MPSAnsatz

from app.src.main.constants import sample_sentences


def classical_compute(sentence):
    # Convert to string diagram
    parser = BobcatParser(verbose='text')
    diagram = parser.sentence2diagram(sentence)  # syntax-based, not bag-of-words
    grammar.draw(diagram, title='h', figsize=(14, 3), fontsize=12)

    # Rewrite string diagram, to reduce performance costs / training time
    rewriter = Rewriter(['prepositional_phrase', 'determiner'])  # lower tensor count on prepositions
    prep_reduced_diagram = rewriter(diagram).normal_form()
    prep_reduced_diagram.draw(figsize=(9, 4), fontsize=13)

    curry_functor = Rewriter(['curry'])  # reduce number of cups
    curried_diagram = curry_functor(prep_reduced_diagram).normal_form()
    curried_diagram.draw(figsize=(5, 4), fontsize=13)

    # Parameterize: convert abstract string diagram to concrete tensor network
    # Define atomic types
    N = AtomicType.NOUN
    S = AtomicType.SENTENCE
    P = AtomicType.PREPOSITIONAL_PHRASE
    C = AtomicType.CONJUNCTION

    # Tensor network
    mps_ansatz = MPSAnsatz({N: Dim(4), S: Dim(2), P: Dim(3), C: Dim(1)}, bond_dim=3)
    mps_diagram = mps_ansatz(diagram)
    mps_diagram.draw(figsize=(13, 7), fontsize=13)

    # Todo: Training

if __name__ == "__main__":
    test_sentence = sample_sentences.ADS_ISSUED
    print(f"Input string: {test_sentence}")
    classical_compute(test_sentence)
