# 📋 Resumo de Comandos - Sistema de Rastreamento de Veículos

## ⚡ Início Rápido

```bash
# 1. Configurar sistema (uma vez apenas)
./setup.sh

# 2. Executar demonstração
make demo

# 3. Detectar veículos em vídeo
make run-video
```

## 🔧 Métodos de Configuração

| Método | Comando | Descrição |
|--------|---------|-----------|
| **Script Automático** | `./setup.sh` | Configura tudo automaticamente |
| **Makefile** | `make setup` | Configuração via Make |
| **Manual** | `source .venv/bin/activate` | Configuração passo a passo |

## 🎬 Métodos de Execução

### Via Makefile (Recomendado)
```bash
make run-video      # Vídeo padrão
make run-webcam     # Webcam
make run-save       # Salvar resultado
make run-custom VIDEO=meu_video.mp4  # Vídeo específico
```

### Via Scripts Shell
```bash
./scripts/run-video.sh              # Vídeo padrão
./scripts/run-video.sh meu_video.mp4 # Vídeo específico
./scripts/run-webcam.sh             # Webcam
./scripts/run-save.sh               # Salvar resultado
./scripts/run-demo.sh               # Demonstração
```

### Via Python Direto
```bash
source .venv/bin/activate
python detect_vehicles.py --source videos/video_1.mp4 --show
python detect_vehicles.py --source 0 --show  # webcam
python simple_detection.py  # versão simples
```

## 🛠️ Comandos de Manutenção

```bash
make help           # Ver todas as opções
make status         # Status do sistema
make test           # Testar funcionamento
make clean          # Limpar arquivos temporários
make demo           # Demonstração de 10 segundos
```

## 📂 Estrutura de Arquivos

```
projeto/
├── Makefile                 # Automação principal
├── setup.sh                 # Configuração automática
├── EXECUCAO.md             # Guia detalhado
├── scripts/                # Scripts de execução
│   ├── run-video.sh        # Executar vídeo
│   ├── run-webcam.sh       # Executar webcam
│   ├── run-save.sh         # Salvar resultado
│   └── run-demo.sh         # Demonstração
├── detect_vehicles.py      # Script principal
├── simple_detection.py     # Versão simplificada
└── videos/                 # Vídeos de entrada
```

## 🎯 Casos de Uso

| Situação | Comando Recomendado |
|----------|-------------------|
| **Primeira vez** | `./setup.sh` + `make demo` |
| **Teste rápido** | `make test` |
| **Vídeo específico** | `make run-custom VIDEO=meu_video.mp4` |
| **Webcam** | `make run-webcam` |
| **Salvar resultado** | `make run-save` |
| **Demonstração** | `make demo` |
| **Ver opções** | `make help` |

## 🚨 Solução de Problemas

| Erro | Solução |
|------|---------|
| Ambiente não encontrado | `./setup.sh` |
| Comando não funciona | `chmod +x setup.sh scripts/*.sh` |
| Modelo não encontrado | `make test` (baixa automaticamente) |
| Vídeo não encontrado | `make status` (ver vídeos disponíveis) |
| Webcam não funciona | Verificar se webcam está conectada |

## 📊 Saídas Esperadas

- **Terminal**: Progresso frame por frame
- **Janela de vídeo**: Detecções em tempo real
- **Pasta runs/**: Resultados salvos (se usar --save)
- **Log**: Número de veículos detectados

## 🎉 Fluxo Completo

```bash
# 1. Clone/baixe o projeto
git clone <repositorio>
cd projeto

# 2. Configure automaticamente
./setup.sh

# 3. Verifique se tudo está funcionando
make status
make test

# 4. Execute demonstração
make demo

# 5. Use o sistema
make run-video    # ou make run-webcam

# 6. Salve resultados (opcional)
make run-save
```

**Todas as opções estão funcionando perfeitamente! 🚀**