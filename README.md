# 🔨 Sistema de Subastas Distribuidas en Tiempo Real

[cite_start]Este proyecto consiste en una aplicación distribuida basada en una arquitectura **Cliente-Servidor** con comportamiento **Pub/Sub**[cite: 19]. [cite_start]Permite gestionar subastas en tiempo real a través de sockets TCP, permitiendo que múltiples compradores compitan por un producto configurado por un subastador central[cite: 1].

## 🚀 Características Técnicas Implementadas

* [cite_start]**Threading & Sockets:** Manejo de conexiones concurrentes para permitir múltiples compradores simultáneos[cite: 1, 19].
* [cite_start]**Arquitectura Pub/Sub:** El subastador (publicador) notifica cambios de estado y nuevas pujas a todos los compradores (suscriptores)[cite: 1, 22].
* [cite_start]**Lógica de Negocio:** * Validación de pujas: Las nuevas ofertas deben ser al menos **$10** superiores a la mejor puja actual[cite: 36, 38].
    * [cite_start]Estado de "Paso": Los usuarios pueden decidir no pujar enviando el comando `paso`[cite: 14, 27].
* [cite_start]**Sincronización:** Uso de `threading.Lock` para garantizar la integridad de los datos al modificar la lista de clientes y las pujas[cite: 19, 22].
* [cite_start]**Logs en tiempo real:** Registro detallado de eventos (conexiones, pujas, ganadores) en cada terminal[cite: 1, 25].

## 💻 Instrucciones de Ejecución

Sigue estos pasos en terminales separadas:

1.  **Iniciar el Subastador:**
    ```bash
    python subastador.py
    ```
    Configura el nombre del producto y el precio base cuando el script lo solicite[cite: 56, 59].

2.  **Iniciar Compradores (mínimo 2 recomendados):**
    ```bash
    python comprador.py
    ```
    Repite este comando en otra terminal para simular la competencia[cite: 1].

3.  **Flujo de Subasta:**
    * [cite_start]En el **Subastador**: Escribe `iniciar` para abrir la ronda de pujas[cite: 57, 59].
    * [cite_start]En el **Comprador**: Introduce un número para pujar o escribe `paso`[cite: 14, 16].
    * [cite_start]En el **Subastador**: Presiona `Enter` para terminar la ronda actual y declarar al ganador[cite: 44, 45].
