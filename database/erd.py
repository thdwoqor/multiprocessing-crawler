import os

from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

os.environ["PATH"] += os.pathsep + "C:\\Program Files\\Graphviz\\bin"
graph = create_schema_graph(metadata=MetaData("sqlite:///test.db"))
graph.write_png("erd.png")
