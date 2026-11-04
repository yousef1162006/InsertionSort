import time
import random
import matplotlib.pyplot as plt


# 1. Insertion Sort
def InsertionSort(arr):
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# 2. Merge Sort
def MergeSort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    L = MergeSort(arr[:mid])
    R = MergeSort(arr[mid:])
    return Merge(L, R)


def Merge(L, R):
    res = []
    i = j = 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            res.append(L[i])
            i += 1
        else:
            res.append(R[j])
            j += 1
    res.extend(L[i:])
    res.extend(R[j:])
    return res


# 3. Quick Sort (using middle pivot to handle sorted/reversed data)
def QuickSort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    L = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    R = [x for x in arr if x > pivot]
    return QuickSort(L) + mid + QuickSort(R)


# 4. Benchmark Function
def benchmark():
    sizes = [100, 200, 500, 1000, 400, 55]  # n from 10^3 upwards
    
    times_insertion = []
    times_merge = []
    times_quick = []
    times_builtin = []
    
    print(f"{'n':>6} | {'Insertion':>10} | {'Merge':>10} | {'Quick':>10} | {'sorted()':>10}")
    print("-" * 55)

    for n in sizes:
        # Testing on random data
        data = [random.randint(0, 10000) for _ in range(n)]

        # Insertion sort
        t0 = time.perf_counter()
        InsertionSort(data)
        t_ins = time.perf_counter() - t0

        # Merge sort
        t0 = time.perf_counter()
        MergeSort(data)
        t_merge = time.perf_counter() - t0

        # Quick sort
        t0 = time.perf_counter()
        QuickSort(data)
        t_quick = time.perf_counter() - t0

        # Python sorted()
        t0 = time.perf_counter()
        sorted(data)
        t_builtin = time.perf_counter() - t0

        times_insertion.append(t_ins)
        times_merge.append(t_merge)
        times_quick.append(t_quick)
        times_builtin.append(t_builtin)

        print(f"{n:>6} | {t_ins:>9.4f}s | {t_merge:>9.4f}s | {t_quick:>9.4f}s | {t_builtin:>9.4f}s")

    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times_insertion, label="Insertion Sort")
    plt.plot(sizes, times_merge, label="Merge Sort")
    plt.plot(sizes, times_quick, label="Quick Sort")
    plt.plot(sizes, times_builtin, label="Python sorted()")

    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Sorting Algorithms Benchmark")
    plt.legend()
    plt.grid(True)
    plt.savefig("benchmark_plot.png")
    print("\nSaved benchmark plot to benchmark_plot.png")


if __name__ == "__main__":
    benchmark()
