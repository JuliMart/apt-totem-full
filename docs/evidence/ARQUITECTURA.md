# Arquitectura - NeoTotem AI

## Componentes
```mermaid
flowchart LR
  subgraph Frontend
    F1[Flutter Totem App]
    F2[Visualización Web /dashboard /visualization]
  end

  subgraph Backend[FastAPI]
    R1[Routers API]
    S1[Servicios AI (MediaPipe/OpenCV)]
    S2[Motor Recomendaciones]
    S3[Search/Analytics]
    WS[WebSocket /ws]
  end

  subgraph Datos
    DB[(BD Relacional)]
    IMG[[product_images]]
  end

  F1 -- WebSocket / REST --> WS
  F2 -- REST --> R1
  R1 --> S1
  R1 --> S2
  R1 --> S3
  R1 <--> DB
  S1 --> IMG
```

## Flujo (tiempo real)
```mermaid
sequenceDiagram
  participant App as Flutter App
  participant WS as WebSocket (/ws)
  participant AI as real_detection.py
  participant DB as Base de Datos
  participant Dash as Dashboard

  App->>WS: image_stream (base64)
  WS->>AI: analyze_realtime_stream_real()
  AI-->>WS: analysis {prenda, color, edad, accesorios}
  WS->>DB: INSERT deteccion + buffer turno
  WS-->>App: realtime_analysis + annotated_image
  Dash->>Backend: GET /dashboard
  Backend-->>Dash: KPIs desde DB
```
