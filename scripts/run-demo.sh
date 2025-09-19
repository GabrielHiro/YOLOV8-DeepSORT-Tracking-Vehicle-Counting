#!/bin/bash
# Script para executar demonstração do sistema
# Uso: ./scripts/run-demo.sh

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
VIDEO_DIR="$PROJECT_DIR/videos"
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

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}    DEMONSTRAÇÃO DO SISTEMA            ${NC}"
    echo -e "${BLUE}  Rastreamento de Veículos YOLO v8     ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# Verificar se o ambiente virtual existe
if [ ! -d "$PROJECT_DIR/.venv" ]; then
    print_error "Ambiente virtual não encontrado!"
    print_info "Execute primeiro: ./setup.sh"
    exit 1
fi

# Navegar para o diretório do projeto
cd "$PROJECT_DIR"

# Demonstração
print_header

print_info "1️⃣  Verificando sistema..."
"$PYTHON" -c "from ultralytics import YOLO; model = YOLO('$MODEL'); print('✅ Modelo YOLO carregado com sucesso!')"
print_success "Sistema funcionando!"
echo ""

print_info "2️⃣  Mostrando status..."
echo "📁 Diretório: $PROJECT_DIR"
echo "🐍 Python: $("$PYTHON" --version)"
echo "🤖 Modelo: $MODEL"
echo "📹 Vídeos disponíveis:"
ls -la "$VIDEO_DIR"/ 2>/dev/null || print_warning "Pasta de vídeos não encontrada"
echo ""

print_info "3️⃣  Executando teste rápido (10 segundos)..."
print_warning "A janela de vídeo será aberta por 10 segundos"
echo ""

# Executar detecção por tempo limitado
timeout 10s "$PYTHON" detect_vehicles.py \
    --source "$VIDEO_DIR/video_1.mp4" \
    --show \
    --model "$MODEL" \
    --conf 0.5 || true

echo ""
print_success "🎉 Demonstração concluída!"
echo ""
print_info "Para executar manualmente:"
print_info "  📹 Vídeo: ./scripts/run-video.sh"
print_info "  📷 Webcam: ./scripts/run-webcam.sh"
print_info "  🔧 Makefile: make help"