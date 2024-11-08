from .Database import Database
class Prato:
    def __init__(self, data:tuple) -> None:
        self.prato_id = data[0]
        self.gerente_id = data[1]
        self.nome = data[2]
        self.ingredientes = data[3]
        self.receita = data[4]
    
    def toJSON(self):
        return {
            "prato_id":self.prato_id,
            "gerente_id":self.gerente_id,
            "nome":self.nome, 
            "ingredientes":self.ingredientes,
            "receita":self.receita
        }
    
    @staticmethod
    def cadastrar(gerente_id, nome, ingredientes, receita = ''):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''INSERT INTO pratos(gerente_id, nome, ingredientes, receita) VALUES (?,?,?,?)'''
            cursor.execute(QUERY, (gerente_id, nome, ingredientes, receita))
            conn.commit()

    @staticmethod
    def excluir(prato_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''DELETE FROM pratos WHERE prato_id = ?'''
            cursor.execute(QUERY, (prato_id,))
            conn.commit()
    
    @staticmethod
    def obterPorGerente(gerente_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''SELECT * FROM pratos WHERE gerente_id = ? ORDER BY nome ASC'''
            cursor.execute(QUERY, (gerente_id,))
            resultado = cursor.fetchall()
            return resultado