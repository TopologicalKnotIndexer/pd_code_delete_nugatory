from copy import deepcopy
import unittest

import pd_code_delete_nugatory as nugatory


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


def diagram_with_nugatory_join():
    first = [[1, 5, 2, 4], [3, 7, 4, 6], [5, 3, 6, 2]]
    second = [[8, 12, 9, 11], [10, 14, 11, 13], [12, 10, 13, 9]]
    return [[1, 7, 8, 14], *first, *second]


class NugatoryTests(unittest.TestCase):
    def test_documented_api_is_exported(self):
        self.assertIn("get_index_of_nugatory", nugatory.__all__)
        self.assertIsNone(nugatory.get_index_of_nugatory(TREFOIL))

    def test_r1_example_is_removed_without_detector_assertion(self):
        pd_code = [[1, 1, 2, 2]]
        self.assertFalse(nugatory.is_nugatory(pd_code, 0))
        self.assertEqual(nugatory.erase_all_nugatory(pd_code), [])

    def test_removes_a_label_independent_nugatory_crossing(self):
        pd_code = diagram_with_nugatory_join()
        original = deepcopy(pd_code)
        self.assertEqual(nugatory.get_index_of_nugatory(pd_code), 0)
        reduced = nugatory.erase_all_nugatory(pd_code)
        self.assertEqual(len(reduced), 6)
        nugatory.validate_pd_code(reduced)
        self.assertEqual(pd_code, original)

    def test_arbitrary_relabeling_does_not_change_detection(self):
        pd_code = diagram_with_nugatory_join()
        labels = sorted({label for crossing in pd_code for label in crossing})
        mapping = {label: 100 + 7 * index for index, label in enumerate(labels)}
        relabeled = [
            [mapping[label] for label in crossing] for crossing in pd_code
        ]
        self.assertEqual(nugatory.get_index_of_nugatory(relabeled), 0)
        reduced = nugatory.erase_all_nugatory(relabeled)
        self.assertEqual(
            {label for crossing in reduced for label in crossing},
            set(range(1, 2 * len(reduced) + 1)),
        )

    def test_accepts_multiple_strand_components(self):
        pd_code = [
            [2, 9, 3, 10],
            [4, 7, 1, 8],
            [6, 11, 7, 12],
            [8, 3, 5, 4],
            [9, 2, 10, 1],
            [12, 5, 11, 6],
        ]
        self.assertEqual(len(nugatory.erase_all_nugatory(pd_code)), 6)

    def test_rejects_invalid_labels_and_non_nugatory_removal(self):
        with self.assertRaisesRegex(ValueError, "exactly twice"):
            nugatory.erase_all_nugatory([[1, 2, 3, 4]])
        with self.assertRaisesRegex(ValueError, "not nugatory"):
            nugatory.erase_one_nugatory(TREFOIL, 0)


if __name__ == "__main__":
    unittest.main()
