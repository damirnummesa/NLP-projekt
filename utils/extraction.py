import re
import json

def clean_python_code(code_string):
    """
    Removes comments, import statements, and print statements from a Python code string.
    """
    # Remove comments (single-line and multi-line)
    # code_string = re.sub(r'#.*', '', code_string)  # Single-line comments
    code_string = re.sub(r'""".*?"""|\'\'\'.*?\'\'\'', '', code_string, flags=re.DOTALL)  # Multi-line comments

    # Remove import statements
    code_string = re.sub(r'^\s*import .*|^\s*from .* import .*', '', code_string, flags=re.MULTILINE)

    # Remove print statements
    code_string = re.sub(r'^\s*print\(.*\)\s*$', '', code_string, flags=re.MULTILINE)

    # Remove empty lines caused by the removals
    code_string = re.sub(r'\n\s*\n', '\n', code_string)

    return code_string.strip()

def get_description_extraction_function_string(cleaned_transform_code: str) -> str:
    get_transformed_data_description_header = "def get_transformed_data_description(data_gdf: gpd.GeoDataFrame) -> str:"
    description_extraction_code = """\n\tbuffer = io.StringIO()\n\ttransformed_gdf.info(buf=buffer)\n\tintermediate_data_description = buffer.getvalue()\n\treturn intermediate_data_description
    """

    description_extraction_function = (
        get_transformed_data_description_header + 
        '\n\t' + cleaned_transform_code.replace('\n', '\n\t') + 
        description_extraction_code
    )
    return description_extraction_function

def get_solution_function_string(cleaned_transform_code: str, cleaned_visualize_code: str) -> str:
    get_transformed_data_description_header = "def solve(data_gdf: gpd.GeoDataFrame, europe_gdf: gpd.GeoDataFrame):"

    function_body = (
        get_transformed_data_description_header + 
        '\n\t' + cleaned_transform_code.replace('\n', '\n\t') + 
        '\n\t' + cleaned_visualize_code.replace('\n', '\n\t')
    )
    
    return function_body

def extract_python_code(response: str) -> str:
    response = response.split("```python")
    if len(response) > 1:
        response = response[1].split("```")
        return response[0].strip()
    return response.strip()

def extract_json(response: str) -> str:
    response = response.split("```json")
    if len(response) > 1:
        response = response[1].split("```")
        return json.loads(response[0].strip())
    return json.loads(response.strip())