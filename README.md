# Using Quantum NLP for Intelligent Understanding of ADR Contract Terms

In this project, we use the quantum NLP library **Lambeq** to process sentences describing contract terms for American depository receipts.

### How it works

1. Sentences are first transformed into string diagrams with a syntax-based model.
2. The string diagram is rewritten and normalized to reduce computational overhead and training time.
3. The abstract string diagram is parametrized, transformed into a concrete quantum circuit (for quantum computers) or tensor network (for classical computers)

Each step of the process is visualized through diagrams. 

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