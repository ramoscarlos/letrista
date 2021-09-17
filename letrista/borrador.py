#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Carlos Ramos.


from letrista.seccion import Seccion


class Borrador:
    """
    """

    SECCIONES_VALIDAS = [
        "Título", "Titulo",
        "Intro",
        "Verso",
        "Precoro", "Precoro2",
        "Coro", "Coro2",
        "Puente", "Puente2",
        "Outro"
    ]

    def __init__(self, letra):
        self.secciones = []

        self._letra = letra

        self.__procesar()

    # Funciones de procesamiento interno.
    def __procesar(self):
        seccion = None
        for line in self._letra.split('\n'):
            if self.__lineaEsIndicadorDeDescarte(line):
                break
            elif self.__lineaEsInstruccion(line):
                seccion = self.__crearSeccion(line)
                self.__agregarSeccion(seccion)
            elif self.__lineaSeImprime(line):
                # ERROR: REVISAR SI HAY SECCIÓN
                if (seccion):
                    seccion.agregarLinea(line)


    def __agregarSeccion(self, seccion):
        self.secciones.append(seccion)

    def __lineaEsIndicadorDeDescarte(self, linea):
        """
        Determina si la línea actual es el indicador del descarte mediante los
        primeros cinco dígitos.
        """
        if "*****" in linea:
            return True

        return False

    def __lineaEsInstruccion(self, linea):
        """
        Determina si la línea es una instrucción o notación.

        En general, las líneas de instrucción son aquellas utilizadas para darle
        darle forma a la canción y hacer notas sobre su estructura.

        Las líneas de instrucción comienzan con "["
        """
        if linea.strip() != '' and linea[0] == "[":
            return True

        return False

    def __lineaSeImprime(self, linea):
        """
        Esta función determina si se imprime o no una línea de texto como parte
        de la letra final.
        Aunque puede ser redundante, se vuelve a verificar que la línea no sea
        una instrucción, y también se omiten las líneas comentadas.
        """
        # Las instrucciones no se imprimen.
        if self.__lineaEsInstruccion(linea):
            return False

        # Los comentarios tampoco se imprimen.
        if len(linea) > 1 and linea[1] == "-":
            return False

        # Si no ha sido descartada, entonces sí es candidata a impresión.
        return True


    def __crearSeccion(self, linea):
        # Crear una nueva sección.
        if linea[1:-1] in self.SECCIONES_VALIDAS:
            seccion = Seccion(linea[1:-1])

        # Verificar si tiene una "R", que indica duplicar una sección anterior.
        if "R" in linea:
            seccion = self.__copiarSeccion(linea[1:-2])

        return seccion

    def __copiarSeccion(self, tipoSeccion):
        """
        Copia las líneas de una sección en otra, y regresa el objeto de la nueva sección
        """
        seccionExistente = next((x for x in self.secciones if x.tipo == tipoSeccion), False)

        seccionCopia = Seccion(seccionExistente.tipo)
        for l in seccionExistente.lineas:
            seccionCopia.agregarLinea(l)

        return seccionCopia

class LetraParaImprimir(Letra):
    def formatear(self):
        """
        Esta función regresa las secciones y las líneas, aún como objetos
        de clases personalizadas, y sin ningún formato.
        """
        lineas = []
        texto_de_seccion = ""
        for seccion in self.secciones:
            for i in range(len(seccion.lineas)):
                texto = self.__formatearLinea(seccion.lineas[i], seccion.tipo)
                # Agregar el "pre" de la sección
                if i == 0:
                    pre = self.__seccionPre(seccion.tipo)
                    texto = pre + texto
                # Agregar el "post" de la sección
                if i == seccion.ultimaLineaConTexto - 1:
                    post = self.__seccionPost(seccion.tipo)
                    texto = texto + post

                lineas.append(texto)
            lineas.append('')

        return lineas

    def __formatearLinea(self, linea, tipoSeccion):
        """
        Regresa la cadena de texto de la línea, más el formato envolvente.
        """
        # Texto normal de la línea.
        texto = linea.texto
        # Decoración previa
        pre = self.__lineaPre(tipoSeccion)
        # Decoración previa
        post = self.__lineaPost(tipoSeccion)

        return (pre + texto + post)

    def __seccionPre(self, tipoSeccion):
        return self.__buscarFormatoEnDict(self.FORMATO_SECCION, tipoSeccion.rstrip('1234567890'), "pre")

    def __seccionPost(self, tipoSeccion):
        return self.__buscarFormatoEnDict(self.FORMATO_SECCION, tipoSeccion.rstrip('1234567890'), "post")

    def __lineaPre(self, tipoSeccion):
        return self.__buscarFormatoEnDict(self.FORMATO_LINEA, tipoSeccion.rstrip('1234567890'), "pre")

    def __lineaPost(self, tipoSeccion):
        return self.__buscarFormatoEnDict(self.FORMATO_LINEA, tipoSeccion.rstrip('1234567890'), "post")

    def __buscarFormatoEnDict(self, diccionario, tipoSeccion, posicion):
        if tipoSeccion not in diccionario:
            return ''

        if posicion in diccionario[tipoSeccion]:
            return diccionario[tipoSeccion][posicion]

        return ''
