#!/usr/bin/env python3
"""
Debugger integrado con el backend para ver análisis en tiempo real
"""
import sys
import os
import json
import time
from datetime import datetime

# Agregar el path del backend
sys.path.append('/Users/julimart/Desktop/apt-totem/apt-totem-backend')

def debug_backend_analysis():
    """Debuggear el análisis del backend en tiempo real"""
    print("🐛 DEBUGGER DEL BACKEND - ANÁLISIS EN TIEMPO REAL")
    print("=" * 60)
    print("📡 Monitoreando análisis del backend...")
    print("📋 Presiona Ctrl+C para salir")
    
    try:
        # Importar los servicios del backend
        from services.ai.real_detection import analyze_real_clothing
        from services.ai.yolo_clothing_detector import YOLOClothingDetector
        from services.nlu.heuristics import extract_intent_advanced
        from services.cv.detector import analyze_image
        
        print("✅ Servicios del backend cargados correctamente")
        
        # Inicializar detector
        detector = YOLOClothingDetector()
        print("✅ Detector YOLO inicializado")
        
        analysis_count = 0
        
        while True:
            print(f"\n🔍 === ESPERANDO ANÁLISIS #{analysis_count + 1} ===")
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
            print("📋 El backend está analizando...")
            
            # Simular análisis (en realidad esto se ejecutaría cuando llegue una imagen)
            time.sleep(2)
            
            # Aquí podrías interceptar las llamadas reales del backend
            # Por ahora, mostramos información del estado
            
            analysis_count += 1
            print(f"✅ Análisis #{analysis_count} completado")
            
            # Mostrar estadísticas del detector
            print(f"📊 Estado del detector:")
            print(f"   - Modelo cargado: {'✅' if hasattr(detector, 'model') else '❌'}")
            print(f"   - Clases disponibles: {len(detector.classes) if hasattr(detector, 'classes') else 'N/A'}")
            
            # Simular análisis de texto
            sample_texts = [
                "busco zapatillas nike",
                "quiero una camiseta azul", 
                "necesito pantalones negros"
            ]
            
            for text in sample_texts:
                try:
                    intent, slots = extract_intent_advanced(text)
                    print(f"🗣️ Texto: '{text}' → Intención: {intent}, Slots: {slots}")
                except Exception as e:
                    print(f"❌ Error analizando '{text}': {e}")
            
            print(f"⏳ Esperando siguiente análisis...")
            time.sleep(5)  # Esperar 5 segundos entre análisis
            
    except KeyboardInterrupt:
        print(f"\n👋 Debugger interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error en debugger: {e}")
        import traceback
        traceback.print_exc()

def debug_api_endpoints():
    """Debuggear los endpoints de la API"""
    print("🐛 DEBUGGER DE ENDPOINTS DE LA API")
    print("=" * 50)
    
    import requests
    
    base_url = "http://127.0.0.1:8000"
    
    endpoints = [
        "/docs",
        "/busqueda/health",
        "/recomendaciones/health", 
        "/analytics/health",
        "/cv/health"
    ]
    
    print(f"🔍 Verificando endpoints en {base_url}")
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK ({response.status_code})")
            else:
                print(f"⚠️ {endpoint} - {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    print(f"\n📊 Resumen de endpoints verificados")

def debug_database_queries():
    """Debuggear las consultas a la base de datos"""
    print("🐛 DEBUGGER DE CONSULTAS A LA BASE DE DATOS")
    print("=" * 50)
    
    try:
        import sqlite3
        
        db_path = "/Users/julimart/Desktop/apt-totem/apt-totem-backend/neototem.db"
        
        if not os.path.exists(db_path):
            print(f"❌ Base de datos no encontrada: {db_path}")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("✅ Conectado a la base de datos")
        
        # Consultas de debug
        queries = [
            ("Productos totales", "SELECT COUNT(*) FROM producto"),
            ("Variantes totales", "SELECT COUNT(*) FROM producto_variante"),
            ("Sesiones activas", "SELECT COUNT(*) FROM sesion"),
            ("Detecciones recientes", "SELECT COUNT(*) FROM deteccion WHERE fecha_hora > datetime('now', '-1 hour')"),
            ("Consultas de voz", "SELECT COUNT(*) FROM consulta_voz WHERE fecha_hora > datetime('now', '-1 hour')")
        ]
        
        print(f"\n📊 === ESTADÍSTICAS DE LA BASE DE DATOS ===")
        
        for name, query in queries:
            try:
                cursor.execute(query)
                result = cursor.fetchone()[0]
                print(f"📈 {name}: {result}")
            except Exception as e:
                print(f"❌ Error en {name}: {e}")
        
        # Mostrar productos con imágenes
        print(f"\n🖼️ === PRODUCTOS CON IMÁGENES ===")
        cursor.execute("""
            SELECT p.nombre, p.marca, COUNT(pv.id_variante) as variantes
            FROM producto p
            JOIN producto_variante pv ON p.id_producto = pv.id_producto
            WHERE pv.image_url IS NOT NULL
            GROUP BY p.id_producto, p.nombre, p.marca
            ORDER BY variantes DESC
            LIMIT 10
        """)
        
        products = cursor.fetchall()
        for nombre, marca, variantes in products:
            print(f"📦 {marca} {nombre}: {variantes} variantes con imagen")
        
        conn.close()
        print(f"\n✅ Análisis de base de datos completado")
        
    except Exception as e:
        print(f"❌ Error en análisis de BD: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🐛 DEBUGGER INTEGRADO DEL BACKEND")
    print("=" * 50)
    print("Opciones:")
    print("1. python3 backend_debug.py analysis    - Debug análisis en tiempo real")
    print("2. python3 backend_debug.py api         - Debug endpoints de la API")
    print("3. python3 backend_debug.py database    - Debug base de datos")
    print("4. python3 backend_debug.py all         - Ejecutar todos los debugs")
    
    if len(sys.argv) < 2:
        print("\n❌ Uso: python3 backend_debug.py [analysis|api|database|all]")
        return
    
    option = sys.argv[1].lower()
    
    if option == "analysis":
        debug_backend_analysis()
    elif option == "api":
        debug_api_endpoints()
    elif option == "database":
        debug_database_queries()
    elif option == "all":
        print("🚀 Ejecutando todos los debugs...")
        debug_api_endpoints()
        print("\n" + "="*50)
        debug_database_queries()
        print("\n" + "="*50)
        debug_backend_analysis()
    else:
        print(f"❌ Opción no válida: {option}")

if __name__ == "__main__":
    main()
