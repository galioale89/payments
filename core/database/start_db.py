import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='64l10770'
    )
    print(f'conn {conn}')
except mysql.connector.Error as err:
    if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
        print('There is something wrong with username and password!')
    else:
        print(err)


cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS `mekal`")
cursor.execute("CREATE DATABASE `mekal`")
cursor.execute("USE `mekal`")

TABLES = {}

TABLES['Supplier'] = ('''
CREATE TABLE `supplier` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `address` varchar(100),
    `contact` varchar(50),
    `phone` varchar(12),
        PRIMARY KEY (`id`)
    )  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['User'] = ('''
CREATE TABLE `user` (
    `name` varchar(100) NOT NULL,
    `nickname` varchar(10) NOT NULL,
    `password` varchar(100) NOT NULL,
    PRIMARY KEY (`nickname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Payment'] = ('''
CREATE TABLE `payment` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `type` int(1) NOT NULL,
    `code` varchar(20), 
    `description` varchar(200),
    `value` decimal(8,2),
    `pay_date` datetime,
    `due_date` datetime,
    `id_supplier` integer,
    PRIMARY KEY (`id`),
    CONSTRAINT fk_pay_supplier FOREIGN KEY (`id_supplier`) REFERENCES Supplier(`id`) 
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
    table_sql = TABLES[table_name]
    try:
        print('Creating tables {}:'.format(table_name),end=' ')
        cursor.execute(table_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Already done.')
        else:
             print(err.msg)
    else:
        print('OK')

# insert users
user_sql = 'INSERT INTO user (name, nickname, password) VALUES (%s,%s,%s)'
user = [("Alexandre Galiotto", "ale", generate_password_hash("mekal").decode('utf-8'))]
cursor.executemany(user_sql, user)
cursor.execute('select * from mekal.User')
print('-------------- Users ----------')
for user in cursor.fetchall():
    print(user[1])

# insert suppliers
supplier_sql = ('INSERT INTO Supplier (name, address, contact, phone) VALUES (%s,%s,%s,%s)')
suppliers = [
    ('Fornecedor Padrão', 'Rua Padrão', 'Vendedor Padrão', '5555555555')
]
cursor.executemany(supplier_sql, suppliers)
cursor.execute('select * from mekal.supplier')
print('-------------- Suppliers ----------')
for supplier in cursor.fetchall():
    print(supplier[1])

# insert payments
payment_sql = (
    'INSERT INTO payment (description, type, code, value, pay_date, due_date) VALUES (%s, %s,%s,%s,%s,%s)')

payments = [('Pagamento Teste', 1,'123456', 100.00, '2020-01-01', '2020-01-01')]

cursor.executemany(payment_sql, payments)
cursor.execute('select * from mekal.payment')
print('-------------- Payments ----------')
for payment in cursor.fetchall():
    print(payment[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()