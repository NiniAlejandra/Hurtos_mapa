import webbrowser
import os
import time

def open_html_file():
    """Abre el archivo HTML portable en el navegador predeterminado"""
    
    # Ruta del archivo HTML
    html_file = "hurtos_portable_fixed.html"
    
    # Verificar que el archivo existe
    if not os.path.exists(html_file):
        print(f"❌ Error: El archivo {html_file} no existe")
        return False
    
    # Obtener la ruta absoluta del archivo
    abs_path = os.path.abspath(html_file)
    
    print(f"📁 Archivo HTML encontrado: {html_file}")
    print(f"📊 Tamaño: {os.path.getsize(html_file) / 1024:.1f} KB")
    print(f"🔗 Ruta: {abs_path}")
    print("\n🌐 Abriendo en el navegador...")
    
    try:
        # Abrir el archivo en el navegador
        webbrowser.open(f"file://{abs_path}")
        print("✅ Archivo HTML abierto exitosamente en el navegador")
        print("\n💡 Instrucciones:")
        print("1. Espera unos segundos para que se carguen los datos")
        print("2. Si los gráficos no aparecen, recarga la página")
        print("3. Verifica que tienes conexión a internet para los mapas")
        print("4. Usa los filtros en el panel izquierdo para explorar los datos")
        return True
    except Exception as e:
        print(f"❌ Error al abrir el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando aplicación HTML portable de Hurtos")
    print("=" * 50)
    
    success = open_html_file()
    
    if success:
        print("\n🎉 ¡Aplicación iniciada correctamente!")
        print("📋 Puedes cerrar esta ventana y usar la aplicación en el navegador")
    else:
        print("\n❌ No se pudo abrir la aplicación")
        print("💡 Intenta abrir manualmente el archivo hurtos_portable_fixed.html")
    
    # Mantener la ventana abierta por 10 segundos
    print("\n⏳ Cerrando en 10 segundos...")
    time.sleep(10) 