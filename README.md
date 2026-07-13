# pd-code-delete-nugatory

Detect and remove nugatory crossings from PD codes.

## Installation

```bash
pip install pd-code-delete-nugatory
```

## Usage example

```python
from pd_code_delete_nugatory import erase_all_nugatory, get_index_of_nugatory

pd = [[1, 1, 2, 2]]
print(get_index_of_nugatory(pd))
print(erase_all_nugatory(pd))
```

## Algorithm

For each candidate crossing, the algorithm removes that crossing from a weak strand graph and compares graph connectivity. A crossing whose removal separates regions is nugatory. Erasing it reconnects the paired arcs, removes any induced Reidemeister-I crossing, and renumbers the remaining component cycles. The process repeats until no candidate remains.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

No external software is required.

## Development

Run examples and package checks before release. Python packages require Python 3.10 or newer. Build PyPI artifacts with:

```bash
poetry check
poetry build
```

## License

MIT. See `LICENSE`.
