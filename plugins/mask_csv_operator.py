from airflow.models import BaseOperator

class MaskCSVOperator(BaseOperator):
    
    def __init__(self, input_file:str, output_fie:str, separator:str, column:str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.input_file = input_file
        self.output_file = output_fie
        self.separator = separator
        self.column = column
        
    def execute(self, context):
        file = ''
        with open(self.put_file,'r') as f:
            for data in f.readlines():
                fields = data.strip('\n').split(self.separator)
                fields(self.column) = '*******'
                fiel += self.separator.join(fields) + '\n'
                
            with open(self.output_file,'r') as f:
                f.write(file)










