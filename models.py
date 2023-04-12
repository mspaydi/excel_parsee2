from sqlalchemy import Table, Column, Integer, String, MetaData


metadata = MetaData()
my_table = Table('oil_liq_data', metadata,
                Column('id', Integer, primary_key=True),
                Column('date', String),
                Column('company', String),
                Column('fact_Qlic_data1', Integer),
                Column('fact_Qlic_data2', Integer),
                Column('fact_Qoil_data1', Integer),
                Column('fact_Qoil_data2', Integer),
                Column('forecast_Qlic_data1', Integer),
                Column('forecast_Qlic_data2', Integer),
                Column('forecast_Qoil_data1', Integer),
                Column('forecast_Qoil_data2', Integer)
                )
