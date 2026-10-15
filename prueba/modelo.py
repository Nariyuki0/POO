from datetime import date


class Departamento:
    def __init__(self, nombre_depa, gerente_asociado):
        self.__nombre_depa = nombre_depa
        self.__gerente_asociado = gerente_asociado
        self.__empleados = []  # agregación: 0..* empleados

    def agregar_empleado(self, empleado):
        self.__empleados.append(empleado)
        empleado._set_departamento(self)

    def crear_depa(self):
        print(f"Creando departamento: {self.__nombre_depa}")

    def editar_depa(self, nombre_depa=None, gerente_asociado=None):
        if nombre_depa:
            self.__nombre_depa = nombre_depa
        if gerente_asociado:
            self.__gerente_asociado = gerente_asociado
        print("Departamento editado")

    def buscar_depa(self):
        print(f"Departamento: {self.__nombre_depa} | Gerente: {self.__gerente_asociado}")
        return self

    def eliminar_depa(self):
        for empleado in self.__empleados:
            empleado._set_departamento(None)  # los empleados no se borran
        self.__empleados.clear()
        print(f"Departamento {self.__nombre_depa} eliminado")


class Empleado:
    def __init__(self, idUnico, nombre, direccion, telefono, email, fechaContrato, salario):
        self.__idUnico = idUnico
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = str(telefono)
        self.__email = email
        self.__fechaContrato = fechaContrato
        self.__salario = salario
        self.__departamento = None
        self.__proyectos = []
        self.__registros = []  # composición: los registros dependen del empleado

    def _set_departamento(self, departamento):
        self.__departamento = departamento

    def trabajar(self):
        print("trabajando...")

    def informacionDe_empleado(self):
        print(f"ID: {self.__idUnico}\nNombre: {self.__nombre}\nDirección: {self.__direccion}\n"
              f"Teléfono: {self.__telefono}\nEmail: {self.__email}\n"
              f"Fecha de contrato: {self.__fechaContrato}\nSalario: {self.__salario}")

    def departamentoDe_empleado(self):
        if self.__departamento is None:
            print("El empleado no tiene departamento asignado")
        return self.__departamento

    def asignar_proyecto(self, proyecto):
        if proyecto not in self.__proyectos:
            self.__proyectos.append(proyecto)
            proyecto._agregar_empleado(self)

    def _quitar_proyecto(self, proyecto):
        if proyecto in self.__proyectos:
            self.__proyectos.remove(proyecto)

    def registrar_tiempo(self, proyecto, horas, fecha, descripcion):
        registro = RegistroTiempo(horas, fecha, descripcion, proyecto)
        self.__registros.append(registro)
        proyecto._agregar_registro(registro)
        return registro


class Proyecto:
    def __init__(self, nombre, fechaInicio, descripcion):
        self.__nombre = nombre
        self.__fechaInicio = fechaInicio
        self.__descripcion = descripcion
        self.__empleados = []
        self.__registros = []

    def _agregar_empleado(self, empleado):
        self.__empleados.append(empleado)

    def _agregar_registro(self, registro):
        self.__registros.append(registro)

    def crear_proyecto(self):
        print(f"Creando proyecto: {self.__nombre}")

    def editar_proyecto(self, nombre=None, descripcion=None):
        if nombre:
            self.__nombre = nombre
        if descripcion:
            self.__descripcion = descripcion
        print("Proyecto editado")

    def buscar_proyecto(self):
        print(f"Proyecto: {self.__nombre} | Inicio: {self.__fechaInicio} | {self.__descripcion}")
        return self

    def eliminar_proyecto(self):
        for empleado in self.__empleados:
            empleado._quitar_proyecto(self)
        self.__empleados.clear()
        self.__registros.clear()
        print(f"Proyecto {self.__nombre} eliminado")


class RegistroTiempo:
    def __init__(self, horas_trabajadas, fechaDe_trabajo, descripcionDel_trabajo, proyecto):
        self.__horas_trabajadas = horas_trabajadas
        self.__fechaDe_trabajo = fechaDe_trabajo
        self.__descripcionDel_trabajo = descripcionDel_trabajo
        self.__proyecto = proyecto

    def registro_proyecto_particular(self):
        print(f"[{self.__proyecto}] {self.__fechaDe_trabajo}: {self.__horas_trabajadas} h - {self.__descripcionDel_trabajo}")

    def registro_empleado_particular(self):
        print(f"{self.__fechaDe_trabajo}: {self.__horas_trabajadas} h - {self.__descripcionDel_trabajo}")


class Informes:
    def informe_empleado(self, empleado):
        empleado.informacionDe_empleado()

    def informe_departamento(self, departamento):
        departamento.buscar_depa()

    def informe_proyecto(self, proyecto):
        proyecto.buscar_proyecto()

    def informe_registro_tiempo(self, registros):
        for registro in registros:
            registro.registro_empleado_particular()

    def exportar_pdf(self):
        print("Pendiente: exportar a PDF (por ejemplo con reportlab)")

    def exportar_excel(self):
        print("Pendiente: exportar a Excel (por ejemplo con openpyxl)")


if __name__ == "__main__":
    depto = Departamento("Primer departamento", "Rodrigo Lopez")
    e1 = Empleado(224724144, "Ignacio", "Boyeco", 28300355, "ignacio@com", date(2016, 10, 15), 230000)
    depto.agregar_empleado(e1)

    p1 = Proyecto("Sistema de gestión", date(2026, 1, 10), "Módulo de empleados")
    e1.asignar_proyecto(p1)
    e1.registrar_tiempo(p1, 6, date(2026, 10, 14), "Diseño de clases")

    e1.trabajar()
    Informes().informe_empleado(e1)
    depto.buscar_depa()