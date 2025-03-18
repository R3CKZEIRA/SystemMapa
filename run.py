import os
import sys
import subprocess

def main():
    print("=== Sistema de Mapeamento de Conhecimentos ===")
    
    # Verificar se o arquivo app.py existe
    if not os.path.exists("app.py"):
        print("ERRO: O arquivo app.py não foi encontrado no diretório atual.")
        print("Por favor, certifique-se de que o arquivo está na mesma pasta que este script.")
        return
    
    # Verificar se a pasta templates existe
    if not os.path.exists("templates"):
        print("Criando pasta templates...")
        os.makedirs("templates")
    
    # Verificar se a pasta data existe
    if not os.path.exists("data"):
        print("Criando pasta data...")
        os.makedirs("data")
    
    # Verificar se o Flask está instalado
    try:
        import flask
        print("Flask já está instalado!")
    except ImportError:
        print("Flask não está instalado. Tentando instalar...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("Flask instalado com sucesso!")
        except subprocess.CalledProcessError:
            print("Erro ao instalar Flask. Por favor, instale manualmente com o comando:")
            print("pip install flask")
            return
    
    # Iniciar a aplicação Flask
    print("\nIniciando a aplicação web...")
    print("Acesse http://127.0.0.1:5000 no seu navegador para usar o sistema.")
    os.system(f"{sys.executable} app.py")

if __name__ == "__main__":
    main()

