from conexion import *
import pytest

class Test_autores:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5081/autores"
        # Insertar país de apoyo (FK requerida)
        sql_pais = "INSERT INTO paises (idPais,continente,nombre) VALUES ('COL','América','Colombia')"
        mi_cursor.execute(sql_pais)
        # Insertar autor de prueba directamente en BD
        sql = "INSERT INTO autores (idAutor,idPais,nombre,email) VALUES ('aut001','COL','Gabriel García','garcia@mail.com')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos (primero autores por FK, luego pais)
        sql = "DELETE FROM autores WHERE idAutor='aut001'"
        mi_cursor.execute(sql)
        sql_pais = "DELETE FROM paises WHERE idPais='COL'"
        mi_cursor.execute(sql_pais)
        mi_db.commit()

    def test_lista_autores(self):
        esperado = "autores"
        calculado = requests.get(self.url)
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            (
                {"id": "aut002", "idPais": "COL", "nombre": "Tomás González", "email": "tomas@mail.com"},
                "Autor agregado con éxito"
            ),
            (
                {"id": "aut001", "idPais": "COL", "nombre": "Gabriel García", "email": "garcia@mail.com"},
                "Id de autor ya existe"
            ),
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        calculado = requests.post(self.url, json=nuevo_entrada)
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("aut001", "Autor encontrado"),
            ("aut999", "Autor no encontrado"),
        ]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        calculado = requests.get(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]

    def test_modifica1(self):
        # Autor existe y se modifica con éxito
        id = "aut001"
        nuevo = {"id": id, "idPais": "COL", "nombre": "Gabriel G. Márquez", "email": "gabriel@mail.com"}
        esperado = "Autor modificado con éxito"
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert datos[2] == "Gabriel G. Márquez" and datos[3] == "gabriel@mail.com"

    def test_modifica2(self):
        # Autor no existe
        id = "aut999"
        nuevo = {"id": id, "idPais": "COL", "nombre": "Nadie", "email": "nadie@mail.com"}
        esperado = "Autor no existe"
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("aut002", "Autor eliminado con éxito!"),
            ("aut999", "Autor no existe"),
        ]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        calculado = requests.delete(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]
        mi_db.commit()
        sql = f"SELECT * FROM autores WHERE idAutor='{id_entrada}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos) == 0