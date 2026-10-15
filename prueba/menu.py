import re
from datetime import datetime

from bd import (ConexionBD, ErrorBD, DepartamentoDAO, EmpleadoDAO,
                ProyectoDAO, RegistroTiempoDAO)
from modelo import Departamento, Empleado, Proyecto, RegistroTiempo


def pedir_texto(msg):
    valor = input(msg).strip()
    while not valor:
        valor = input("Este campo es obligatorio. " + msg).strip()
    return valor


def pedir_entero(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Debe ser un número entero.")


def pedir_real_positivo(msg):
    while True:
        try:
            valor = float(input(msg))
            if valor > 0:
                return valor
            print("Debe ser mayor que cero.")
        except ValueError:
            print("Debe ser un número.")


def pedir_email(msg):
    while True:
        email = input(msg).strip()
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return email
        print("Email inválido (ejemplo: nombre@dominio.cl).")


def pedir_fecha(msg):
    while True:
        texto = input(msg).strip()
        try:
            datetime.strptime(texto, "%Y-%m-%d")
            return texto
        except ValueError:
            print("Formato inválido. Usa AAAA-MM-DD.")


def menu_departamentos(conn):
    dao = DepartamentoDAO(conn)
    while True:
        print("\n--- DEPARTAMENTOS ---\n1. Crear  2. Consultar  3. Editar  4. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                depto = Departamento(dao, pedir_texto("Nombre: "), pedir_texto("Gerente: "))
                print(f"Departamento creado con id {depto.crear_depa()}")
            elif op == "2":
                Departamento(dao, "", "", pedir_entero("ID: ")).buscar_depa()
            elif op == "3":
                id_depa = pedir_entero("ID: ")
                ok = Departamento(dao, "", "", id_depa).editar_depa(
                    pedir_texto("Nuevo nombre: "), pedir_texto("Nuevo gerente: "))
                print("Departamento editado" if ok else "No encontrado")
            elif op == "4":
                ok = Departamento(dao, "", "", pedir_entero("ID: ")).eliminar_depa()
                print("Departamento eliminado" if ok else "No encontrado")
            elif op == "0":
                return
            else:
                print("Opción inválida")
        except ErrorBD as e:
            print(f"Error: {e}")


def menu_empleados(conn):
    dao = EmpleadoDAO(conn)
    while True:
        print("\n--- EMPLEADOS ---\n1. Crear  2. Consultar  3. Editar  4. Eliminar"
              "  5. Asignar proyecto  0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                dao.insertar(
                    pedir_entero("ID único: "),
                    pedir_texto("Nombre: "),
                    pedir_texto("Dirección: "),
                    pedir_texto("Teléfono: "),
                    pedir_email("Email: "),
                    pedir_fecha("Fecha de contrato (AAAA-MM-DD): "),
                    pedir_real_positivo("Salario: "),
                    pedir_entero("ID departamento (0 si no tiene): ") or None)
                print("Empleado registrado")
            elif op == "2":
                f = dao.consultar(pedir_entero("ID único: "))
                if f is None:
                    print("Empleado no encontrado")
                else:
                    emp = Empleado(f["id_unico"], f["nombre"], f["direccion"], f["telefono"],
                                   f["email"], f["fecha_contrato"], f["salario"], f["id_depa"])
                    emp.informacionDe_empleado()
                    emp.departamentoDe_empleado()
            elif op == "3":
                id_unico = pedir_entero("ID único: ")
                ok = dao.actualizar(
                    id_unico,
                    pedir_texto("Nueva dirección: "),
                    pedir_texto("Nuevo teléfono: "),
                    pedir_email("Nuevo email: "),
                    pedir_real_positivo("Nuevo salario: "),
                    pedir_entero("ID departamento (0 si no tiene): ") or None)
                print("Empleado actualizado" if ok else "Empleado no encontrado")
            elif op == "4":
                ok = dao.eliminar(pedir_entero("ID único: "))
                print("Empleado eliminado" if ok else "Empleado no encontrado")
            elif op == "5":
                dao.asignar_proyecto(pedir_entero("ID único empleado: "),
                                     pedir_entero("ID proyecto: "))
                print("Proyecto asignado")
            elif op == "0":
                return
            else:
                print("Opción inválida")
        except ErrorBD as e:
            print(f"Error: {e}")


def menu_proyectos(conn):
    dao = ProyectoDAO(conn)
    while True:
        print("\n--- PROYECTOS ---\n1. Crear  2. Consultar  3. Editar  4. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                proy = Proyecto(dao, pedir_texto("Nombre: "),
                                pedir_fecha("Fecha de inicio (AAAA-MM-DD): "),
                                pedir_texto("Descripción: "))
                print(f"Proyecto creado con id {proy.crear_proyecto()}")
            elif op == "2":
                Proyecto(dao, "", "", "", pedir_entero("ID: ")).buscar_proyecto()
            elif op == "3":
                id_proyecto = pedir_entero("ID: ")
                ok = Proyecto(dao, "", "", "", id_proyecto).editar_proyecto(
                    pedir_texto("Nuevo nombre: "),
                    pedir_fecha("Nueva fecha de inicio (AAAA-MM-DD): "),
                    pedir_texto("Nueva descripción: "))
                print("Proyecto editado" if ok else "No encontrado")
            elif op == "4":
                ok = Proyecto(dao, "", "", "", pedir_entero("ID: ")).eliminar_proyecto()
                print("Proyecto eliminado" if ok else "No encontrado")
            elif op == "0":
                return
            else:
                print("Opción inválida")
        except ErrorBD as e:
            print(f"Error: {e}")


def menu_registros(conn):
    dao = RegistroTiempoDAO(conn)
    while True:
        print("\n--- REGISTRO DE TIEMPO ---\n1. Registrar  2. Ver por empleado"
              "  3. Ver por proyecto  4. Editar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                id_reg = dao.insertar(
                    pedir_real_positivo("Horas trabajadas: "),
                    pedir_fecha("Fecha (AAAA-MM-DD): "),
                    pedir_texto("Descripción del trabajo: "),
                    pedir_entero("ID empleado: "),
                    pedir_entero("ID proyecto: "))
                print(f"Registro creado con id {id_reg}")
            elif op == "2":
                RegistroTiempo(dao, 0, "", "", pedir_entero("ID empleado: "), 0
                               ).registro_empleado_particular()
            elif op == "3":
                RegistroTiempo(dao, 0, "", "", 0, pedir_entero("ID proyecto: ")
                               ).registro_proyecto_particular()
            elif op == "4":
                ok = dao.actualizar(
                    pedir_entero("ID registro: "),
                    pedir_real_positivo("Nuevas horas: "),
                    pedir_fecha("Nueva fecha (AAAA-MM-DD): "),
                    pedir_texto("Nueva descripción: "))
                print("Registro actualizado" if ok else "No encontrado")
            elif op == "5":
                ok = dao.eliminar(pedir_entero("ID registro: "))
                print("Registro eliminado" if ok else "No encontrado")
            elif op == "0":
                return
            else:
                print("Opción inválida")
        except ErrorBD as e:
            print(f"Error: {e}")


def main():
    bd = ConexionBD()
    try:
        conn = bd.conectar()
    except ErrorBD as e:
        print(e)
        return
    try:
        while True:
            print("\n=== SISTEMA DE GESTIÓN DE EMPLEADOS ===\n"
                  "1. Departamentos  2. Empleados  3. Proyectos  4. Registro de tiempo  0. Salir")
            op = input("Opción: ").strip()
            if op == "1":
                menu_departamentos(conn)
            elif op == "2":
                menu_empleados(conn)
            elif op == "3":
                menu_proyectos(conn)
            elif op == "4":
                menu_registros(conn)
            elif op == "0":
                break
            else:
                print("Opción inválida")
    finally:
        bd.cerrar()


if __name__ == "__main__":
    main()