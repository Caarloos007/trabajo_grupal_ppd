# Sistema de Subastas Distribuidas en Tiempo Real

Este proyecto consiste en una aplicación distribuida basada en una arquitectura **Cliente-Servidor** con comportamiento **Pub/Sub**. Permite gestionar subastas en tiempo real a través de sockets TCP, permitiendo que múltiples compradores compitan por un producto configurado por un subastador central.

## Características Técnicas Implementadas

* **Threading & Sockets:** Manejo de conexiones concurrentes para permitir múltiples compradores simultáneos.
* **Arquitectura Pub/Sub:** El subastador (publicador) notifica cambios de estado y nuevas pujas a todos los compradores (suscriptores).
* **Lógica de Negocio:** * Validación de pujas: Las nuevas ofertas deben ser al menos **$10** superiores a la mejor puja actual.
    * Estado de "Paso": Los usuarios pueden decidir no pujar enviando el comando `paso`.
* **Sincronización:** Uso de `threading.Lock` para garantizar la integridad de los datos al modificar la lista de clientes y las pujas.
* **Logs en tiempo real:** Registro detallado de eventos (conexiones, pujas, ganadores) en cada terminal.

## Instrucciones de Ejecución

Sigue estos pasos en terminales separadas:

1.  **Iniciar el Subastador:**
    ```bash
    python subastador.py
    ```
    Configura el nombre del producto y el precio base cuando el script lo solicite.

2.  **Iniciar Compradores (mínimo 2 recomendados):**
    ```bash
    python comprador.py
    ```
    Repite este comando en otra terminal para simular la competencia.

3.  **Flujo de Subasta:**
    * En el **Subastador**: Escribe `iniciar` para abrir la ronda de pujas.
    * En el **Comprador**: Introduce un número para pujar o escribe `paso`.
    * En el **Subastador**: Presiona `Enter` para terminar la ronda actual y declarar al ganador.
