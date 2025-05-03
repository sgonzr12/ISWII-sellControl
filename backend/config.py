from configparser import ConfigParser
import logging
import os

from typing import Dict, List

def load_config(filename: str = "../database.ini", section: str = "postgresql") -> Dict[str, str]:
    
    logging.info("Loading configuration file")
    logging.debug(f"Config file path: {filename}")
    filename = os.path.abspath(filename)+filename
    
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config: Dict[str, str] = {}
    if parser.has_section(section):
        params: List[tuple[str,str]] = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
        logging.debug(f"Configuration loaded: {config}")
    else:
        logging.error(f"Section {section} not found in the {filename} file")
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config