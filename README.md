# Quantum Workflow
![image](https://github.com/user-attachments/assets/c14ffef5-f587-48c7-87e2-cea55f2b18c3)

## 1. Splitter
The Splitter node splits the quantum circuit into smaller sub-circuits for parallel execution. It handles the creation of observables, identifies the cut points in the circuit, partitions the circuit into sub-circuits, and prepares the data for further processing. Key functions include `create_observables`, which generates a list of observables for the quantum circuit, and `user_function`, which deserializes the input circuit, finds cuts, partitions the problem, and prepares sub-experiments for further steps.

## 2. Transpiler
The Transpiler node transpiles the sub-circuits to make them compatible with the target quantum hardware or simulator. It deserializes sub-experiments, selects the appropriate backend (real quantum device or simulator), runs the preset pass manager for transpilation if necessary, and prepares transpiled sub-experiments for submission.

## 3. Submitter
The Submitter node submits the transpiled sub-circuits to the quantum hardware or simulator for execution. It deserializes sub-experiments, sets up the Qiskit Runtime Service, configures execution options, and submits the jobs while tracking their status.

## 4. Merger
The Merger node merges the results from the executed sub-circuits. It combines the results from different sub-circuits into a single object for further processing.

## 5. Poller
The Poller node polls the submitted jobs to check their execution status. It iterates over the submitted jobs, checks their status using the Qiskit Runtime Service, retrieves results for completed jobs, and marks jobs for re-polling if they are not yet complete.

## 6. Reconstructor
The Reconstructor node reconstructs the final expectation values from the merged results. It decodes the results from sub-circuits, reconstructs expectation values using the provided coefficients and subobservables, and prepares the final output.

