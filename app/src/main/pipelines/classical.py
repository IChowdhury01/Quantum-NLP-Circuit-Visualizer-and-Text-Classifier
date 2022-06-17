from discopy import grammar
from lambeq import BobcatParser, Rewriter

from app.src.main.constants import sample_sentences


def classical_compute(sentence):
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

    # Todo: Parameterize: convert abstract string diagram to concrete tensor network
    # Todo: Training


test_sentence = sample_sentences.BASIC_TEST
classical_compute(test_sentence)
