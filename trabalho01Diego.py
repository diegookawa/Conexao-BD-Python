import sys
import csv
import MySQLdb
import psycopg2

def main(args):

    args = args[1:]
    tipoBancoDados = args[0]
    endereco = args[1]
    usuario = args[2]
    senha = args[3]
    nomeBancoDados = args[4]
    
    database = conectarBancoDados(tipoBancoDados, endereco, usuario, senha, nomeBancoDados)

    cursor = database.cursor()

    semestre = input()
    listarDisciplinasProfessor(cursor, nomeBancoDados, semestre)

    encerrarConexao(cursor, database)

def conectarBancoDados(tipoBancoDados, endereco, usuario, senha, nomeBancoDados):

    try:

        if tipoBancoDados.lower() == "mysql":

            database = MySQLdb.connect(
                endereco,
                usuario,
                senha,
                nomeBancoDados)

        elif tipoBancoDados.lower() == "postgresql":

            database = psycopg2.connect(
                host = endereco,
                user = usuario, 
                password = senha, 
                database = nomeBancoDados)

        else:
            print("Erro ao escolher a database")

    except Exception as e:

        print("Erro: ", e)
        return None

    return database


def listarDisciplinasProfessor(cursor, nomeBancoDados, semestre):

    cursor.execute(f"""
        SELECT instructor.id, instructor.name, course.course_id, course.title, section.room_number, teaches.semester
            FROM instructor
            JOIN teaches on teaches.id = instructor.id
            JOIN section on section.sec_id = teaches.sec_id
            JOIN course on section.course_id = course.course_id
            where teaches.semester = '{semestre}'
            order by instructor.id;
        """)

    colunas = cursor.fetchall()
    print(colunas)

def encerrarConexao(cursor, database):

    cursor.close()
    database.close()

if __name__ == '__main__':
    main(sys.argv)