import json
from collections import deque

class SistemaTareas:
    def __init__(self):
        self.tareas = []
        self.historial = []
        self.tareas_urgentes = deque()  # Usamos deque para mejor rendimiento en colas
        self.arbol_tareas = {
            "Proyecto Principal": {
                "frontend": ["Diseño UI", "Revisión de estilos"],
                "backend": ["API Login", "Gestión de BD"]
            }
        }
    
    def agregar_tarea(self):
        tarea = input("Ingrese la tarea a agregar: ")
        self.tareas.append(tarea)
        self.registrar_historial(f"Tarea agregada: {tarea}")
        print("✓ Tarea agregada con éxito")
    
    def mostrar_tareas(self):
        print("\n📋 Tareas actuales:")
        if not self.tareas:
            print("No hay tareas registradas.")
        else:
            for i, t in enumerate(self.tareas, 1):
                print(f"{i}. {t}")
    
    def editar_tarea(self):
        self.mostrar_tareas()
        try:
            indice = int(input("Ingrese el número de la tarea a editar: ")) - 1
            if 0 <= indice < len(self.tareas):
                nueva = input("Ingrese el nuevo nombre de la tarea: ")
                self.registrar_historial(f"Tarea editada: {self.tareas[indice]} → {nueva}")
                self.tareas[indice] = nueva
                print("✓ Tarea actualizada")
            else:
                print("❌ Índice fuera de rango")
        except ValueError:
            print("❌ Por favor ingrese un número válido")
    
    def eliminar_tarea(self):
        self.mostrar_tareas()
        try:
            indice = int(input("Ingrese el número de la tarea a eliminar: ")) - 1
            if 0 <= indice < len(self.tareas):
                tarea_eliminada = self.tareas.pop(indice)
                self.registrar_historial(f"Tarea eliminada: {tarea_eliminada}")
                print("✓ Tarea eliminada")
            else:
                print("❌ Índice fuera de rango")
        except ValueError:
            print("❌ Por favor ingrese un número válido")
    
    def agregar_urgencia(self):
        urgente = input("Ingrese una tarea urgente: ")
        self.tareas_urgentes.append(urgente)
        self.registrar_historial(f"Tarea urgente agregada: {urgente}")
        print(f"✓ Tarea urgente agregada. Posición en cola: {len(self.tareas_urgentes)}")
    
    def procesar_urgencias(self):
        if self.tareas_urgentes:
            tarea = self.tareas_urgentes.popleft()
            print(f"⚡ Procesando tarea urgente: {tarea}")
            self.registrar_historial(f"Tarea urgente procesada: {tarea}")
        else:
            print("ℹ️ No hay tareas urgentes para procesar")
    
    def mostrar_arbol(self):
        print("\n🌳 Organización jerárquica de tareas:")
        for area, subtareas in self.arbol_tareas["Proyecto Principal"].items():
            print(f"\n{area.upper()}:")
            for sub in subtareas:
                print(f"  ├─ {sub}")
    
    def ver_cola_urgente(self):
        if self.tareas_urgentes:
            print("\n🚨 Tareas Urgentes en cola:")
            print(f"  Primera en la cola: {self.tareas_urgentes[0]}")
            print(f"  Última en la cola: {self.tareas_urgentes[-1]}")
            print(f"  Total en cola: {len(self.tareas_urgentes)}")
        else:
            print("\nℹ️ No hay tareas urgentes en cola.")
    
    def mostrar_historial(self):
        print("\n📜 Historial de cambios (últimos 5):")
        for i, accion in enumerate(reversed(self.historial[-5:]), 1):
            print(f"{i}. {accion}")
    
    def registrar_historial(self, accion):
        self.historial.append(accion)
    
    def guardar_estado(self, archivo="tareas_backup.json"):
        estado = {
            "tareas": self.tareas,
            "historial": self.historial[-50:],  # Guardamos solo los últimos 50
            "tareas_urgentes": list(self.tareas_urgentes),
            "arbol_tareas": self.arbol_tareas
        }
        with open(archivo, 'w') as f:
            json.dump(estado, f)
        print(f"✓ Estado guardado en {archivo}")
    
    def cargar_estado(self, archivo="tareas_backup.json"):
        try:
            with open(archivo, 'r') as f:
                estado = json.load(f)
            self.tareas = estado.get("tareas", [])
            self.historial = estado.get("historial", [])
            self.tareas_urgentes = deque(estado.get("tareas_urgentes", []))
            self.arbol_tareas = estado.get("arbol_tareas", {})
            print(f"✓ Estado cargado desde {archivo}")
        except FileNotFoundError:
            print(f"ℹ️ No se encontró el archivo {archivo}")
        except json.JSONDecodeError:
            print(f"❌ Error al leer el archivo {archivo}")
    
    def menu(self):
        while True:
            print("\n" + "="*50)
            print("MENÚ PRINCIPAL - SISTEMA DE GESTIÓN DE TAREAS".center(50))
            print("="*50)
            print("1. Agregar tarea")
            print("2. Editar tarea")
            print("3. Eliminar tarea")
            print("4. Mostrar tareas")
            print("5. Agregar tarea urgente")
            print("6. Procesar tarea urgente")
            print("7. Mostrar el historial de cambios")
            print("8. Ver estructura del árbol de tareas")
            print("9. Ver cola de tareas urgentes")
            print("10. Guardar estado actual")
            print("11. Cargar estado guardado")
            print("12. Salir")
            
            try:
                opcion = int(input("\nSeleccione una opción: "))
                
                if opcion == 1:
                    self.agregar_tarea()
                elif opcion == 2:
                    self.editar_tarea()
                elif opcion == 3:
                    self.eliminar_tarea()
                elif opcion == 4:
                    self.mostrar_tareas()
                elif opcion == 5:
                    self.agregar_urgencia()
                elif opcion == 6:
                    self.procesar_urgencias()
                elif opcion == 7:
                    self.mostrar_historial()
                elif opcion == 8:
                    self.mostrar_arbol()
                elif opcion == 9:
                    self.ver_cola_urgente()
                elif opcion == 10:
                    self.guardar_estado()
                elif opcion == 11:
                    self.cargar_estado()
                elif opcion == 12:
                    print("\n¡Hasta pronto! 👋")
                    break
                else:
                    print("❌ Opción no válida. Por favor, seleccione una opción del 1 al 12.")
            except ValueError:
                print("❌ Por favor ingrese un número válido")

if __name__ == "__main__":
    sistema = SistemaTareas()
    sistema.menu()