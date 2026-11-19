"""Módulo de servicios y cálculo polimórfico de tarifas para Software FJ.

Autor: Jennifer Perdomo (Líder del equipo - Curso Programación 213023, UNAD)
"""

from abc import abstractmethod
from src.entidad_base import EntidadSistema
from src.excepciones import DatoInvalidoError, ServicioNoDisponibleError
from src.logger import obtener_logger

logger = obtener_logger("servicios")


class Servicio(EntidadSistema):
    """Clase base abstracta para los servicios ofertados en Software FJ."""

    def __init__(
        self,
        nombre_servicio: str,
        tarifa_base_hora: float,
        disponible: bool = True,
        id_entidad: str | None = None,
    ) -> None:
        """Inicializa un servicio con tarifa base y estado de disponibilidad.

        Args:
            nombre_servicio: Nombre comercial del servicio.
            tarifa_base_hora: Valor base por hora en moneda local (> 0).
            disponible: Indica si el servicio se encuentra habilitado para reserva.
            id_entidad: Identificador opcional del servicio.
        """
        super().__init__(id_entidad=id_entidad)
        self.__nombre_servicio: str = ""
        self.__tarifa_base_hora: float = 0.0
        self.__disponible: bool = True

        self.nombre_servicio = nombre_servicio
        self.tarifa_base_hora = tarifa_base_hora
        self.disponible = disponible

    @property
    def nombre_servicio(self) -> str:
        """Retorna el nombre del servicio."""
        return self.__nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor: str) -> None:
        """Valida y asigna el nombre del servicio."""
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(
                "El nombre del servicio debe tener al menos 3 caracteres.",
                codigo_error="FJ-105",
            )
        self.__nombre_servicio = valor.strip()

    @property
    def tarifa_base_hora(self) -> float:
        """Retorna la tarifa base por hora del servicio."""
        return self.__tarifa_base_hora

    @tarifa_base_hora.setter
    def tarifa_base_hora(self, valor: float) -> None:
        """Valida que la tarifa base por hora sea un número positivo."""
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise DatoInvalidoError(
                "La tarifa base por hora debe ser un valor numérico mayor que cero.",
                codigo_error="FJ-106",
            )
        self.__tarifa_base_hora = float(valor)

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para ser reservado."""
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Asigna el estado de disponibilidad del servicio."""
        if not isinstance(valor, bool):
            raise DatoInvalidoError(
                "El estado de disponibilidad debe ser un valor booleano.",
                codigo_error="FJ-107",
            )
        self.__disponible = valor

    def verificar_disponibilidad(self) -> None:
        """Comprueba si el servicio está disponible; lanza excepción en caso contrario."""
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__nombre_servicio}' (ID: {self.id_entidad}) no está disponible.",
                codigo_error="FJ-202",
            )

    def calcular_costo(
        self,
        horas: float,
        descuento_porcentaje: float = 0.0,
        impuesto_iva: float = 0.19,
        recargo_extra: float | None = None,
    ) -> float:
        """Calcula el costo total mediante sobrecarga funcional con parámetros opcionales.

        Args:
            horas: Cantidad de horas solicitadas (> 0).
            descuento_porcentaje: Porcentaje de descuento adicional (0 a 100).
            impuesto_iva: Tasa de impuesto IVA aplicable (por defecto 19%).
            recargo_extra: Recargo fijo opcional por servicios adicionales.

        Returns:
            Costo total calculado redondeado a 2 decimales.
        """
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatoInvalidoError(
                "Las horas deben ser un número positivo mayor a cero.",
                codigo_error="FJ-108",
            )
        if not (0.0 <= descuento_porcentaje <= 100.0):
            raise DatoInvalidoError(
                "El descuento debe estar comprendido entre 0% y 100%.",
                codigo_error="FJ-109",
            )
        if impuesto_iva < 0:
            raise DatoInvalidoError(
                "El impuesto IVA no puede ser negativo.",
                codigo_error="FJ-110",
            )

        subtotal = self.calcular_tarifa_especifica(float(horas))
        if recargo_extra is not None:
            if recargo_extra < 0:
                raise DatoInvalidoError(
                    "El recargo extra no puede ser negativo.",
                    codigo_error="FJ-111",
                )
            subtotal += float(recargo_extra)

        monto_descuento = subtotal * (descuento_porcentaje / 100.0)
        base_gravable = max(0.0, subtotal - monto_descuento)
        total = base_gravable * (1.0 + impuesto_iva)
        return round(total, 2)

    @abstractmethod
    def calcular_tarifa_especifica(self, horas: float) -> float:
        """Calcula el subtotal propio de cada tipo de servicio."""

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna la descripción técnica y comercial específica del servicio."""


class ReservaSala(Servicio):
    """Servicio concreto para la reserva de salas de trabajo o conferencias."""

    def __init__(
        self,
        nombre_servicio: str,
        tarifa_base_hora: float,
        capacidad: int,
        disponible: bool = True,
        id_entidad: str | None = None,
    ) -> None:
        """Inicializa una sala reservable validando su capacidad de personas.

        Args:
            nombre_servicio: Nombre o código de la sala.
            tarifa_base_hora: Tarifa estándar por hora de uso.
            capacidad: Aforo máximo permitido en la sala (> 0).
            disponible: Disponibilidad actual de la sala.
            id_entidad: Identificador opcional.
        """
        super().__init__(
            nombre_servicio=nombre_servicio,
            tarifa_base_hora=tarifa_base_hora,
            disponible=disponible,
            id_entidad=id_entidad,
        )
        self.__capacidad: int = 0
        self.capacidad = capacidad
        logger.info(
            "Servicio ReservaSala creado: %s | Capacidad: %d | Disponible: %s",
            self.nombre_servicio,
            self.capacidad,
            self.disponible,
        )

    @property
    def capacidad(self) -> int:
        """Retorna el aforo máximo de la sala."""
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        """Valida que la capacidad sea un entero positivo."""
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise DatoInvalidoError(
                "La capacidad de la sala debe ser un número entero mayor a cero.",
                codigo_error="FJ-112",
            )
        self.__capacidad = valor

    def calcular_tarifa_especifica(self, horas: float) -> float:
        """Calcula el subtotal aplicando un 10% de descuento si las horas superan 4."""
        subtotal = self.tarifa_base_hora * horas
        if horas > 4:
            subtotal *= 0.90
            logger.debug(
                "Descuento automático del 10%% aplicado en sala '%s' por %.1f horas.",
                self.nombre_servicio,
                horas,
            )
        return subtotal

    def describir_servicio(self) -> str:
        """Retorna una descripción detallada de la sala y su capacidad."""
        estado_txt = "Disponible" if self.disponible else "No disponible"
        return (
            f"Sala '{self.nombre_servicio}' (Capacidad: {self.__capacidad} personas, "
            f"Tarifa base: ${self.tarifa_base_hora:,.2f}/h, Estado: {estado_txt})"
        )

    def validar_integridad(self) -> bool:
        """Verifica la validez de la tarifa base y la capacidad de la sala."""
        return self.tarifa_base_hora > 0 and self.__capacidad > 0

    def obtener_resumen(self) -> str:
        """Retorna el resumen estructurado del servicio ReservaSala."""
        return f"Servicio [{self.id_entidad}] | {self.describir_servicio()}"


# ==============================================================
# INTEGRANTE 2 — Mathias Claros-Clase AlquilerEquipo
# ==============================================================

class AlquilerEquipo(Servicio):
    """Clase derivada que representa el servicio de alquiler de equipos"""

    def __init__(self, nombre_servicio, tarifa_base, tipo_equipo: str, requiere_deposito: bool):
        super().__init__(nombre_servicio, tarifa_base)
        self.__tipo_equipo = tipo_equipo
        self.__requiere_deposito = requiere_deposito

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) == 0:
            raise DatoInvalidoError("El tipo de equipo debe ser un texto válido")
        self.__tipo_equipo = valor.strip()

    @property
    def requiere_deposito(self):
        return self.__requiere_deposito

    @requiere_deposito.setter
    def requiere_deposito(self, valor: bool):
        if not isinstance(valor, bool):
            raise DatoInvalidoError("El valor de requiere_deposito debe ser Verdadero o Falso")
        self.__requiere_deposito = valor

    def calcular_tarifa_especifica(self, horas: float) -> float:
        if horas <= 0:
            raise DatoInvalidoError("Las horas deben ser un valor mayor a cero")
        
        tarifa = self._tarifa_base * horas
        if self.__requiere_deposito:
            tarifa += tarifa * 0.05
        
        return round(tarifa, 2)

    def describir_servicio(self) -> str:
        dep = "Sí" if self.__requiere_deposito else "No"
        return f"Alquiler de Equipo: {self.__tipo_equipo} | Tarifa base: ${self._tarifa_base:.2f} | Requiere depósito: {dep}"

    def validar_integridad(self) -> bool:
        try:
            if not isinstance(self.__tipo_equipo, str) or len(self.__tipo_equipo.strip()) == 0:
                return False
            if not isinstance(self.__requiere_deposito, bool):
                return False
            if self._tarifa_base <= 0:
                return False
            return True
        except:
            return False

    def obtener_resumen(self) -> str:
        return f"Servicio [{self._id_entidad}] | {self.describir_servicio()}"
# ==============================================================================


# ==============================================================================
# TODO - INTEGRANTE 3: Implementar clase derivada AsesoriaEspecializada(Servicio)
# Instrucciones para el Integrante 3:
# 1. Heredar de `Servicio`.
# 2. Agregar atributos privados encapsulados: `__area_tematica` (str) y `__modalidad` ('PRESENCIAL' | 'VIRTUAL').
# 3. Implementar propiedades y setters validados.
# 4. Implementar `calcular_tarifa_especifica(self, horas: float) -> float`:
#    - Aplicar recargo del 15% si modalidad == 'PRESENCIAL', sin recargo si es 'VIRTUAL'.
# 5. Implementar `describir_servicio(self) -> str`, `validar_integridad(self) -> bool`
#    y `obtener_resumen(self) -> str`.
# ==============================================================================

# Integrante 3: Cristian Camilo Barragan Perdomo
# Implementacion de la clase AsesoriaEspecializada


class AsesoriaEspecializada(Servicio):
    """Representa una asesoria presencial o virtual."""

    def __init__(
        self,
        nombre_servicio: str,
        tarifa_base_hora: float,
        area_tematica: str,
        modalidad: str,
        disponible: bool = True,
        id_entidad: str | None = None,
    ) -> None:
        super().__init__(
            nombre_servicio=nombre_servicio,
            tarifa_base_hora=tarifa_base_hora,
            disponible=disponible,
            id_entidad=id_entidad,
        )
        self.__area_tematica = ""
        self.__modalidad = ""
        self.area_tematica = area_tematica
        self.modalidad = modalidad

        logger.info(
            "Asesoria creada: %s | Area: %s | Modalidad: %s",
            self.nombre_servicio,
            self.area_tematica,
            self.modalidad,
        )

    @property
    def area_tematica(self) -> str:
        """Obtiene el area de la asesoria."""
        return self.__area_tematica

    @area_tematica.setter
    def area_tematica(self, valor: str) -> None:
        """Valida el area tematica."""
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(
                "El area tematica debe tener al menos 3 caracteres.",
                codigo_error="FJ-114",
            )
        self.__area_tematica = valor.strip()

    @property
    def modalidad(self) -> str:
        """Obtiene la modalidad de la asesoria."""
        return self.__modalidad

    @modalidad.setter
    def modalidad(self, valor: str) -> None:
        """Permite solamente modalidad presencial o virtual."""
        if not isinstance(valor, str) or valor.strip().upper() not in (
            "PRESENCIAL", "VIRTUAL"
        ):
            raise DatoInvalidoError(
                "La modalidad debe ser PRESENCIAL o VIRTUAL.",
                codigo_error="FJ-115",
            )
        self.__modalidad = valor.strip().upper()

    def calcular_tarifa_especifica(self, horas: float) -> float:
        """Aplica un recargo del 15% en modalidad presencial."""
        self.verificar_disponibilidad()

        if (
            not isinstance(horas, (int, float))
            or isinstance(horas, bool)
            or horas <= 0
        ):
            raise DatoInvalidoError(
                "Las horas deben ser un numero positivo.",
                codigo_error="FJ-116",
            )

        subtotal = self.tarifa_base_hora * horas

        if self.modalidad == "PRESENCIAL":
            subtotal *= 1.15

        return round(subtotal, 2)

    def describir_servicio(self) -> str:
        """Describe las caracteristicas de la asesoria."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Asesoria '{self.nombre_servicio}' | "
            f"Area: {self.area_tematica} | "
            f"Modalidad: {self.modalidad} | "
            f"Tarifa: ${self.tarifa_base_hora:,.2f}/h | "
            f"Estado: {estado}"
        )

    def validar_integridad(self) -> bool:
        """Comprueba que los datos sean validos."""
        return (
            self.tarifa_base_hora > 0
            and len(self.area_tematica) >= 3
            and self.modalidad in ("PRESENCIAL", "VIRTUAL")
        )

    def obtener_resumen(self) -> str:
        """Genera un resumen del servicio."""
        return (
            f"Servicio [{self.id_entidad}] | "
            f"{self.describir_servicio()}"
        )
