# Makefile para Sistema de Rastreamento de Veículos YOLO v8 + DeepSORT
# Autor: Sistema automatizado
# Data: 2025-09-19

# Variáveis
PYTHON = .venv/bin/python
VENV_DIR = .venv
PROJECT_DIR = $(shell pwd)
VIDEO_DIR = videos
VIDEO = $(VIDEO_DIR)/video_1.mp4
MODEL = yolov8n.pt

# Cores para output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

# Regra padrão
.PHONY: help
help:
	@echo "$(BLUE)========================================$(NC)"
	@echo "$(BLUE)  Sistema de Rastreamento de Veículos  $(NC)"
	@echo "$(BLUE)        YOLO v8 + DeepSORT            $(NC)"
	@echo "$(BLUE)========================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Comandos disponíveis:$(NC)"
	@echo "  $(GREEN)make setup$(NC)          - Configura o ambiente virtual e dependências"
	@echo "  $(GREEN)make install$(NC)        - Instala dependências do projeto"
	@echo "  $(GREEN)make configure-line$(NC) - Configura linha de contagem visualmente"
	@echo "  $(GREEN)make run-video$(NC)      - Executa detecção no vídeo padrão"
	@echo "  $(GREEN)make run-webcam$(NC)     - Executa detecção na webcam"
	@echo "  $(GREEN)make run-config$(NC)     - Executa com configuração personalizada"
	@echo "  $(GREEN)make run-webcam-config$(NC) - Executa webcam com configuração"
	@echo "  $(GREEN)make run-save$(NC)       - Executa detecção e salva resultado"
	@echo "  $(GREEN)make run-custom$(NC)     - Executa detecção em vídeo customizado"
	@echo "  $(GREEN)make show-config$(NC)    - Mostra configuração atual"
	@echo "  $(GREEN)make edit-config$(NC)    - Edita arquivo de configuração"
	@echo "  $(GREEN)make test$(NC)           - Testa o sistema com vídeo curto"
	@echo "  $(GREEN)make clean$(NC)          - Remove arquivos temporários"
	@echo "  $(GREEN)make status$(NC)         - Mostra status do sistema"
	@echo "  $(GREEN)make demo$(NC)           - Executa demonstração completa"
	@echo ""
	@echo "$(YELLOW)Exemplos de uso:$(NC)"
	@echo "  make configure-line              - Configurar linha visualmente"
	@echo "  make run-custom VIDEO=caminho/para/video.mp4"
	@echo "  make run-video MODEL=yolov8s.pt"
	@echo "  make show-config                 - Ver configuração atual"
	@echo ""

# Configuração inicial
.PHONY: setup
setup:
	@echo "$(YELLOW)🚀 Configurando ambiente...$(NC)"
	@python3 -m venv $(VENV_DIR)
	@$(PYTHON) -m pip install --upgrade pip
	@echo "$(GREEN)✅ Ambiente virtual criado!$(NC)"
	@$(MAKE) install

# Instalação de dependências
.PHONY: install
install:
	@echo "$(YELLOW)📦 Instalando dependências...$(NC)"
	@$(PYTHON) -m pip install torch torchvision opencv-python numpy matplotlib PyYAML tqdm pillow scipy easydict hydra-core
	@$(PYTHON) -m pip install -e .
	@echo "$(GREEN)✅ Dependências instaladas!$(NC)"

# Executar detecção em vídeo
.PHONY: run-video
run-video:
	@echo "$(YELLOW)🎬 Executando detecção em vídeo...$(NC)"
	@if [ ! -f "$(VIDEO_DIR)/video_1.mp4" ]; then \
		echo "$(RED)❌ Vídeo não encontrado: $(VIDEO_DIR)/video_1.mp4$(NC)"; \
		exit 1; \
	fi
	@$(PYTHON) detect_vehicles.py --source $(VIDEO_DIR)/video_1.mp4 --show --model $(MODEL)

# Executar detecção na webcam
.PHONY: run-webcam
run-webcam:
	@echo "$(YELLOW)📹 Executando detecção na webcam...$(NC)"
	@echo "$(BLUE)💡 Pressione 'q' na janela do vídeo para sair$(NC)"
	@$(PYTHON) detect_vehicles.py --source 0 --show --model $(MODEL)

# Executar detecção e salvar resultado
.PHONY: run-save
run-save:
	@echo "$(YELLOW)💾 Executando detecção e salvando resultado...$(NC)"
	@$(PYTHON) detect_vehicles.py --source $(VIDEO_DIR)/video_1.mp4 --save --model $(MODEL)
	@echo "$(GREEN)✅ Resultado salvo em runs/detect/$(NC)"

# Executar detecção em vídeo customizado
.PHONY: run-custom
run-custom:
	@if [ -z "$(VIDEO)" ]; then \
		echo "$(RED)❌ Especifique o vídeo: make run-custom VIDEO=caminho/para/video.mp4$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)🎬 Executando detecção em: $(VIDEO)$(NC)"
	@$(PYTHON) detect_vehicles.py --source $(VIDEO) --show --model $(MODEL)

# Teste rápido do sistema
.PHONY: test
test:
	@echo "$(YELLOW)🧪 Testando sistema...$(NC)"
	@$(PYTHON) -c "from ultralytics import YOLO; model = YOLO('$(MODEL)'); print('✅ Modelo carregado com sucesso!')"
	@echo "$(GREEN)✅ Sistema funcionando corretamente!$(NC)"

# Limpeza de arquivos temporários
.PHONY: clean
clean:
	@echo "$(YELLOW)🧹 Limpando arquivos temporários...$(NC)"
	@rm -rf runs/
	@rm -rf __pycache__/
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name ".DS_Store" -delete
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

# Status do sistema
.PHONY: status
status:
	@echo "$(BLUE)📊 Status do Sistema$(NC)"
	@echo "========================"
	@echo "Diretório: $(PROJECT_DIR)"
	@echo "Python: $(shell $(PYTHON) --version 2>/dev/null || echo 'Não instalado')"
	@echo "Ambiente virtual: $(shell [ -d "$(VENV_DIR)" ] && echo '✅ Ativo' || echo '❌ Não configurado')"
	@echo "Modelo YOLO: $(shell [ -f "$(MODEL)" ] && echo '✅ Disponível' || echo '❌ Não encontrado')"
	@echo "Vídeos disponíveis:"
	@ls -la $(VIDEO_DIR)/ 2>/dev/null || echo "  ❌ Pasta de vídeos não encontrada"
	@echo ""

# Demonstração completa
.PHONY: demo
demo:
	@echo "$(BLUE)🎪 DEMONSTRAÇÃO COMPLETA$(NC)"
	@echo "=========================="
	@$(MAKE) status
	@echo ""
	@echo "$(YELLOW)1. Testando sistema...$(NC)"
	@$(MAKE) test
	@echo ""
	@echo "$(YELLOW)2. Executando detecção em vídeo (5 segundos)...$(NC)"
	@timeout 5s $(PYTHON) detect_vehicles.py --source $(VIDEO_DIR)/video_1.mp4 --show --model $(MODEL) || echo "$(GREEN)✅ Demo concluída!$(NC)"
	@echo ""
	@echo "$(GREEN)🎉 Demonstração finalizada!$(NC)"

# Verificar se o ambiente virtual existe
.PHONY: check-venv
check-venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(RED)❌ Ambiente virtual não encontrado. Execute: make setup$(NC)"; \
		exit 1; \
	fi

# Verificar dependências
.PHONY: check-deps
check-deps: check-venv
	@$(PYTHON) -c "import ultralytics" 2>/dev/null || (echo "$(RED)❌ Dependências não instaladas. Execute: make install$(NC)" && exit 1)

# Novos comandos para configuração de linha
.PHONY: configure-line
configure-line: check-deps
	@echo "$(YELLOW)🖱️ Configurando linha de contagem visualmente...$(NC)"
	@mkdir -p config
	@$(PYTHON) scripts/configure_line.py
	@echo "$(GREEN)✅ Configuração concluída!$(NC)"

.PHONY: show-config
show-config: check-venv
	@echo "$(BLUE)📋 Configuração Atual$(NC)"
	@echo "$(YELLOW)════════════════════════════════════$(NC)"
	@if [ -f config/counting_config.py ]; then \
		$(PYTHON) -c "import sys; sys.path.append('config'); from counting_config import *; \
		print('Linha de contagem:', COUNTING_LINE); \
		print('ROI habilitado:', ENABLE_ROI); \
		print('Área ROI:', ROI_AREA if ENABLE_ROI else 'Desabilitado'); \
		print('Classes de veículos:', VEHICLE_CLASSES); \
		print('Confiança mínima:', MIN_CONFIDENCE); \
		print('Direção de contagem:', COUNTING_DIRECTION)"; \
	else \
		echo "$(RED)❌ Arquivo de configuração não encontrado$(NC)"; \
		echo "$(YELLOW)💡 Execute: make configure-line$(NC)"; \
	fi
	@echo "$(YELLOW)════════════════════════════════════$(NC)"

.PHONY: edit-config
edit-config:
	@echo "$(YELLOW)📝 Abrindo editor de configuração...$(NC)"
	@mkdir -p config
	@${EDITOR:-nano} config/counting_config.py

.PHONY: run-config
run-config: check-deps
	@echo "$(YELLOW)⚙️ Executando com configuração personalizada...$(NC)"
	@$(PYTHON) simple_config_run.py --source $(VIDEO) --model $(MODEL) --show

.PHONY: run-webcam-config
run-webcam-config: check-deps
	@echo "$(YELLOW)📹 Executando webcam com configuração personalizada...$(NC)"
	@$(PYTHON) simple_config_run.py --source 0 --model $(MODEL) --show

# Executar com verificações
run-video run-webcam run-save run-custom run-config: check-deps