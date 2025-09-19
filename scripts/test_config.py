#!/usr/bin/env python3
"""
Script para testar a configuração de contagem
"""

import sys
import os

# Adicionar o diretório config ao path
config_path = os.path.join(os.path.dirname(__file__), '..', 'config')
sys.path.append(config_path)

def test_config():
    """Testar se a configuração está válida"""
    try:
        from counting_config import *
        
        print("✅ Configuração carregada com sucesso!")
        print("\n📋 Configuração atual:")
        print(f"  • Linha de contagem: {COUNTING_LINE}")
        print(f"  • ROI habilitado: {ENABLE_ROI}")
        if ENABLE_ROI:
            print(f"  • Área ROI: {ROI_AREA}")
        print(f"  • Classes de veículos: {VEHICLE_CLASSES}")
        print(f"  • Confiança mínima: {MIN_CONFIDENCE}")
        print(f"  • Direção de contagem: {COUNTING_DIRECTION}")
        print(f"  • Pixels por metro: {PIXELS_PER_METER}")
        
        # Validar configuração
        errors = []
        
        if len(COUNTING_LINE) != 2:
            errors.append("COUNTING_LINE deve ter exatamente 2 pontos")
        
        if ENABLE_ROI and len(ROI_AREA) != 2:
            errors.append("ROI_AREA deve ter exatamente 2 pontos")
        
        if MIN_CONFIDENCE < 0 or MIN_CONFIDENCE > 1:
            errors.append("MIN_CONFIDENCE deve estar entre 0 e 1")
        
        if COUNTING_DIRECTION not in ['up', 'down', 'both']:
            errors.append("COUNTING_DIRECTION deve ser 'up', 'down' ou 'both'")
        
        if not VEHICLE_CLASSES:
            errors.append("VEHICLE_CLASSES não pode estar vazio")
        
        if errors:
            print("\n❌ Erros na configuração:")
            for error in errors:
                print(f"  • {error}")
            return False
        else:
            print("\n✅ Configuração válida!")
            return True
            
    except ImportError as e:
        print(f"❌ Erro ao importar configuração: {e}")
        print("💡 Execute: make configure-line")
        return False
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

if __name__ == "__main__":
    success = test_config()
    sys.exit(0 if success else 1)