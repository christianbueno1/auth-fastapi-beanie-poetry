## Notes

### Best Approach for Your Issue?
- ✅ Try using Python 3.12 first (best stability).
- ✅ If that doesn’t work, remove poetry.lock and retry installation.
- ✅ If you want to test without removing, use poetry install --no-lock.

## Error
- The issue comes from Pydantic-Core (2.18.2) trying to build using Python 3.13, but PyO3 (0.21.1) does not support Python 3.13 yet.

```
# If Python 3.12 is not installed, install it with Fedora’s package manager:
sudo dnf install python3.12
poetry env use python3.12
poetry install

```