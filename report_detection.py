#!/usr/bin/env python3
"""
Script com relatório para detecção de veículos
"""

import argparse
import signal
import sys
import os
import time
from collections import defaultdict
from ultralytics import YOLO

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

# Variáveis globais para estatísticas
stats = {
    'total_vehicles': 0,
    'vehicles_by_class': defaultdict(int),
    'start_time': None,
    'frames_processed': 0,
    'interrupted': False
}

def signal_handler(signum, frame):
    """Handler para capturar Ctrl+C e gerar relatório"""
    print("\n\n🛑 INTERRUPÇÃO DETECTADA!")
    stats['interrupted'] = True
    generate_report()
    sys.exit(0)

def generate_report():
    """Gerar relatório final de detecções"""
    end_time = time.time()
    duration = end_time - stats['start_time'] if stats['start_time'] else 0
    
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL DE DETECÇÃO DE VEÍCULOS")
    print("="*60)
    
    print(f"⏱️  Tempo de execução: {duration:.1f} segundos")
    print(f"🎬 Frames processados: {stats['frames_processed']}")
    if duration > 0:
        fps = stats['frames_processed'] / duration
        print(f"⚡ FPS médio: {fps:.1f}")
    
    print(f"\n🚗 TOTAL DE VEÍCULOS DETECTADOS: {stats['total_vehicles']}")
    
    if stats['vehicles_by_class']:
        print("\n📋 Detalhamento por classe:")
        for class_name, count in sorted(stats['vehicles_by_class'].items()):
            percentage = (count / stats['total_vehicles']) * 100 if stats['total_vehicles'] > 0 else 0
            print(f"   🔸 {class_name}: {count} ({percentage:.1f}%)")
    else:
        print("❌ Nenhum veículo detectado")
    
    print(f"\n⚙️  Configurações utilizadas:")
    print(f"   📍 Linha de contagem: {COUNTING_LINE}")
    print(f"   🎯 ROI: {'Habilitado' if ENABLE_ROI else 'Desabilitado'}")
    print(f"   🔍 Confiança mínima: {MIN_CONFIDENCE}")
    print(f"   🚙 Classes monitoradas: {VEHICLE_CLASSES}")
    
    if stats['interrupted']:
        print(f"\n⚠️  Execução interrompida pelo usuário (Ctrl+C)")
    else:
        print(f"\n✅ Execução concluída normalmente")
    
    print("="*60)

class VehicleCounter:
    """Contador personalizado para acompanhar as predições"""
    
    def __init__(self, model):
        self.model = model
        
    def __call__(self, im, augment=False, visualize=False, val=False):
        """Interceptar predições para contar"""
        # Fazer predição normal
        results = self.model.predictor(im, augment, visualize, val)
        
        # Contar veículos
        for result in results:
            stats['frames_processed'] += 1
            
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    if class_id in VEHICLE_CLASSES:
                        class_name = self.model.names[class_id]
                        conf = float(box.conf[0])
                        
                        # Incrementar contadores
                        stats['total_vehicles'] += 1
                        stats['vehicles_by_class'][class_name] += 1
            
            # Mostrar estatísticas a cada 30 frames
            if stats['frames_processed'] % 30 == 0:
                elapsed = time.time() - stats['start_time']
                fps = stats['frames_processed'] / elapsed if elapsed > 0 else 0
                print(f"Frame {stats['frames_processed']:5d} | "
                      f"Veículos: {stats['total_vehicles']:4d} | "
                      f"FPS: {fps:5.1f} | "
                      f"Tempo: {elapsed:6.1f}s")
        
        return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='0', help='Fonte (webcam=0 ou arquivo)')
    parser.add_argument('--model', default='yolov8n.pt', help='Modelo YOLO')
    parser.add_argument('--show', action='store_true', help='Mostrar vídeo')
    args = parser.parse_args()
    
    # Configurar handler para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"🚀 Iniciando detecção com {args.model}")
    print("💡 Pressione Ctrl+C para parar e ver relatório")
    
    # Carregar modelo
    model = YOLO(args.model)
    
    # Inicializar estatísticas
    stats['start_time'] = time.time()
    
    print("🎬 Processando vídeo...")
    print("📊 Estatísticas em tempo real:")
    
    try:
        # Usar predict com callback customizado
        # Substituir o método predict temporariamente
        original_predictor = model.predictor
        model.predictor = VehicleCounter(model)
        
        # Executar predição
        results = model.predict(
            source=args.source,
            conf=MIN_CONFIDENCE,
            show=args.show,
            save=False,
            verbose=False
        )
        
        # Restaurar predictor original
        model.predictor = original_predictor
    
    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C detectado!")
        stats['interrupted'] = True
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        stats['interrupted'] = True
    
    finally:
        # Sempre gerar relatório no final
        generate_report()

if __name__ == "__main__":
    main()