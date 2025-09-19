#!/bin/bash
# Script para executar detecção de veículos na webcam
# Uso: ./scripts/run-webcam.sh

set -e

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configurações
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="$PROJECT_DIR/.venv/bin/python"
MODEL="yolov8n.pt"

# Função para imprimir mensagens
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar se o ambiente virtual existe
if [ ! -d "$PROJECT_DIR/.venv" ]; then
    print_error "Ambiente virtual não encontrado!"
    print_info "Execute primeiro: ./setup.sh"
    exit 1
fi

# Navegar para o diretório do projeto
cd "$PROJECT_DIR"

# Executar detecção na webcam
print_info "📹 Iniciando detecção na webcam..."
print_info "🤖 Modelo: $MODEL"
print_warning "Pressione 'q' na janela do vídeo para sair"
print_warning "Certifique-se de que a webcam está conectada"
echo ""

"$PYTHON" detect_vehicles.py \
    --source 0 \
    --show \
    --model "$MODEL" \
    --conf 0.5

print_success "Detecção finalizada!"