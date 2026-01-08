from sqlalchemy import Integer, Column, String, Table
from sqlalchemy.orm import relationship, Mapper

from app.infrastructure.persistence_sqla.registry import mapper_registry
from app.domain.entities import Batch, Product


products = Table(
    "products",
    mapper_registry.metadata,
    Column("sku", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
)


def map_product_tables(batches_mapper: Mapper[Batch]) -> Mapper[Product]:
    
    products_mapper = mapper_registry.map_imperatively(
        Product, 
        products, 
        properties={
            "batches": relationship(batches_mapper)
        }
    )
    
    return products_mapper
