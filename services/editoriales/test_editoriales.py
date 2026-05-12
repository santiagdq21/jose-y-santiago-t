from conexion import *
import pytest

class Test_editoriales:

    def setup_class(self):
        # Limpiar por si quedaron datos de corridas anteriores
        mi_cursor.execute("DELETE FROM editoriales WHERE idEditorial='E1'")
        mi_cursor.execute("DELETE FROM editoriales WHERE idEditorial='E2'")
        mi_db.commit()
        # Asegurar que exista el país requerido por la FK
        mi_cursor.execute("SELECT COUNT(*) FROM paises WHERE idPais='CO'")
        if mi_cursor.fetchone()[0] == 0:
            mi_cursor.execute("INSERT INTO paises (idPais, nombre, continente) VALUES ('CO','Colombia','América')")
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5082/editoriales"
        sql = "INSERT INTO editoriales (idEditorial,idPais,nombre) VALUES ('E1','CO','Editorial Colombia')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        mi_cursor.execute("DELETE FROM editoriales WHERE idEditorial='E1'")
        mi_cursor.execute("DELETE FROM editoriales WHERE idEditorial='E2'")
        mi_db.commit()

    def test_lista_editoriales(self):
        esperado = "editoriales"
        calculado = requests.get(self.url)
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"id": "E2", "idPais": "CO", "nombre": "Editorial México"}, "Editorial agregada con éxito"),
            ({"id": "E1", "idPais": "CO", "nombre": "Editorial Colombia"}, "Id de editorial ya existe"),
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        calculado = requests.post(self.url, json=nuevo_entrada)
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("E1", "Editorial encontrada"),
            ("XX", "Editorial no encontrada"),
        ]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        calculado = requests.get(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]

    def test_modifica1(self):
        id = "E1"
        nuevo = {"id": id, "idPais": "CO", "nombre": "Editorial Colombia Modificada"}
        esperado = "Editorial modificada con éxito"
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert datos[1] == "Editorial Colombia Modificada" and datos[2] == "CO"

    def test_modifica2(self):
        id = "XX"
        nuevo = {"id": id, "idPais": "CO", "nombre": "Inexistente"}
        esperado = "Editorial no existe"
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("E2", "Editorial eliminada con éxito!"),
            ("XX", "Editorial no existe"),
        ]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        calculado = requests.delete(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]
        mi_db.commit()
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{id_entrada}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos) == 0