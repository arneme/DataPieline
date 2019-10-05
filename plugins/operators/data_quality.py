from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):


    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, redshift_conn_id="", debug="", sparkify_tables=None, sqls=None, *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.debug = debug
        self.sparkify_tables = sparkify_tables
        self.sqls = sqls


    def execute(self, context):
        # Check if all tables have data in them

        if not self.debug:
            redshift_hook = PostgresHook(self.redshift_conn_id)
            for table in self.sparkify_tables:
                if not self.debug:
                    query = self.sqls.format(table)
                    records = redshift_hook.get_records(query)
                    self.log.info(f'Found {records} in {table}')
                    if records is None or len(records[0]) < 1:
                        self.log.error(f"No records found in {table}")
                        raise ValueError(f'No records found in {table}')
                    else:
                        self.log.info(f"Data quality check passed: found {records} in {table}")
        else:
            for table in self.sparkify_tables:
                query = self.sqls.format(table)
                self.log.info(f'redshift_hook.run({query})')

            