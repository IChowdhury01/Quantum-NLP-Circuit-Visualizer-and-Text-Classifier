# Quantum NLP Circuit Visualizer and Text Classifier

Abhijit Alur, Ivan Chowdhury, Anthony Escalante

JPMorgan Chase Hackathon Project

## Background

In this project, we use the quantum NLP library **lambeq** to transform sentences into quantum circuits and visualize them. These quantum circuits can be used by a quantum computer to train a model for NLP tasks at exponentially high speeds. 

Using this technique, we also trained a fully syntax-based classifier that can understand the ordering of words within a sentence, using the DisCoCat model. 

![Results](docs/screenshots/QuantumTrainingResults.PNG)

Our classifier recorded **92.86% accuracy** after 200 epochs.

### How it works

1. Sentences are first transformed into string diagrams
   - The string diagrams have a syntax-based model, understanding the context of word ordering in the sentence (i.e. "Rabbits chase dogs" is interpreted differently from "Dogs chase rabbits".
3. The string diagram is rewritten and normalized to reduce computational overhead and training time.
4. The string diagram is parametrized (transformed) into a quantum circuit (for quantum computers) or tensor network (for classical computers)
   - We show 3 different visualizations of the same circuit: DisCoPy, pytket, and tket.
5. By sending many sentences into this pipeline, we can train a model off their quantum circuits to perform specific NLP tasks, like classification. 

Each step of the process is visualized through the diagrams below: Raw string diagram -> Normalized string diagram -> Tket quantum circuit. 
![1](docs/screenshots/RabbitsStringDiagram.PNG)
![2](docs/screenshots/RabbitsNormalizedStringDiagram.png)
![3](docs/screenshots/RabbitsTketCircuit.png)

## Setup

### Installation

1. Install python and pip. 
2. Install required libraries:
   ```
   pip install lambeq 
   pip install ipython  # For data visualization
   pip install pytket-qiskit
   pip install pylatexenc
   pip install pytest  # For running tests
   ```
   
### Usage

- [quantum_user_input.py](app/src/main/quantum_user_input.py)
  - Send a sentence into the quantum pipeline, and view the resulting string diagrams and quantum circuit.
- [classical_user_input.py](app/src/main/classical_user_input.py)
  - Send a sentence into the classical pipeline, and view the resulting string diagrams and tensor network.
- [quantum_training.py](app/src/main/quantum_training.py)
  - Trains a classifier off of ~100 quantum circuits, to classify sentences as containing an object-based or subject-based relative clause.

## Limitations

- The lambeq library is still in development, so our pipeline is currently limited to simple sentences. Very long, complex sentences and run-on sentences may fail parsing. 

## Acknowledgements
- Cambridge Quantum Computing research paper: https://arxiv.org/pdf/2110.04236.pdf
- lambeq documentation: https://cqcl.github.io/lambeq/notebooks.html
