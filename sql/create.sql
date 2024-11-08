CREATE TABLE IF NOT EXISTS gerentes (
    gerente_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome_gerente TEXT NOT NULL,
    nome_restaurante TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pratos (
    prato_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    gerente_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    ingredientes TEXT NOT NULL,
    receita TEXT NOT NULL,
    FOREIGN KEY (gerente_id) REFERENCES gerentes(gerente_id)
);

CREATE TABLE IF NOT EXISTS mesas (
    mesa_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    gerente_id INTEGER NOT NULL,
    numero TEXT NOT NULL,
    FOREIGN KEY (gerente_id) REFERENCES gerentes(gerente_id)
);

CREATE TABLE IF NOT EXISTS menus (
    menu_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    gerente_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    FOREIGN KEY (gerente_id) REFERENCES gerentes(gerente_id)
);

CREATE TABLE IF NOT EXISTS reservas (
    reserva_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    cliente_nome TEXT NOT NULL,
    cliente_cpf TEXT NOT NULL,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    mesa_id INTEGER NOT NULL,
    FOREIGN KEY (mesa_id) REFERENCES mesas(mesa_id)
);

CREATE TABLE IF NOT EXISTS menus_pratos (
    rel_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    menu_id INTEGER NOT NULL,
    prato_id INTEGER NOT NULL,
    preco REAL NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menus(menu_id),
    FOREIGN KEY (prato_id) REFERENCES pratos(prato_id)
);