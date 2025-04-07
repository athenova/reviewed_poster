import importlib
import sys

project_name = sys.argv[1]
module = importlib.import_module(f"projects.{project_name}")
if len(sys.argv)<3:
    module.post()
else:
    module.post(index=sys.argv[2])