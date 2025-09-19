#!/usr/bin/env python3
"""
Script para executar o sistema de rastreamento e contagem de veículos usando YOLO v8 + DeepSORT
"""

import os
import sys
import argparse
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

def main():
    parser = argparse.ArgumentParser(description='Sistema de Rastreamento e Contagem de Veículos')
    parser.add_argument('--source', type=str, default='0', 
                       help='Fonte do vídeo (webcam=0, arquivo de vídeo ou URL)')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                       help='Modelo YOLO para detecção')
    parser.add_argument('--conf', type=float, default=0.5,
                       help='Confiança mínima para detecção')
    parser.add_argument('--save', action='store_true',
                       help='Salvar vídeo de saída')
    parser.add_argument('--show', action='store_true', default=True,
                       help='Mostrar vídeo em tempo real')
    parser.add_argument('--device', type=str, default='',
                       help='Dispositivo (cpu, 0, 1, ...)')
    
    args = parser.parse_args()
    
    # Configurar ambiente
    os.environ['PYTHONPATH'] = str(ROOT)
    
    print("🚗 Iniciando Sistema de Rastreamento de Veículos...")
    print(f"📹 Fonte: {args.source}")
    print(f"🤖 Modelo: {args.model}")
    print(f"🎯 Confiança: {args.conf}")
    
    try:
        # Usar a API simples do YOLO
        from ultralytics import YOLO
        
        print("🚀 Carregando modelo...")
        model = YOLO(args.model)
        
        print("🚀 Iniciando detecção...")
        results = model.predict(
            source=args.source,
            conf=args.conf,
            save=args.save,
            show=args.show,
            device=args.device,
            verbose=True
        )
        
        # Processar resultados
        if hasattr(results, '__iter__'):
            # Para múltiplos resultados (vídeo)
            for r in results:
                if r.boxes is not None:
                    # Filtrar apenas veículos (classes COCO: 2=car, 3=motorcycle, 5=bus, 7=truck)
                    vehicle_classes = [2, 3, 5, 7]
                    vehicle_detections = [box for box in r.boxes if int(box.cls) in vehicle_classes]
                    
                    if vehicle_detections:
                        print(f"🚗 Veículos detectados: {len(vehicle_detections)}")
        else:
            # Para resultado único
            if results.boxes is not None:
                vehicle_classes = [2, 3, 5, 7]
                vehicle_detections = [box for box in results.boxes if int(box.cls) in vehicle_classes]
                
                if vehicle_detections:
                    print(f"🚗 Veículos detectados: {len(vehicle_detections)}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\nℹ️  Dicas para solucionar:")
        print(f"   - Verifique se o arquivo existe: {args.source}")
        print("   - Certifique-se que o modelo está correto")
        print("   - Tente usar --device cpu se houver problemas de GPU")
        return 1
    
    print("✅ Finalizado!")
    return 0

if __name__ == '__main__':
    sys.exit(main())