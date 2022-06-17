from lambeq import BobcatParser

sentence = 'Program means 100% during the Contract'

# Get a string diagram
parser = BobcatParser(verbose='text')
diagram = parser.sentence2diagram(sentence)

from lambeq import AtomicType, IQPAnsatz

# Define atomic types
N = AtomicType.NOUN
S = AtomicType.SENTENCE

from lambeq import SpiderAnsatz
from discopy import Dim

#spider_ansatz = SpiderAnsatz({N: Dim(4), S: Dim(2)})
#spider_diagram = spider_ansatz(diagram)
#spider_diagram.draw(figsize=(13,6), fontsize=13)

from lambeq import MPSAnsatz
from discopy import Dim

mps_ansatz = MPSAnsatz({N: Dim(4), S: Dim(2)}, bond_dim=3)
mps_diagram = mps_ansatz(diagram)
mps_diagram.draw(figsize=(13,7), fontsize=13)