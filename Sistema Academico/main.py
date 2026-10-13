from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteController, MateriaController, MatriculaController

estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)

def pausa():
    input("\nPresione Enter para continuar...")

def pedir_entero(etiqueta):
    try: return int(input(etiqueta))
    except ValueError: return None

def mostrar_resultado(exito, mensaje):
    if exito: imprimir_exito(mensaje)
    else: imprimir_error(mensaje)

def mostrar_lista(objetos, vacio="No hay registros todavía."):
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos: print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")

def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")

def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: "),
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()

def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer())
    pausa()

def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    term = input("Buscar (Nombre, apellido, email, carnet): ")
    mostrar_lista(estudiantes.buscar(term))
    pausa()

def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    e = estudiantes.obtener(pedir_entero("Id: "))
    if e: mostrar_detalle(e)
    else: imprimir_error("No encontrado")
    pausa()

def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_e = pedir_entero("Id: ")
    e = estudiantes.obtener(id_e)
    if not e:
        imprimir_error("No encontrado")
        return pausa()
    imprimir_info(f"Editando: {e.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")
    cambios = {}
    for c in ("nombre", "apellido", "email", "carnet", "carrera"):
        nuevo = input(f"{c.capitalize()} [{getattr(e, c)}]: ").strip()
        if nuevo: cambios[c] = nuevo
    mostrar_resultado(*estudiantes.actualizar(id_e, cambios))
    pausa()

def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_e = pedir_entero("Id: ")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*estudiantes.eliminar(id_e))
    pausa()

def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Código: "),
        "creditos": input("Créditos: "),
        "cupos": input("Cupos: "),
    }
    mostrar_resultado(*materias.crear(datos))
    pausa()

def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer())
    pausa()

def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    term = input("Buscar (Nombre, código): ")
    mostrar_lista(materias.buscar(term))
    pausa()

def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    m = materias.obtener(pedir_entero("Id: "))
    if m: mostrar_detalle(m)
    else: imprimir_error("No encontrado")
    pausa()

def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_m = pedir_entero("Id: ")
    m = materias.obtener(id_m)
    if not m:
        imprimir_error("No encontrado")
        return pausa()
    imprimir_info(f"Editando: {m.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")
    cambios = {}
    for c in ("nombre", "codigo", "creditos", "cupos"):
        nuevo = input(f"{c.capitalize()} [{getattr(m, c)}]: ").strip()
        if nuevo: cambios[c] = nuevo
    mostrar_resultado(*materias.actualizar(id_m, cambios))
    pausa()

def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_m = pedir_entero("Id: ")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*materias.eliminar(id_m))
    pausa()

def matricular():
    imprimir_titulo("REGISTRAR MATRICULA")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())
    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": input("Periodo: "),
        "nota": input("Nota inicial: ")
    }
    mostrar_resultado(*matriculas.crear(datos))
    pausa()

def listar_matriculas():
    imprimir_titulo("MATRICULAS")
    mostrar_lista(matriculas.leer())
    pausa()

def registrar_nota():
    imprimir_titulo("REGISTRAR NOTA")
    id_mat = pedir_entero("Id de matrícula: ")
    nota = input("Nueva nota: ")
    mostrar_resultado(*matriculas.registrar_nota(id_mat, nota))
    pausa()

def ver_certificado():
    imprimir_titulo("CERTIFICADO")
    txt = matriculas.certificado(pedir_entero("Id de la matrícula: "))
    if txt: print(txt)
    else: imprimir_error("No existe esa matrícula")
    pausa()

def retirar_matricula():
    imprimir_titulo("RETIRAR MATRICULA")
    id_mat = pedir_entero("Id de la matrícula: ")
    if id_mat and confirmar("Se devolverá el cupo. ¿Confirma?"):
        mostrar_resultado(*matriculas.eliminar(id_mat))
    pausa()

def resumen():
    imprimir_titulo("RESUMEN")
    print(f"  Estudiantes         : {len(estudiantes.leer())}")
    print(f"  Carreras distintas  : {', '.join(estudiantes.carreras()) or '-'}")
    print(f"  Materias totales    : {len(materias.leer())}")
    sin_cupos = materias.materias_sin_cupo()
    print(f"  Materias sin cupo   : {', '.join(m.nombre for m in sin_cupos) or 'ninguna'}")
    print(f"  Matrículas          : {len(matriculas.leer())}")
    print(f"  Matrículas aprobadas: {matriculas.aprobadas()}")
    pausa()

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Matricular", matricular),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota),
    "4": ("Ver certificado", ver_certificado),
    "5": ("Retirar matrícula", retirar_matricula),
    "0": ("Volver", None),
}

def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _) in opciones.items():
            print(f"  {tecla}. {texto}")
        
        tecla = input("\nOpción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue
            
        _, funcion = opciones[tecla]
        if funcion is None: break
        funcion()

def main():
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")
        
        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("MATERIAS", MENU_MATERIAS)
        elif tecla == "3":
            ejecutar_menu("MATRICULAS", MENU_MATRICULAS)
        elif tecla == "4":
            resumen()
        elif tecla == "0":
            break
        else:
            imprimir_error("Opción no válida")
            pausa()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\nPrograma interrumpido por el usuario.")