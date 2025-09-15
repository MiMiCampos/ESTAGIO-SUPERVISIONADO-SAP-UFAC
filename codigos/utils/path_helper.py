import sys
import os

def resource_path(relative_path):
    """ 
    Retorna o caminho absoluto para o recurso, funcionando tanto no
    modo de desenvolvimento quanto no executável do PyInstaller.
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver rodando no PyInstaller, calcula o caminho a partir da
        # localização deste arquivo de ajuda para chegar na raiz do projeto.
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    return os.path.join(base_path, relative_path)