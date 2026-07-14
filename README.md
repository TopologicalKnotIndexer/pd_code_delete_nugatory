# pd-code-delete-nugatory

Detect and remove Reidemeister-I and nugatory crossings from knot or link
planar diagram (PD) codes.

The implementation is self-contained and uses only the Python standard
library. This repository is an independent checkout and has no nested Git or
runtime repository dependency.

## Usage

```python
from pd_code_delete_nugatory import (
    erase_all_nugatory,
    get_index_of_nugatory,
)

trefoil = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
print(get_index_of_nugatory(trefoil))  # None
print(erase_all_nugatory([[1, 1, 2, 2]]))  # []
```

The earlier README called `get_index_of_nugatory()` on the one-crossing R1
example even though the old detector asserted that all four crossing labels
were distinct. The public detector now reports repeated-label crossings as
non-nugatory, while `erase_all_nugatory()` removes them in its R1 preprocessing
stage.

## Algorithm

Every input crossing must contain four positive integer arc labels, and every
label must occur exactly twice across the whole PD code.

1. Repeated-label crossings are removed by Reidemeister-I reduction.
2. Crossings and arc labels are represented as a bipartite incidence graph.
3. A remaining crossing is nugatory when deleting its crossing vertex
   increases the graph's connected-component count.
4. Its opposite strands are reconnected, labels are renumbered by traversing
   each link component, and R1 reduction is run again.
5. Detection and removal repeat to a fixed point.

Unlike the previous implementation, detection does not depend on consecutive
input labels, supports multiple link components, validates public inputs, and
never mutates caller-owned lists.

## Public API

- `erase_all_nugatory(pd_code)` removes all R1 and nugatory crossings.
- `erase_one_nugatory(pd_code, index)` removes one verified crossing.
- `get_index_of_nugatory(pd_code)` returns the first matching index or `None`.
- `is_nugatory(pd_code, index)` tests one crossing.
- `renumber(pd_code)` assigns consecutive labels along components.
- `validate_pd_code(pd_code)` returns a normalized validated copy.

## Development

Python 3.10 or newer is required.

```bash
python -m unittest discover -s tests -v
```

No PyPI publication is performed as part of this repository's maintenance.

## License

MIT. See [`LICENSE`](LICENSE).

## Citation

If you use this repository in academic work, please cite it as:

```bibtex
@software{topologicalknotindexer_pd_code_delete_nugatory,
  author = {{TopologicalKnotIndexer contributors}},
  title = {{pd\_code\_delete\_nugatory}},
  year = {2026},
  url = {https://github.com/TopologicalKnotIndexer/pd_code_delete_nugatory}
}
```
