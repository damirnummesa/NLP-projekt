from enum import Enum

class QueryType(Enum):
    TYPE = 0,
    TRANSFORM = 2,
    VISUALIZE_PRINT = 3,
    VISUALIZE_GRAPH = 4,
    VISUALIZE_MAP = 5,
            
class QueryProvider():

    prompt_queries = {}
    
    prompt_queries[QueryType.TYPE] = """
    You are a query reasoner model tasked with analyzing user queries related to geospatial data transformations and visualizations using GeoDataFrames (GDF). 
    Your job is to determine the appropriate type of response required for the following query: '''%s'''. 
    Based on the query analysis, classify it into one of the following categories:

    - print: For simple transformations whose results should be directly printed.
    - graph: For queries that require visualizing transformed data as plots or graphs (e.g., histograms, scatter plots).
    - map: For queries requiring overlaying transformed results on a map of Europe already loaded as a GeoDataFrame (europe_gdf).
    When classifying the query:

    Consider whether the result is purely textual or numerical (print).
    Identify queries requesting trends, distributions, or patterns suitable for graphing (graph).
    Detect if spatial visualizations or geographical overlays are explicitly or implicitly needed (map).
    Your response should only contain the category name (print, graph, or map) with no additional information or explanation.
    """
    
    prompt_queries[QueryType.TRANSFORM] = """
    You are a code generation model specialized in transforming geospatial data stored in a GeoDataFrame (data_gdf). 
    Based on the objective, your task is to provide only the Python code required to perform the specified transformations.

    Objective:
    %s
    
    Data Context:
    The input GeoDataFrame has the following columns:
    %s

    Available Python Packages:
    You have access to the following Python packages for data transformations and analysis:

    import pandas as pd
    from sklearn.cluster import KMeans
    import scipy.stats as stats
    import sklearn as sk 

    Instructions:
    All transformations should be performed on the GeoDataFrame data_gdf.
    Write only the Python code required for the transformation.
    Ignore any instructions for outputting or displaying the results.
    Store the transformed results in a new GeoDataFrame called transformed_gdf.
    Ensure the code is concise, valid, and leverages the appropriate packages listed above.
    Avoid any additional explanations or comments in the code.
    """

    prompt_queries[QueryType.VISUALIZE_PRINT] = """
    You are a code generation model specialized in printing results for transformed geospatial data stored in the GeoDataFrame transformed_gdf.

    Query Context:
    Initial query: %s
    
    Data has already been transformed and is available in transformed_gdf.
    The GeoDataFrame has the following structure based on transformed_gdf.info():
    %s
    
    Instructions:
    Ignore any transformation instructions.
    Focus solely on printing the transformed data in a meaningful and concise way based on the query results.
    Provide only the code required to print the result. Avoid any additional comments or explanations.
    """
    

    prompt_queries[QueryType.VISUALIZE_GRAPH] = """
    You are a code generation model specialized in creating data visualizations for transformed geospatial data stored in the GeoDataFrame transformed_gdf.

    Query Context:
    Initial query: %s
    
    Data has already been transformed and is available in transformed_gdf.
    The GeoDataFrame has the following structure based on transformed_gdf.info():
    %s
    
    Available Python Packages:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    Instructions:
    Ignore any transformation instructions.
    Focus solely on generating a plot or graph based on the transformed data that effectively visualizes the query results.
    The code should only produce the graph without additional comments or explanations.
    Ensure the graph conveys meaningful insights through axis labels, titles, and legend when relevant.
    Provide only the code. Avoid any additional comments or explanations.
    """
    

    prompt_queries[QueryType.VISUALIZE_MAP] = """
    You are a code generation model specialized in creating map-based visualizations for transformed geospatial data stored in the GeoDataFrame transformed_gdf.
    All data is from Europe.
    
    Query Context:
    Initial query: %s
    
    Data has already been transformed and is available in transformed_gdf.
    The GeoDataFrame has the following structure based on transformed_gdf.info():
    %s
    
    Available Python Packages:
    import geopandas as gpd
    import matplotlib.pyplot as plt
    
    Instructions:
    Ignore any transformation instructions.
    Focus solely on generating a map-based visualization by overlaying data from transformed_gdf on a map of Europe.
    The map of Europe is already loaded in europe_gdf. It can be set as the base using the following line:
    europe_gdf.plot(ax=ax, edgecolor='black', color='lightgray')
    
    Only plot the data locations from transformed_gdf.
    Other available information from the data can be used to color or style the plotted locations meaningfully.
    Provide only the code for generating the map, without comments or explanations
    """

    
    @staticmethod
    def get_query(query_type: QueryType, objective: str = None, data_description: str = None, functions: list[str]=None, intermediate_data_description: str = None, europe_gdf_description: str = None) -> str:
        assert query_type in QueryType
        assert objective is not None
        
        if query_type in [QueryType.TYPE]:
            return QueryProvider.prompt_queries[query_type] % (objective)
        elif query_type in [QueryType.TRANSFORM]:
            assert data_description is not None
            return QueryProvider.prompt_queries[query_type] % (objective, data_description)
        elif query_type in [QueryType.VISUALIZE_PRINT]:
            assert intermediate_data_description is not None
            return QueryProvider.prompt_queries[query_type] % (objective, intermediate_data_description)
        elif query_type in [QueryType.VISUALIZE_GRAPH]:
            assert intermediate_data_description is not None
            return QueryProvider.prompt_queries[query_type] % (objective, intermediate_data_description)
        elif query_type in [QueryType.VISUALIZE_MAP]:
            assert intermediate_data_description is not None
            return QueryProvider.prompt_queries[query_type] % (objective, intermediate_data_description)
            
    def wrap_with_instruction(query: str) -> str:
        return f"[INST]\n{query}\n[/INST]"