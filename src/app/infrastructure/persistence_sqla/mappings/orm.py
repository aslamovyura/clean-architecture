from sqlalchemy import ForeignKey, Integer, Date, Column, MetaData, String, Table
from sqlalchemy.orm import relationship

from app.infrastructure.persistence_sqla.registry import mapper_registry
from app.domain.entities import OrderLine, Batch


order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def map_tables() -> MetaData:
    lines_mapper = mapper_registry.map_imperatively(
        OrderLine,
        order_lines,
        properties={
            'sku': order_lines.c.sku,
            'qty': order_lines.c.qty,
            'orderid': order_lines.c.orderid,
        }
    )
    
    mapper_registry.map_imperatively(
        Batch,
        batches,
        properties={
            'reference': batches.c.reference,  # Map reference column
            'sku': batches.c.sku,
            '_purchased_quantity': batches.c._purchased_quantity,
            'eta': batches.c.eta,
            '_allocations': relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
                backref="batches"  # Optional: for bidirectional relationship
            )
        }
    )
    
    return mapper_registry.metadata
