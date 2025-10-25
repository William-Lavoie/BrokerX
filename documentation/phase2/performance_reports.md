### Performance reports

The following table shows various metrics calculated at various stages of phase 2.
| Monolith | Monolith + Redis | Monolith + Redis + Nginx | Microservices |
|----------|------------------|----------|-------------------------------|
| P95 | **Maintainability** | Separation of concerns through the use of the hexagonal architecture |
| P90 | **Persistence** | Support of a backend database with MySQL |
| P50 | **Availability** | Greater or equal to 90% uptime |
| Throughput (orders/s) | **Testability** | Coverage greater or equal than 80% |
| P95 on POST /order | **Traceability** | Logging of errors in dedicated files |
| Max concurent users (error rate < 5%) | 