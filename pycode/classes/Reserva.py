from .Database import Database
class Reserva:
    def __init__(self, data:tuple) -> None:
        self.reserva_id = data[0]
        self.cliente_nome = data[1]
        self.cliente_cpf = data[2]
        self.data = data[3]
        self.hora = data[4]
        self.mesa_id = data[5]
        try:
            self.numero = data[6]
        except:
            self.numero = -1
    
    def toJSON(self):
        return {
            "reserva_id":self.reserva_id,
            "cliente_nome":self.cliente_nome, 
            "cliente_cpf":self.cliente_cpf,
            "data":self.data,
            "hora":self.hora,
            "mesa_id":self.mesa_id
        } if (int(self.numero) < 0) else {
            "reserva_id":self.reserva_id,
            "cliente_nome":self.cliente_nome, 
            "cliente_cpf":self.cliente_cpf,
            "data":self.data,
            "hora":self.hora,
            "mesa_id":self.mesa_id,
            "numero":self.numero
        }
    
    @staticmethod
    def cadastrar(cliente_nome, cliente_cpf, data, hora, mesa_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''INSERT INTO reservas(cliente_nome, cliente_cpf, data, hora, mesa_id) VALUES (?,?,?,?,?)'''
            cursor.execute(QUERY, (cliente_nome, cliente_cpf, data, hora, mesa_id))
            conn.commit()

    @staticmethod
    def obterPorGerente(gerente_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''SELECT 
                r.reserva_id,
                r.cliente_nome,
                r.cliente_cpf,
                r.data,
                r.hora,
                m.mesa_id,
                m.numero
              FROM mesas AS m JOIN reservas AS r ON m.mesa_id = r.mesa_id 
              WHERE m.gerente_id = ?
              ORDER BY r.data ASC'''
            cursor.execute(QUERY, (gerente_id,))
            resultado = cursor.fetchall()
            return resultado
    
    def excluir(reserva_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''DELETE FROM reservas WHERE reserva_id = ?'''
            cursor.execute(QUERY, (reserva_id,))
            conn.commit()