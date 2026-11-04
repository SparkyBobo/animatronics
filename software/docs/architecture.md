# Software Architecture

```mermaid
flowchart TD
    PM[Performance Messages]
    BD[Behaviour Dispatcher]

    subgraph Behaviours
        B1[Behaviour 1]
        B2[Behaviour 2]
        B3[Behaviour 3]
    end

    PQ[Planning Queue]
    PP[Planner Processor]
    P[Planner]

    EQ[Execution Queue]
    EP[Execution Processor]
    E[Executor]
    AM[Active Messages]
    EV[Evaluator]

    DD[Driver Dispatcher]
    D[Individual Drivers]

    PM --> BD

    BD --> B1
    BD --> B2
    BD --> B3

    B1 --> PQ
    B2 --> PQ
    B3 --> PQ

    PQ --> PP
    PP --> P
    P --> EQ

    EQ --> EP
    EP --> E
    E --> AM
    AM --> EV

    EV -->|Generate commands| E
    EV -->|Remove message| E

    E --> DD
    DD --> D
```

## Planning

The Planner takes the PerformanceMessage events and considers the desired state specified by each event's commands, the current state of the affected drivers, the available time, and the desired transition profile. It calculates the start time and the transition profile parameters required to execute the command.

```mermaid
flowchart TD
    CS[Current State]
    DS[Desired State]
    PR[Profile]
    AT[Available Time]

    PL[Planner]

    ST[Start Time]
    TR[Trajectory / Sequence]
    
    CS --> PL
    DS --> PL
    PR --> PL
    AT --> PL

    PL --> ST
    ST --> TR
    TR --> PC
```

Current state and Available time are based on the last planned event for the driver, which is stored in a cache after the Trajectory / Sequence has been calculated:

```mermaid
flowchart
    CS[Current State]
    AT[Available Time]

    PL[Planner]

    PC1[Planar Cache]
    PC2[Planar Cache]
    
    PC1 --> CS
    PC1 --> AT

    CS --> PL
    AT --> PL

    PL --> PC2
```