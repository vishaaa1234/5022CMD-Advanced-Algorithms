"""
performance_experiment.py - Hash table search vs one-dimensional array search.

For several data sizes N, the SAME N medicines are inserted into a hash table
and a list. A fixed set of lookups (90% existing IDs, 10% missing IDs) is then
timed on both structures. The best of several trials is reported, which
removes most operating-system noise.
"""

import random
import time

from hashtable import HashTable
from inventory import linear_search
from medicine import Medicine

DATA_SIZES = [5, 10, 100, 1_000, 10_000]
LOOKUPS = 1_000
TRIALS = 5


def build_data(n):
    ids = random.sample(range(1000, 1000 + n * 10), n)
    medicines = [Medicine(i, f"Medicine-{i}", 5.0, 10) for i in ids]
    table = HashTable(size=max(7, 2 * n), auto_resize=False)   # load factor ~0.5
    for medicine in medicines:
        table.insert(medicine.medicine_id, medicine)
    return medicines, table, ids


def build_targets(ids, n):
    existing = [random.choice(ids) for _ in range(int(LOOKUPS * 0.9))]
    missing = [random.randint(1000 + n * 10 + 1, 1000 + n * 20)
               for _ in range(LOOKUPS - len(existing))]
    targets = existing + missing
    random.shuffle(targets)
    return targets


def time_searches(search_function, targets):
    """Best-of-TRIALS average time per search, in nanoseconds."""
    best = None
    for _ in range(TRIALS):
        start = time.perf_counter_ns()
        for target in targets:
            search_function(target)
        elapsed = time.perf_counter_ns() - start
        best = elapsed if best is None else min(best, elapsed)
    return best / len(targets)


def main():
    random.seed(42)                       # repeatable experiment
    print("PHARMACY SEARCH PERFORMANCE EXPERIMENT")
    print(f"{LOOKUPS} lookups per trial (90% found, 10% missing), "
          f"best of {TRIALS} trials\n")
    header = f"{'Records':>8} | {'Hash (ns/search)':>17} | {'Array (ns/search)':>18} | {'Faster':>22}"
    print(header)
    print("-" * len(header))

    results = []
    for n in DATA_SIZES:
        medicines, table, ids = build_data(n)
        targets = build_targets(ids, n)
        hash_ns = time_searches(table.search, targets)
        array_ns = time_searches(lambda t: linear_search(medicines, t), targets)
        ratio = array_ns / hash_ns
        faster = (f"Hash x{ratio:.1f}" if ratio >= 1 else f"Array x{1 / ratio:.1f}")
        print(f"{n:>8} | {hash_ns:>17,.1f} | {array_ns:>18,.1f} | {faster:>22}")
        results.append((n, hash_ns, array_ns))

    try:                                  # optional chart for the report
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        sizes = [r[0] for r in results]
        plt.figure(figsize=(7, 4.5))
        plt.plot(sizes, [r[1] for r in results], "o-", label="Hash table (open addressing)")
        plt.plot(sizes, [r[2] for r in results], "s-", label="Array (linear search)")
        plt.xscale("log"); plt.yscale("log")
        plt.xlabel("Number of records"); plt.ylabel("Average time per search (ns)")
        plt.title("Search time: hash table vs array"); plt.grid(True, which="both", alpha=.3)
        plt.legend(); plt.tight_layout(); plt.savefig("search_performance.png", dpi=150)
        print("\nChart saved as search_performance.png")
    except ImportError:
        print("\n(matplotlib not installed - chart skipped)")


if __name__ == "__main__":
    main()
