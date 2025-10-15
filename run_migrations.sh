
#!/usr/bin/env bash
set -e
alembic upgrade head || true
python -c "from app.seed import seed; seed()"
echo 'Done'
