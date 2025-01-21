from enum import Enum

class QueryType(Enum):
    INITIAL = 1,
    TRANSFORM = 2,
    VISUALIZE = 3,
            
class QueryProvider():

    prompt_queries = {}
    
    prompt_queries[QueryType.INITIAL] = """
    You are working with the LUCAS-SOIL-2018 dataset that contains data from Europe.
    LUCAS-SOIL-2018 dataset is loaded into a geopandas GeoDataFrame called 'data_gdf'.
    Given:
    1. An objective: %s
    2. A description of the 'data_gdf' GeoDataFrame: %s
    Decompose the objective into two subproblems: 'transform' and 'visualize'. 

    Your response must be a dictionary with the following structure:
    {
        "transform": "A single string describing, in detail, the part of the objective that transforms the data. Results are in 'transformed_gdf' GeoDataFrame. Include specific column names and operations. Do NOT include any code.",
        "visualize": "A single string describing, in detail, the part of the objective that visualizes specified data from 'transformed_gdf' GeoDataFrame. Visualizations may include printing some result, outputting graphs or overlaying some data on map of Europe. Include specific column names and operations. Do NOT include any code."
    }

    **Output Requirements:**
    - Response must ONLY be in JSON format.
    - Use the exact format: '''json<content>'''
    - DO NOT include anything else in the response.
    """

    prompt_queries[QueryType.TRANSFORM] = """
    You are working with the LUCAS-SOIL-2018 dataset that contains data from Europe.
    LUCAS-SOIL-2018 dataset is loaded into a geopandas GeoDataFrame called 'data_gdf'.
    Your task is to handle ONLY the transformation part of the data. DO NOT include visualization.

    Given:
    1. A description of the 'data_gdf' GeoDataFrame: %s
    2. A detailed transformation description: %s
    3. A list of available functions: %s

    Write Python code to perform the required transformation. Follow these rules:
    - Store the transformed data in a variable called 'transformed_data', always keep geometry column.
    - Map of Europe is loaded as 'europe_gdf' GeoDataFrame.
    - Use only the provided descriptions and functions to guide the transformation.
    - Write all code outside of functions.
    - Result of the transformation should be a 'transformed_data' GeoDataFrame.
    - DO NOT create additional data or output anything.
    - Write ONLY the code necessary for the transformation. 

    **Output Requirements:**
    - Return only Python code in the format: '''python<code>'''
    - DO NOT include anything else in the response.
    """

    prompt_queries[QueryType.VISUALIZE] = """
    You are working with a transformed LUCAS-SOIL-2018 dataset that contains data from Europe. 
    Transformed LUCAS-SOIL-2018 dataset is loaded into a geopandas GeoDataFrame called 'transformed_data'.
    Your task is to handle ONLY the visualization part of the data. DO NOT include transformation.

    Given:
    1. A description of the 'transformed_data' GeoDataFrame: %s
    2. A description of the 'europe_gdf' GeoDataFrame: %s
    2. A detailed visualization description: %s
    3. A list of available functions: %s

    Write Python code to perform the required visualization. Follow these rules:   
    - Start with 'transformed_data' GeoDataFrame. 
    - Don't load map of Europe, it is already loaded as 'europe_gdf' GeoDataFrame.
    - 'europe_gdf' GeoDataFrame contains only borders of countries as polygons and should be only used as base map.
    - When visualizing data on a map, set 'europe_gdf' as the base map with following line: europe_gdf.plot(ax=ax, edgecolor='black', color='lightgray').
    - When plotting on map, if no specific column is mentioned visualize only data location with following line: transformed_data.plot(ax=ax, markersize=5, ...).
    - Add legends, titles, and labels as needed for better visualization.
    - Use only the provided descriptions and functions to guide the visualization.
    - Write all code outside of functions.
    - DO NOT include transformation or unrelated operations.
    - Write ONLY the code necessary for the visualization.

    **Output Requirements:**
    - Return only Python code in the format: '''python<code>'''
    - DO NOT include anything else in the response.
    """

    
    @staticmethod
    def get_query(query_type: QueryType, objective: str, data_description: str = None, functions: list[str]=None, intermediate_data_description: str = None, europe_gdf_description: str = None) -> str:
        assert query_type in QueryType
        assert objective is not None
        
        if query_type in [QueryType.INITIAL]:
            assert data_description is not None
            return QueryProvider.prompt_queries[query_type] % (objective, data_description)
        elif query_type in [QueryType.TRANSFORM]:
            assert data_description is not None
            assert functions is not None
            return QueryProvider.prompt_queries[query_type] % (data_description, objective, functions)
        elif query_type in [QueryType.VISUALIZE]:
            assert functions is not None
            assert intermediate_data_description is not None
            assert europe_gdf_description is not None
            return QueryProvider.prompt_queries[query_type] % (intermediate_data_description, europe_gdf_description, objective, functions)
            
    def wrap_with_instruction(query: str) -> str:
        return f"[INST]\n{query}\n[/INST]"