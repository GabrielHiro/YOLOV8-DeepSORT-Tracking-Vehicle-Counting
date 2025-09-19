#!/usr/bin/env python3
"""
Script simplificado e robusto para executar detecção de veículos usando YOLO v8
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
    parser = argparse.ArgumentParser(description='Sistema de Detecção de Veículos YOLO v8')
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
    
    print("🚗 Sistema de Detecção de Veículos YOLO v8")
    print(f"📹 Fonte: {args.source}")
    print(f"🤖 Modelo: {args.model}")
    print(f"🎯 Confiança: {args.conf}")
    print("🚀 Iniciando detecção...")
    
    try:
        from ultralytics import YOLO
        
        # Carrega o modelo
        model = YOLO(args.model)
        
        # Configurações para a predição
        predict_args = {
            'source': args.source,
            'conf': args.conf,
            'show': args.show,
            'save': args.save,
            'verbose': True
        }
        
        # Adiciona device se especificado
        if args.device:
            predict_args['device'] = args.device
            
        # Executa a predição
        results = model.predict(**predict_args)
        
        print("✅ Detecção concluída!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Interrompido pelo usuário")
    except FileNotFoundError as e:
        print(f"❌ Arquivo não encontrado: {args.source}")
        print("💡 Verifique se o caminho do arquivo está correto")
        return 1
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\nℹ️  Dicas para solucionar:")
        print(f"   - Verifique se o arquivo existe: {args.source}")
        print("   - Certifique-se que o modelo está correto")
        print("   - Tente usar --device cpu se houver problemas de GPU")
        print("   - Para webcam, use --source 0")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())