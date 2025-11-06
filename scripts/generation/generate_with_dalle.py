#!/usr/bin/env python3
"""
Script para generar imágenes de productos usando DALL-E
Ejecutar: python3 generate_with_dalle.py
"""

import openai
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

OUTPUT_DIR = 'generated_images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_image(url, path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f'✅ Downloaded: {path}')

def generate_image_with_dalle(prompt, filename):
    try:
        print(f'🎨 Generating: {filename}')
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size='512x512'
        )
        image_url = response['data'][0]['url']
        download_image(image_url, os.path.join(OUTPUT_DIR, filename))
        return image_url
    except Exception as e:
        print(f'❌ Error generating {filename}: {e}')
        return None

if __name__ == '__main__':
    print('🚀 Iniciando generación de imágenes con DALL-E...')
    print(f'📁 Guardando en: {OUTPUT_DIR}')

    # 1. Adidas Adidas Ultraboost 22
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Adidas Adidas Ultraboost 22, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "adidas-adidas-ultraboost-22.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    # 2. Adidas Hoodie Adidas Originals
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Adidas Hoodie Adidas Originals, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "adidas-hoodie-adidas-originals.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    # 3. Adidas Pantalón Adidas Tiro
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Adidas Pantalón Adidas Tiro, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "adidas-pantalón-adidas-tiro.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    # 4. Converse Converse Chuck Taylor
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Converse Converse Chuck Taylor, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "converse-converse-chuck-taylor.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    # 5. Nike Camiseta Nike Dri-FIT
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Nike Camiseta Nike Dri-FIT, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "nike-camiseta-nike-dri-fit.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    # 6. Nike Nike Air Max 270
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Nike Nike Air Max 270, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "nike-nike-air-max-270.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    # 7. Nike Pantalón Nike Tech Fleece
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Nike Pantalón Nike Tech Fleece, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "nike-pantalón-nike-tech-fleece.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    # 8. Puma Puma RS-X
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Puma Puma RS-X, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "puma-puma-rs-x.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    # 9. Vans Vans Old Skool
    # Colores: Negro, Blanco, Azul
    generate_image_with_dalle(
        "Professional product photography of Vans Vans Old Skool, white background, studio lighting, high quality, commercial style, product shot, clean and minimalist, 512x512 pixels",
        "vans-vans-old-skool.jpg"
    )
    time.sleep(2)  # Pausa entre requests

    print('🎉 Generación completada!')
    print(f'📁 Imágenes guardadas en: {OUTPUT_DIR}')