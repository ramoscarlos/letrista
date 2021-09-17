#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Carlos Ramos.

from letrista.linea import Linea


class Seccion:
    """
    Esta clase es utilizada para describir las siguientes secciones:
    - Titulo
    - Verso
    - Precoro
    - Coro
    - Puente
    - Intro
    - Outro

    En sí, una sección es una colección de líneas, con propiedades adicionales
    como lo son:
    - cantidadDeLineas
    - cantidadDePalabras
    """

    def __init__(self, tipo):
        self.lineas = []

        self._tipo = tipo

    def agregarLinea(self, line):
        # Si el argumento es una cadena, lo convertimos a una línea.
        # Si no es cadena, se asume que es una instancia de "Linea".
        if isinstance(line, str):
            linea = Linea(line)
        else:
            linea = line

        # Las líneas vacías no se agregan.
        if linea.tipo == linea.TIPO_SALTO:
            return

        self.lineas.append(linea)

    @property
    def ultimaLineaConTexto(self):
        """
        Regresa el número de la última línea de la sección que no es salto.
        """
        for i in range(len(self.lineas) - 1, 0, -1):
            if self.lineas[i].tipo == Linea.TIPO_SALTO:
                return i

        return len(self.lineas)

    @property
    def tipo(self):
        return self._tipo