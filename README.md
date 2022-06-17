# Using Quantum NLP for Intelligent Understanding of ADR Contract Terms

In this project, we use the quantum NLP library **Lambeq** to process sentences into quantum circuits, which can then be trained on a quantum computer for syntax-based understanding.

The end goal of this project is to be able to parse American depository receipt (ADR) engagement letters and intelligently decipher the terms of the contracts. 

Model recorded **92.86% accuracy** after 200 epochs.

![Results](docs/screenshots/QuantumTrainingResults.PNG)

### How it works

1. Sentences are first transformed into string diagrams with a syntax-based model.
2. The string diagram is rewritten and normalized to reduce computational overhead and training time.
3. The abstract string diagram is parametrized, transformed into a concrete quantum circuit (for quantum computers) or tensor network (for classical computers)
4. By sending many sentences into this pipeline, we can train a model off the quantum circuits to perform specific NLP tasks, like classification. 

Each step of the process is visualized through the below diagrams. 
![1](docs/screenshots/RabbitsStringDiagram.PNG)
![2](docs/screenshots/RabbitsNormalizedStringDiagram.png)
![3](docs/screenshots/RabbitsQiskitCircuit.png)

### Installation

1. Install python and pip. 
2. Run the following commands to install required libraries:
   ```
   pip install lambeq 
   pip install ipython  # For data visualization
   pip install pytket-qiskit
   pip install pylatexenc
   pip install pytest  # For running tests
   ```
   
### Usage

- [quantum_user_input.py](app/src/main/quantum_user_input.py)
  - Send a sentence into the quantum pipeline, and view resulting string diagrams and quantum circuits.
- [classical_user_input.py](app/src/main/classical_user_input.py)
  - Send a sentence into the classical pipeline, and see the resulting string diagrams and tensor networks.
- [quantum_training.py](app/src/main/quantum_training.py)
  - Trains a model off quantum circuits, to classify sentences as containing an object-based or subject-based relative clause.