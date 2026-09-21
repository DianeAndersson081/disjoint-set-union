"""Core implementation of Disjoint Set Union.

The DSU maintains a collection of non-overlapping sets, supporting efficient
unification of sets and checking whether two elements belong to the same set.
"""

from typing import Dict, Hashable, Iterable, List, Optional, Tuple


class DisjointSetUnion:
    """A disjoint-set data structure with path compression and union by rank.

    Elements may be any hashable objects. Each element starts in its own
    singleton set. The structure supports near-constant-time `find` and `union`
    operations, amortized, by keeping trees shallow.
    """

    def __init__(self, elements: Optional[Iterable[Hashable]] = None) -> None:
        """Initialize the DSU, optionally with a collection of initial elements.

        If `elements` is provided, every item in the iterable is added as a
        singleton set. Duplicates are ignored. If omitted, the DSU starts empty
        and elements can be added later via `add` or automatically through
        `union`.

        Args:
            elements: Optional iterable of hashable elements to pre-populate.
        """
        self._parent: Dict[Hashable, Hashable] = {}
        self._rank: Dict[Hashable, int] = {}
        if elements is not None:
            for elem in elements:
                self.add(elem)

    def add(self, element: Hashable) -> None:
        """Add a new element as a singleton set.

        If the element already exists, this method does nothing. This is
        intentional: adding an existing element must not break the invariant
        that each element is managed exactly once.
        """
        if element not in self._parent:
            self._parent[element] = element
            self._rank[element] = 0

    def find(self, element: Hashable) -> Hashable:
        """Return the representative (root) of the set containing `element`.

        Uses path compression: every node along the path to the root is
        re-parented directly to the root, flattening the tree and speeding up
        subsequent finds.

        Raises:
            KeyError: If `element` has not been added to the structure.
        """
        parent = self._parent
        if element not in parent:
            raise KeyError(f"Element {element!r} not found in DisjointSetUnion")

        # Find the root
        root = element
        while parent[root] != root:
            root = parent[root]

        # Path compression: re-point all visited nodes to root
        current = element
        while parent[current] != root:
            nxt = parent[current]
            parent[current] = root
            current = nxt

        return root

    def union(self, a: Hashable, b: Hashable) -> None:
        """Merge the sets containing elements `a` and `b`.

        If `a` and `b` are already in the same set, this method does nothing.
        If either element has not been added, it is automatically added as a
        singleton before merging. This convenience avoids requiring an explicit
        `add` call for every element.

        Union by rank: the root with smaller rank is attached to the root with
        larger rank. If ranks are equal, one root is chosen arbitrarily and its
        rank is incremented. This keeps trees balanced, giving amortized
        O(alpha(n)) find and union operations.
        """
        self.add(a)
        self.add(b)

        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        rank_a = self._rank[root_a]
        rank_b = self._rank[root_b]

        if rank_a < rank_b:
            self._parent[root_a] = root_b
        elif rank_a > rank_b:
            self._parent[root_b] = root_a
        else:
            self._parent[root_b] = root_a
            self._rank[root_a] += 1

    def connected(self, a: Hashable, b: Hashable) -> bool:
        """Return True if `a` and `b` are in the same set.

        Both elements must already be present; otherwise KeyError is raised.
        This is stricter than `union`, which auto-adds missing elements. The
        distinction is deliberate: `connected` is a query, not a mutation, and
        silently adding elements would hide errors in user logic.
        """
        return self.find(a) == self.find(b)

    def get_sets(self) -> List[List[Hashable]]:
        """Return a list of all current disjoint sets.

        Each set is represented as a list of its elements. The order of sets
        and the order of elements within a set are unspecified. Use this only
        when you need the actual groupings, not for ordering-sensitive logic.
        """
        groups: Dict[Hashable, List[Hashable]] = {}
        for elem in self._parent:
            root = self.find(elem)
            groups.setdefault(root, []).append(elem)
        return list(groups.values())

    def __len__(self) -> int:
        """Return the number of distinct elements currently managed."""
        return len(self._parent)

    def __contains__(self, element: Hashable) -> bool:
        """Return True if `element` has been added to the structure."""
        return element in self._parent

    def __repr__(self) -> str:
        return f"DisjointSetUnion({self.get_sets()!r})"
