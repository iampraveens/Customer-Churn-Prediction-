import os
from box.exceptions import BoxValueError
import yaml
from CustomerChurn import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file from the given path and returns its contents as a ConfigBox object.
    
    Args:
        path_to_yaml (Path): The path to the YAML file to be read.
        
    Returns:
        ConfigBox: The contents of the YAML file as a ConfigBox object.
        
    Raises:
        ValueError: If the YAML file is empty.
        Exception: If any other error occurs while reading the YAML file.
    """
    
    try:
        with open(path_to_yaml,) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates directories at the specified paths.
    Args:
        path_to_directories (list): A list of paths where directories will be created.
        verbose (bool): If True, logs information about created directories. Defaults to True.
    Returns:
        None
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")
            
            
@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves a dictionary to a JSON file.
    Args:
        path (Path): The path where the JSON file will be saved.
        data (dict): The dictionary to be saved.
    Returns:
        None
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    
    logger.info(f"json file saved at: {path}")
    
    
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads a JSON file from the specified path and returns its content as a ConfigBox.
    Args:
        path (Path): The path to the JSON file.
    Returns:
        ConfigBox: The content of the JSON file.
    """
    with open(path) as f:
        content = json.load(f)
        
    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_binary(path: Path, data: Any):
    """
    Saves binary data to a file using joblib.
    
    Args:
        path (Path): The path where the binary file will be saved.
        data (Any): The data to be saved.
    
    Returns:
        None
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")
    
    
@ensure_annotations
def load_binary(path: Path) -> Path:
    """
    Loads binary data from a file using joblib.
    
    Args:
        path (Path): The path to the binary file.
    
    Returns:
        Path: The loaded binary data.
    """
    with open(path) as f:
        data = joblib.load(f)
        logger.info(f"binary file loaded from: {path}")
        return data
    
    
@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns the size of a file in kilobytes.
    Args:
        path (Path): The path to the file.
    Returns:
        str: The size of the file in kilobytes, rounded to the nearest whole number.
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    logger.info(f"total size for the {path} is {size_in_kb} KB")
    return f"~ {size_in_kb} KB"  