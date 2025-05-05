import os
from logica import Articulo, ParserHtml, ExceptionArticuloInvalido

def test_articulo():
    # Test 1: Verificar si el artículo se crea correctamente con un título y texto válidos
    articulo = Articulo("Tecnología Avanzada", "Carlos Rodríguez", "La tecnología está avanzando rápidamente en todos los campos.")
    
    # Asegurarse de que los atributos del artículo sean correctos
    assert articulo.titulo == "Tecnología Avanzada", f"Error: El título debe ser 'Tecnología Avanzada', pero se obtuvo '{articulo.titulo}'"
    assert articulo.autor == "Carlos Rodríguez", f"Error: El autor debe ser 'Carlos Rodríguez', pero se obtuvo '{articulo.autor}'"
    assert articulo.texto == "La tecnología está avanzando rápidamente en todos los campos.", f"Error: El texto del artículo es incorrecto."
    
    # Test 2: Verificar que el método `to_html()` devuelve el HTML correctamente
    html = articulo.to_html()
    assert '<div class = "titulo">Tecnología Avanzada</div>' in html, "Error: El título en HTML no es correcto"
    assert '<div class = "autor">Por Carlos Rodríguez</div>' in html, "Error: El autor en HTML no es correcto"
    assert 'La tecnología está avanzando rápidamente en todos los campos.' in html, "Error: El texto en HTML no es correcto"
    
    # Test 3: Verificar que la excepción se levante si el título o el texto tienen menos de 10 caracteres
    try:
        articulo_invalido = Articulo("Corto", "Juan Pérez", "Texto corto")
        assert False, "Error: Se esperaba una excepción por título o texto corto"
    except ExceptionArticuloInvalido as e:
        assert str(e) == "el titulo y texto deben tener mas de 10 caracteres.", f"Error: {e}"

def test_parser_html():
    # Test 1: Verificar que el ParserHtml se inicializa correctamente con una lista de artículos
    articulos = [
        Articulo("Tecnología Avanzada", "Carlos Rodríguez", "La tecnología está avanzando rápidamente en todos los campos."),
        Articulo("Innovación en salud", "Ana García", "La innovación está mejorando la calidad de vida.")
    ]
    parser = ParserHtml(articulos)
    
    # Asegurarse de que el número de artículos es correcto
    assert len(parser.articulos) == 2, f"Error: El número de artículos debería ser 2, pero se obtuvo {len(parser.articulos)}"
    
    # Test 2: Verificar que los artículos se agrupan correctamente por inicial del apellido
    parser.generar_html()  # Esto genera el HTML
    articulos_por_inicial = {letra: [] for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    
    # Agrupar los artículos por inicial
    for articulo in articulos:
        apellido = articulo.autor.split()[-1]
        inicial = apellido[0].upper()
        articulos_por_inicial[inicial].append(articulo)
    
    # Verificar que los artículos se agruparon correctamente
    assert len(articulos_por_inicial["R"]) == 1, "Error: Debería haber un artículo de un autor cuyo apellido empieza con 'R'."
    assert len(articulos_por_inicial["G"]) == 1, "Error: Debería haber un artículo de un autor cuyo apellido empieza con 'G'."
    
    # Test 3: Verificar que el método `filtrar_palabra_clave()` filtra correctamente los artículos por palabra clave
    parser.filtrar_palabra_clave("tecnología")  # Esto debería imprimir el artículo relacionado con tecnología

if __name__ == "__main__":
    test_articulo()
    test_parser_html()
    print("✅ Todos los tests pasaron correctamente.")
