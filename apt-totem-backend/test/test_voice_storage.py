#!/usr/bin/env python3
"""
Script para probar el almacenamiento de consultas de voz
"""
import asyncio
import websockets
import json
from datetime import datetime

async def test_voice_storage():
    """Probar el almacenamiento de consultas de voz vía WebSocket"""
    
    uri = "ws://127.0.0.1:8001/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🔌 Conectado al WebSocket")
            
            # Enviar mensaje de voz de prueba
            test_message = {
                "type": "voice",
                "text": "Busco zapatillas deportivas en color azul",
                "timestamp": datetime.now().isoformat(),
                "session_id": "test_session_123"
            }
            
            print(f"📤 Enviando mensaje de voz: {test_message['text']}")
            await websocket.send(json.dumps(test_message))
            
            # Esperar respuesta
            response = await websocket.recv()
            result = json.loads(response)
            
            print(f"📥 Respuesta recibida:")
            print(f"  - Tipo: {result.get('type')}")
            print(f"  - Texto original: {result.get('original_text')}")
            print(f"  - Intención: {result.get('intent')}")
            print(f"  - Entidades: {result.get('entities')}")
            print(f"  - Confianza: {result.get('confidence')}")
            
            print("\n✅ Prueba completada. Verifica la base de datos para confirmar el almacenamiento.")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

if __name__ == "__main__":
    print("🧪 Probando almacenamiento de consultas de voz...")
    asyncio.run(test_voice_storage())

