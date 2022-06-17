import os
import warnings
import webbrowser

import numpy as np
from discopy import grammar
from lambeq import BobcatParser, Rewriter, AtomicType, IQPAnsatz, remove_cups, TketModel, QuantumTrainer, SPSAOptimizer, \
    Dataset
from matplotlib import pyplot
from pytket.circuit.display import render_circuit_as_html
from pytket.extensions.qiskit import tk_to_qiskit, AerBackend

from settings import GEN_PATH, PROJECT_ROOT_PATH

PATH_TO_TRAINING = os.path.join(PROJECT_ROOT_PATH, 'data', 'rp_train_data.txt')
PATH_TO_TESTING = os.path.join(PROJECT_ROOT_PATH, 'data', 'rp_test_data.txt')


def send_into_quantum_pipeline(sentence):
    # Convert to string diagram
    parser = BobcatParser(verbose='text')
    diagram = parser.sentence2diagram(sentence)  # syntax-based, not bag-of-words
    grammar.draw(diagram, title='h', figsize=(14, 3), fontsize=12)

    # Rewrite string diagram, to reduce performance costs / training time
    rewriter = Rewriter(['prepositional_phrase', 'determiner'])  # lower tensor count on prepositions
    prep_reduced_diagram = rewriter(diagram).normal_form()

    curry_functor = Rewriter(['curry'])  # reduce number of cups
    curried_diagram = curry_functor(prep_reduced_diagram).normal_form()
    curried_diagram.draw(figsize=(5, 4), fontsize=13)

    # Parameterize: convert abstract string diagram to concrete quantum circuit
    N = AtomicType.NOUN
    S = AtomicType.SENTENCE
    P = AtomicType.PREPOSITIONAL_PHRASE
    C = AtomicType.CONJUNCTION
    ansatz = IQPAnsatz({N: 1, S: 1, P: 1, C: 1}, n_layers=4)

    discopy_circuit = ansatz(diagram)  # Quantum circuit, DisCoPy format
    discopy_circuit.draw(figsize=(15, 10))

    tket_circuit = discopy_circuit.to_tk()  # Quantum circuit, pytket format
    save_path = os.path.join(GEN_PATH, 'tket_circuit.html')
    with open(save_path, "w") as file:
        file.write(render_circuit_as_html(tket_circuit, False))
    webbrowser.open_new(save_path)

    qiskit_circuit = tk_to_qiskit(tket_circuit)  # qiskit format
    qiskit_circuit.draw(output='mpl')
    pyplot.show()


def read_data(filename):
    labels, sentences = [], []
    with open(PATH_TO_TRAINING) as f:
        for line in f:
            t = int(line[0])
            labels.append([t, 1 - t])
            sentences.append(line[1:].strip())
        return labels, sentences


def train_data():
    warnings.filterwarnings('ignore')
    os.environ['TOKENIZERS_PARALLELISM'] = 'true'

    BATCH_SIZE = 30
    EPOCHS = 200
    SEED = 2

    train_labels, train_data = read_data(PATH_TO_TRAINING)
    val_labels, val_data = read_data(PATH_TO_TESTING)

    parser = BobcatParser(root_cats=('NP', 'N'), verbose='text')
    raw_train_diagrams = parser.sentences2diagrams(train_data, suppress_exceptions=True)
    raw_val_diagrams = parser.sentences2diagrams(val_data, suppress_exceptions=True)

    train_diagrams = [
        diagram.normal_form()
        for diagram in raw_train_diagrams if diagram is not None
    ]
    val_diagrams = [
        diagram.normal_form()
        for diagram in raw_val_diagrams if diagram is not None
    ]

    train_labels = [
        label for (diagram, label)
        in zip(raw_train_diagrams, train_labels)
        if diagram is not None
    ]
    val_labels = [
        label for (diagram, label)
        in zip(raw_val_diagrams, val_labels)
        if diagram is not None
    ]

    ansatz = IQPAnsatz({AtomicType.NOUN: 1, AtomicType.SENTENCE: 0},
                       n_layers=1, n_single_qubit_params=3)

    train_circuits = [ansatz(remove_cups(diagram)) for diagram in train_diagrams]
    test_circuits = [ansatz(remove_cups(diagram)) for diagram in val_diagrams]
    all_circuits = train_circuits + test_circuits

    backend = AerBackend()
    backend_config = {
        'backend': backend,
        'compilation': backend.default_compilation_pass(2),
        'shots': 8192
    }

    model = TketModel.from_diagrams(all_circuits, backend_config=backend_config)
    loss = lambda y_hat, y: -np.sum(y * np.log(y_hat)) / len(y)  # binary cross-entropy loss
    acc = lambda y_hat, y: np.sum(np.round(y_hat) == y) / len(y) / 2  # half due to double-counting
    eval_metrics = {"acc": acc}

    trainer = QuantumTrainer(
        model,
        loss_function=loss,
        epochs=EPOCHS,
        optimizer=SPSAOptimizer,
        optim_hyperparams={'a': 0.05, 'c': 0.06, 'A': 0.01 * EPOCHS},
        evaluate_functions=eval_metrics,
        evaluate_on_train=True,
        verbose='text',
        seed=0
    )

    train_dataset = Dataset(
        train_circuits,
        train_labels,
        batch_size=BATCH_SIZE)

    test_dataset = Dataset(test_circuits, val_labels, shuffle=False)

    trainer.fit(train_dataset, test_dataset, evaluation_step=1, logging_step=20)  # Train
    test_acc = acc(model(test_circuits), val_labels)  # Record accuracy
    print('Test accuracy:', test_acc.item())
