
## load envs:
```bash	
export $(cat .env |grep -v ^# | xargs)
```

## run tests:
```bash
PYTHONPATH=$(pwd) uv run python tests/test.py
```
