#!/usr/bin/env python3
"""
Script simplificado para executar detecção de veículos usando YOLO v8
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

def main():
    try:
        # Comando simples para detecção usando YOLO
        print("🚗 Executando detecção de veículos com YOLO v8...")
        print("📹 Fonte: webcam (pressione 'q' para sair)")
        
        from ultralytics import YOLO
        
        # Carrega o modelo
        model = YOLO('yolov8n.pt')
        
        # Executa detecção em tempo real
        results = model.predict(
            source=0,  # webcam
            show=True,  # mostra video
            conf=0.5,   # confiança mínima
            save=False,
            verbose=True,
            stream=True  # modo streaming
        )
        
        # Processa resultados
        for r in results:
            # Filtra apenas veículos (classes 2,3,5,7 do COCO)
            vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
            if r.boxes is not None:
                # Conta veículos detectados
                vehicle_count = sum(1 for cls in r.boxes.cls if int(cls) in vehicle_classes)
                if vehicle_count > 0:
                    print(f"🚗 Veículos detectados: {vehicle_count}")
            
            # Pressione 'q' para sair (na janela de vídeo)
        
    except KeyboardInterrupt:
        print("\n⏹️  Interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\nℹ️  Certifique-se de que:")
        print("   - Uma webcam está conectada")
        print("   - O ambiente virtual está ativado")
        print("   - As dependências estão instaladas")
        return 1
    
    print("✅ Finalizado!")
    return 0

if __name__ == '__main__':
    sys.exit(main())