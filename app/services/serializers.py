def serialize_inventory_item(item):
    return {
        "id": item.id,
        "name": item.name,
        "current_stock": item.current_stock,
        "reorder_level": item.reorder_level,
        "unit": item.unit,
    }

