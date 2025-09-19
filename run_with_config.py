#!/usr/bin/env python3
"""
Script para executar detecção com configuração personalizada de linha e ROI
"""

import argparse
import sys
import os
import cv2
import torch
import numpy as np
from pathlib import Path

# Adicionar ultralytics ao path
ultralytics_path = os.path.join(os.path.dirname(__file__), 'ultralytics')
if ultralytics_path not in sys.path:
    sys.path.append(ultralytics_path)

from ultralytics import YOLO

# Importar configurações
config_path = os.path.join(os.path.dirname(__file__), 'config')
if config_path not in sys.path:
    sys.path.append(config_path)

try:
    from counting_config import *
    print("✅ Configurações carregadas com sucesso!")
except ImportError:
    print("❌ Arquivo de configuração não encontrado. Use: make configure-line")
    sys.exit(1)

class VehicleCountingDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """Inicializar detector com configurações"""
        self.model = YOLO(model_path)
        self.vehicle_counts = {}
        self.tracked_objects = {}
        self.frame_count = 0
        
        print(f"📋 Configuração carregada:")
        print(f"  • Linha de contagem: {COUNTING_LINE}")
        print(f"  • ROI habilitado: {ENABLE_ROI}")
        if ENABLE_ROI:
            print(f"  • Área ROI: {ROI_AREA}")
        print(f"  • Classes: {VEHICLE_CLASSES}")
        print(f"  • Confiança mínima: {MIN_CONFIDENCE}")
        
    def is_in_roi(self, bbox):
        """Verificar se objeto está dentro da ROI"""
        if not ENABLE_ROI:
            return True
        
        center_x = int((bbox[0] + bbox[2]) / 2)
        center_y = int((bbox[1] + bbox[3]) / 2)
        
        return (ROI_AREA[0][0] <= center_x <= ROI_AREA[1][0] and 
                ROI_AREA[0][1] <= center_y <= ROI_AREA[1][1])
    
    def check_line_crossing(self, center_x, center_y, class_name):
        """Verificar se objeto cruzou a linha de contagem"""
        line_y = COUNTING_LINE[0][1]  # Assumindo linha horizontal
        
        # Verificar se está próximo da linha
        if abs(center_y - line_y) <= CROSSING_THRESHOLD:
            # Criar ID único baseado na posição (simplificado)
            object_id = f"{center_x}_{center_y}_{self.frame_count}"
            
            if object_id not in self.tracked_objects:
                self.tracked_objects[object_id] = True
                
                if class_name not in self.vehicle_counts:
                    self.vehicle_counts[class_name] = 0
                
                self.vehicle_counts[class_name] += 1
                print(f"🚗 {class_name} detectado - Total: {self.vehicle_counts[class_name]}")
    
    def draw_interface(self, frame):
        """Desenhar linha de contagem, ROI e contadores"""
        # Desenhar ROI
        if ENABLE_ROI:
            cv2.rectangle(frame, ROI_AREA[0], ROI_AREA[1], ROI_COLOR, 2)
            cv2.putText(frame, "ROI", (ROI_AREA[0][0], ROI_AREA[0][1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, ROI_COLOR, 2)
        
        # Desenhar linha de contagem
        cv2.line(frame, COUNTING_LINE[0], COUNTING_LINE[1], LINE_COLOR, LINE_THICKNESS)
        cv2.putText(frame, "LINHA DE CONTAGEM", 
                   (COUNTING_LINE[0][0], COUNTING_LINE[0][1] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, LINE_COLOR, 2)
        
        # Desenhar contadores
        if SHOW_COUNTERS and self.vehicle_counts:
            # Fundo para contadores
            max_width = max([len(f"{k}: {v}") for k, v in self.vehicle_counts.items()]) * 12
            height = 40 + len(self.vehicle_counts) * 30
            cv2.rectangle(frame, (10, 10), (max_width + 20, height), (0, 0, 0), -1)
            
            # Título
            cv2.putText(frame, "CONTAGEM DE VEICULOS", (15, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Contadores por classe
            y_offset = 60
            for idx, (class_name, count) in enumerate(self.vehicle_counts.items()):
                text = f"{class_name}: {count}"
                cv2.putText(frame, text, (15, y_offset + idx * 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def process_frame(self, frame):
        """Processar um frame"""
        self.frame_count += 1
        
        # Criar uma cópia do frame para processamento
        result_frame = frame.copy()
        
        # Fazer predição - passar apenas o frame sem usar o método predict do modelo
        results = self.model.predict(source=frame, conf=MIN_CONFIDENCE, verbose=False, save=False, show=False)
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Extrair informações da detecção
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].cpu().numpy()
                    
                    # Verificar se é uma classe de veículo
                    if class_id in VEHICLE_CLASSES:
                        class_name = self.model.names[class_id]
                        
                        # Verificar se está na ROI
                        if self.is_in_roi(bbox):
                            # Verificar tamanho mínimo
                            width = bbox[2] - bbox[0]
                            height = bbox[3] - bbox[1]
                            
                            if width >= MIN_OBJECT_SIZE[0] and height >= MIN_OBJECT_SIZE[1]:
                                # Desenhar detecção
                                cv2.rectangle(result_frame, 
                                            (int(bbox[0]), int(bbox[1])),
                                            (int(bbox[2]), int(bbox[3])),
                                            (0, 255, 0), 2)
                                
                                # Label
                                label = f'{class_name} {confidence:.2f}'
                                cv2.putText(result_frame, label, 
                                          (int(bbox[0]), int(bbox[1] - 10)),
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                
                                # Verificar cruzamento da linha
                                center_x = int((bbox[0] + bbox[2]) / 2)
                                center_y = int((bbox[1] + bbox[3]) / 2)
                                self.check_line_crossing(center_x, center_y, class_name)
        
        # Desenhar interface
        result_frame = self.draw_interface(result_frame)
        return result_frame
    
    def run(self, source, show=False, save=False, output_path='output.mp4'):
        """Executar detecção"""
        print(f"🎬 Iniciando detecção em: {source}")
        
        # Configurar captura
        if source == '0' or source == 0:
            cap = cv2.VideoCapture(0)
            print("📹 Usando webcam")
        else:
            cap = cv2.VideoCapture(source)
            print(f"📁 Usando arquivo: {source}")
        
        if not cap.isOpened():
            print(f"❌ Erro ao abrir fonte: {source}")
            return
        
        # Configurar gravação se necessário
        writer = None
        if save:
            fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"💾 Salvando em: {output_path}")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Processar frame
                processed_frame = self.process_frame(frame)
                
                # Mostrar se solicitado
                if show:
                    cv2.imshow('Vehicle Counting', processed_frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q') or key == 27:  # 'q' ou ESC
                        break
                
                # Salvar se solicitado
                if writer:
                    writer.write(processed_frame)
        
        except KeyboardInterrupt:
            print("\n⏹️ Interrompido pelo usuário")
        
        finally:
            # Limpar recursos
            cap.release()
            if writer:
                writer.release()
            if show:
                cv2.destroyAllWindows()
            
            # Mostrar estatísticas finais
            print("\n📊 Estatísticas finais:")
            total = sum(self.vehicle_counts.values())
            print(f"  • Total de veículos: {total}")
            for class_name, count in self.vehicle_counts.items():
                print(f"  • {class_name}: {count}")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Detecção de veículos com linha de contagem configurável')
    parser.add_argument('--source', default='0', help='Fonte de vídeo (webcam=0, ou caminho do arquivo)')
    parser.add_argument('--model', default='yolov8n.pt', help='Modelo YOLO a usar')
    parser.add_argument('--show', action='store_true', help='Mostrar vídeo durante processamento')
    parser.add_argument('--save', action='store_true', help='Salvar vídeo processado')
    parser.add_argument('--output', default='output.mp4', help='Caminho para salvar vídeo')
    
    args = parser.parse_args()
    
    # Criar detector
    detector = VehicleCountingDetector(args.model)
    
    # Executar
    detector.run(
        source=args.source,
        show=args.show,
        save=args.save,
        output_path=args.output
    )

if __name__ == "__main__":
    main()