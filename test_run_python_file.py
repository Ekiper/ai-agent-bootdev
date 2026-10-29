from functions.run_python_file import run_python_file

def main():
    print("Test 1: main.py sin argumentos (Debería mostrar las instrucciones)")
    print(run_python_file("calculator", "main.py"))
    print("-" * 50)

    print("Test 2: main.py con argumentos (Debería ejecutar la calculadora)")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("-" * 50)

    print("Test 3: tests.py (Debería ejecutar los tests)")
    print(run_python_file("calculator", "tests.py"))
    print("-" * 50)

    print("Test 4: Ruta fuera del directorio (Debería dar error de seguridad)")
    print(run_python_file("calculator", "../main.py"))
    print("-" * 50)

    print("Test 5: Archivo inexistente (Debería dar error de existencia)")
    print(run_python_file("calculator", "nonexistent.py"))
    print("-" * 50)

    print("Test 6: Archivo no Python (Debería dar error de extensión)")
    print(run_python_file("calculator", "lorem.txt"))
    print("-" * 50)

if __name__ == "__main__":
    main()