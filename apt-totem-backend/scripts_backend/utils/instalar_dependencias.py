#!/usr/bin/env python3
"""
Script para instalar las dependencias faltantes
"""

import subprocess
import sys
import os

def instalar_dependencias():
    """Instalar las dependencias faltantes"""
    print("🔧 Instalando dependencias faltantes...")
    print("=" * 50)
    
    # Lista de dependencias que pueden estar faltando
    dependencias = [
        "sqlalchemy>=2.0,<3.0",
        "scikit-learn==1.6.1",
        "numpy==2.0.2",
        "opencv-python==4.12.0.88",
        "pillow==11.3.0",
        "fastapi>=0.110,<1.0",
        "uvicorn[standard]>=0.29,<1.0",
        "pydantic>=2,<3",
        "python-multipart>=0.0.9,<0.1.0",
        "alembic>=1.13,<2.0",
        "faster-whisper==1.0.3",
        "python-dotenv>=1.0,<2.0",
        "requests>=2.31,<3.0",
        "schedule>=1.2.0,<2.0"
    ]
    
    print("📦 Instalando dependencias...")
    
    for dep in dependencias:
        try:
            print(f"   Instalando {dep}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], capture_output=True, text=True, check=True)
            print(f"   ✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error instalando {dep}: {e}")
            print(f"   📝 Output: {e.stdout}")
            print(f"   📝 Error: {e.stderr}")
        except Exception as e:
            print(f"   ❌ Error inesperado con {dep}: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Verificando instalación...")
    
    # Verificar que las dependencias estén instaladas
    dependencias_verificar = [
        "sqlalchemy",
        "sklearn",
        "numpy",
        "cv2",
        "PIL",
        "fastapi",
        "uvicorn"
    ]
    
    for dep in dependencias_verificar:
        try:
            if dep == "cv2":
                import cv2
                print(f"   ✅ {dep} (OpenCV) disponible")
            elif dep == "PIL":
                from PIL import Image
                print(f"   ✅ {dep} (Pillow) disponible")
            elif dep == "sklearn":
                import sklearn
                print(f"   ✅ {dep} (scikit-learn) disponible")
            else:
                __import__(dep)
                print(f"   ✅ {dep} disponible")
        except ImportError:
            print(f"   ❌ {dep} NO disponible")
        except Exception as e:
            print(f"   ❌ Error verificando {dep}: {e}")
    
    print("\n🎉 Instalación completada!")
    print("\n📝 Para verificar que todo funciona:")
    print("   cd apt-totem-backend")
    print("   uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload")

if __name__ == "__main__":
    instalar_dependencias()

