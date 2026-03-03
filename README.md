# pd_code_delete_nugatory
delete all nugatory crossing from a pd_code (link or knot).

## Install

```bash
pip install pd-code-delete-nugatory
```

## Usage

```python
import pd_code_delete_nugatory


pd_code = [[8, 11, 9, 12], [12, 9, 13, 10], [10, 13, 11, 14], [7, 14, 8, 1], [4, 1, 5, 2], [2, 5, 3, 6], [6, 3, 7, 4]]

# output a 6-crossing knot
print(pd_code_delete_nugatory.erase_all_nugatory(pd_code))
```
