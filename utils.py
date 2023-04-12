from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import date, timedelta
from random import randint


class DatabaseWriter:
    def __init__(self, engine):
        self.engine = engine

    def write_data(self, tbl, df):
        df.to_sql(tbl.name, con=self.engine, if_exists='replace', index=False)


class ExcelDataReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        df = pd.read_excel(self.file_path, header=2,names=['id',
                                                           'company',
                                                           'fact_Qlic_data1',
                                                           'fact_Qlic_data2',
                                                           'fact_Qoil_data1',
                                                           'fact_Qoil_data2',
                                                           'forecast_Qlic_data1',
                                                           'forecast_Qlic_data2',
                                                           'forecast_Qoil_data1',
                                                           'forecast_Qoil_data2'
                                                           ]
                           )
        date_list = [date(2022, 1, 1) + timedelta(days=randint(10, 20)) for _ in range(len(df))]
        df.insert(2, 'date', date_list)
        return df


class QuerySaver:
    def __init__(self, engine, file_path):
        self.engine = engine
        self.file_path = file_path

    def ttl_by_date_to_txt(self, tbl):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(
            tbl.c.date,
            func.sum(tbl.c.fact_Qoil_data1 + tbl.c.fact_Qoil_data2).label('total_Qoil_fact'),
            func.sum(tbl.c.fact_Qlic_data1 + tbl.c.fact_Qlic_data2).label('total_Qlic_fact'),
            func.sum(tbl.c.forecast_Qoil_data1 + tbl.c.forecast_Qoil_data2).label('total_Qoil_forecast'),
            func.sum(tbl.c.forecast_Qlic_data1 + tbl.c.forecast_Qlic_data2).label('total_Qlic_forecast')
        ).group_by(tbl.c.date).all()
        session.close()
        with open(self.file_path, 'w') as f:
            f.write(f"Date\t\tQoil_ttl_fact\tQliq_ttl_fact\tQliq_ttl_frcst\tQliq_ttl_frcst\n")
            for row in result:
                f.write(f"{row.date}\t\t{row.total_Qoil_fact}\t\t\t\t{row.total_Qlic_fact}\t"
                        f"\t\t\t{row.total_Qoil_forecast}\t\t\t\t{row.total_Qoil_forecast}\n")



