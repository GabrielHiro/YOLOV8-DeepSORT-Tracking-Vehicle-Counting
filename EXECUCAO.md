# Guia de Execução - Makefile e Scripts

Este documento explica como usar o Makefile e scripts shell para executar o sistema de rastreamento de veículos.

## 🚀 Configuração Inicial

### Opção 1: Usando o script de configuração
```bash
./setup.sh
```

### Opção 2: Usando Makefile
```bash
make setup
```

## 📋 Comandos do Makefile

### Ajuda e Informações
```bash
make help          # Mostra todos os comandos disponíveis
make status         # Mostra status do sistema
```

### Execução
```bash
make run-video      # Executa detecção no vídeo padrão
make run-webcam     # Executa detecção na webcam
make run-save       # Executa detecção e salva resultado
make run-custom VIDEO=caminho/para/video.mp4  # Vídeo customizado
```

### Teste e Demonstração
```bash
make test           # Testa o sistema
make demo           # Execução demonstração completa
```

### Manutenção
```bash
make clean          # Remove arquivos temporários
make install        # Reinstala dependências
```

## 🛠️ Scripts Shell

### Script de Configuração
```bash
./setup.sh          # Configura todo o ambiente automaticamente
```

### Scripts de Execução
```bash
# Detecção em vídeo
./scripts/run-video.sh                    # Vídeo padrão
./scripts/run-video.sh caminho/video.mp4  # Vídeo específico

# Detecção na webcam
./scripts/run-webcam.sh

# Salvar resultado
./scripts/run-save.sh                     # Vídeo padrão
./scripts/run-save.sh caminho/video.mp4   # Vídeo específico

# Demonstração
./scripts/run-demo.sh                     # Demo completa
```

## 🎯 Exemplos de Uso

### Configuração Rápida
```bash
# 1. Clonar/baixar projeto
# 2. Executar configuração
./setup.sh
# 3. Testar sistema
make test
```

### Execução Simples
```bash
# Detecção no vídeo padrão
make run-video

# Detecção na webcam
make run-webcam
```

### Execução Avançada
```bash
# Vídeo específico com modelo maior
make run-custom VIDEO=videos/meu_video.mp4 MODEL=yolov8s.pt

# Salvar resultado processado
make run-save
```

### Demonstração Completa
```bash
# Demo automática (10 segundos)
make demo

# Ou usando script
./scripts/run-demo.sh
```

## 📁 Estrutura de Arquivos

```
projeto/
├── Makefile                 # Comandos de automação
├── setup.sh                 # Script de configuração
├── scripts/                 # Scripts de execução
│   ├── run-video.sh         # Executa detecção em vídeo
│   ├── run-webcam.sh        # Executa detecção na webcam
│   ├── run-save.sh          # Salva resultado
│   └── run-demo.sh          # Demonstração
├── videos/                  # Vídeos de entrada
├── runs/                    # Resultados salvos
└── .venv/                   # Ambiente virtual
```

## 🔧 Personalização

### Variáveis do Makefile
```bash
# Modificar modelo YOLO
make run-video MODEL=yolov8s.pt

# Vídeo específico
make run-custom VIDEO=/caminho/absoluto/video.mp4
```

### Configurações nos Scripts
Edite as variáveis no início de cada script:
- `MODEL`: Modelo YOLO a usar
- `VIDEO_DIR`: Diretório dos vídeos
- Parâmetros de confiança, etc.

## 🐛 Solução de Problemas

### Erro: "Ambiente virtual não encontrado"
```bash
./setup.sh
# ou
make setup
```

### Erro: "Comando não encontrado"
```bash
# Dar permissões aos scripts
chmod +x setup.sh scripts/*.sh
```

### Erro: "Modelo não encontrado"
```bash
# O script baixa automaticamente, mas se falhar:
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Erro: "Vídeo não encontrado"
```bash
# Verificar vídeos disponíveis
ls -la videos/
# Ou usar webcam
make run-webcam
```

## 📊 Saídas do Sistema

### Arquivos Gerados
- `runs/detect/expN/`: Resultados salvos
- `yolov8n.pt`: Modelo YOLO baixado
- `.venv/`: Ambiente virtual

### Logs e Outputs
- Terminal: Progresso em tempo real
- Janela de vídeo: Detecções visualizadas
- Arquivos salvos: Vídeos processados

## 🎪 Fluxo Completo

```bash
# 1. Configuração inicial
./setup.sh

# 2. Verificar sistema
make status

# 3. Testar
make test

# 4. Executar detecção
make run-video

# 5. Salvar resultado
make run-save

# 6. Limpeza (opcional)
make clean
```

Este sistema fornece múltiplas formas de executar o projeto, desde comandos simples até automação completa com Makefile! 🚀