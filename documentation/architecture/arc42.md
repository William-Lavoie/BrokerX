# BrokerX -  Architecture Documentation
This document is based on the arc42 model and describes the BrokerX platform, an web-based simulated stock broking platform as a term project for LOG430, Fall 2025, ÉTS, Montréal.


## 1. Introduction and Goals
### Requirements overview
The BrokerX application is a web-based  client-server system for simulated stock broking. It is an educational project that aims to replicate in a simulated environment online broking applications such as Wealthsimple. No real money or personal information will be collected, exchanged, and/or used in the making, deployment and/or use of this application.

### Quality goals
Note that quality requirements refer strictly to Phase 1 of the project and will be updated in later phases to reflect the current expectations.

| Priority | Quality goal | Scenario |
|----------|------------------|----------|
| 1 | **Maintenability** | Separation of concerns through the use of the hexagonal architecture |
| 2 | **Persistence** | Support of a backend database with PostgreSQL |
| 3 | **Latency** | P95: Less than 500 ms to place a buy order |
| 4 | **Throughput** | More than 300 buy orders per second |
| 5 | **Availability** | Greater or equal to 90% uptime |


### Stakeholders
- Developer : Learning how to design and implement a system from beginning to end.
- Clients : Exchange financial assets through a web-based interface.
- Professor/Lab assistants : Assess learning progress and competency.

---

## 2. Architectural Constraints
| Constraint | Description | Justification |
|----------|---------------|---------------|
| **Technologies** | Use of Java, PostgreSQL, Docker| Well documented and lightweight tools |
| **Testing** | JUnit (unit testing), Cypress (E2E) | Reliable testing frameworks that allow full coverage |
| **CI/CD** | Continuous integration and deployment through GitHub Actions | Ease of use, tests and deployment automation |
| **Deployment** | Deployment in Docker containers | Chosen for simplicity and portability |
| **Educational** | Use of a monolithic architecture (Phase 1) | Must conform to course requirements |


## 3. System Scope and Context

### 3.1 Business Context
![Activity Diagram](../images/activity.png)

The system currently allows clients to add funds to their wallets. Additional functionalities (including placing order and seeing their portfolio) will be added during the following phases of the project.
### 3.2 Technical Context
- **Client**: `BrokerX.java`- Web-based java application
- **Database Layer**: PostgreSQL database with DAO pattern.
- **Simulated Payment Service**: JSON file that mocks a banking account for clients to withdraw money.

![Context Diagram](../images/context.png)

---

## 4. Solution Strategy
- [ ] High-level architectural style (Hexagonal, MVC, Layered)
- [ ] Key patterns and tactics (e.g., CQRS, dependency inversion)
- [ ] Design rationale and alternatives considered
- [ ] Quality and risk mitigation strategies

---

## 5. Building Block View (Logical View – 4+1)
- [ ] Description of main building blocks (modules, layers, components)
- [ ] Interfaces and interactions between blocks

> 📌 *Include a **Logical Component Diagram** here*

---

## 6. Runtime View (Process + Scenarios – 4+1)

### 6.1 Typical Execution Flows
- [ ] How components collaborate at runtime
- [ ] Runtime interactions and control flow

> 📌 *Include a **Process View Diagram** (e.g., component interactions)*

### 6.2 Scenarios
- [ ] Example use case walkthroughs
- [ ] Sequence or activity diagrams

> 📌 *Include **Sequence Diagrams** for 2–3 core scenarios*

---

## 7. Deployment View (4+1)
- [ ] Mapping of software artifacts to infrastructure
- [ ] Nodes, environments (dev, staging, prod), network zones

> 📌 *Include a **Deployment Diagram** (servers, containers, DBs, etc.)*

---

## 8. Cross-cutting Concepts
- [ ] Security and authentication
- [ ] Error and exception handling
- [ ] Logging and monitoring
- [ ] Configuration
- [ ] API versioning
- [ ] Performance optimizations
- [ ] Internationalization/localization (if applicable)

---

## 9. Design Decisions
- [ ] List of key architectural decisions (linked to ADRs)
- [ ] Alternatives considered
- [ ] Justification for final choices

> 📌 *Include or reference at least 3 ADRs (e.g., architecture style, persistence, error strategy)*

---

## 10. Quality Requirements

### 10.1 Quality Scenarios
- [ ] Performance, availability, scalability, modifiability, testability

### 10.2 Quality Tree (optional)
> 📌 *Use a quality attribute tree to visualize priorities (e.g., ISO/25010 or custom)*

---

## 11. Risks and Technical Debt
- [ ] Known technical risks
- [ ] Potential architectural trade-offs
- [ ] Mitigation strategies
- [ ] Assumptions and limitations

---

## 12. Glossary
- [ ] List of domain-specific terms
- [ ] Acronyms and abbreviations
- [ ] Links to external references

---

# 📎 Appendix

## A. Architectural Decision Records (ADR)
- [ ] ADR-001: Architecture Style
- [ ] ADR-002: Persistence
- [ ] ADR-003: Error Handling and Versioning
- [ ] (more ADRs as needed)

## B. References
- This project has been made in collaboration with chatGPT for the purposes listed below. Note that uses of artifical intelligence in this project is limited to strictly those listed below. In particular, it has **not** be used to generate artefacts.
  - Creation of templates for use cases, glossary, MoSCoW priorization table and arc42.
  - Asking if the artefacts satisfy the requirements.
  - Used as a search engine.
  - Improve readibility (phrasing, grammar, spelling, etc)
- Petrillo, F. (2025, Fall). Class notes [pdf]. LOG430, École de Technologie Supérieure.
- Ullman, G. (2025, Fall). Github labs. LOG430, École de Technologie Supérieure.


