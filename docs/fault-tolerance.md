# Fault tolerance

- How does the application handle errors and distribution?

## Fault tolerance experiments

### Different modi

With fixed amount of data, ressources and in standalone modus:

1. Multiple worker
2. One worker with multiple executors

Evaluation with Task manager:

1. Kill Java processes
3. Observe ressources

- How does the system behave under Node/CPU/Memory/Hardware/... errors and failures?
- What happens during network interruptions and partitioning?
- How do error handling mechanisms affect efficiency/scale/latency/throughput/... etc.?
- Are there any worst/best case considerations?
