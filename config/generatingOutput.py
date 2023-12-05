from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData, create_engine
from config.config import Config
from src.database.models import Base  # Ensure this imports all your models
def get_engine():
    config = Config()
    database_url = config.DATABASE_URL
    return create_engine(database_url)


def generate_er_diagram(output_path="output/er_diagram.png"):

    # Bind the engine to the metadata of the base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = get_engine()
    Base.metadata.reflect(bind=get_engine())

    graph = create_schema_graph(
        metadata=Base.metadata,
        show_datatypes=True,  # The image would show datatypes
        show_indexes=True,  # The image would show index names and columns
        rankdir='LR',  # Left to right alignment
        concentrate=False  # Don't try to join the relation lines together
    )


    graph.write_png(output_path)
    print(f"ER Diagram generated at {output_path}")

if __name__ == "__main__":
    generate_er_diagram()
