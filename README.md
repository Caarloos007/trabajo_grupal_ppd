# Práctica: Aplicación Distribuida de Subastas

**Objetivo:** Desarrollar un sistema de subasta en tiempo real usando arquitectura Pub/Sub.

## Requisitos Técnicos Implementados:
- **Threading & Sockets:** Manejo de conexiones concurrentes.
- **Nodos:** 1 Publicador (subastador) y 2 Suscriptores (compradores).
- **Datos Dinámicos:** Actualización de precios automática.
- **Logs:** Registro de eventos en cada terminal.

## Instrucciones de Ejecución:
1. Abrir una terminal y ejecutar: `python subastador.py`
2. Abrir una segunda terminal y ejecutar: `python comprador.py`
3. Abrir una tercera terminal y ejecutar: `python comprador.py` (para el segundo suscriptor).