#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Carlos Ramos.

import unittest
from letrista.linea import Linea

class TestLinea(unittest.TestCase):

    def test_detecta_linea_con_rima(self):
        """
        Si inicia con una letra mayúscula sola, seguida de un espacio,
        se asume que es el esquema de rima.
        """

        linea = Linea("A La primer letra es el esquema de rima")

        self.assertEqual(Linea.TIPO_RIMA, linea.tipo)

    def test_detecta_linea_con_rima_y_silabas(self):
        """
        Detecta que el primer carácter es rima, el segundo un espacio,
        el tercero y cuarto es la cantidad de sílabas, y el quinto
        debe ser un espacio.
        """

        linea = Linea("A 05 Aquí hay cinco")

        self.assertEqual(Linea.TIPO_SILABAS, linea.tipo)

    def test_detecta_linea_sin_rima_ni_silabas(self):

        linea = Linea("Aquí hay cinco")

        self.assertEqual(Linea.TIPO_TEXTO, linea.tipo)

    def test_detecta_linea_de_instruccion(self):

        linea = Linea("[Esto es instrucción por empezar en corchetes]")

        self.assertEqual(Linea.TIPO_INSTRUCCION, linea.tipo)

    def test_detecta_linea_es_salto_de_linea(self):

        linea = Linea("")

        self.assertEqual(Linea.TIPO_SALTO, linea.tipo)

    def test_elimina_gorritos(self):

        linea = Linea("Esta línea tiene gorritos^A que se eliminan^B al final")

        self.assertEqual(
            "Esta línea tiene gorritos que se eliminan al final",
            linea.texto
        )


if __name__ == '__main__':
    unittest.main()
