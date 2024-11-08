from .Database import Database
class Mesa:
    def __init__(self, data:tuple) -> None:
        self.mesa_id = data[0]
        self.gerente_id = data[1]
        self.numero = data[2]
    
    def toJSON(self):
        return {
            "mesa_id":self.mesa_id,
            "gerente_id":self.gerente_id, 
            "numero":self.numero,
        }
    
    @staticmethod
    def cadastrar(gerente_id, numero):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''INSERT INTO mesas(gerente_id, numero) VALUES (?,?)'''
            cursor.execute(QUERY, (gerente_id, numero))
            conn.commit()
    
    @staticmethod
    def excluir(mesa_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''DELETE FROM mesas WHERE mesa_id = ?'''
            cursor.execute(QUERY, (mesa_id,))
            conn.commit()

    @staticmethod
    def obterPorGerente(gerente_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''SELECT * FROM mesas WHERE gerente_id = ? ORDER BY numero ASC'''
            cursor.execute(QUERY, (gerente_id,))
            resultado = cursor.fetchall()
            return resultado
    
    @staticmethod
    def obterReservasComMesa(mesa_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''SELECT * FROM reservas WHERE mesa_id = ?'''
            cursor.execute(QUERY, (mesa_id,))
            resultado = cursor.fetchall()
            return resultado