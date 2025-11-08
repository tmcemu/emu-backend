#!/bin/bash

# ============================================
# Валидация конфигурации
# ============================================

validate_env_var() {
    local var_name=$1
    local var_value=$2
    local error_message=$3

    if [ -z "$var_value" ]; then
        echo "❌ Ошибка конфигурации: $error_message"
        echo "   Отсутствует переменная: $var_name"
        exit 1
    fi
}

export_to_github_env() {
    local var_name=$1
    local var_value=$2
    echo "$var_name=$var_value" >> $GITHUB_ENV
}

# ============================================
# Основной загрузчик конфигурации
# ============================================

load_server_config() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              ЗАГРУЗКА КОНФИГУРАЦИИ                         ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    local config_file="/root/.env.runner"

    # Проверка существования файла конфигурации
    if [ ! -f "$config_file" ]; then
        echo "❌ Файл конфигурации не найден: $config_file"
        exit 1
    fi

    echo "📄 Файл: $config_file"

    # Загрузка переменных окружения из файла конфигурации
    set -a
    source "$config_file"
    set +a

    echo "✅ Переменные загружены"
    echo ""
    echo "─────────────────────────────────────────"
    echo "Валидация обязательных переменных"
    echo "─────────────────────────────────────────"

    # Валидация требуемой конфигурации API
    validate_env_var "STAGE_DOMAIN" "$STAGE_DOMAIN" "STAGE_DOMAIN не настроен"
    validate_env_var "PROD_DOMAIN" "$PROD_DOMAIN" "PROD_DOMAIN не настроен"
    validate_env_var "STAGE_HOST" "$STAGE_HOST" "STAGE_HOST не настроен"
    validate_env_var "STAGE_PASSWORD" "$STAGE_PASSWORD" "STAGE_PASSWORD не настроен"

    echo "✅ Все обязательные переменные присутствуют"

    # Извлечение и построение префикса сервиса
    SERVICE_PREFIX=$(echo "$SERVICE_NAME" | tr '[:lower:]' '[:upper:]' | tr '-' '_')
    SERVICE_PREFIX_VAR_NAME="${SERVICE_PREFIX}_PREFIX"
    SERVICE_PREFIX="${!SERVICE_PREFIX_VAR_NAME}"

    echo ""
    echo "─────────────────────────────────────────"
    echo "Экспорт в окружение GitHub Actions"
    echo "─────────────────────────────────────────"

    # Экспорт основной конфигурации
    export_to_github_env "SERVICE_PREFIX" "$SERVICE_PREFIX"
    export_to_github_env "STAGE_HOST" "$STAGE_HOST"
    export_to_github_env "STAGE_PASSWORD" "$STAGE_PASSWORD"
    export_to_github_env "STAGE_DOMAIN" "$STAGE_DOMAIN"
    export_to_github_env "PROD_DOMAIN" "$PROD_DOMAIN"

    # Экспорт префиксов сервисов
    export_to_github_env "EMU_TG_BOT_PREFIX" "$EMU_TG_BOT_PREFIX"
    export_to_github_env "EMU_ACCOUNT_PREFIX" "$EMU_ACCOUNT_PREFIX"
    export_to_github_env "EMU_AUTHORIZATION_PREFIX" "$EMU_AUTHORIZATION_PREFIX"
    export_to_github_env "EMU_EMPLOYEE_PREFIX" "$EMU_EMPLOYEE_PREFIX"
    export_to_github_env "EMU_ORGANIZATION_PREFIX" "$EMU_ORGANIZATION_PREFIX"
    export_to_github_env "EMU_CONTENT_PREFIX" "$EMU_CONTENT_PREFIX"
    export_to_github_env "EMU_RELEASE_TG_BOT_PREFIX" "$EMU_RELEASE_TG_BOT_PREFIX"
    export_to_github_env "EMU_INTERSERVER_SECRET_KEY" "$EMU_INTERSERVER_SECRET_KEY"

    echo "✅ Переменные экспортированы"

    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              КОНФИГУРАЦИЯ ЗАГРУЖЕНА                        ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Сервис:          $SERVICE_NAME"
    echo "🔧 Префикс:         $SERVICE_PREFIX"
    echo "🖥️  Stage хост:      $STAGE_HOST"
    echo "🌐 Stage домен:     $STAGE_DOMAIN"
    echo "🌐 Production домен: $PROD_DOMAIN"
    echo ""
    echo "Префиксы сервисов:"
    echo "  • TG Bot:         $EMU_TG_BOT_PREFIX"
    echo "  • Account:        $EMU_ACCOUNT_PREFIX"
    echo "  • Authorization:  $EMU_AUTHORIZATION_PREFIX"
    echo "  • Employee:       $EMU_EMPLOYEE_PREFIX"
    echo "  • Organization:   $EMU_ORGANIZATION_PREFIX"
    echo "  • Content:        $EMU_CONTENT_PREFIX"
    echo "  • Release Bot:    $EMU_RELEASE_TG_BOT_PREFIX"
    echo ""
}