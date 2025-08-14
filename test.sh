set -eo pipefail # 스크립트 중 오류 발생 시 종료

echo "Starting ruff"
uv run ruff format
uv run ruff check --fix
echo "OK"