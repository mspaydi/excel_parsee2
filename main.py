from sqlalchemy import create_engine
from models import metadata, my_table
from utils import DatabaseWriter, ExcelDataReader, QuerySaver


# Создаем соединение с базой данных SQLite
engine = create_engine('sqlite:///example.db', echo=True)

# Создаем таблицу в базе данных
metadata.create_all(engine)

# Парсим данные из файла Excel и добавляем столбец "дата" с случайными значениями
excel_reader = ExcelDataReader('data.xlsx')
df = excel_reader.read_data()

# Сохраняем данные в БД
db_writer = DatabaseWriter(engine)
db_writer.write_data(my_table, df)

# Сохраняем результаты запроса в txt файл
total_writer = QuerySaver(engine, 'total.txt')
total_writer.ttl_by_date_to_txt(my_table)












