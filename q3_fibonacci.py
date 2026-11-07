"""
5022CMD Advanced Algorithms - Question 3: Concurrent process

Calculates Fibonacci(35), Fibonacci(38) and Fibonacci(40)
  (a) with multithreading - one thread per value
  (b) without multithreading - one value after another
for 10 rounds each, and reports the time taken (ns) per round and on average.

Time per round (multithreaded), as defined in the brief:
    T = End_Time_Of_Thread_Finished_Last - Start_Time_Of_Thread_That_Started_First

Usage:
    python q3_fibonacci.py                          # full experiment (10 rounds, 35/38/40)
    python q3_fibonacci.py --rounds 2 --inputs 25 27 30   # quick test
"""

import argparse
import threading
import time

FIB_INPUTS = (35, 38, 40)
ROUNDS = 10


# --------------------------------------------------------------------------
# Fibonacci function
# --------------------------------------------------------------------------
def fibonacci(n):
    """Return the nth Fibonacci number using plain recursion.

    Primitive operations per call (see report for the derivation):
        n <= 1 comparison ........ 1
        n - 1 and n - 2 .......... 2
        addition of two results .. 1
        return ................... 1
    => T(n) = T(n-1) + T(n-2) + c, which grows as O(2^n).
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# --------------------------------------------------------------------------
# With multithreading
# --------------------------------------------------------------------------
def _fib_worker(n, results, timings, lock):
    """Thread body: compute fibonacci(n) and record its own start/end time."""
    start = time.perf_counter_ns()          # when THIS thread begins its work
    value = fibonacci(n)
    end = time.perf_counter_ns()            # when THIS thread finishes

    # The dictionaries are shared by all threads, so the writes are guarded
    # by a lock to keep the shared data consistent.
    with lock:
        results[n] = value
        timings[n] = (start, end)


def run_with_threads(inputs):
    """Create one thread per input value; return (results, T in ns)."""
    results = {}
    timings = {}
    lock = threading.Lock()

    threads = [
        threading.Thread(target=_fib_worker,
                         args=(n, results, timings, lock),
                         name=f"Fib-{n}")
        for n in inputs
    ]

    for thread in threads:      # start all threads
        thread.start()
    for thread in threads:      # wait until every thread has finished
        thread.join()

    t1 = min(start for start, _ in timings.values())   # first thread to start
    t2 = max(end for _, end in timings.values())       # last thread to finish
    return results, t2 - t1


# --------------------------------------------------------------------------
# Without multithreading
# --------------------------------------------------------------------------
def run_without_threads(inputs):
    """Calculate every value one after another; return (results, T in ns)."""
    start = time.perf_counter_ns()
    results = {n: fibonacci(n) for n in inputs}
    end = time.perf_counter_ns()
    return results, end - start


# --------------------------------------------------------------------------
# Experiment driver and output
# --------------------------------------------------------------------------
def format_results(results, inputs):
    return ", ".join(f"Fib({n})={results[n]}" for n in inputs)


def run_experiment(title, runner, inputs, rounds):
    """Run `runner` for the given number of rounds, print each round and the
    average, and return the list of per-round times in nanoseconds."""
    print(f"=== Fibonacci Computation ({title}) ===")
    times = []
    for round_no in range(1, rounds + 1):
        results, elapsed_ns = runner(inputs)
        times.append(elapsed_ns)
        print(f"Round {round_no:>2}: {format_results(results, inputs)} "
              f"| T = {elapsed_ns:,} ns")

    average = sum(times) // len(times)
    print(f"Total of all rounds  ({title}): {sum(times):,} ns")
    print(f"Average T ({title}): {average:,} ns "
          f"({average / 1e9:.3f} s)\n")
    return times


def print_observation(avg_threads, avg_sequential):
    difference = (avg_sequential - avg_threads) / avg_sequential * 100
    if difference > 0:
        print(f"Observation: Multithreading reduced the average completion "
              f"time by approximately {difference:.1f}%.")
    else:
        print(f"Observation: Multithreading did NOT reduce the average "
              f"completion time; it was approximately {abs(difference):.1f}% "
              f"slower.")


def main():
    parser = argparse.ArgumentParser(description="Fibonacci threading experiment")
    parser.add_argument("--rounds", type=int, default=ROUNDS)
    parser.add_argument("--inputs", type=int, nargs="+", default=list(FIB_INPUTS))
    args = parser.parse_args()

    threaded = run_experiment("With Multithreading", run_with_threads,
                              args.inputs, args.rounds)
    sequential = run_experiment("Without Multithreading", run_without_threads,
                                args.inputs, args.rounds)

    print_observation(sum(threaded) / len(threaded),
                      sum(sequential) / len(sequential))


if __name__ == "__main__":
    main()
