#!/usr/bin/env python3
"""
Script simples com relatório de Ctrl+C
"""

import signal
import sys
import os
import time
from collections import defaultdict
from ultralytics import YOLO

# Carregar configurações
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

try:
    from counting_config import *
    print("✅ Configurações carregadas!")
    print(f"📍 Linha: {COUNTING_LINE}")
    print(f"🎯 ROI: {'Habilitado' if ENABLE_ROI else 'Desabilitado'}")
except ImportError:
    print("❌ Configure primeiro: make configure-line")
    sys.exit(1)

# Estatísticas globais
vehicle_count = 0
vehicle_by_class = defaultdict(int)
start_time = time.time()

def signal_handler(signum, frame):
    """Capturar Ctrl+C e mostrar relatório"""
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n\n🛑 INTERRUPÇÃO DETECTADA!")
    print("="*60)
    print("📊 RELATÓRIO FINAL DE DETECÇÃO")
    print("="*60)
    print(f"⏱️  Tempo de execução: {duration:.1f} segundos")
    print(f"🚗 TOTAL DE VEÍCULOS: {vehicle_count}")
    
    if vehicle_by_class:
        print("\n📋 Por tipo de veículo:")
        for vtype, count in vehicle_by_class.items():
            pct = (count/vehicle_count)*100 if vehicle_count > 0 else 0
            print(f"   🔸 {vtype}: {count} ({pct:.1f}%)")
    
    print(f"\n⚙️  Configurações:")
    print(f"   📍 Linha: {COUNTING_LINE}")
    print(f"   🎯 ROI: {'Sim' if ENABLE_ROI else 'Não'}")
    print(f"   🔍 Confiança: {MIN_CONFIDENCE}")
    print(f"   🚙 Classes: {VEHICLE_CLASSES}")
    print(f"\n⚠️  Interrompido pelo usuário")
    print("="*60)
    sys.exit(0)

def on_predict_end(predictor):
    """Callback chamado ao final de cada predição"""
    global vehicle_count, vehicle_by_class
    
    if hasattr(predictor, 'results') and predictor.results:
        for result in predictor.results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    if class_id in VEHICLE_CLASSES:
                        class_name = predictor.model.names[class_id]
                        vehicle_count += 1
                        vehicle_by_class[class_name] += 1
                        
                        # Log periodicamente
                        if vehicle_count % 10 == 0:
                            elapsed = time.time() - start_time
                            print(f"🚗 Veículos detectados: {vehicle_count} | Tempo: {elapsed:.1f}s")

def main():
    import argparse
    global vehicle_count, vehicle_by_class  # Declarar globais
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='videos/video_1.mp4')
    parser.add_argument('--model', default='yolov8n.pt')
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()
    
    # Configurar Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"🚀 Iniciando detecção com {args.model}")
    print("💡 Pressione Ctrl+C para parar e ver relatório")
    
    # Verificar se o source existe
    if args.source != '0' and not os.path.exists(args.source):
        print(f"❌ Arquivo não encontrado: {args.source}")
        return
    
    print(f"🎬 Processando: {args.source}")
    print("📊 Estatísticas em tempo real:")
    
    # Carregar modelo
    model = YOLO(args.model)
    
    try:
        # Executar predição com melhor controle
        frames_processed = 0
        results = model.predict(
            source=args.source,
            conf=MIN_CONFIDENCE,
            show=args.show,
            save=False,
            verbose=True
        )
        
        # Processar resultados
        for result in results:
            frames_processed += 1
            
            # Contar veículos no frame atual
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    if class_id in VEHICLE_CLASSES:
                        class_name = model.names[class_id]
                        vehicle_count += 1
                        vehicle_by_class[class_name] += 1
            
            # Log de progresso a cada 100 frames
            if frames_processed % 100 == 0:
                elapsed = time.time() - start_time
                fps = frames_processed / elapsed if elapsed > 0 else 0
                print(f"📊 Frame {frames_processed} | Veículos: {vehicle_count} | FPS: {fps:.1f}")
        
        # Relatório final (execução completa)
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL DE DETECÇÃO DE VEÍCULOS")
        print("="*60)
        print(f"⏱️  Tempo de execução: {duration:.1f} segundos")
        print(f"🎬 Frames processados: {frames_processed}")
        print(f"⚡ FPS médio: {frames_processed/duration:.1f}" if duration > 0 else "⚡ FPS médio: N/A")
        print(f"\n🚗 TOTAL DE VEÍCULOS DETECTADOS: {vehicle_count}")
        
        if vehicle_by_class:
            print("\n📋 Detalhamento por tipo de veículo:")
            for vtype, count in vehicle_by_class.items():
                pct = (count/vehicle_count)*100 if vehicle_count > 0 else 0
                print(f"   🔸 {vtype}: {count} veículos ({pct:.1f}%)")
        else:
            print("❌ Nenhum veículo detectado")
        
        print(f"\n⚙️  Configurações utilizadas:")
        print(f"   📍 Linha de contagem: {COUNTING_LINE}")
        print(f"   🎯 ROI: {'Habilitado' if ENABLE_ROI else 'Desabilitado'}")
        print(f"   🔍 Confiança mínima: {MIN_CONFIDENCE}")
        print(f"   🚙 Classes monitoradas: {VEHICLE_CLASSES}")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        import traceback
        print("🔍 Detalhes do erro:")
        traceback.print_exc()
        signal_handler(None, None)

if __name__ == "__main__":
    main()