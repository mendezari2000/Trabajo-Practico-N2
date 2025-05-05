import os
from datetime import datetime
import string
print("🏁 Iniciando generador...")

class ExceptionArticuloInvalido(Exception):
     def __init__(self, mensaje):
          super().__init__(mensaje)

class Articulo:
    def __init__(self, titulo, autor, texto):
        if len(titulo)>=10 and len(texto)>=10:
            self.titulo = titulo
            self.autor = autor
            self.texto = texto
        else:
             raise ExceptionArticuloInvalido("el titulo y texto deben tener mas de 10 caracteres.")
        
    def to_html(self):
        texto_corto = self.texto
        if len(texto_corto) > 300:
            texto_corto = self.texto[:300] + "..."
        return f"""
        <div class = "articulo">
            <div class = "titulo">{self.titulo}</div>
            <div class = "autor">Por {self.autor}</div>
            <div class = "texto">{self.texto}</div>
        </div>
        """
    def generar_html_articulo(self, nombre_archivo,anterior=None, siguiente = None, carpeta="salida/articulos"):
        html=f"""
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>{self.titulo}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }}
        h1 {{ text-align: center; }}
        .articulo {{ background-color: white; padding: 20px; border-radius: 8px; }}
    </style>
</head>
<body>
    {self.to_html()}
        <p>
        <a href="../index.html">← Volver al índice</a><br>
        {'<a href="' + anterior + '">← Artículo anterior</a><br>' if anterior else ''}
        {'<a href="' + siguiente + '">Siguiente artículo →</a>' if siguiente else ''}
    </p>
 
</body>
</html>
"""
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, nombre_archivo)
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(html)
        


class ParserHtml:
    def filtrar_palabra_clave(self,palabra):
            encontrado=False
            for articulo in self.articulos:
                if palabra in articulo.texto:
                    print(articulo.to_html())
                    encontrado=True
            if not encontrado: print("no encontrado")

    def __init__(self, articulos):
        """
        Inicializa la clase con una lista de tuplas que representan los artículos.
        Cada tupla tiene el formato: (titulo, autor, texto).
        """
        self.articulos = articulos

    def es_articulo_valido(self,titulo, autor, texto):
            return bool(titulo.strip()) and autor.strip() and texto.strip()
        
    def normalizar_autor(self,autor):
            return ' '.join(autor.split()).title()
        
    def generar_id_autor(self,autor):
            return autor.lower().replace(" ", "-")

    def generar_html(self, ruta_salida='salida/index.html'):#arma el index.html con la lista de enlaces de cada artiuclo individual
        """
        Genera el archivo HTML con el contenido de los artículos.
        """
        # Crear la carpeta de salida si no existe
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        
        #creo la lista de letras
        letras = list(string.ascii_uppercase)
        #inicializo dicc
        articulos_por_inicial = {letra:[] for letra in letras}

        

        for articulo in self.articulos:
             apellido = articulo.autor.split()[-1]
             inicial_apellido = apellido[0].upper()
             if inicial_apellido in articulos_por_inicial:
                  articulos_por_inicial[inicial_apellido].append(articulo)

        html_index = """<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

            <title>Noticias del Día</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }
                h1 { text-align: center; }
                .articulo { background-color: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); }
                .titulo { font-size: 24px; font-weight: bold; }
                .autor { font-size: 16px; color: #555; margin-bottom: 10px; }
                .texto { font-size: 18px; }
            </style>
        </head>
        <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Inicio</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#autores">Autores</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="articulos/articulo1.html">Artículo 1</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <header>
        <h1>Artículos Periodísticos</h1>
    </header>

            
        """

        html_index += """<h2>Índice de Autores por Inicial</h2>\n"""
        for letra in letras:
            if articulos_por_inicial[letra]:  # Solo mostrar las letras que tienen artículos
                html_index += f"<h3>{letra}</h3>\n<ul>\n"
            for articulo in articulos_por_inicial[letra]:
                html_index += f'<li><a href="articulos/{articulo.titulo}.html">{articulo.titulo}</a> - {articulo.autor}</li>\n'
            html_index += "</ul>\n"

        #html +=f"""<h2>Articulos por autor</h2>"""
        #agrupo los textos por autor
        articulos_por_autor = {}
        for articulo in self.articulos:
            if not self.es_articulo_valido(articulo.titulo,articulo.autor,articulo.texto):
                continue
            #html +=articulo.to_html()
            autor_normalizado = self.normalizar_autor(articulo.autor)
            if autor_normalizado not in articulos_por_autor:
                articulos_por_autor[autor_normalizado] = []
            #agrego al diccionario
            articulos_por_autor[autor_normalizado].append((articulo))


        html_index += "<h2>Cantidad de articulos por autor</h2>\n"
        html_index += """<table class="table table-striped">
        <thead><tr><th>Autor</th><th>Cantidad de artículos</th></tr></thead><tbody>
        """
        for autor, lista in articulos_por_autor.items():
            html_index += f"<tr><td>{autor}</td><td>{len(lista)}</td></tr>\n"
        html_index += "</tbody></table>\n"



        #primero genero todos los archivos individuales:indices de los art
        #armo lista de filas
        html_index += """<div class = "container">"""
        

                # Filtrar solo los artículos válidos
        articulos_validos = [a for a in self.articulos if self.es_articulo_valido(a.titulo, a.autor, a.texto)]

        html_index += '<div class="container">'
        for i, articulo in enumerate(articulos_validos):
            nombre_archivo = f"articulo{i+1}.html"
            anterior = f"articulo{i}.html" if i > 0 else None
            siguiente = f"articulo{i+2}.html" if i < len(articulos_validos) - 1 else None

            articulo.generar_html_articulo(nombre_archivo, anterior, siguiente)

            if i % 3 == 0:
                html_index += '<div class="row">'
            html_index += f"""<div class="col-md-4">
                <a href="articulos/{nombre_archivo}">{articulo.titulo}</a> - {articulo.autor}
            </div>"""
            if i % 3 == 2 or i == len(articulos_validos) - 1:
                html_index += '</div>'  # Cierra la fila
        html_index += '</div>'  # Cierra el contenedor

        html_index +='</div>'
        
        #indice de autores
        
            # Índice de Autores con enlaces a sus páginas
        html_index += "<h2>Índice de Autores</h2>\n<ul>\n"
    # Primero, construí un mapear artículo→archivo
        articulos_validos = [a for a in self.articulos if self.es_articulo_valido(a.titulo, a.autor, a.texto)]
        filename_map = {art: f"articulo{i+1}.html" for i, art in enumerate(articulos_validos)}

        for autor, lista in articulos_por_autor.items():
            html_index += f"<li>{autor}\n  <ul>\n"
            for articulo in lista:
                fn = filename_map[articulo]
                html_index += f'    <li><a href="articulos/{fn}">{articulo.titulo}</a></li>\n'
            html_index += "  </ul>\n</li>\n"
        html_index += "</ul>\n"

        #imprime el contenido por autor
        for autor, articulos in articulos_por_autor.items():
            id_autor = self.generar_id_autor(autor)
            html_index += f'<h3 id="{id_autor}">{autor}</h3>\n'
            for articulo in articulos:
                html_index += articulo.to_html()

        html_index += generar_pie_pagina()

        html_index += """
            </body>
            </html>
            """
        
        # Escribir el archivo HTML
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(html_index)
        
        
        

def generar_pie_pagina():
     ahora = datetime.now()
     anio_actual = ahora.year
     fecha_hora = ahora.strftime("%d/%m/%Y, %H:%M:%S")
     return f"""
        <footer class = "text-center mt-4">
            <p>Generado el {fecha_hora} - &copy; {anio_actual}</p>
        </footer>
     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    """