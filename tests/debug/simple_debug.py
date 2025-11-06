#!/usr/bin/env python3
"""
Debugger simple para ver el análisis en tiempo real
"""
import sys
import os
import cv2
import numpy as np
from datetime import datetime
import json

# Agregar el path del backend
sys.path.append('/Users/julimart/Desktop/apt-totem/apt-totem-backend')

def debug_webcam_analysis():
    """Debuggear el análisis de la cámara web"""
    print("🐛 DEBUGGER DE ANÁLISIS EN TIEMPO REAL")
    print("=" * 50)
    print("📹 Iniciando captura de cámara...")
    
    # Inicializar cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: No se pudo abrir la cámara")
        return
    
    print("✅ Cámara iniciada correctamente")
    print("📋 Presiona 'q' para salir, 's' para analizar frame actual")
    
    frame_count = 0
    analysis_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: No se pudo leer el frame")
                break
            
            frame_count += 1
            
            # Mostrar frame
            cv2.imshow('Debug Analysis', frame)
            
            # Analizar cada 30 frames (aproximadamente cada segundo)
            if frame_count % 30 == 0:
                analysis_count += 1
                print(f"\n🔍 === ANÁLISIS #{analysis_count} - {datetime.now().strftime('%H:%M:%S')} ===")
                
                # Información básica del frame
                height, width, channels = frame.shape
                print(f"📏 Dimensiones: {width}x{height}x{channels}")
                
                # Análisis de colores básico
                try:
                    # Convertir a RGB
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Obtener colores dominantes usando K-means
                    from sklearn.cluster import KMeans
                    
                    # Redimensionar para análisis más rápido
                    small_frame = cv2.resize(rgb_frame, (100, 100))
                    pixels = small_frame.reshape(-1, 3)
                    
                    # K-means para 3 colores dominantes
                    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
                    kmeans.fit(pixels)
                    
                    colors = kmeans.cluster_centers_.astype(int)
                    labels = kmeans.labels_
                    
                    print(f"🎨 Colores dominantes detectados:")
                    for i, color in enumerate(colors):
                        count = np.sum(labels == i)
                        percentage = (count / len(labels)) * 100
                        print(f"  {i+1}. RGB({color[0]}, {color[1]}, {color[2]}) - {percentage:.1f}%")
                        
                        # Clasificar color básico
                        r, g, b = color
                        if r > g and r > b:
                            color_name = "Rojo"
                        elif g > r and g > b:
                            color_name = "Verde"
                        elif b > r and b > g:
                            color_name = "Azul"
                        elif r > 200 and g > 200 and b > 200:
                            color_name = "Blanco"
                        elif r < 50 and g < 50 and b < 50:
                            color_name = "Negro"
                        else:
                            color_name = "Mixto"
                        
                        print(f"     Clasificación: {color_name}")
                    
                except Exception as e:
                    print(f"❌ Error en análisis de colores: {e}")
                
                # Análisis de brillo
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness = np.mean(gray)
                print(f"💡 Brillo promedio: {brightness:.1f}/255")
                
                if brightness > 200:
                    print("   🌞 Imagen muy brillante")
                elif brightness < 50:
                    print("   🌙 Imagen muy oscura")
                else:
                    print("   ☀️ Brillo normal")
                
                # Análisis de contraste
                contrast = np.std(gray)
                print(f"🎭 Contraste: {contrast:.1f}")
                
                if contrast > 50:
                    print("   📈 Alto contraste")
                elif contrast < 20:
                    print("   📉 Bajo contraste")
                else:
                    print("   📊 Contraste normal")
                
                print(f"✅ Análisis completado")
            
            # Control de teclado
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n👋 Saliendo del debugger...")
                break
            elif key == ord('s'):
                # Análisis manual del frame actual
                analysis_count += 1
                print(f"\n🔍 === ANÁLISIS MANUAL #{analysis_count} - {datetime.now().strftime('%H:%M:%S')} ===")
                
                # Guardar frame para análisis
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                frame_path = f"/Users/julimart/Desktop/apt-totem/debug_frame_{timestamp}.jpg"
                cv2.imwrite(frame_path, frame)
                print(f"💾 Frame guardado: {frame_path}")
                
                # Análisis detallado
                height, width, channels = frame.shape
                print(f"📏 Frame: {width}x{height}x{channels}")
                
                # Análisis de colores RGB
                b, g, r = cv2.split(frame)
                print(f"🔴 Canal Rojo - Min: {r.min()}, Max: {r.max()}, Promedio: {r.mean():.1f}")
                print(f"🟢 Canal Verde - Min: {g.min()}, Max: {g.max()}, Promedio: {g.mean():.1f}")
                print(f"🔵 Canal Azul - Min: {b.min()}, Max: {b.max()}, Promedio: {b.mean():.1f}")
                
                # Detectar bordes
                edges = cv2.Canny(gray, 50, 150)
                edge_pixels = np.sum(edges > 0)
                total_pixels = edges.shape[0] * edges.shape[1]
                edge_percentage = (edge_pixels / total_pixels) * 100
                print(f"📐 Bordes detectados: {edge_pixels} píxeles ({edge_percentage:.1f}%)")
                
                if edge_percentage > 10:
                    print("   📈 Muchos bordes - posible textura compleja")
                elif edge_percentage < 2:
                    print("   📉 Pocos bordes - superficie lisa")
                else:
                    print("   📊 Bordes normales")
    
    except KeyboardInterrupt:
        print("\n👋 Interrumpido por usuario")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Cámara liberada")

def debug_static_image(image_path):
    """Debuggear una imagen estática"""
    print(f"🐛 DEBUGGING IMAGEN: {image_path}")
    print("=" * 50)
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Imagen no encontrada: {image_path}")
        return
    
    # Cargar imagen
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Error: No se pudo cargar la imagen")
        return
    
    print(f"✅ Imagen cargada correctamente")
    
    # Información básica
    height, width, channels = image.shape
    print(f"📏 Dimensiones: {width}x{height}x{channels}")
    print(f"💾 Tamaño en memoria: {image.nbytes} bytes")
    
    # Análisis de colores
    print(f"\n🎨 === ANÁLISIS DE COLORES ===")
    
    # Convertir a RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Análisis por canales
    r, g, b = cv2.split(rgb_image)
    print(f"🔴 Canal Rojo - Min: {r.min()}, Max: {r.max()}, Promedio: {r.mean():.1f}")
    print(f"🟢 Canal Verde - Min: {g.min()}, Max: {g.max()}, Promedio: {g.mean():.1f}")
    print(f"🔵 Canal Azul - Min: {b.min()}, Max: {b.max()}, Promedio: {b.mean():.1f}")
    
    # Colores dominantes
    try:
        from sklearn.cluster import KMeans
        
        # Redimensionar para análisis
        small_image = cv2.resize(rgb_image, (100, 100))
        pixels = small_image.reshape(-1, 3)
        
        # K-means
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        colors = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        
        print(f"\n🌈 Colores dominantes:")
        for i, color in enumerate(colors):
            count = np.sum(labels == i)
            percentage = (count / len(labels)) * 100
            print(f"  {i+1}. RGB({color[0]}, {color[1]}, {color[2]}) - {percentage:.1f}%")
    
    except Exception as e:
        print(f"❌ Error en análisis de colores: {e}")
    
    # Análisis de brillo y contraste
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    contrast = np.std(gray)
    
    print(f"\n💡 === PROPIEDADES DE LA IMAGEN ===")
    print(f"💡 Brillo: {brightness:.1f}/255")
    print(f"🎭 Contraste: {contrast:.1f}")
    
    # Detectar bordes
    edges = cv2.Canny(gray, 50, 150)
    edge_pixels = np.sum(edges > 0)
    total_pixels = edges.shape[0] * edges.shape[1]
    edge_percentage = (edge_pixels / total_pixels) * 100
    print(f"📐 Bordes: {edge_pixels} píxeles ({edge_percentage:.1f}%)")
    
    print(f"\n✅ Análisis completado")

def main():
    print("🐛 DEBUGGER DE ANÁLISIS DE IMÁGENES")
    print("=" * 50)
    print("Opciones:")
    print("1. python3 simple_debug.py webcam    - Análisis en tiempo real")
    print("2. python3 simple_debug.py <imagen>  - Análisis de imagen estática")
    
    if len(sys.argv) < 2:
        print("\n❌ Uso: python3 simple_debug.py [webcam|<ruta_imagen>]")
        return
    
    if sys.argv[1] == "webcam":
        debug_webcam_analysis()
    else:
        debug_static_image(sys.argv[1])

if __name__ == "__main__":
    main()
