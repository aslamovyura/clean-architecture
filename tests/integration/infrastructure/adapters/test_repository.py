from sqlalchemy import text
from app.domain.entities import Batch, OrderLine, Product
from app.infrastructure.adapters import ProductRepository


def test_repository_can_save_a_batch(session):
    sku = "RUSTY-SOAPDISH"
    batch = Batch("batch1", sku, 100, eta=None)
    product = Product(sku, [batch])
    
    repo = ProductRepository(session)
    repo.add(product)
    session.commit()

    batches = session.execute(text(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    ))
    
    products = session.execute(text(
        'SELECT sku, version_number FROM "products"'
    ))
    assert list(batches) == [("batch1", sku, 100, None)]
    assert list(products) == [(sku, 0)]


def insert_product(session):
    session.execute(text(
        "INSERT INTO products (sku, version_number)"
        ' VALUES ("GENERIC-SOFA", 1)'
        )
    )

def insert_order_line(session):
    session.execute(text(
        "INSERT INTO order_lines (orderid, sku, qty)"
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    ))
    [[orderline_id]] = session.execute(
        text("SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku"),
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return orderline_id


def insert_batch(session, batch_id):
    session.execute(
        text("INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
            ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)'),
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        text('SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"'),
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        text("INSERT INTO allocations (orderline_id, batch_id)"
            " VALUES (:orderline_id, :batch_id)"),
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )



def test_repository_can_retrieve_a_product_with_batches(session):
    sku = "GENERIC-SOFA"
    insert_product(session)
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = ProductRepository(session)
    retrieved : Product = repo.get(sku)

    expected = Product("GENERIC-SOFA", [], 1)
    assert retrieved.sku == expected.sku
    assert retrieved.version_number == 1
    assert len(retrieved.batches) == 2