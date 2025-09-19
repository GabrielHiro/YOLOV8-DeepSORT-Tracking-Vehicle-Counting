#!/usr/bin/env python3
"""
Configurador Visual de Linha de Contagem
Permite configurar visualmente a linha de contagem e ROI usando o mouse
"""

import cv2
import numpy as np
import sys
import os

# Adicionar o diretório config ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

class LineConfigurator:
    def __init__(self, video_path=None):
        self.video_path = video_path
        self.cap = None
        self.frame = None
        self.original_frame = None
        
        # Pontos da linha de contagem
        self.line_points = []
        
        # Pontos da ROI
        self.roi_points = []
        
        # Estado da configuração
        self.configuring_line = True  # True para linha, False para ROI
        self.drawing = False
        
        # Cores
        self.line_color = (0, 255, 0)  # Verde
        self.roi_color = (255, 255, 0)  # Ciano
        self.temp_color = (0, 0, 255)  # Vermelho para linha temporária
        
        print("=== Configurador Visual de Linha de Contagem ===")
        print("Instruções:")
        print("1. Primeiro configure a LINHA DE CONTAGEM (verde)")
        print("   - Clique em dois pontos para definir a linha")
        print("2. Depois configure a ROI (área de interesse - ciano)")
        print("   - Clique em dois pontos: canto superior esquerdo e inferior direito")
        print("3. Pressione 's' para salvar as configurações")
        print("4. Pressione 'r' para resetar")
        print("5. Pressione 'ESC' para sair sem salvar")
        print("6. Pressione SPACE para alternar entre linha e ROI")
        print()

    def setup_video(self):
        """Configurar captura de vídeo"""
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                print(f"Erro: Não foi possível abrir o vídeo {self.video_path}")
                return False
        else:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Erro: Não foi possível abrir a webcam")
                return False
        
        # Capturar primeiro frame
        ret, frame = self.cap.read()
        if not ret:
            print("Erro: Não foi possível capturar frame")
            return False
            
        self.frame = frame.copy()
        self.original_frame = frame.copy()
        return True

    def mouse_callback(self, event, x, y, flags, param):
        """Callback para eventos do mouse"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.configuring_line:
                # Configurando linha de contagem
                self.line_points.append((x, y))
                
                if len(self.line_points) == 2:
                    print(f"Linha de contagem definida: {self.line_points}")
                    self.configuring_line = False
                    print("Agora configure a ROI (área de interesse)")
                    
            else:
                # Configurando ROI
                self.roi_points.append((x, y))
                
                if len(self.roi_points) == 2:
                    print(f"ROI definida: {self.roi_points}")

    def draw_current_config(self):
        """Desenhar configuração atual no frame"""
        self.frame = self.original_frame.copy()
        
        # Desenhar linha de contagem
        if len(self.line_points) >= 2:
            cv2.line(self.frame, self.line_points[0], self.line_points[1], 
                    self.line_color, 3)
            cv2.putText(self.frame, "LINHA DE CONTAGEM", 
                       (self.line_points[0][0], self.line_points[0][1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.line_color, 2)
        elif len(self.line_points) == 1:
            cv2.circle(self.frame, self.line_points[0], 5, self.temp_color, -1)
        
        # Desenhar ROI
        if len(self.roi_points) >= 2:
            cv2.rectangle(self.frame, self.roi_points[0], self.roi_points[1], 
                         self.roi_color, 2)
            cv2.putText(self.frame, "ROI", 
                       (self.roi_points[0][0], self.roi_points[0][1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.roi_color, 2)
        elif len(self.roi_points) == 1:
            cv2.circle(self.frame, self.roi_points[0], 5, self.temp_color, -1)
        
        # Mostrar instruções
        mode = "LINHA" if self.configuring_line else "ROI"
        cv2.putText(self.frame, f"Configurando: {mode}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.putText(self.frame, "S=Salvar | R=Reset | ESC=Sair | SPACE=Alternar", 
                   (10, self.frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 2)

    def save_config(self):
        """Salvar configuração no arquivo"""
        if len(self.line_points) < 2:
            print("Erro: Linha de contagem não foi definida completamente")
            return False
            
        if len(self.roi_points) < 2:
            print("Erro: ROI não foi definida completamente")
            return False
        
        # Garantir que ROI está no formato correto (superior esquerdo, inferior direito)
        roi_p1 = self.roi_points[0]
        roi_p2 = self.roi_points[1]
        
        roi_top_left = (min(roi_p1[0], roi_p2[0]), min(roi_p1[1], roi_p2[1]))
        roi_bottom_right = (max(roi_p1[0], roi_p2[0]), max(roi_p1[1], roi_p2[1]))
        
        config_content = f'''# Configuração gerada automaticamente pelo configurador visual
# Linha de contagem e ROI

# LINHA DE CONTAGEM
COUNTING_LINE = [{self.line_points[0]}, {self.line_points[1]}]

# ÁREA DE INTERESSE (ROI)
ROI_AREA = [{roi_top_left}, {roi_bottom_right}]
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

print(f"Configuração salva:")
print(f"Linha de contagem: {self.line_points}")
print(f"ROI: [{roi_top_left}, {roi_bottom_right}]")
'''
        
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'counting_config.py')
        
        try:
            with open(config_path, 'w') as f:
                f.write(config_content)
            print(f"Configuração salva em: {config_path}")
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False

    def reset_config(self):
        """Resetar configuração"""
        self.line_points = []
        self.roi_points = []
        self.configuring_line = True
        print("Configuração resetada. Configure novamente a linha de contagem.")

    def run(self):
        """Executar configurador"""
        if not self.setup_video():
            return False
        
        cv2.namedWindow('Configurador de Linha', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('Configurador de Linha', self.mouse_callback)
        
        while True:
            self.draw_current_config()
            cv2.imshow('Configurador de Linha', self.frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC
                print("Saindo sem salvar...")
                break
            elif key == ord('s') or key == ord('S'):
                if self.save_config():
                    print("Configuração salva com sucesso!")
                    break
            elif key == ord('r') or key == ord('R'):
                self.reset_config()
            elif key == ord(' '):  # SPACE
                self.configuring_line = not self.configuring_line
                mode = "LINHA" if self.configuring_line else "ROI"
                print(f"Alternado para modo: {mode}")
        
        cv2.destroyAllWindows()
        if self.cap:
            self.cap.release()
        
        return True

def main():
    """Função principal"""
    print("Configurador Visual de Linha de Contagem")
    print("Escolha uma opção:")
    print("1. Usar webcam")
    print("2. Usar arquivo de vídeo")
    
    choice = input("Digite sua escolha (1 ou 2): ").strip()
    
    if choice == '1':
        configurator = LineConfigurator()
    elif choice == '2':
        video_path = input("Digite o caminho do vídeo: ").strip()
        if not os.path.exists(video_path):
            print(f"Erro: Arquivo {video_path} não encontrado")
            return
        configurator = LineConfigurator(video_path)
    else:
        print("Opção inválida")
        return
    
    configurator.run()

if __name__ == "__main__":
    main()