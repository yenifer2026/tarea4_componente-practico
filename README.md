# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto colaborativo desarrollado para la **Fase 4 del curso Programación (213023)** de la **Universidad Nacional Abierta y a Distancia (UNAD)**, programa de Ingeniería de Sistemas.

**Líder del equipo:** Jennifer Perdomo (`yenniferperdomo276@gmail.com`)

---

## Descripción del Proyecto

**Software FJ** es una solución modular orientada a objetos en Python 3 (sin bases de datos externas) diseñada para gestionar de forma integral el registro validado de clientes, el catálogo polimórfico de servicios y el ciclo de vida de reservas, incorporando jerarquía personalizada de excepciones, encadenamiento de errores y registro centralizado de eventos (*logging*).

---

## Estructura de Carpetas

```text
tarea4_componente-practico/
├── .gitignore
├── main.py                  # Script principal con 5 operaciones base simuladas
├── README.md                # Documentación oficial del proyecto
├── logs/                    # Carpeta generada automáticamente (ignorada en Git)
│   └── sistema_fj.log       # Registro de trazabilidad y errores
└── src/
    ├── __init__.py          # Inicializador del paquete
    ├── excepciones.py       # Jerarquía personalizada (ErrorSistemaFJ)
    ├── logger.py            # Configuración de logging (archivo + consola)
    ├── entidad_base.py      # Clase abstracta EntidadSistema(ABC)
    ├── cliente.py           # Clase Cliente con validación estricta y regex
    ├── servicios.py         # Clase abstracta Servicio y derivada ReservaSala
    └── reserva.py           # Clase Reserva con estados y confirmación
```

---

## Instrucciones de Ejecución

1. Verificar que se cuenta con **Python 3.10 o superior**.
2. Clonar el repositorio e ingresar a la carpeta raíz:
   ```bash
   git clone https://github.com/yenifer2026/tarea4_componente-practico.git
   cd tarea4_componente-practico
   ```
3. Ejecutar el script principal:
   ```bash
   python main.py
   ```
   *(En sistemas Linux/macOS puede usarse `python3 main.py`).*
4. Al finalizar la ejecución, revisar los resultados en consola y el registro detallado generado en `logs/sistema_fj.log`.

---

## Asignación de Tareas del Equipo Colaborativo

La arquitectura base queda completamente funcional desde el primer commit oficial de **Jennifer Perdomo**, con bloques `# TODO` delimitados para evitar conflictos durante los *merges*:

| Rol | Archivo Destino | Módulo / Responsabilidad Asignada | Etiqueta en Código |
| :--- | :--- | :--- | :--- |
| **Líder (Jennifer Perdomo)** | Arquitectura Core (`src/*`, `main.py`, `README.md`) | Base POO, excepciones, logger, `Cliente`, `Servicio`, `ReservaSala`, `Reserva` y operaciones 1–5. | *Implementado* |
| **Integrante 2(Mathias Claros)** | `src/servicios.py` | Implementar clase derivada `AlquilerEquipo(Servicio)` con seguro técnico del 5% y atributos encapsulados. | `# TODO - INTEGRANTE 2` |
| **Integrante 3** | `src/servicios.py` | Implementar clase derivada `AsesoriaEspecializada(Servicio)` con recargo según modalidad. | `# TODO - INTEGRANTE 3` |
| **Integrante 4** | `src/reserva.py` | Implementar `cancelar_reserva(self, motivo: str)` y validaciones avanzadas de transición de estados. | `# TODO - INTEGRANTE 4` |
| **Integrante 5** | `main.py` | Agregar operaciones simuladas 6 a 10+ integrando los nuevos servicios, cancelaciones y reporte final. | `# TODO - INTEGRANTE 5` |
