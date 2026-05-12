"""
Modelo para la gestión de países.
Maneja toda la persistencia (SQL) relacionada con la tabla paises.
Columnas: idPais (PRI, varchar), continente (varchar), nombre (varchar)
"""
from conexion import *

class Paises:
    def listar(self):
        sql = "SELECT * FROM paises"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def consultar(self, id):
        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id, continente, nombre):
        sql = f"INSERT INTO paises (idPais,continente,nombre) VALUES ('{id}','{continente}','{nombre}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, continente, nombre):
        sql = f"UPDATE paises SET continente='{continente}', nombre='{nombre}' WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        sql = f"DELETE FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

mis_paises = Paises()