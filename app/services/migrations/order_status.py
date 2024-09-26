from app.database.models import OrderStatus


def upgrade_init(op) -> None:
    op.bulk_insert(
        OrderStatus.__table__,
        [
            {'service_name': 'pending', 'user_name': 'В процессе'},
            {'service_name': 'created', 'user_name': 'Создан'},
            {'service_name': 'shipped', 'user_name': 'Отправлен'},
            {'service_name': 'delivered', 'user_name': 'Доставлен'},
            {'service_name': 'canceled', 'user_name': 'Отменён'},
            # Добавьте больше записей по необходимости
        ]
    )


def downgrade_init(op) -> None:
    op.execute(
        'DELETE FROM orderstatuses WHERE service_name IN ('
        '"pending",'
        '"created",'
        '"shipped",'
        '"delivered",'
        '"canceled",'
        ')'
    )
