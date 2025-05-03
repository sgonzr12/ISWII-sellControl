from configparser import ConfigParser

from typing import Dict, List
import os

def load_config(filename: str = "../database.ini", section: str = "postgresql") -> Dict[str, str]:
    # Resolve the path relative to the script's directory
    filename = os.path.join(os.path.dirname(__file__), filename)
    
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"The configuration file '{os.path.abspath(filename)}' does not exist. Please ensure the file exists at the specified path.")
    
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config: Dict[str, str] = {}
    if parser.has_section(section):
        params: List[tuple[str,str]] = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

if __name__ == '__main__':
    config = load_config()
    print(config)