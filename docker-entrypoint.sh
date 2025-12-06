#!/bin/bash
set -e

main() {
  echo "🐳 Rachinsky Bot - Docker Entrypoint"

  echo "🔄 Применяем миграции..."
  aerich upgrade
  echo "✅ Миграции применены"

  echo "🚀 Запускаем бота..."

  # Запускаем команду переданную в docker
  exec "$@"
}

main "$@"
