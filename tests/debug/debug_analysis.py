#!/usr/bin/env python3
"""
Debugger para ver el análisis de imágenes en tiempo real
"""
import sys
import os
import cv2
import numpy as np
from PIL import Image
import json
from datetime import datetime

# Agregar el path del backend
sys.path.append('/Users/julimart/Desktop/apt-totem/apt-totem-backend')

# Importar los servicios de análisis
from services.ai.real_detection import analyze_real_clothing
from services.ai.yolo_clothing_detector import YOLOClothingDetector
from services.cv.color import get_dominant_colors
from services.nlu.heuristics import extract_intent_advanced

class AnalysisDebugger:
    def __init__(self):
        self.detector = YOLOClothingDetector()
        self.analysis_count = 0
        
    def debug_analysis(self, image_path=None, image_data=None):
        """Debuggear el análisis de una imagen"""
        self.analysis_count += 1
        print(f"\n🔍 === ANÁLISIS #{self.analysis_count} - {datetime.now().strftime('%H:%M:%S')} ===")
        
        try:
            # Cargar imagen
            if image_path:
                print(f"📸 Cargando imagen: {image_path}")
                image = cv2.imread(image_path)
                if image is None:
                    print("❌ Error: No se pudo cargar la imagen")
                    return
            elif image_data is not None:
                print("📸 Procesando imagen desde datos")
                # Convertir bytes a imagen
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                print("❌ Error: No se proporcionó imagen")
                return
            
            print(f"📏 Dimensiones: {image.shape}")
            
            # 1. Análisis de detección de ropa
            print("\n👕 === DETECCIÓN DE ROPA ===")
            try:
                detections = self.detector.detect_clothing(image)
                print(f"🎯 Detecciones encontradas: {len(detections)}")
                
                for i, detection in enumerate(detections):
                    print(f"  {i+1}. {detection['class']} (confianza: {detection['confidence']:.2f})")
                    print(f"     Posición: {detection['bbox']}")
                    
                    # Análisis de color para cada detección
                    if 'color' in detection:
                        print(f"     Color detectado: {detection['color']}")
                        
            except Exception as e:
                print(f"❌ Error en detección: {e}")
            
            # 2. Análisis de colores dominantes
            print("\n🎨 === ANÁLISIS DE COLORES ===")
            try:
                dominant_colors = get_dominant_colors(image, k=5)
                print(f"🌈 Colores dominantes: {dominant_colors}")
                
                # Mostrar colores en RGB
                for i, color in enumerate(dominant_colors):
                    rgb = color['rgb']
                    name = color.get('name', 'Sin nombre')
                    print(f"  {i+1}. RGB({rgb[0]}, {rgb[1]}, {rgb[2]}) - {name}")
                    
            except Exception as e:
                print(f"❌ Error en análisis de colores: {e}")
            
            # 3. Análisis completo con MediaPipe
            print("\n🤖 === ANÁLISIS COMPLETO ===")
            try:
                result = analyze_real_clothing(image)
                print(f"📊 Resultado del análisis:")
                print(f"   Detecciones: {result.get('detections', [])}")
                print(f"   Colores: {result.get('colors', [])}")
                print(f"   Tiempo: {result.get('processing_time', 0):.2f}ms")
                
                # Mostrar detalles de cada detección
                for detection in result.get('detections', []):
                    print(f"   - {detection.get('item', 'N/A')}: {detection.get('confidence', 0):.2f}")
                    if 'color' in detection:
                        print(f"     Color: {detection['color']}")
                        
            except Exception as e:
                print(f"❌ Error en análisis completo: {e}")
            
            # 4. Análisis de texto (si hay transcripción)
            print("\n🗣️ === ANÁLISIS DE TEXTO ===")
            sample_texts = [
                "busco zapatillas nike",
                "quiero una camiseta azul",
                "necesito pantalones negros",
                "tienes chaquetas deportivas"
            ]
            
            for text in sample_texts:
                try:
                    intent, slots = extract_intent_advanced(text)
                    print(f"   Texto: '{text}'")
                    print(f"   Intención: {intent}")
                    print(f"   Slots: {slots}")
                except Exception as e:
                    print(f"   Error analizando '{text}': {e}")
            
            print(f"\n✅ Análisis completado en {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"❌ Error general: {e}")
            import traceback
            traceback.print_exc()

def create_test_image():
    """Crear una imagen de prueba para debuggear"""
    # Crear una imagen simple con colores
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    
    # Fondo azul
    img[:] = (100, 150, 200)
    
    # Rectángulo rojo (simulando ropa)
    cv2.rectangle(img, (100, 100), (300, 300), (0, 0, 255), -1)
    
    # Texto
    cv2.putText(img, "TEST IMAGE", (120, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Guardar imagen de prueba
    test_path = "/Users/julimart/Desktop/apt-totem/test_debug_image.jpg"
    cv2.imwrite(test_path, img)
    print(f"📸 Imagen de prueba creada: {test_path}")
    
    return test_path

def main():
    print("🐛 DEBUGGER DE ANÁLISIS DE IMÁGENES")
    print("=" * 50)
    
    debugger = AnalysisDebugger()
    
    # Crear imagen de prueba
    test_image_path = create_test_image()
    
    # Analizar imagen de prueba
    debugger.debug_analysis(test_image_path)
    
    print("\n🎯 Para debuggear en tiempo real:")
    print("1. Coloca una imagen en el directorio")
    print("2. Ejecuta: python3 debug_analysis.py <ruta_imagen>")
    print("3. O usa el debugger interactivo")
    
    # Si se proporciona una imagen como argumento
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            print(f"\n🔍 Analizando imagen: {image_path}")
            debugger.debug_analysis(image_path)
        else:
            print(f"❌ Imagen no encontrada: {image_path}")

if __name__ == "__main__":
    main()
