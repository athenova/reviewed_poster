import importlib
import sys

project_name = sys.argv[1]
module = importlib.import_module(f"projects.{project_name}")
module.post()