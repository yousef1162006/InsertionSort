# Max-Heap Implementation for OS Task Scheduler

class MaxHeap:
    def __init__(self):
        # Each element is a tuple: (priority, task_name)
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def LeftChild(self, i):
        return 2 * i + 1

    def RightChild(self, i):
        return 2 * i + 2

    def insert(self, task_name, priority):
        """INSERT a task with given priority into the max-heap."""
        self.heap.append((priority, task_name))
        self._sift_up(len(self.heap) - 1)
        print(f"INSERT: '{task_name}' (Priority: {priority})")

    def ExtractMax(self):
        """EXTRACT-MAX: Remove and return the task with the highest priority."""
        if not self.heap:
            return None
        
        maxitem = self.heap[0]
        lastitem = self.heap.pop()

        if self.heap:
            self.heap[0] = lastitem
            self._sift_down(0)

        return maxitem

    def _sift_up(self, i):
        while i > 0 and self.heap[i][0] > self.heap[self.parent(i)][0]:
            p = self.parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def _sift_down(self, i):
        size = len(self.heap)
        while True:
            largest = i
            left = self.left_child(i)
            right = self.right_child(i)

            if left < size and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < size and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            if largest != i:
                self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
                i = largest
            else:
                break


# OS Task Scheduler Simulation
if __name__ == "__main__":
    scheduler = MaxHeap()

    print("--- 1. Inserting Tasks into Scheduler ---")
    scheduler.insert("Background Backup", 10)
    scheduler.insert("Music Player", 50)
    scheduler.insert("User Mouse Click", 90)
    scheduler.insert("Antivirus Scan", 30)
    scheduler.insert("System Update", 20)

    print("\n--- 2. Scheduling & Executing (EXTRACT-MAX) ---")
    while scheduler.heap:
        priority, task = scheduler.extract_max()
        print(f"Executing: '{task}' with Priority {priority}")
    
