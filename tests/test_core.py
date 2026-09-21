"""Tests for DisjointSetUnion."""

import unittest

from disjoint_set_union import DisjointSetUnion


class TestDisjointSetUnion(unittest.TestCase):
    def test_initialization_empty(self):
        dsu = DisjointSetUnion()
        self.assertEqual(len(dsu), 0)
        self.assertEqual(dsu.get_sets(), [])

    def test_initialization_with_elements(self):
        dsu = DisjointSetUnion([1, 2, 3])
        self.assertEqual(len(dsu), 3)
        # Three singleton sets
        sets = dsu.get_sets()
        self.assertEqual(len(sets), 3)
        # Each set contains exactly one element
        for s in sets:
            self.assertEqual(len(s), 1)

    def test_initialization_ignores_duplicates(self):
        dsu = DisjointSetUnion([1, 2, 2, 3, 1])
        self.assertEqual(len(dsu), 3)

    def test_add_new_element(self):
        dsu = DisjointSetUnion()
        dsu.add("a")
        self.assertIn("a", dsu)
        self.assertEqual(len(dsu), 1)
        self.assertEqual(dsu.find("a"), "a")

    def test_add_existing_element_is_noop(self):
        dsu = DisjointSetUnion(["a"])
        dsu.add("a")
        self.assertEqual(len(dsu), 1)
        self.assertEqual(dsu.find("a"), "a")

    def test_find_missing_element_raises_keyerror(self):
        dsu = DisjointSetUnion()
        with self.assertRaises(KeyError):
            dsu.find(42)

    def test_connected_missing_element_raises_keyerror(self):
        dsu = DisjointSetUnion([1])
        with self.assertRaises(KeyError):
            dsu.connected(1, 2)
        with self.assertRaises(KeyError):
            dsu.connected(2, 1)

    def test_union_basic(self):
        dsu = DisjointSetUnion()
        dsu.union(1, 2)
        self.assertTrue(dsu.connected(1, 2))
        self.assertEqual(dsu.find(1), dsu.find(2))
        # Only one set now
        self.assertEqual(len(dsu.get_sets()), 1)

    def test_union_auto_adds_elements(self):
        dsu = DisjointSetUnion()
        dsu.union("x", "y")
        self.assertIn("x", dsu)
        self.assertIn("y", dsu)
        self.assertTrue(dsu.connected("x", "y"))

    def test_union_same_set_noop(self):
        dsu = DisjointSetUnion([1, 2, 3])
        dsu.union(1, 2)
        root_before = dsu.find(1)
        dsu.union(1, 2)
        self.assertEqual(dsu.find(1), root_before)
        self.assertEqual(dsu.find(2), root_before)

    def test_union_chain(self):
        dsu = DisjointSetUnion()
        dsu.union(1, 2)
        dsu.union(2, 3)
        dsu.union(3, 4)
        self.assertTrue(dsu.connected(1, 4))
        self.assertEqual(dsu.find(1), dsu.find(4))

    def test_union_disjoint_sets_merge(self):
        dsu = DisjointSetUnion([1, 2, 3, 4])
        dsu.union(1, 2)
        dsu.union(3, 4)
        dsu.union(2, 3)
        # All four should be connected
        for a in [1, 2, 3, 4]:
            for b in [1, 2, 3, 4]:
                self.assertTrue(dsu.connected(a, b))
        self.assertEqual(len(dsu.get_sets()), 1)

    def test_get_sets_returns_expected_groups(self):
        dsu = DisjointSetUnion([1, 2, 3, 4, 5])
        dsu.union(1, 2)
        dsu.union(2, 3)
        dsu.union(4, 5)
        sets = dsu.get_sets()
        self.assertEqual(len(sets), 2)
        # Convert to sorted tuples for comparison
        normalized = sorted(tuple(sorted(s)) for s in sets)
        self.assertEqual(normalized, [(1, 2, 3), (4, 5)])

    def test_get_sets_empty(self):
        dsu = DisjointSetUnion()
        self.assertEqual(dsu.get_sets(), [])

    def test_contains(self):
        dsu = DisjointSetUnion([10])
        self.assertIn(10, dsu)
        self.assertNotIn(20, dsu)

    def test_len(self):
        dsu = DisjointSetUnion()
        self.assertEqual(len(dsu), 0)
        dsu.add("a")
        self.assertEqual(len(dsu), 1)
        dsu.union("a", "b")
        self.assertEqual(len(dsu), 2)

    def test_path_compression_does_not_break_find(self):
        dsu = DisjointSetUnion()
        # Create a deep chain by forcing ranks manually? We can't directly set
        # ranks, but we can use union and then check find correctness after
        # many operations.
        elements = list(range(100))
        for i in range(1, len(elements)):
            dsu.union(elements[i - 1], elements[i])
        # Now find many times to trigger compression
        for _ in range(5):
            for e in elements:
                self.assertEqual(dsu.find(e), dsu.find(elements[0]))

    def test_repr(self):
        dsu = DisjointSetUnion([1, 2])
        dsu.union(1, 2)
        rep = repr(dsu)
        self.assertIn("DisjointSetUnion", rep)
        self.assertIn("1", rep)
        self.assertIn("2", rep)

    def test_elements_can_be_strings_and_tuples(self):
        dsu = DisjointSetUnion()
        dsu.union("a", "b")
        dsu.union((1, 2), (1, 3))
        self.assertTrue(dsu.connected("a", "b"))
        self.assertTrue(dsu.connected((1, 2), (1, 3)))
        self.assertFalse(dsu.connected("a", (1, 2)))


if __name__ == "__main__":
    unittest.main()
