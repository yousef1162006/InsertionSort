from collections import deque
from typing import Dict, List, Literal, Optional, Tuple, Union
import numpy as np


class IslandCounter:

    DIRECTIONS_4: List[Tuple[int, int]] = [
        (-1, 0),  
        (1, 0),   
        (0, -1),  
        (0, 1)    
    ]

    DIRECTIONS_8: List[Tuple[int, int]] = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    def __init__(self, grid: Union[np.ndarray, List[List[Union[int, str]]]]):
        self.grid = self._parse_grid(grid)
        self.rows, self.cols = self.grid.shape

    @staticmethod
    def _parse_grid(grid: Union[np.ndarray, List[List[Union[int, str]]]]) -> np.ndarray:
        arr = np.array(grid, dtype=int)
        if arr.ndim != 2:
            raise ValueError(f"Grid must be 2-dimensional, got shape {arr.shape}")
        if not np.all(np.isin(arr, [0, 1])):
            raise ValueError("Grid cells must only contain 0 (water) or 1 (land)")
        return arr

    def _get_directions(self, connectivity: int) -> List[Tuple[int, int]]:
        if connectivity == 4:
            return self.DIRECTIONS_4
        elif connectivity == 8:
            return self.DIRECTIONS_8
        else:
            raise ValueError(f"Unsupported connectivity: {connectivity}. Choose 4 or 8.")

    def count_islands_bfs(self, connectivity: int = 4) -> int:
        if self.rows == 0 or self.cols == 0:
            return 0

        visited = np.zeros((self.rows, self.cols), dtype=bool)
        directions = self._get_directions(connectivity)
        island_count = 0

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c] == 1 and not visited[r, c]:
                    island_count += 1
                    visited[r, c] = True
                    queue = deque([(r, c)])

                    while queue:
                        curr_r, curr_c = queue.popleft()
                        for dr, dc in directions:
                            nr, nc = curr_r + dr, curr_c + dc
                            if (
                                0 <= nr < self.rows
                                and 0 <= nc < self.cols
                                and self.grid[nr, nc] == 1
                                and not visited[nr, nc]
                            ):
                                visited[nr, nc] = True
                                queue.append((nr, nc))

        return island_count

    def count_islands_dfs(self, connectivity: int = 4, iterative: bool = True) -> int:
        if self.rows == 0 or self.cols == 0:
            return 0

        visited = np.zeros((self.rows, self.cols), dtype=bool)
        directions = self._get_directions(connectivity)
        island_count = 0

        if iterative:
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r, c] == 1 and not visited[r, c]:
                        island_count += 1
                        visited[r, c] = True
                        stack = [(r, c)]

                        while stack:
                            curr_r, curr_c = stack.pop()
                            for dr, dc in directions:
                                nr, nc = curr_r + dr, curr_c + dc
                                if (
                                    0 <= nr < self.rows
                                    and 0 <= nc < self.cols
                                    and self.grid[nr, nc] == 1
                                    and not visited[nr, nc]
                                ):
                                    visited[nr, nc] = True
                                    stack.append((nr, nc))
        else:
            def dfs(curr_r: int, curr_c: int):
                visited[curr_r, curr_c] = True
                for dr, dc in directions:
                    nr, nc = curr_r + dr, curr_c + dc
                    if (
                        0 <= nr < self.rows
                        and 0 <= nc < self.cols
                        and self.grid[nr, nc] == 1
                        and not visited[nr, nc]
                    ):
                        dfs(nr, nc)

            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r, c] == 1 and not visited[r, c]:
                        island_count += 1
                        dfs(r, c)

        return island_count

    def label_islands(
        self,
        method: Literal["bfs", "dfs"] = "bfs",
        connectivity: int = 4
    ) -> Tuple[int, np.ndarray, Dict[int, int]]:
        labeled_grid = np.zeros((self.rows, self.cols), dtype=int)
        directions = self._get_directions(connectivity)
        current_id = 0
        island_sizes: Dict[int, int] = {}

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c] == 1 and labeled_grid[r, c] == 0:
                    current_id += 1
                    area = 0
                    labeled_grid[r, c] = current_id

                    if method == "bfs":
                        queue = deque([(r, c)])
                        while queue:
                            curr_r, curr_c = queue.popleft()
                            area += 1
                            for dr, dc in directions:
                                nr, nc = curr_r + dr, curr_c + dc
                                if (
                                    0 <= nr < self.rows
                                    and 0 <= nc < self.cols
                                    and self.grid[nr, nc] == 1
                                    and labeled_grid[nr, nc] == 0
                                ):
                                    labeled_grid[nr, nc] = current_id
                                    queue.append((nr, nc))
                    else:
                        stack = [(r, c)]
                        while stack:
                            curr_r, curr_c = stack.pop()
                            area += 1
                            for dr, dc in directions:
                                nr, nc = curr_r + dr, curr_c + dc
                                if (
                                    0 <= nr < self.rows
                                    and 0 <= nc < self.cols
                                    and self.grid[nr, nc] == 1
                                    and labeled_grid[nr, nc] == 0
                                ):
                                    labeled_grid[nr, nc] = current_id
                                    stack.append((nr, nc))

                    island_sizes[current_id] = area

        return current_id, labeled_grid, island_sizes

    def max_area(self, connectivity: int = 4) -> int:
        num_islands, _, sizes = self.label_islands(connectivity=connectivity)
        return max(sizes.values()) if sizes else 0

    def summary(self, connectivity: int = 4) -> Dict[str, Union[int, float, List[int]]]:
        num_islands, _, sizes = self.label_islands(connectivity=connectivity)
        areas = list(sizes.values())
        return {
            "total_islands": num_islands,
            "total_land_cells": int(np.sum(self.grid == 1)),
            "total_water_cells": int(np.sum(self.grid == 0)),
            "max_island_area": max(areas) if areas else 0,
            "min_island_area": min(areas) if areas else 0,
            "mean_island_area": float(np.mean(areas)) if areas else 0.0,
            "all_areas": areas,
        }


def count_islands(grid: Union[np.ndarray, List[List[Union[int, str]]]], method: str = "bfs", connectivity: int = 4) -> int:
    counter = IslandCounter(grid)
    if method.lower() == "dfs":
        return counter.count_islands_dfs(connectivity=connectivity)
    return counter.count_islands_bfs(connectivity=connectivity)


if __name__ == "__main__":
    sample_grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1]
    ]

    print("--- Sample Grid ---")
    for row in sample_grid:
        print(" ".join(str(x) for x in row))

    counter = IslandCounter(sample_grid)
    bfs_count = counter.count_islands_bfs()
    dfs_count = counter.count_islands_dfs()
    print(f"\nNumber of Islands (BFS): {bfs_count}")
    print(f"Number of Islands (DFS): {dfs_count}")

    num_islands, labeled, sizes = counter.label_islands()
    print("\n--- Labeled Islands Grid ---")
    print(labeled)
    print(f"\nIsland Sizes: {sizes}")
    print(f"Max Island Area: {counter.max_area()}")
