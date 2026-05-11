from conexion import *
import pytest

class Test_paises:

    def setup_class(self):
        # Limpiar por si quedaron datos de corridas anteriores
        mi_cursor.execute("DELETE FROM paises WHERE idPais='CO'")
        mi_cursor.execute("DELETE FROM paises WHERE idPais='MX'")
        mi_db.commit()
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5083/paises"
        sql = "INSERT INTO paises (idPais,continente,nombre) VALUES ('CO','América','Colombia')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        mi_cursor.execute("DELETE FROM paises WHERE idPais='CO'")
        mi_cursor.execute("DELETE FROM paises WHERE idPais='MX'")
        mi_db.commit()

    def test_lista_paises(self):
        esperado = "paises"
        calculado = requests.get(self.url)
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"id": "MX", "continente": "América", "nombre": "México"}, "País agregado con éxito"),
            ({"id": "CO", "continente": "América", "nombre": "Colombia"}, "Id de país ya existe"),
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        calculado = requests.post(self.url, json=nuevo_entrada)
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("CO", "País encontrado"),
            ("XX", "País no encontrado"),
        ]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        calculado = requests.get(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]

    def test_modifica1(self):
        id = "CO"
        nuevo = {"id": id, "continente": "América del Sur", "nombre": "República de Colombia"}
        esperado = "País modificado con éxito"
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert datos[1] == "República de Colombia" and datos[2] == "América del Sur"

    def test_modifica2(self):
        id = "XX"
        nuevo = {"id": id, "continente": "X", "nombre": "Inexistente"}
        esperado = "País no existe"
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("MX", "País eliminado con éxito!"),
            ("XX", "País no existe"),
        ]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        calculado = requests.delete(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]
        mi_db.commit()
        sql = f"SELECT * FROM paises WHERE idPais='{id_entrada}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos) == 0