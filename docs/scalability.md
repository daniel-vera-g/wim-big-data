# Scalability

- Does the solution scale?
- How is parallelization carried out?
- How is data distributed?

- How would you dimension a real system or setup given realistic data or query sets?
- How does the "data" run through the system?
- Which paths are IO-bound/Memory-bound/CPU- bound?
- Which paths are easy/more difficult to scale?
- How is scaling, how are data/requests/queries partitioned?
- What happens when data or queries skew and bias
- Is your system real-time capable?
- Are there any setup/bootstrapping etc. costs?

## Scalability experiments

## Variable Datenmengen

**Input:** 

- Konstante Ressourcen
- Variable Datenmenge
    - What happens when the amount of data increases in the orders of magnitude (1x/10x/100x... or 2x/4x/8x/16x/...)?
    - What happens if request or query intake increases ore latency conditions decrease in magnitude?

**Output:** 

- Zeit
- Spark Auslastung

## Variable Ressourcen

**Input:** 

- Variable Ressourcen
- Konstante Datenmenge

**Output:** 

- Zeit
- Spark Auslastung
