*This project has been created as part of the 42 curriculum by srasolov.*

# Codexion

## Description

Codexion is a concurrency simulation written in C with POSIX threads.
`number_of_coders` coders sit in a circle, with one USB dongle between each
pair of neighbours (as many dongles as coders). To compile, a coder needs
**two** dongles at the same time. After compiling they debug, then refactor,
then try to compile again. A coder who does not *start* a compile within
`time_to_burnout` ms of the start of their previous compile (or of the
simulation) burns out and the simulation stops. It also stops when every
coder has compiled at least `number_of_compiles_required` times.

The goal is to share the dongles with **no deadlock**, **no starvation**,
a mandatory **cooldown** after each release, a fair scheduler (`fifo` or
`edf`), precise burnout detection (< 10 ms) and **serialized logs**.

Overview of the sources:

| File | Role |
|------|------|
| `main.c` | Entry point, error handling |
| `parse.c` | Argument validation |
| `init.c` / `cleanup.c` | Creation / destruction of all resources |
| `run.c` | Thread creation (coders + monitor) and joins |
| `coder.c` | Life cycle of a coder thread |
| `monitor.c` | Burnout / end-of-simulation detection thread |
| `dongle.c` | Acquire / release a dongle (queue + cooldown) |
| `queue.c` | Priority-queue operations and initialization |
| `heap.c` | Binary min-heap used by FIFO and EDF |
| `fifo_scheduler.c`, `edf_scheduler.c` | FIFO and EDF scheduling policies |
| `queue_error.c` | Queue-capacity error handling |
| `state.c` | Stop flag, serialized logging, wake-up of waiters |
| `time_utils.c` | Clock, interruptible sleep, timeout conversion |

## Instructions

Build (flags: `-Wall -Wextra -Werror -pthread`):

```
make        # builds ./codexion
make clean  # removes object files
make fclean # removes objects and binary
make re     # fclean + all
```

Run:

```
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug \
           time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

Example:

```
./codexion 5 800 200 200 200 7 0 edf
./codexion 4 1000 200 100 100 5 50 fifo
./codexion 1 200 100 50 50 3 10 fifo    # a lone coder always burns out
```

All times are in milliseconds. Invalid input (negative numbers, non-integers,
wrong argument count, scheduler other than `fifo`/`edf`) is rejected with a
usage message and exit code 1.

## Blocking cases handled

- **Deadlock prevention (Coffman's conditions).** Two conditions are broken.
  *Circular wait*: every dongle has an index and a coder always goes for the
  dongle with the **lowest index first**. *Hold and wait*: a coder never
  sleeps while holding a dongle. It takes the first dongle, tries the second
  one **without waiting**, and if it is not available it gives the first one
  back, starting its cooldown, and sleeps until the second
  dongle changes state. Mutual exclusion and no-preemption are inherent to
  the problem. Since two Coffman conditions are broken, no deadlock is possible.
- **No "chain" serialization.** Without the give-back, on a multi-core machine
  every coder could grab its first dongle at the same time and wait for the
  neighbour's one, so only one coder at the end of the chain could compile and
  the others would burn out in turn. Giving the first dongle back keeps two
  coders compiling in parallel.
- **Single coder.** With one coder there is only one dongle. The coder takes
  it and waits; the monitor reports the burnout at `time_to_burnout`. The
  program never tries to lock the same dongle twice.
- **Starvation prevention.** Each dongle has its own binary min-heap, sized to
  hold one outstanding request from every coder.
  With `fifo`, each request receives an arrival sequence and the smallest
  sequence is served first;
  with `edf` the key is the deadline
  `last_compile_start + time_to_burnout`, so the coder closest to
  burnout is served first. Equal keys are broken by the coder id, which
  makes the order fully deterministic. A coder that backs off stays registered
  in the queue of the second dongle, so it keeps its rank and cannot be
  overtaken by a less urgent coder.
- **Cooldown.** On release or give-back a dongle stores
  `available_at = now + cooldown`.
  The coder at the head of the queue waits with `pthread_cond_timedwait`
  until that date, without busy-waiting.
- **Precise burnout detection.** A dedicated monitor thread checks every
  coder every 0.5 ms, so a burnout is printed well within the 10 ms limit.
- **Log serialization.** All output goes through `log_mutex`. Once the stop
  flag is raised, no coder line is printed any more, and the burnout line is
  written in the same critical section that raises the flag, so it is always
  the last line.
- **Clean shutdown.** Every sleep is interruptible (`smart_sleep` checks the
  stop flag) and every blocked waiter is woken by the monitor, so all threads
  can be joined quickly and all memory is freed.

## Thread synchronization mechanisms

- **`pthread_mutex_t` per dongle** protects `in_use`, `available_at`, the
  arrival counter and the heap. Nobody reads or writes a dongle's
  state without holding its mutex, so two coders can never get the same
  dongle.
- **`pthread_cond_t` per dongle** lets waiting coders sleep instead of
  spinning. Releases call `pthread_cond_broadcast`; the coder at the
  highest-priority waiter re-checks its condition (`I am first && dongle free &&
  cooldown over`) in a `while` loop, which also protects against spurious
  wake-ups.
- **`version` counter per dongle** (protected by the dongle mutex) is
  incremented each time the dongle is released or given back. A coder that
  failed to get the second dongle records the version it saw (under the
  mutex) and sleeps in `pthread_cond_wait` until the version changes, which
  avoids both busy-waiting and lost wake-ups.
- **`pthread_mutex_t` per coder (`lock`)** protects `last_compile_start` and
  `compile_count`, written by the coder and read by the monitor.
- **`stop_mutex`** protects the shared `stop` flag (`is_stopped` / `set_stop`).
- **`log_mutex`** serializes `printf` calls.

Race-condition examples:

- *Lost wake-up on stop.* A coder checks `stop` while holding the dongle
  mutex and then enters `pthread_cond_wait`, which atomically releases that
  mutex. The monitor raises `stop`, then locks each dongle mutex before
  broadcasting. It can only get the mutex once the coder is already waiting,
  so the broadcast can never be missed.
- *Monitor vs. coder data.* The monitor never reads `last_compile_start`
  without the coder's `lock`.
- *Lock order.* Locks are only nested as `dongle -> stop` and
  `log -> stop`; nobody takes them in the opposite order, so the mutexes
  themselves cannot deadlock.

Coder -> monitor communication is done only through that shared, mutex
protected state (compile counters and start times). Monitor -> coder
communication is the `stop` flag plus the condition-variable broadcast.

## Resources

- [pthread](https://man7.org/linux/man-pages/man7/pthreads.7.html)
- [pthread_mutex_lock, pthread_cond_wait,
  pthread_cond_timedwait, clock_gettime](https://www.geeksforgeeks.org/c/thread-functions-in-c-c/)
- [Condition de Coffman](https://cs341.cs.illinois.edu/coursebook/Deadlock#coffman-conditions)
- [FIFO](https://www.publicsofttools.com/tools/stack-queue-simulator)
- [Priority queue](https://www.dsavisualizer.in/visualizer/queue/types/priority)
- [Earliest Deadline First scheduling](https://www.geeksforgeeks.org/operating-systems/earliest-deadline-first-edf-cpu-scheduling-algorithm/)

**Use of AI:** AI assisted with understanding the concurrency requirements, reviewing and debugging the queue and scheduler implementation, and checking the code against the subject and Norminette. In particular, it helped implement and verify the binary heap used for FIFO/EDF arbitration and the cooldown and log-format corrections. I am responsible for reviewing, understanding, and validating these changes.
