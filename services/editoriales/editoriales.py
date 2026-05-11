"""
Modelo para la gestión de editoriales.
Maneja toda la persistencia (SQL) relacionada con la tabla editoriales.
Columnas: idEditorial (PRI, varchar), idPais (MUL, varchar FK), nombre (varchar)
"""
from conexion import *

class Editoriales:
    def listar(self):
        sql = "SELECT * FROM editoriales"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def consultar(self, id):
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id, id_pais, nombre):
        sql = f"INSERT INTO editoriales (idEditorial,idPais,nombre) VALUES ('{id}','{id_pais}','{nombre}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, id_pais, nombre):
        sql = f"UPDATE editoriales SET idPais='{id_pais}', nombre='{nombre}' WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        sql = f"DELETE FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

mis_editoriales = Editoriales()