from lambeq import BobcatParser

# Parse the sentence
parser = BobcatParser(verbose='suppress')
diagram = parser.sentence2diagram("Miles gave Gwen a ride")

diagram.draw(figsize=(11,5), fontsize=13)

#from lambeq import Rewriter

# Apply rewrite rule for prepositional phrases

#rewriter = Rewriter(['prepositional_phrase', 'determiner'])
#rewritten_diagram = rewriter(diagram)

#rewritten_diagram.draw(figsize=(11,5), fontsize=13)

#normalised_diagram = rewritten_diagram.normal_form()
#normalised_diagram.draw(figsize=(9,4), fontsize=13)

#curry_functor = Rewriter(['curry'])
#curried_diagram = curry_functor(normalised_diagram)
#curried_diagram.draw(figsize=(9,4), fontsize=13)

#curried_diagram.normal_form().draw(figsize=(5,4), fontsize=13)