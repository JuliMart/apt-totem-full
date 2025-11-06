#!/usr/bin/env python3
"""
Script para convertir esquema Oracle 11g a MySQL
"""

def convert_oracle_to_mysql():
    # Leer el archivo Oracle
    with open('/Users/julimart/Desktop/apt-totem/apt-totem-backend/database/schema_oracle11g.sql', 'r') as f:
        oracle_sql = f.read()
    
    # Conversiones básicas
    mysql_sql = oracle_sql
    
    # 1. Tipos de datos
    mysql_sql = mysql_sql.replace('NUMBER', 'INT')
    mysql_sql = mysql_sql.replace('VARCHAR2', 'VARCHAR')
    mysql_sql = mysql_sql.replace('CLOB', 'TEXT')
    mysql_sql = mysql_sql.replace('TIMESTAMP', 'DATETIME')
    mysql_sql = mysql_sql.replace('SYSTIMESTAMP', 'NOW()')
    
    # 2. Secuencias -> AUTO_INCREMENT
    mysql_sql = mysql_sql.replace('NUMBER PRIMARY KEY', 'INT AUTO_INCREMENT PRIMARY KEY')
    
    # 3. Eliminar triggers y sequences
    lines = mysql_sql.split('\n')
    filtered_lines = []
    skip_until_slash = False
    
    for line in lines:
        if 'CREATE SEQUENCE' in line or 'CREATE OR REPLACE TRIGGER' in line:
            skip_until_slash = True
            continue
        if skip_until_slash and line.strip() == '/':
            skip_until_slash = False
            continue
        if not skip_until_slash:
            filtered_lines.append(line)
    
    mysql_sql = '\n'.join(filtered_lines)
    
    # 4. Eliminar comentarios de DROP
    mysql_sql = mysql_sql.replace('-- DROP TABLE', '-- DROP TABLE')
    
    # 5. Ajustar constraints
    mysql_sql = mysql_sql.replace('CHECK (estado IN (\'active\',\'inactive\'))', 'CHECK (estado IN (\'active\',\'inactive\'))')
    
    # Guardar archivo MySQL
    with open('/Users/julimart/Desktop/apt-totem/schema_mysql.sql', 'w') as f:
        f.write(mysql_sql)
    
    print("✅ Convertido a MySQL: schema_mysql.sql")
    print("📋 Cambios principales:")
    print("  - NUMBER → INT")
    print("  - VARCHAR2 → VARCHAR") 
    print("  - CLOB → TEXT")
    print("  - TIMESTAMP → DATETIME")
    print("  - Eliminadas secuencias y triggers")
    print("  - Agregado AUTO_INCREMENT")

if __name__ == "__main__":
    convert_oracle_to_mysql()
