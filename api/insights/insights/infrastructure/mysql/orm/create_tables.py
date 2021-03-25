from mapper_base import MapperBase
from autogen_entities import *


database = 'data_clarus_de'

mapper_base = MapperBase(database)
base = mapper_base.get_base()
base.metadata.create_all(mapper_base.get_engine())

