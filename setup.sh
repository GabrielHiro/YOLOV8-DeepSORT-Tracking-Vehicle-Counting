#!/bin/bash
# Script de configuração para o Sistema de Rastreamento de Veículos
# Autor: Sistema automatizado
# Data: 2025-09-19

set -e  # Para o script em caso de erro

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções utilitárias
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Sistema de Rastreamento de Veículos  ${NC}"
    echo -e "${BLUE}        YOLO v8 + DeepSORT            ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
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

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar se o Python está instalado
check_python() {
    if command -v python3 &> /dev/null; then
        print_success "Python3 encontrado: $(python3 --version)"
        return 0
    else
        print_error "Python3 não encontrado!"
        print_info "Instale o Python3 antes de continuar:"
        print_info "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-venv python3-pip"
        print_info "  CentOS/RHEL: sudo yum install python3 python3-venv python3-pip"
        return 1
    fi
}

# Criar ambiente virtual
setup_venv() {
    print_info "Criando ambiente virtual..."
    
    if [ -d ".venv" ]; then
        print_warning "Ambiente virtual já existe. Removendo..."
        rm -rf .venv
    fi
    
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    print_success "Ambiente virtual criado!"
}

# Instalar dependências
install_dependencies() {
    print_info "Instalando dependências..."
    
    source .venv/bin/activate
    
    # Dependências básicas
    pip install torch torchvision opencv-python numpy matplotlib PyYAML tqdm pillow scipy easydict hydra-core
    
    # Instalar o projeto
    pip install -e .
    
    print_success "Dependências instaladas!"
}

# Verificar instalação
verify_installation() {
    print_info "Verificando instalação..."
    
    source .venv/bin/activate
    
    # Testar importações
    python -c "from ultralytics import YOLO; print('✅ Ultralytics YOLO importado com sucesso')"
    python -c "import cv2; print('✅ OpenCV importado com sucesso')"
    python -c "import torch; print('✅ PyTorch importado com sucesso')"
    
    # Baixar modelo se não existir
    if [ ! -f "yolov8n.pt" ]; then
        print_info "Baixando modelo YOLO..."
        python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
    fi
    
    print_success "Instalação verificada!"
}

# Função principal
main() {
    print_header
    
    print_info "Iniciando configuração do sistema..."
    echo ""
    
    # Verificar Python
    if ! check_python; then
        exit 1
    fi
    echo ""
    
    # Configurar ambiente virtual
    setup_venv
    echo ""
    
    # Instalar dependências
    install_dependencies
    echo ""
    
    # Verificar instalação
    verify_installation
    echo ""
    
    print_success "🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!"
    echo ""
    print_info "Próximos passos:"
    echo "  1. Ativar o ambiente virtual: source .venv/bin/activate"
    echo "  2. Executar detecção: make run-video"
    echo "  3. Ver todas as opções: make help"
    echo ""
    print_info "Para executar comandos diretamente:"
    echo "  ./scripts/run-video.sh"
    echo "  ./scripts/run-webcam.sh"
    echo "  ./scripts/run-demo.sh"
}

# Executar função principal
main "$@"