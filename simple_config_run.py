#!/usr/bin/env python3
"""
Script simples para execução com configuração de linha de contagem
"""

import argparse
import cv2
from ultralytics import YOLO
import sys
import os

# Importar configurações
config_path = os.path.join(os.path.dirname(__file__), 'config')
sys.path.append(config_path)

try:
    from counting_config import *
    print("✅ Configurações carregadas!")
    print(f"📍 Linha: {COUNTING_LINE}")
    print(f"🎯 ROI: {'Habilitado' if ENABLE_ROI else 'Desabilitado'}")
except ImportError:
    print("❌ Configure primeiro: make configure-line")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='0', help='Fonte (webcam=0 ou arquivo)')
    parser.add_argument('--model', default='yolov8n.pt', help='Modelo YOLO')
    parser.add_argument('--show', action='store_true', help='Mostrar vídeo')
    args = parser.parse_args()
    
    print(f"🚀 Iniciando detecção com {args.model}")
    
    # Carregar modelo
    model = YOLO(args.model)
    
    # Contador simples
    vehicle_count = 0
    
    # Executar predição com as configurações
    results = model.predict(
        source=args.source,
        conf=MIN_CONFIDENCE,
        show=args.show,
        save=False,
        verbose=True
    )
    
    print("🎬 Processando vídeo...")
    
    try:
        for result in results:
            # Contar veículos detectados
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    if class_id in VEHICLE_CLASSES:
                        vehicle_count += 1
                        class_name = model.names[class_id]
                        conf = float(box.conf[0])
                        print(f"🚗 {class_name} detectado (conf: {conf:.2f}) - Total: {vehicle_count}")
    
    except KeyboardInterrupt:
        print("\n⏹️ Interrompido")
    
    print(f"\n📊 Total de veículos detectados: {vehicle_count}")

if __name__ == "__main__":
    main()