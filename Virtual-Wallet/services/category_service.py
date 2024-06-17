from data_.models import Categories, Transactions
from data_.database import insert_query, read_query, update_query
from fastapi import HTTPException


def create_category(user_id: int, title: str) -> Categories:
    existing_category = read_query('''
        SELECT id FROM categories WHERE user_id = ? AND title = ?
    ''', (user_id, title))

    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists.")

    category_id = insert_query('''
        INSERT INTO categories (user_id, title) VALUES (?, ?)
    ''', (user_id, title))

    return Categories(id=category_id, title=title, user_id=user_id)


def view_categories(user_id: int) -> list[Categories]:
    data = read_query('''
        SELECT id, title, user_id FROM categories WHERE user_id = ?
    ''', (user_id,))

    return [Categories.from_query_result(*row) for row in data]


def link_transaction_to_category(user_id: int, transaction_id: int, category_id: int) -> str:
    transaction = read_query('''
        SELECT id 
        FROM transactions 
        WHERE id = ? AND (receiver_id = ? OR wallet_id = (SELECT id FROM wallet WHERE user_id = ?))
    ''', (transaction_id, user_id, user_id))

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    category = read_query('SELECT id FROM categories WHERE id = ? AND user_id = ?', (category_id, user_id))

    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    update_query('''
        UPDATE transactions SET category_id = ? WHERE id = ?
    ''', (category_id, transaction_id))

    return "Transaction linked to category successfully."