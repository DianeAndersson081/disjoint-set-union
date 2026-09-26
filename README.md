# Disjoint Set Union

A small, dependency-free Python implementation of the disjoint-set (union-find) data structure with path compression and union by rank.

## Usage

```python
from disjoint_set_union import DisjointSetUnion

dsu = DisjointSetUnion()
dsu.union(1, 2)
dsu.union(2, 3)
print(dsu.connected(1, 3))  # True
print(dsu.get_sets())       # [[1, 2, 3]]
```

You can also initialize with an iterable of elements:

```python
dsu = DisjointSetUnion(["a", "b", "c", "d"])
dsu.union("a", "b")
dsu.union("c", "d")
print(dsu.connected("a", "b"))  # True
print(dsu.connected("a", "c"))  # False
```

## Why this exists

The disjoint-set data structure solves the problem of dynamically tracking groups of connected items where the only operations needed are "merge two groups" and "check if two items are in the same group". It is commonly used in graph algorithms such as Kruskal's minimum spanning tree, image processing for connected components, and equivalence-class maintenance.

This implementation uses **union by rank** (attach the shallower tree under the deeper one) and **path compression** (flatten the tree during find operations). Together these give an amortized near-constant time per operation, making it suitable for large datasets.

## Edge cases and design decisions

- **Auto-adding elements**: `union(a, b)` will add `a` and `b` as singletons if they are not already present. This is convenient but can hide typos. If you need strict checking, use `add` explicitly before calling `union`.
- **`connected` requires existing elements**: unlike `union`, `connected(a, b)` raises `KeyError` if either element is missing. This is intentional: a query should not silently mutate the structure.
- **`get_sets` order**: the returned list of sets has no guaranteed order, either among sets or within a set. Treat it as an unordered collection.
- **Element types**: any hashable object can be used as an element, including strings, numbers, and tuples.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

