from .Database import Database
class MenuPrato:
    def __init__(self, data:tuple) -> None:
        self.rel_id = data[0]
        self.menu_id = data[1]
        self.prato_id = data[2]
        self.preco = data[3]
    
    def toJSON(self):
        return {
            "rel_id":self.rel_id,
            "menu_id":self.menu_id, 
            "prato_id":self.prato_id,
            "preco":self.preco
        }
    
    @staticmethod
    def cadastrar(menu_id, prato_id, preco) :
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''INSERT INTO menus_pratos(menu_id, prato_id, preco) VALUES (?, ?, ?)'''
            cursor.execute(QUERY, (menu_id, prato_id, preco))
            conn.commit()
    
    @staticmethod
    def excluir(menu_id, prato_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''DELETE FROM menus_pratos WHERE menu_id = ? AND prato_id = ?;'''
            cursor.execute(QUERY, (menu_id, prato_id))
            conn.commit()

    @staticmethod
    def obterPorGerente(gerente_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''
                SELECT mp.* FROM menus_pratos AS mp 
                JOIN menus AS m ON mp.menu_id = m.menu_id
                WHERE m.gerente_id = ?'''
            cursor.execute(QUERY, (gerente_id,))
            resultado = cursor.fetchall()
            return resultado