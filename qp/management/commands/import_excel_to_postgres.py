import pandas as pd
from sqlalchemy import create_engine
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Upload Excel data to PostgreSQL'

    
    def handle(self, *args, **kwargs):        
        # Load the Excel file with multiple sheets
        excel_file = r'D:\vikram\mind2i\Question Module\document\MIND2i_questions.xlsx'
        # "D:\vikram\mind2i\Question Module\document\MIND2i_questions.xlsx"
        sheets_dict = pd.read_excel(excel_file, sheet_name=None, header=3)

        # PostgreSQL connection string
        db_url = 'postgresql://postgres:vikrampsg@localhost:5432/Sample1'
        engine = create_engine(db_url)

        # Upload to PostgreSQL
        def upload_to_postgres(df, table_name, engine):
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Table '{table_name}' uploaded successfully.")

        for sheet_name, df in sheets_dict.items():
            # Remove spaces and special characters from sheet names for valid table names
            table_name = sheet_name.replace(' ', '_').lower()

            # Upload each sheet to a PostgreSQL table
            upload_to_postgres(df, table_name, engine)
