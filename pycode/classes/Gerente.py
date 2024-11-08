from .Database import Database
class Gerente:
    def __init__(self, data:tuple) -> None:
        self.gerente_id = data[0]
        self.nome_gerente = data[1]
        self.nome_restaurante = data[2]
        self.email = data[3]
        self.senha = data[4]
    
    def toJSON(self):
        return {
            "gerente_id":self.gerente_id,
            "nome_gerente":self.nome_gerente,
            "nome_restaurante":self.nome_restaurante,
            "email":self.email,
            "senha":self.senha
        }

    @staticmethod
    def cadastrarGerente(nome_gerente,nome_restaurante,email,senha):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''INSERT INTO gerentes(nome_gerente,nome_restaurante,email,senha) VALUES (?,?,?,?)'''
            cursor.execute(QUERY, (nome_gerente, nome_restaurante, email, senha))
            conn.commit()

    @staticmethod
    def buscarGerentePorEmail(email):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''SELECT * FROM gerentes WHERE email = ?'''
            cursor.execute(QUERY, (email,))
            resultado = cursor.fetchall()
            try:
                return resultado[0] #caso haja
            except:
                return False #caso nao haja
    
    @staticmethod
    def obterQNTMesasPorGerente(gerente_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''SELECT COUNT(numero) FROM mesas WHERE gerente_id = ?'''
            cursor.execute(QUERY, (gerente_id,))
            resultado = cursor.fetchall()
            return resultado[0][0]
        
    @staticmethod
    def obterQNTReservaPorGerente(gerente_id):
        with Database() as conn:
            cursor = conn.cursor()
            QUERY = '''SELECT COUNT(*) FROM mesas AS m JOIN reservas AS r ON m.mesa_id = r.mesa_id WHERE gerente_id = ?'''
            cursor.execute(QUERY, (gerente_id,))
            resultado = cursor.fetchall()
            return resultado[0][0]