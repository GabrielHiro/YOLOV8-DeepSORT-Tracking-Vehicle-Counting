# Configuração de Linha de Contagem e ROI

Este sistema permite configurar facilmente onde contar veículos e qual área analisar.

## 🎯 Como Configurar a Linha de Contagem

### Método 1: Configuração Visual (Recomendado)

Execute o configurador visual interativo:

```bash
make configure-line
```

Ou diretamente:

```bash
python scripts/configure_line.py
```

**Instruções:**
1. Escolha usar webcam (1) ou arquivo de vídeo (2)
2. Clique em dois pontos para definir a **linha de contagem** (verde)
3. Clique em dois pontos para definir a **ROI** (área de interesse - ciano)
4. Pressione **'s'** para salvar
5. Pressione **'r'** para resetar
6. Pressione **ESC** para sair

### Método 2: Edição Manual

Edite o arquivo de configuração diretamente:

```bash
make edit-config
```

Ou abra o arquivo:
```bash
nano config/counting_config.py
```

## 📐 Parâmetros Principais

### Linha de Contagem
```python
COUNTING_LINE = [(100, 400), (1100, 400)]  # (x1,y1), (x2,y2)
```

### Área de Interesse (ROI)
```python
ROI_AREA = [(50, 100), (1200, 600)]  # Canto sup. esquerdo, inf. direito
ENABLE_ROI = True  # Habilitar/desabilitar ROI
```

### Classes de Veículos
```python
VEHICLE_CLASSES = [2, 3, 5, 7, 8]  # car, motorcycle, bus, truck, train
```

### Direção de Contagem
```python
COUNTING_DIRECTION = 'both'  # 'up', 'down', ou 'both'
```

## 🎨 Configurações Visuais

### Cores das Linhas
```python
LINE_COLOR = (0, 255, 0)      # Verde (BGR)
ROI_COLOR = (255, 255, 0)     # Ciano (BGR)
LINE_THICKNESS = 3
```

### Contadores na Tela
```python
SHOW_COUNTERS = True
COUNTER_POSITION = (20, 50)
```

## ⚙️ Configurações Avançadas

### Velocidade
```python
PIXELS_PER_METER = 8         # Ajustar conforme escala do vídeo
SPEED_TIME_WINDOW = 15       # Frames para cálculo de velocidade
```

### Detecção
```python
MIN_CONFIDENCE = 0.5         # Confiança mínima (0.0 - 1.0)
MIN_OBJECT_SIZE = (30, 30)   # Tamanho mínimo em pixels (largura, altura)
CROSSING_THRESHOLD = 10      # Threshold para cruzamento da linha
```

## 📋 Presets Pré-configurados

Use configurações otimizadas para diferentes cenários:

```python
ACTIVE_PRESET = 'highway'    # highway, city_street, parking_lot, train_station
```

### Presets Disponíveis:

1. **highway**: Rodovias e vias expressas
2. **city_street**: Ruas urbanas
3. **parking_lot**: Estacionamentos
4. **train_station**: Estações de trem

## 🧪 Testar Configuração

Verificar se a configuração está válida:

```bash
make show-config
```

Ou testar diretamente:
```bash
python scripts/test_config.py
```

## 🚀 Executar com Configuração

Depois de configurar, execute o sistema:

```bash
# Com webcam
make run-webcam

# Com vídeo
make run-video VIDEO=seu_video.mp4

# Com configuração personalizada
make run-config
```

## 💡 Dicas de Configuração

### Posicionamento da Linha
- **Horizontal**: Para contar veículos que se movem verticalmente
- **Vertical**: Para contar veículos que se movem horizontalmente
- **Diagonal**: Para vias em ângulo

### ROI (Área de Interesse)
- Use ROI para focar apenas na área relevante
- Remove bordas desnecessárias que podem gerar falsos positivos
- Melhora a performance ao processar menos pixels

### Ajuste de Escala
- `PIXELS_PER_METER`: Ajuste conforme a distância da câmera
- Mais próximo = mais pixels por metro
- Mais distante = menos pixels por metro

### Classes de Veículos (COCO Dataset IDs)
- `0`: pessoa
- `1`: bicicleta  
- `2`: carro
- `3`: motocicleta
- `5`: ônibus
- `7`: caminhão
- `8`: trem

## 🔧 Solução de Problemas

### Linha não aparece
- Verifique se `SHOW_COUNTERS = True`
- Verifique se as coordenadas estão dentro da resolução do vídeo

### Contagem imprecisa
- Ajuste `CROSSING_THRESHOLD`
- Verifique se a linha está perpendicular ao movimento
- Ajuste `MIN_CONFIDENCE` para filtrar detecções ruins

### Performance baixa
- Habilite ROI para processar menos área
- Use modelo menor (yolov8n.pt ao invés de yolov8l.pt)
- Reduza resolução do vídeo

## 📁 Estrutura de Arquivos

```
config/
  ├── counting_config.py     # Configuração principal
  └── presets/              # Configurações predefinidas
scripts/
  ├── configure_line.py     # Configurador visual
  └── test_config.py        # Teste de configuração
```

## 🔄 Backup e Restauração

Fazer backup da configuração:
```bash
make backup-config
```

Restaurar última configuração:
```bash
make restore-config
```