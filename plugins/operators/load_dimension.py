from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self, redshift_conn_id="", debug=False, sqls=None, *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.debug = debug
        self.stage_event_sqls = sqls


    def execute(self, context):

        self.log.info('Starting LoadDimensionOperator, self.redshift_conn_id = '+ self.redshift_conn_id)
        
        if not self.debug:
            redshift_hook = PostgresHook(self.redshift_conn_id)
        
        
        if not self.debug:
            for query in self.stage_event_sqls:
                redshift_hook.run(query)
            
        else:
            for query in self.stage_event_sqls:
                self.log.info(f'redshift_hook.run({query})')

        
        self.log.info('Leaving LoadDimensionOperator...')
