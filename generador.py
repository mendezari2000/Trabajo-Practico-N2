# generador.py
from logica import Articulo, ParserHtml,ExceptionArticuloInvalido
from logica import generar_pie_pagina


if __name__ == "__main__":
    datos_articulos = [
        Articulo("La economía crece un 90%", "María López", "El crecimiento económico ha sorprendido a los analistas..."),
        Articulo("Se inaugura nuevo hospital", "Juan Pérez", "Hoy se inauguró un moderno hospital en la ciudad de..."),
        Articulo("Tecnología y su impacto social", "Carlos Rodríguez", "La tecnología está cambiando todos los aspectos de nuestras vidas..."),
        Articulo("Tecadsaggdgasfa", "Ccarlos Rodadddassafíguez", "La tecnologia esta cmanieando.."),
    ]
    
    articulos =[]
    for articulo in datos_articulos:
        try:
            #articulo = Articulo(titulo,autor,texto)
            articulos.append(articulo)
        except ExceptionArticuloInvalido as e:
            print(f"articulo invalido: {e}")
    
    parser = ParserHtml(articulos)
    parser.generar_html()
    print("✅ El archivo HTML ha sido generado correctamente en la carpeta 'salida'.")
    
    palabra = input("ingrese palabra a buscar: ")
    parser.filtrar_palabra_clave(palabra)
    
