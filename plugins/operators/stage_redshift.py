from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from helpers import SparkifySqlQueries

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self, redshift_conn_id="", debug=False, delete="", sqls=None, *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.debug = debug
        self.delete_sql = delete
        self.stage_event_sqls = sqls


    def execute(self, context):
        # Create and copy data from S3 into the staging_events_table
        # First create the table if it does not already exist and then
        # copy from S3 to the staging_events_table using Redshift SQL COPY

        self.log.info('Starting StageToRedshiftOperator, self.redshift_conn_id = '+ self.redshift_conn_id)
        
        if not self.debug:
            redshift_hook = PostgresHook(self.redshift_conn_id)
            # Check to see if we 
            if self.delete_sql != "":
                redshift_hook.run(self.delete_sql)
            for query in self.stage_event_sqls:
                redshift_hook.run(query)
            
        else:
            if self.delete_sql != "":
                self.log.info(self.delete_sql)
            for query in self.stage_event_sqls:
                self.log.info(f'redshift_hook.run({query})')
        
        self.log.info('Leaving StageToRedshiftOperator...')
