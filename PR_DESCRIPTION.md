# Fix typos and improve int input handling for OrganisasjonsnummerValidator

## Summary
This PR fixes several small issues found during a code review.

## Changes

### 🐛 Bug fix
**`OrganisasjonsnummerValidator` now accepts `int` input**

Previously, passing an integer like `123456789` would crash:
```python
>>> OrganisasjonsnummerValidator.validate_python(123456789)
AttributeError: 'int' object has no attribute 'replace'
```

Fixed by converting to `str` before calling `.replace()` in `_types.py`:
```python
# Before
BeforeValidator(lambda v: v.replace(" ", ""))

# After  
BeforeValidator(lambda v: str(v).replace(" ", ""))
```

### ✏️ Typos in `EnhetQuery` (`_queries.py`)

| Before (typo) | After (correct) |
|---------------|-----------------|
| `registert_i_foretaksregisteret` | `registrert_i_foretaksregisteret` |
| `under_tvangsavvikling_eller_trangsopplosning` | `under_tvangsavvikling_eller_tvangsopplosning` |

### 📝 Documentation fix (`_client.py`)
Fixed incorrect docstring in `get_roller()` method:
```python
# Before
"""Get :class:`Enhet` given an organization number."""

# After
"""Get roles for an entity given an organization number."""
```

## Testing
All 40 existing tests pass.

## Breaking Changes
⚠️ The typo fixes are breaking changes for anyone using the old (misspelled) attribute names directly in their code.
