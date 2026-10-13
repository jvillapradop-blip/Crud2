from abc import ABC, abstractmethod
from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

class CrudBase(ABC):
    @abstractmethod
    def leer(self): pass
    @abstractmethod
    def obtener(self, id_registro): pass
    @abstractmethod
    def buscar(self, texto): pass
    @abstractmethod
    def siguiente(self): pass
    @abstractmethod
    def crear(self, datos): pass
    @abstractmethod
    def actualizar(self, id_registro, datos): pass
    @abstractmethod
    def eliminar(self, id_registro): pass

class EstudianteController(CrudBase):
    def __init__(self, archivo="data/estudiantes.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = [Estudiante.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([e.a_diccionario() for e in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "carnet"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            usados = {e.email for e in self.lista if e.id != id_actual}
            if email in usados:
                return "Ese email ya está registrado"

        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip().upper()
            carnets_usados = {e.carnet for e in self.lista if e.id != id_actual}
            if carnet in carnets_usados:
                return "Ese carnet ya está registrado"

        return None

    def leer(self): return self.lista
    
    def obtener(self, id_estudiante):
        for e in self.lista:
            if e.id == id_estudiante: return e
        return None
        
    def buscar(self, texto):
        texto = texto.strip().lower()
        if not texto: return []
        return [e for e in self.lista if texto in e.nombre.lower() or texto in e.apellido.lower() or texto in e.carnet.lower() or texto in e.email]
        
    def siguiente(self):
        return max([e.id for e in self.lista] + [0]) + 1
        
    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        est = Estudiante(self.siguiente(), str(datos["nombre"]).strip().title(), 
                         str(datos["apellido"]).strip().title(), 
                         str(datos["email"]).strip().lower(), 
                         str(datos["carnet"]).strip().upper(), 
                         str(datos.get("carrera", "")).strip().title())
        self.lista.append(est)
        self.guardar()
        return True, f"Estudiante creado: {est.etiqueta()}"
        
    def actualizar(self, id_estudiante, datos):
        est = self.obtener(id_estudiante)
        if not est: return False, "No encontrado"
        if not datos: return False, "Sin cambios"
        
        permitidos = {"nombre", "apellido", "email", "carnet", "carrera"}
        desconocidos = set(datos) - permitidos
        if desconocidos: return False, f"Campos inválidos: {', '.join(desconocidos)}"
        
        error = self.validar(datos, id_estudiante)
        if error: return False, error
        
        for campo, valor in datos.items():
            val = str(valor).strip()
            if campo in ("nombre", "apellido", "carrera"): val = val.title()
            elif campo == "email": val = val.lower()
            elif campo == "carnet": val = val.upper()
            setattr(est, campo, val)
        self.guardar()
        return True, "Estudiante actualizado"
        
    def eliminar(self, id_estudiante):
        est = self.obtener(id_estudiante)
        if not est: return False, "No encontrado"
        self.lista.remove(est)
        self.guardar()
        return True, "Estudiante eliminado"
        
    def carreras(self):
        return sorted({e.carrera for e in self.lista if e.carrera})

class MateriaController(CrudBase):
    def __init__(self, archivo="data/materias.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = [Materia.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo"):
                if str(datos.get(campo, "")).strip() == "": 
                    return f"El campo {campo} es obligatorio"
                    
        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()
            usados = {m.codigo for m in self.lista if m.id != id_actual}
            if codigo in usados: return "Ese código ya existe"
            
        if "creditos" in datos:
            try:
                c = int(datos["creditos"])
                if not (1 <= c <= 10): return "Créditos debe estar entre 1 y 10"
            except ValueError: return "Créditos debe ser entero"
            
        if "cupos" in datos:
            try:
                cupos = int(datos["cupos"])
                if not (0 <= cupos <= Materia.CUPOS_MAXIMOS): 
                    return f"Cupos debe estar entre 0 y {Materia.CUPOS_MAXIMOS}"
            except ValueError: return "Cupos debe ser entero"
        return None

    def leer(self): return self.lista
    
    def obtener(self, id_materia):
        for m in self.lista:
            if m.id == id_materia: return m
        return None
        
    def buscar(self, texto):
        t = texto.strip().lower()
        if not t: return []
        return [m for m in self.lista if t in m.nombre.lower() or t in m.codigo.lower()]
        
    def siguiente(self):
        return max([m.id for m in self.lista] + [0]) + 1
        
    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        m = Materia(self.siguiente(), str(datos["nombre"]).strip().title(), 
                    str(datos["codigo"]).strip().upper(), datos.get("creditos", 0), datos.get("cupos", 0))
        self.lista.append(m)
        self.guardar()
        return True, f"Materia creada: {m.etiqueta()}"
        
    def actualizar(self, id_materia, datos):
        m = self.obtener(id_materia)
        if not m: return False, "No encontrado"
        if not datos: return False, "Sin cambios"
        
        desconocidos = set(datos) - {"nombre", "codigo", "creditos", "cupos"}
        if desconocidos: return False, "Campos inválidos"
        
        error = self.validar(datos, id_materia)
        if error: return False, error
        
        if "nombre" in datos: m.nombre = str(datos["nombre"]).strip().title()
        if "codigo" in datos: m.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos: m.creditos = int(datos["creditos"])
        if "cupos" in datos: m.cupos = int(datos["cupos"])
        self.guardar()
        return True, "Materia actualizada"
        
    def eliminar(self, id_materia):
        m = self.obtener(id_materia)
        if not m: return False, "No encontrado"
        self.lista.remove(m)
        self.guardar()
        return True, "Materia eliminada"
        
    def materias_sin_cupo(self):
        return [m for m in self.lista if not m.hay_cupo()]

class MatriculaController(CrudBase):
    def __init__(self, estudiantes, materias, archivo="data/matriculas.json"):
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON(archivo)
        self.lista = [Matricula.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def validar(self, datos):
        try:
            est_id = int(datos.get("estudiante_id", 0))
            mat_id = int(datos.get("materia_id", 0))
            nota = float(datos.get("nota", 0))
        except (TypeError, ValueError): 
            return "IDs deben ser enteros y nota numérica"

        if self.estudiantes.obtener(est_id) is None: return f"Estudiante {est_id} no existe"
        materia = self.materias.obtener(mat_id)
        if materia is None: return f"Materia {mat_id} no existe"
        if not materia.hay_cupo(): return "No hay cupos en la materia"
        if not Materia.es_nota_valida(nota): return "Nota inválida (0-20)"
        
        periodo = str(datos.get("periodo", "")).strip()
        for m in self.lista:
            if m.estudiante_id == est_id and m.materia_id == mat_id and m.periodo == periodo:
                return "El estudiante ya está matriculado en esta materia este periodo"
        return None

    def leer(self): return self.lista
    
    def obtener(self, id_mat):
        for m in self.lista:
            if m.id == id_mat: return m
        return None
        
    def buscar(self, texto):
        t = texto.strip()
        if not t: return []
        return [m for m in self.lista if t in m.periodo]
        
    def siguiente(self):
        return max([m.id for m in self.lista] + [0]) + 1
        
    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        materia = self.materias.obtener(int(datos["materia_id"]))
        mat = Matricula(self.siguiente(), int(datos["estudiante_id"]), materia.id, 
                        str(datos["periodo"]).strip(), float(datos["nota"]))
        materia.ocupar_cupo()
        self.materias.guardar()
        self.lista.append(mat)
        self.guardar()
        return True, "Matrícula registrada exitosamente"
        
    def actualizar(self, id_mat, datos): 
        return False, "Las matrículas no se pueden modificar, elimínela y registre otra"
        
    def eliminar(self, id_mat):
        mat = self.obtener(id_mat)
        if not mat: return False, "No encontrado"
        materia = self.materias.obtener(mat.materia_id)
        if materia:
            materia.liberar_cupo()
            self.materias.guardar()
        self.lista.remove(mat)
        self.guardar()
        return True, "Matrícula retirada y cupo devuelto"

    def registrar_nota(self, id_mat, nota):
        if not Materia.es_nota_valida(nota): return False, "Nota inválida"
        mat = self.obtener(id_mat)
        if not mat: return False, "No encontrado"
        mat.nota = float(nota)
        self.guardar()
        return True, "Nota actualizada"

    def certificado(self, id_mat):
        mat = self.obtener(id_mat)
        if not mat: return None
        
        indice_est = {e.id: e for e in self.estudiantes.leer()}
        indice_mat = {m.id: m for m in self.materias.leer()}
        
        est = indice_est.get(mat.estudiante_id)
        materia = indice_mat.get(mat.materia_id)
        
        txt = f"CERTIFICADO #{mat.id}   periodo: {mat.periodo}\n"
        txt += f"Estudiante: {est.nombre_completo() if est else 'Eliminado'}   ({est.carnet if est else ''})\n"
        txt += f"Materia   : {materia.nombre if materia else 'Eliminado'}   ({materia.codigo if materia else ''}) · {materia.creditos if materia else 0} créditos\n"
        txt += "-" * 42 + "\n"
        txt += f"Nota      : {mat.nota:.2f}\n"
        txt += f"Estado    : {mat.estado()}"
        return txt

    def matriculas_por_estudiante(self):
        agrupadas = {}
        for m in self.lista:
            agrupadas.setdefault(m.estudiante_id, []).append(m)
        return agrupadas

    def aprobadas(self):
        return sum(1 for m in self.lista if m.esta_aprobada())