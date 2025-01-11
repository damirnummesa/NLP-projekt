from enum import Enum

class QueryType(Enum):
    INITIAL = 1,
    TRANSFORM = 2,
    VISUALIZE = 3,
            
class QueryProvider():

    prompt_queries = {}
    
    prompt_queries[QueryType.INITIAL] = """
    You are working on a LUCAS-SOIL-2018 dataset that is stored in a CSV file in './data/LUCAS-SOIL-2018.csv'.
    Given an objective %s and data description: %s, decompose the problem into 'transform' and 'visualize' subproblems. 
    Output must be dictionary with keys ('transform', 'visualize', 'column_definitions') and values like the following:
    {
        "transform": "Describe in detail part of objective that transforms the data. Include column names and operations.",
        "visualize": "Describe in detail part of objective that visualizes the data. Include column names and operations.",
        "column_definitions": "List of column definitions after transformation."
    }
    Response should only be in JSON format. DO NOT include anything else in the response.
    """
    
    prompt_queries[QueryType.TRANSFORM] = """
    You are working on a LUCAS-SOIL-2018 dataset that is stored in a CSV file in './data/LUCAS-SOIL-2018.csv'.
    You are responsible only for the transformation part of the data. DO NOT INCLUDE VISUALIZATION.
    Given an input dataframe description: %s, a transformation description: %s, the expected output format: %s, and a list of Pandas functions: %s, return only Python code to perform the transformation. 
    Return only the Python code that solves transformation. Final dataframe must be in variable named 'final_dataframe' and the dataframe must be according to expected output format. DO NOT include anything else except Python code. Output format must be '''python<code>'''.
    """
    # """
    # This is part of the data transformation query.
    # Given a description of input dataframe: %s, description of needed transformation: %s, expected output format: %s and list of Pandas functions that can applied to the data: %s, return only Python code that transforms the data. 
    # """
    
    prompt_queries[QueryType.VISUALIZE] = """
    You are working on a LUCAS-SOIL-2018 dataset that is stored in a CSV file in './data/LUCAS-SOIL-2018.csv'.
    You are responsible only for the visualization part of the data. DO NOT INCLUDE TRANSFORMATION.
    The data has been transformed and is stored in a variable named 'final_dataframe'.
    Given a description of input dataframe: %s, description of needed visualization: %s, and list of Pandas functions: %s, return only Python code to perform the visualization. Save it as plot.png. DO NOT include anything else except Python code. Output format must be '''python<code>'''.
    """
    
    

    @staticmethod
    def get_query(query_type: QueryType, objective: str, data_description: str = None, functions: list[str]=None, intermediate_data_description: str = None) -> str:
        assert query_type in QueryType
        assert objective is not None
        
        if query_type in [QueryType.INITIAL]:
            assert data_description is not None
            return QueryProvider.prompt_queries[query_type] % (objective, data_description)
        elif query_type in [QueryType.TRANSFORM]:
            assert data_description is not None
            assert functions is not None
            assert intermediate_data_description is not None
            return QueryProvider.prompt_queries[query_type] % (data_description, objective, intermediate_data_description, functions)
        elif query_type in [QueryType.VISUALIZE]:
            assert functions is not None
            assert intermediate_data_description is not None
            return QueryProvider.prompt_queries[query_type] % (intermediate_data_description, objective, functions)
            
    def wrap_with_instruction(query: str) -> str:
        return f"[INST]\n{query}\n[/INST]"