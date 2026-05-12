"""
Modelo para la gestión de autores.
Maneja toda la persistencia (SQL) relacionada con la tabla autores.
Columnas: idAutor (PRI, varchar), idPais (MUL, varchar FK), nombre (varchar), email (varchar)
"""
from conexion import *

class Autores:
    def listar(self):
        sql = "SELECT * FROM autores"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def consultar(self, id):
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id, id_pais, nombre, email):
        sql = f"INSERT INTO autores (idAutor,idPais,nombre,email) VALUES ('{id}','{id_pais}','{nombre}','{email}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, id_pais, nombre, email):
        sql = f"UPDATE autores SET idPais='{id_pais}', nombre='{nombre}', email='{email}' WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        sql = f"DELETE FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

mis_autores = Autores()