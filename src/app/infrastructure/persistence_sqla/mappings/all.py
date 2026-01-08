from sqlalchemy import MetaData
from app.infrastructure.persistence_sqla.registry import mapper_registry
from app.infrastructure.persistence_sqla.mappings import (
    map_batch_tables, 
    map_product_tables
)

def map_tables() -> MetaData:
    batch_mapper = map_batch_tables()
    map_product_tables(batch_mapper)
    
    return mapper_registry.metadata