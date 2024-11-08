from .Database import Database
class Menu:
    def __init__(self, data:tuple) -> None:
        self.menu_id = data[0]
        self.gerente_id = data[1]
        self.nome = data[2]
    
    def toJSON(self):
        return {
            "menu_id":self.menu_id,
            "gerente_id":self.gerente_id, 
            "nome":self.nome,
        }
    
    @staticmethod
    def cadastrar(gerente_id, nome):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''INSERT INTO menus(gerente_id, nome) VALUES (?, ?)'''
            cursor.execute(QUERY, (gerente_id, nome))
            conn.commit()

    @staticmethod
    def excluir(menu_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''DELETE FROM menus WHERE menu_id = ?'''
            cursor.execute(QUERY, (menu_id,))
            conn.commit()
    
    @staticmethod
    def obterPorGerente(gerente_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''SELECT * FROM menus WHERE gerente_id = ? ORDER BY nome ASC'''
            cursor.execute(QUERY, (gerente_id,))
            resultado = cursor.fetchall()
            return resultado