import os
import sys
import subprocess

def main():
    print("=== Instalador do Sistema de Mapeamento de Conhecimentos ===")
    
    # Verificar se Python está instalado
    python_version = sys.version_info
    print(f"Python versão {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Criar diretórios necessários
    print("\nCriando diretórios necessários...")
    os.makedirs('templates', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    print("Diretórios criados com sucesso!")
    
    # Instalar dependências
    print("\nInstalando dependências necessárias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("Flask instalado com sucesso!")
    except subprocess.CalledProcessError:
        print("Erro ao instalar Flask. Por favor, instale manualmente com o comando:")
        print("pip install flask")
        return False
    
    # Verificar se os arquivos existem
    print("\nVerificando arquivos do sistema...")
    if not os.path.exists("app.py"):
        print("ERRO: O arquivo app.py não foi encontrado no diretório atual.")
        return False
    
    if not os.path.exists("templates/index.html"):
        print("ERRO: O arquivo templates/index.html não foi encontrado.")
        return False
    
    print("Todos os arquivos necessários foram encontrados!")
    
    print("\n=== Instalação concluída com sucesso! ===")
    print("\nPara iniciar o sistema, execute o comando:")
    print("python app.py")
    print("\nDepois, abra seu navegador e acesse: http://127.0.0.1:5000")
    
    return True

if __name__ == "__main__":
    main()

