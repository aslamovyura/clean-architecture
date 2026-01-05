from sqlalchemy import UUID, ForeignKey, Integer, Date, Boolean, Column, Enum, LargeBinary, String, Table
from sqlalchemy.orm import composite, relationship

# from app.domain.entities.user import User
# from app.domain.enums.user_role import UserRole
# from app.domain.value_objects.user_id import UserId
# from app.domain.value_objects.user_password_hash import UserPasswordHash
# from app.domain.value_objects.username import Username
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


def map_batches_table() -> None:
    lines_mapper = mapper_registry.map_imperatively(OrderLine, order_lines)
    mapper_registry.map_imperatively(Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations, collection_class=set,
            )
        },
    )
