from flask import Flask, render_template, redirect, session, request
from pycode.classes import Gerente, Mesa, Reserva, Prato, Menu, MenuPrato, Database

app = Flask(__name__)
app.secret_key = 'log_key'

#rota principal
@app.route('/', methods=['GET','POST'])
def pageLogin():
    if (request.method == 'POST'):
        email = request.form.get('email')
        senha = request.form.get('senha')
        resultado = Gerente.buscarGerentePorEmail(email)
        if (not resultado):
            return render_template('sys_login.html', error=1)
        else:
            gerente = Gerente(resultado)
            if (gerente.senha != senha):
                return render_template('sys_login.html', error=1)
            else:
                gerente.senha = 'secret! :)'
                session['gerente'] = gerente.toJSON()
                return redirect('/home')

    return render_template('sys_login.html', error=0)

@app.route('/logout')
def pageLogout():
    session.clear()
    return redirect('/')

#cadastro de gerente
@app.route('/cadastrar/gerente', methods=['GET','POST'])
def pageCadastrarGerente():
    if (request.method == 'POST'):
        nome_gerente = request.form.get('nome_gerente')
        nome_restaurante = request.form.get('nome_restaurante')
        email = request.form.get('email')
        senha = request.form.get('senha')
        gerente = Gerente.buscarGerentePorEmail(email)

        if (gerente):
            return render_template('sys_cadastrarGerente.html', error=1)
        else:
            Gerente.cadastrarGerente(nome_gerente, nome_restaurante, email, senha)
            return redirect('/')

    return render_template('sys_cadastrarGerente.html', error=0)

#menu principal
@app.route('/home')
def pageMenuPrincipal():
    #volta pro login caso não haja template
    gerente = session.get('gerente')
    if (not gerente):
        return redirect('/')
    
    qntMesas = Gerente.obterQNTMesasPorGerente(gerente['gerente_id'])
    qntReservas = Gerente.obterQNTReservaPorGerente(gerente['gerente_id'])
    qntPratos = Gerente.obterQNTReservaPorGerente(gerente['gerente_id'])

    return render_template('main_menuPrincipal.html', error=0, qntMesas=qntMesas, qntReservas=qntReservas, qntPratos=qntPratos)

#rota geral para cadastros
@app.route('/cadastrar/<item>', methods=['GET', 'POST'])
def pageMenuGenericAdd(item:str = 'none'):
    #volta pro login caso não haja template
    gerente = session.get('gerente')
    if (not gerente):
        return redirect('/')
    
    error = 0

    if (request.method == 'POST'):
        match (item):
            case "mesa":
                gerente_id = request.form.get('gerente_id')
                numero = request.form.get('numero')
                Mesa.cadastrar(gerente_id, numero)
                error = -1

            case "reserva":
                cliente_nome = request.form.get('cliente_nome')
                cliente_cpf = request.form.get('cliente_cpf')
                data = request.form.get('data')
                hora = request.form.get('hora')
                mesa_id = request.form.get('mesa_id')
                Reserva.cadastrar(cliente_nome, cliente_cpf, data, hora, mesa_id)
                error = -1

            case "prato":
                gerente_id = request.form.get('gerente_id')
                nome = request.form.get('nome')
                ingredientes = request.form.get('ingredientes')
                receita = request.form.get('receita')
                Prato.cadastrar(gerente_id, nome, ingredientes, receita)
                error = -1

            case "menu":
                gerente_id = request.form.get('gerente_id')
                nome = request.form.get('nome')
                Menu.cadastrar(gerente_id, nome)
                error = -1

            case _:
                print('Não encontrado')

    try:
        resultado = Mesa.obterPorGerente(gerente['gerente_id'])
        mesas = []
        for r_mesa in resultado:
            mesas.append(Mesa(r_mesa).toJSON())
        return render_template(f'''add_{item}.html''', error=error, gerente=gerente, mesas=mesas)
    except:
        print()
        return redirect('/home')
    
@app.route('/deletar/<item>', methods=['POST'])
def pageMenuGenericRemove(item:str = 'none'):
    #volta pro login caso não haja template
    gerente = session.get('gerente')
    if (not gerente):
        return redirect('/')
    
    match (item):
        case "mesa":
            mesa_id = request.form.get('mesa_id')
            if (len(Mesa.obterReservasComMesa(mesa_id)) == 0):
                Mesa.excluir(mesa_id)
            else:
                resultado = Mesa.obterPorGerente(gerente['gerente_id'])
                mesas = []
                for data in resultado:
                    mesas.append(Mesa(data).toJSON())
                return render_template(f'''add_{item}.html''', error=1, gerente=gerente, mesas=mesas)
            
        case "reserva":
            reserva_id = request.form.get('reserva_id')
            Reserva.excluir(reserva_id)
            return redirect('/visualizar/reserva')
        
        case "prato":
            prato_id = request.form.get('prato_id');
            Prato.excluir(prato_id)
            return redirect('/visualizar/prato')
        
        case "menu":
            menu_id = request.form.get('menu_id');
            Menu.excluir(menu_id)
            return redirect('/visualizar/menu')
        
        case "rel":
            menu_id = request.form.get('menu_id');
            prato_id = request.form.get('prato_id');
            MenuPrato.excluir(menu_id, prato_id)
            return redirect('/visualizar/menu')

        case _:
            print('Não encontrado')
            return redirect('/home')

    return redirect(f'/cadastrar/{item}')

@app.route('/visualizar/<item>', methods=['GET', 'POST'])
def pageMenuGenericView(item):
    #volta pro login caso não haja template
    gerente = session.get('gerente')
    if (not gerente):
        return redirect('/')

    match (item):
        case "reserva":
            #reservas em json
            resultado = Reserva.obterPorGerente(gerente['gerente_id'])
            reservas = []
            for data in resultado:
                reservas.append(Reserva(data).toJSON())

            return render_template(f'''view_{item}.html''', error=0, gerente=gerente, reservas=reservas)

        case "prato":
            resultado = Prato.obterPorGerente(gerente['gerente_id'])
            pratos = []
            for data in resultado:
                pratos.append(Prato(data).toJSON())
            
            return render_template(f'''view_{item}.html''', error=0, gerente=gerente, pratos=pratos)

        case "menu":
            resultado = Prato.obterPorGerente(gerente['gerente_id'])
            pratos = []
            for data in resultado:
                pratos.append(Prato(data).toJSON())

            resultado = Menu.obterPorGerente(gerente['gerente_id'])
            menus = []
            for data in resultado:
                menus.append(Menu(data).toJSON())

            resultado = MenuPrato.obterPorGerente(gerente['gerente_id'])
            menusPratos = []
            print("Menus Pratos:\n")
            for data in resultado:
                print(data)
                menusPratos.append(MenuPrato(data).toJSON())

            return render_template(f'''view_{item}.html''', error=0, gerente=gerente, pratos=pratos, menus=menus, menusPratos=menusPratos)


        case _:
            print('Não encontrado')
            return redirect('/home')

    return redirect(f'/visualizar/{item}')

@app.route('/associar-prato-menu', methods=['POST'])
def addPratoMenu():
    gerente = session.get('gerente')
    if (not gerente):
        return redirect('/')
    
    menu_id = request.form.get('menu_id');
    prato_id = request.form.get('prato_id');
    preco = request.form.get('preco');
    MenuPrato.cadastrar(menu_id, prato_id, preco)

    return redirect('/visualizar/menu')


if __name__ == '__main__':
    app.run(debug=True)