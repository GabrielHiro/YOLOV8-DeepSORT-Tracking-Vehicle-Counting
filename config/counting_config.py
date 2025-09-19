# Configuração gerada automaticamente pelo configurador visual
# Linha de contagem e ROI

# LINHA DE CONTAGEM
COUNTING_LINE = [(1386, 902), (2746, 933)]

# ÁREA DE INTERESSE (ROI)
ROI_AREA = [(782, 439), (2923, 2149)]
ENABLE_ROI = True

# Configurações padrão
CROSSING_THRESHOLD = 10
COUNTING_DIRECTION = 'both'
VEHICLE_CLASSES = [2, 3, 5, 7, 8]  # car, motorcycle, bus, truck, train

# Cores das linhas (BGR format)
LINE_COLOR = (0, 255, 0)
ROI_COLOR = (255, 255, 0)
LINE_THICKNESS = 3

# Configuração visual
SHOW_COUNTERS = True
COUNTER_POSITION = (20, 50)

# Configuração de velocidade
PIXELS_PER_METER = 8
SPEED_TIME_WINDOW = 15

# Configurações de detecção
MIN_CONFIDENCE = 0.5
MIN_OBJECT_SIZE = (30, 30)
TRACKING_BUFFER = 30
