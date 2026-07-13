# pd-code-delete-nugatory

Detect and remove nugatory crossings from PD codes.

## Installation

```bash
pip install pd-code-delete-nugatory
```

## Quick start

`from pd_code_delete_nugatory import erase_all_nugatory`.

PD codes are lists of four-entry crossings. Each arc label must occur exactly twice. Functions validate their inputs and do not mutate caller-owned PD-code lists unless explicitly documented.

## Development

Use Python 3.10 or newer for Python packages. Build distributions with `poetry build`. Run the package's tests or examples before publishing. C++ projects require a modern standards-compliant compiler.

## License

MIT. See `LICENSE`.
