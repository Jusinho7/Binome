*This project has been created as part of the 42 curriculum by srasolov.*

# Codexion

## Description

Codexion is a multithreaded simulation of a classic resource-sharing / synchronization
problem (a variant of the dining philosophers problem), reframed around a group of
**coders** sharing a set of scarce **USB dongles** in a circular co-working space.

Each coder repeatedly cycles through three phases: **compiling** (which requires
simultaneously holding two dongles — one on each side), **debugging**, and
**refactoring**. Dongles sit between adjacent coders, must be shared fairly, and become
temporarily unusable during a cooldown period after being released. A dedicated
**monitor thread** watches every coder and stops the simulation the instant one of them
**burns out** by failing to start a new compile within `time_to_burnout` milliseconds.

The goal of the project is to practice real concurrent programming with POSIX threads:
mutual exclusion, condition variables, deadlock avoidance, fair resource arbitration
(FIFO / EDF), and precise, race-free timing and logging.

## Instructions

### Compilation

```sh
make
```

This produces the `codexion` executable at the project root. Available Makefile rules:
`all`, `clean`, `fclean`, `re`.

### Execution

```sh
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug \
           time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

| Argument                    | Meaning                                                                 |
|------------------------------|--------------------------------------------------------------------------|
| `number_of_coders`           | Number of coders (and number of dongles).                               |
| `time_to_burnout` (ms)       | Max time since the last compile start before a coder burns out.         |
| `time_to_compile` (ms)       | Duration of the compile phase.                                          |
| `time_to_debug` (ms)         | Duration of the debug phase.                                            |
| `time_to_refactor` (ms)      | Duration of the refactor phase.                                         |
| `number_of_compiles_required`| Simulation stops once every coder reaches this many compiles.           |
| `dongle_cooldown` (ms)       | Time a dongle stays unavailable after being released.                   |
| `scheduler`                  | Dongle arbitration policy: `fifo` or `edf`.                             |

Example:

```sh
./codexion 4 800 200 200 200 5 50 edf
```

All arguments are mandatory and strictly validated: negative numbers, non-integer
values, or a scheduler other than `fifo`/`edf` are rejected with an error message and a
non-zero exit code.

## Resources

- *The Little Book of Semaphores* — Allen B. Downey (classic reference on the dining
  philosophers problem and resource-sharing synchronization patterns).
- Linux manual pages: `pthread_create(3)`, `pthread_mutex_lock(3)`,
  `pthread_cond_timedwait(3)`, `gettimeofday(2)`.
- E. G. Coffman et al., *"System Deadlocks"* (1971) — the four Coffman conditions used
  to reason about deadlock avoidance.
- C. L. Liu and J. Layland, *"Scheduling Algorithms for Multiprogramming in a Hard-
  Real-Time Environment"* (1973) — background on Earliest-Deadline-First scheduling.

**How AI was used:** an AI assistant (Claude) was used to help draft the initial
architecture (data structures for coders/dongles/waiters, the resource-ordering
deadlock-avoidance strategy, and the FIFO/EDF waiter-selection logic) and to generate
a first version of the C source files and this README. All generated code was reviewed,
compiled, and manually tested (single coder, multiple coders under both schedulers,
invalid-argument rejection, and a forced burnout scenario) before being considered part
of the submission. No AI was used to fabricate test results or logs shown above; all
example runs were produced by actually executing the compiled binary.

## Blocking cases handled

- **Deadlock prevention (Coffman's conditions):** a coder needs two dongles
  simultaneously (one on each side). Instead of always taking "left then right" (which
  can produce a circular wait when every coder holds one dongle and waits for the
  next), every coder acquires its two dongles in a fixed **global order of dongle id**
  (lowest id first, highest id second). Because *every* thread respects the same total
  order, a circular wait — and therefore Coffman's "circular wait" condition — can never
  arise, which rules out deadlock. The single-coder edge case (where the coder's left
  and right dongle are the same object) is special-cased to avoid a coder deadlocking
  on itself.
- **Starvation prevention:** each dongle keeps a list of current waiters. Under `fifo`,
  the waiter with the earliest arrival timestamp is granted the dongle first; under
  `edf`, the waiter with the earliest burnout deadline
  (`last_compile_start + time_to_burnout`) is granted first. Both policies guarantee
  that a waiting coder is eventually selected once the dongle is free and its cooldown
  has elapsed, as long as the simulation parameters are feasible (i.e. the time budget
  allows every requester to compile before its own deadline).
- **Cooldown handling:** a dongle keeps a `free_since` timestamp when released. It is
  only considered available again once `now - free_since >= dongle_cooldown`. Waiting
  threads use `pthread_cond_timedwait` with a wake-up time aligned to the cooldown
  expiry (or a short polling interval while the dongle is in use), so cooldown is
  respected without busy-waiting.
- **Precise burnout detection:** a dedicated monitor thread polls every coder's state
  every millisecond. A coder is declared burned out as soon as
  `now - last_compile_start > time_to_burnout` while it is not currently compiling,
  guaranteeing the "burned out" log is emitted within the required 10 ms tolerance.
- **Log serialization:** all log lines (`has taken a dongle`, `is compiling`,
  `is debugging`, `is refactoring`, `burned out`) go through a single `log_event()`
  function that locks a shared print mutex around the timestamp read and `printf`,
  so two messages can never interleave on the same line.

## Thread synchronization mechanisms

- **`pthread_mutex_t` per dongle (`t_dongle.lock`):** protects the dongle's `in_use`
  flag, its `free_since` cooldown timestamp, and its waiter list. Every read or mutation
  of this state happens exclusively while the mutex is held, preventing two coders from
  ever believing they both hold the same dongle.
- **`pthread_cond_t` per dongle (`t_dongle.cond`):** coders waiting for a dongle block
  on this condition variable via `pthread_cond_timedwait` (bounded by the cooldown
  expiry or a short polling window), instead of busy-spinning. `dongle_release()`
  calls `pthread_cond_broadcast()` so every waiter re-evaluates whether it is now the
  selected waiter (per the FIFO/EDF policy) without needing direct thread-to-thread
  signalling.
- **`pthread_mutex_t` per coder (`t_coder.state_lock`):** protects each coder's mutable
  state (`state`, `last_compile_start`, `compiles_done`, `burned_out`). This is the
  mechanism that lets the monitor thread safely read a coder's deadline and phase
  concurrently with the coder thread updating them — a classic reader/writer race that
  is avoided by always taking this lock before touching the fields on either side.
- **Global print mutex (`t_sim.print_lock`):** serializes all `log_event()` calls
  across every coder thread and the monitor thread, guaranteeing atomic, non-interleaved
  log lines.
- **Global stop mutex (`t_sim.stop_lock`):** protects the `stop` flag that the monitor
  sets on burnout or completion, and that every coder / dongle-wait loop polls to know
  when to exit promptly.
- **Resource-ordering discipline:** rather than a synchronization *primitive*, the
  fixed low-id-first / high-id-first acquisition order described above is the core
  technique that prevents deadlock between coders that need two dongles at once —
  it turns a potential circular-wait dependency graph into a simple linear one.
