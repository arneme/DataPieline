from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self, redshift_conn_id="", table="", debug=False, aws_credentials_id="", *args, **kwargs):


        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.aws_credentials_id = aws_credentials_id
        self.debug = debug


    def execute(self, context):
        self.log.info('Starting StageToRedshiftOperator, self.redshift_conn_id = '+self.redshift_conn_id+' table is: '+self.table)
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        self.log.info('In StageToRedshiftOperator credentials.access_key: ' + credentials.access_key)
        if not self.debug:
            redshift_hook = PostgresHook(self.redshift_conn_id)
        # Create and copy data from S3 into the staging_events_table
        # First create the table if it does not already exist and then
        # copy from S3 to the staging_events_table using Redshift SQL COPY
        self.log.info('Drop: ' + SparkifySqlQueries.staging_events_table_drop)
        
        self.log.info('Leaving StageToRedshiftOperator...')
