# Como Executar o Sistema de Rastreamento de Veículos

Este projeto implementa um sistema de rastreamento e contagem de veículos usando YOLO v8 e DeepSORT.

## 🚀 Configuração Inicial

### Opção 1: Script Automático (Recomendado)
```bash
./setup.sh
```

### Opção 2: Makefile
```bash
make setup
```

### Opção 3: Manual
```bash
# Ativa o ambiente virtual
source .venv/bin/activate

# Instala dependências
pip install torch torchvision opencv-python numpy matplotlib PyYAML tqdm pillow scipy easydict hydra-core
pip install -e .
```

## 📋 Comandos do Makefile

### Ver Ajuda
```bash
make help          # Mostra todos os comandos disponíveis
make status         # Mostra status do sistema
```

### Execução Principal
```bash
make run-video      # Executa detecção no vídeo padrão
make run-webcam     # Executa detecção na webcam
make run-save       # Executa detecção e salva resultado
make run-custom VIDEO=caminho/para/video.mp4  # Vídeo customizado
```

### Teste e Demonstração
```bash
make test           # Testa o sistema
make demo           # Executa demonstração completa (10 segundos)
make clean          # Remove arquivos temporários
```

## 🛠️ Scripts Shell

### Configuração
```bash
./setup.sh          # Configura todo o ambiente automaticamente
```

### Execução
```bash
# Detecção em vídeo
./scripts/run-video.sh                    # Vídeo padrão
./scripts/run-video.sh caminho/video.mp4  # Vídeo específico

# Detecção na webcam
./scripts/run-webcam.sh

# Salvar resultado
./scripts/run-save.sh                     # Processa e salva vídeo padrão
./scripts/run-save.sh caminho/video.mp4   # Processa e salva vídeo específico

# Demonstração completa
./scripts/run-demo.sh                     # Demo automática com status
```

## 🎯 Execução Rápida (Método Antigo)

```bash
# Ativa o ambiente virtual
source .venv/bin/activate

# Executa com webcam
python simple_detection.py

# Executa com arquivo de vídeo
python detect_vehicles.py --source videos/video_1.mp4 --show

# Executa e salva o resultado
python detect_vehicles.py --source videos/video_1.mp4 --save
```

## 🎪 Fluxo Completo Recomendado

```bash
# 1. Configuração (uma vez apenas)
./setup.sh

# 2. Verificar sistema
make status

# 3. Testar rapidamente
make demo

# 4. Executar detecção
make run-video    # ou make run-webcam

# 5. Salvar resultado (opcional)
make run-save
```

## 🛠️ Configuração do Ambiente

O ambiente já foi configurado com:
- Python 3.8.10
- PyTorch + Torchvision
- OpenCV
- Ultralytics YOLO v8
- Todas as dependências necessárias

## 📝 Parâmetros Disponíveis

### run_vehicle_tracking.py
- `--source`: Fonte do vídeo (0=webcam, arquivo, URL)
- `--model`: Modelo YOLO (yolov8n.pt, yolov8s.pt, etc.)
- `--conf`: Confiança mínima (0.0-1.0)
- `--save`: Salvar vídeo de saída
- `--show`: Mostrar vídeo em tempo real
- `--device`: Dispositivo (cpu, 0, 1, cuda)

## 🎯 Classes de Veículos (COCO Dataset)
- 2: car
- 3: motorcycle  
- 5: bus
- 7: truck

## 🔧 Solução de Problemas

Se houver erros:
1. Certifique-se que a webcam está conectada
2. Verifique se o ambiente virtual está ativado
3. Execute: `pip install -r requirements.txt`
4. Para CPU apenas: adicione `--device cpu`

## 📊 Recursos Implementados
- ✅ Detecção de veículos em tempo real
- ✅ Interface simplificada
- ✅ Suporte a webcam e arquivos de vídeo
- ⚠️ Rastreamento (DeepSORT) - em desenvolvimento
- ⚠️ Contagem de veículos - em desenvolvimento
- ⚠️ Estimação de velocidade - em desenvolvimento

Para usar o sistema completo com rastreamento, alguns ajustes ainda são necessários no código do DeepSORT.