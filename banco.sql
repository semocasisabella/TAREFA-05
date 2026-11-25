PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS produtos (
    codigo TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL DEFAULT '',
    preco REAL NOT NULL CHECK (preco >= 0),
    quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
    estoque_minimo INTEGER NOT NULL DEFAULT 5 CHECK (estoque_minimo >= 0)
);

CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_codigo TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    data TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_codigo) REFERENCES produtos(codigo)
);

CREATE TABLE IF NOT EXISTS usuarios (
    usuario TEXT PRIMARY KEY,
    salt BLOB NOT NULL,
    senha_hash BLOB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_movimentacoes_produto_data
    ON movimentacoes(produto_codigo, data DESC);

CREATE TRIGGER IF NOT EXISTS movimentacao_saida_com_estoque
BEFORE INSERT ON movimentacoes
WHEN NEW.tipo = 'saida'
 AND NEW.quantidade > COALESCE(
     (SELECT quantidade FROM produtos WHERE codigo = NEW.produto_codigo), 0
 )
BEGIN
    SELECT RAISE(ABORT, 'Estoque insuficiente para esta saída.');
END;

CREATE TRIGGER IF NOT EXISTS movimentacao_atualiza_estoque
AFTER INSERT ON movimentacoes
BEGIN
    UPDATE produtos
    SET quantidade = quantidade + CASE NEW.tipo
        WHEN 'entrada' THEN NEW.quantidade
        ELSE -NEW.quantidade
    END
    WHERE codigo = NEW.produto_codigo;
END;
