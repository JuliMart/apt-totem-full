#!/usr/bin/env python3
"""
Script para mapear imágenes generadas a todas las variantes de productos
Ejecutar después de generar las imágenes
"""

import sqlite3
import os
import shutil

def map_images_to_variants():
    conn = sqlite3.connect('apt-totem-backend/neototem.db')
    cursor = conn.cursor()

    # Obtener todas las variantes
    cursor.execute("""
        SELECT pv.id_variante, p.nombre, p.marca, pv.color, pv.talla
        FROM producto_variante pv
        JOIN producto p ON pv.id_producto = p.id_producto
        WHERE p.marca IN ('Nike', 'Adidas', 'Puma', 'Converse', 'Vans', 'New Balance', 'Under Armour')
        ORDER BY p.marca, p.nombre
    """)

    variants = cursor.fetchall()
    
    # Crear estructura de carpetas
    base_path = 'product_images'
    for brand in ['nike', 'adidas', 'puma', 'converse', 'vans', 'new-balance', 'under-armour']:
        os.makedirs(f'{base_path}/{brand}', exist_ok=True)

    # Mapear imágenes
    for variant in variants:
        id_variante, nombre, marca, color, talla = variant
        
        # Crear nombre de archivo base
        clean_nombre = nombre.lower().replace(' ', '-').replace(',', '')
        clean_marca = marca.lower().replace(' ', '-')
        clean_color = color.lower().replace(' ', '-')
        clean_talla = talla.lower()
        
        # Archivo base (sin talla)
        base_filename = f'{clean_marca}-{clean_nombre}.jpg'
        # Archivo específico (con talla)
        specific_filename = f'{clean_nombre}-{clean_color}-{clean_talla}.jpg'
        
        # Rutas
        source_path = f'generated_images/{base_filename}'
        target_path = f'{base_path}/{clean_marca}/{specific_filename}'
        
        # Copiar imagen si existe
        if os.path.exists(source_path):
            shutil.copy2(source_path, target_path)
            
            # Actualizar URL en BD
            web_url = f'/product_images/{clean_marca}/{specific_filename}'
            cursor.execute(
                'UPDATE producto_variante SET image_url = ? WHERE id_variante = ?',
                (web_url, id_variante)
            )
            print(f'✅ Mapeado: {marca} {nombre} ({color}, {talla})')
        else:
            print(f'❌ No encontrado: {source_path}')

    conn.commit()
    conn.close()
    print('🎉 Mapeo completado!')

if __name__ == '__main__':
    map_images_to_variants()