# Benjamin Rodriguez       
dict_planes = {
    "F001": ["plan basico", "mensual", 1, False, False, "libre"],
    "F002": ["Plan Full", "mensual", 1, True, True, "libre"],
    "F003": ["plan estudiante", "trimestral", 3, False, True, "Tarde"],
    "F004": ["plan senior", "trimestral", 3, False, True, "mañana"], 
    "F005": ["plan anual pro", "anual", 12, True, False, "libre"],
    "F006": ["plan nocturno", "mensual", 1, False, True, "noche"]
}


inscripciones = {
    "F001": [14990, 30],
    "F002": [22990, 10],
    "F003": [39990, 0],
    "F004": [35990, 6], 
    "F005": [15990, 2],
    "F006": [18990, 15]
}


def es_texto_valido(texto):
    return texto.strip() != ""

def es_rango_valido(p_min, p_max):
    return p_min <= p_max

def leer_texto(mensaje):
    while True:
        texto = input(mensaje)
        if es_texto_valido(texto):
            return texto
        print("Error: no puede estar vacio.")

def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero valido.")

def validacion_tipo(mensaje):
    tipos_planes = ["mensual", "trimestral", "anual"]
    while True:
        tipo = input(mensaje).strip().lower()
        if tipo in tipos_planes:
            return tipo
        print("Solo puedes ingresar los tipos de planes: mensual, trimestral o anual.")

def validacion_S_N(mensaje):
    while True:
        texto = input(mensaje).strip().upper()
        if texto in ["S", "N"]:
            return True if texto == "S" else False
        print("Solo se puede ingresar específicamente S o N.")

def validacion_codigo_nuevo(mensaje):
    while True:
        codigo = leer_texto(mensaje).upper()
        if buscar_producto(dict_planes, codigo) is not None:
            print("Ese codigo ya existe. Intenta con otro.")
        else:
            return codigo

def leer_entero_positivo(mensaje):
    while True:
        valor = leer_entero(mensaje)
        if valor >= 0:
            return valor
        print("Error: El valor debe ser mayor o igual a 0.")



def buscar_producto(dict_planes, codigo):
    return dict_planes.get(codigo)

def busqueda_precio(p_min, p_max, inscripciones, dict_planes):
    print(f"\n--- Planes entre ${p_min} y ${p_max} ---")
    encontrados = False
    for codigo, datos_inscripcion in inscripciones.items():
        precio = datos_inscripcion[0]
        if p_min <= precio <= p_max:
            plan_info = buscar_producto(dict_planes, codigo)
            nombre_plan = plan_info[0] if plan_info else "Desconocido"
            print(f"Código: {codigo} - Nombre: {nombre_plan} - Precio: ${precio} - Cupos: {datos_inscripcion[1]}")
            encontrados = True
    if not encontrados:
        print("No hay productos en ese rango de precio.")

def eliminar_producto(codigo, dict_planes):
    if buscar_producto(dict_planes, codigo) is not None:
        del dict_planes[codigo]
        del inscripciones[codigo]
        return True
    return False

def agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina, incluye_clases, horario, precio, cupos):
    if buscar_producto(dict_planes, codigo) is not None:
        return False
    dict_planes[codigo] = [nombre, tipo, duracion, acceso_piscina, incluye_clases, horario]
    inscripciones[codigo] = [precio, cupos]
    return True


def mostrar_menu():
    print("\n--- MENU PRINCIPAL ---")
    print("1. Cupos por tipo de plan")
    print("2. Busqueda de planes por rango de precio")
    print("3. Actualizar precio de plan")
    print("4. Agregar plan")
    print("5. Eliminar plan")
    print("6. Salir")

def leer_opcion():
    while True:
        try:
            opcion = int(input("Seleccione una opción (1-6): "))
            if 1 <= opcion <= 6:
                return opcion
            print("Error: la opción debe estar entre 1 y 6.")
        except ValueError:
            print("Error: debe ingresar un número entero válido.")

def main():
    while True:
        mostrar_menu()
        opcion = leer_opcion()
        
        
        if opcion == 1:
            tipo_buscar = validacion_tipo("Ingrese tipo de plan a consultar (mensual/trimestral/anual): ")
            total_cupos = 0
            print(f"\n--- Cupos para planes de tipo: {tipo_buscar} ---")
            for codigo, datos in dict_planes.items():
                if datos[1] == tipo_buscar:
                    cupos = inscripciones[codigo][1]
                    print(f"Plan: {datos[0]} ({codigo}) - Cupos disponibles: {cupos}")
                    total_cupos += cupos
            print(f"total de cupos disponibles para {tipo_buscar}: {total_cupos}")

        
        elif opcion == 2:
            p_min = leer_entero_positivo("ingrese el precio minimo: ")
            while True:
                p_max = leer_entero_positivo("ingrese el precio maximo: ")
                if es_rango_valido(p_min, p_max):
                    break
                print("Error: El precio maximo no puede ser menor al precio minimo.")
            busqueda_precio(p_min, p_max, inscripciones, dict_planes)

        
        elif opcion == 3:
            codigo = leer_texto("Ingrese el código del plan a actualizar: ").upper()
            plan = buscar_producto(dict_planes, codigo)
            if plan is not None:
                print(f"Plan encontrado: {plan[0]}. Precio actual: ${inscripciones[codigo][0]}")
                nuevo_precio = leer_entero_positivo("Ingrese el nuevo precio: ")
                inscripciones[codigo][0] = nuevo_precio
                print("Precio actualizado correctamente.")
            else:
                print("Error: El código de plan no existe.")

        
        elif opcion == 4:
            codigo = validacion_codigo_nuevo("Ingrese el código único a agregar (ej: F007): ")
            nombre = leer_texto("Ingrese el nombre del plan: ")
            tipo = validacion_tipo("Ingrese el tipo (mensual, trimestral o anual): ")
            duracion = leer_entero_positivo("Ingrese la duración (en meses): ")
            acceso_piscina = validacion_S_N("¿Tiene acceso a piscina? (S/N): ")
            incluye_clases = validacion_S_N("¿Incluye clases? (S/N): ")
            horario = leer_texto("Ingrese el horario (ej: mañana, tarde, noche, libre): ")
            precio = leer_entero_positivo("Ingrese el precio del plan: ")
            cupos = leer_entero_positivo("Ingrese la cantidad de cupos: ")
            
            if agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina, incluye_clases, horario, precio, cupos):
                print("Plan agregado correctamente")
            else:
                print("Error al agregar el plan.")

        
        elif opcion == 5:
            codigo = leer_texto("Ingrese código del plan a eliminar: ").upper()
            if eliminar_producto(codigo, dict_planes):
                print("Plan eliminado exitosamente de ambos registros.")
            else:
                print("El codigo no existe.")
                
        
        elif opcion == 6:
            print("Programa finalizado")
            break


main()