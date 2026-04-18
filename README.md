# OS Scheduling Simulator

This is a CPU scheduling simulator I built for my Operating Systems course. It simulates how an OS manages processes, handles I/O, allocates resources, and detects deadlocks — all running concurrently using threads.

---

## What does it do?

The simulator reads a list of processes from a file (`Process.txt`) and runs them through a scheduling algorithm. Each process has an arrival time, a priority, and a sequence of operations it needs to do (CPU bursts, I/O bursts, or resource requests).

Here's what the system handles:

- **Round Robin scheduling** with a quantum of 10 units
- **Priority-based preemption** — higher priority processes jump to the front
- **I/O handling** — processes that need I/O go to a waiting queue and come back when they're done
- **Resource allocation** — processes can request and release shared resources (R1 to R5)
- **Deadlock detection and resolution** — if a deadlock is detected, the simulator resolves it and re-queues the affected process
- **Gantt chart output** at the end showing how each process was scheduled
- **Average waiting time and turnaround time** calculations

---

## How to run it

Make sure you have Python installed, then just run:

```bash
python OS_Project.py
```

You also need a `Process.txt` file in the same directory. Each line in that file represents one process in this format:

```
<PID> <ArrivalTime> <Priority> <Sequence>
```

The sequence part is a series of operations like `CPU{20}`, `IO{5}`, `R{R[1]}`, `F{F[1]}` etc. separated by double spaces.

---

## How it works internally

The simulator spins up 6 threads that all run at the same time:

| Thread | What it does |
|--------|--------------|
| `timer` | Acts as the system clock, increments a global counter |
| `addProcess` | Adds processes to the ready/waiting queue when their arrival time comes |
| `addRR` | Manages the Round Robin queue and handles priority grouping |
| `IO` | Handles I/O bursts using separate threads for each process |
| `request` | Resolves pending resource requests |
| `resolveDeadloak` | Detects and resolves deadlocks |

The main `scheduling()` function runs the actual CPU simulation — it picks processes from the RR queue and executes them tick by tick.

---

## Output

At the end of the run you get something like:

```
Gantt Chart 😊
| 0  P1  10 | | 10  P2  15 | | 15  P1  20 | ...

Average waiting Time:  12.5
Average Turnaround Time:  30.0
done :)
```

---

## Notes

- The quantum size (`Q`) is set to 10 by default, you can change it at the top of the file
- There's a second input file (`s.txt`) commented out in the code, probably used for testing
- The deadlock resolution works by freeing all resources held by the deadlocked process and re-adding it to the ready queue from scratch

---

## Built with

- Python 3
- `threading` module
- `time` module
