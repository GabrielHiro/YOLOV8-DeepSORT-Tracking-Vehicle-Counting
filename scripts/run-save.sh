#!/bin/bash
# Script para salvar resultado da detecção
# Uso: ./scripts/run-save.sh [caminho_do_video]

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
DEFAULT_VIDEO="$VIDEO_DIR/video_1.mp4"
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

# Determinar vídeo de entrada
if [ -n "$1" ]; then
    VIDEO_SOURCE="$1"
    print_info "Usando vídeo especificado: $VIDEO_SOURCE"
else
    VIDEO_SOURCE="$DEFAULT_VIDEO"
    print_info "Usando vídeo padrão: $VIDEO_SOURCE"
fi

# Verificar se o arquivo de vídeo existe
if [ ! -f "$VIDEO_SOURCE" ]; then
    print_error "Arquivo de vídeo não encontrado: $VIDEO_SOURCE"
    print_info "Vídeos disponíveis:"
    ls -la "$VIDEO_DIR"/ 2>/dev/null || print_warning "Pasta de vídeos não encontrada"
    exit 1
fi

# Executar detecção e salvar
print_info "💾 Processando e salvando resultado..."
print_info "📹 Fonte: $VIDEO_SOURCE"
print_info "🤖 Modelo: $MODEL"
echo ""

"$PYTHON" detect_vehicles.py \
    --source "$VIDEO_SOURCE" \
    --save \
    --model "$MODEL" \
    --conf 0.5

# Encontrar o arquivo de saída mais recente
OUTPUT_DIR="runs/detect"
if [ -d "$OUTPUT_DIR" ]; then
    LATEST_RUN=$(ls -t "$OUTPUT_DIR" | head -n1)
    if [ -n "$LATEST_RUN" ]; then
        print_success "Resultado salvo em: $OUTPUT_DIR/$LATEST_RUN"
        print_info "📁 Conteúdo da pasta de saída:"
        ls -la "$OUTPUT_DIR/$LATEST_RUN"
    fi
else
    print_warning "Pasta de saída não encontrada"
fi

print_success "Processamento finalizado!"