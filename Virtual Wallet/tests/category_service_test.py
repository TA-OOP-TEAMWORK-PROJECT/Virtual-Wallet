import sys
import os
from unittest.mock import patch, ANY
from fastapi import HTTPException
import pytest
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from services.category_service import create_category, link_transaction_to_category, view_categories
from data_.models import Categories


@patch('services.category_service.read_query')
@patch('services.category_service.insert_query')
def test_create_category_success(mock_insert_query, mock_read_query):
    mock_read_query.return_value = []
    mock_insert_query.return_value = 1  
    
    result = create_category(user_id=1, title='New Category')
    
    assert isinstance(result, Categories)


@patch('services.category_service.read_query')
@patch('services.category_service.insert_query')
def test_create_category_failure(mock_insert_query, mock_read_query):
    mock_read_query.return_value = [(1,)]
    mock_insert_query.return_value = None

    with pytest.raises(HTTPException):
        create_category(user_id=1, title='Existing Category')


@patch('services.category_service.read_query')
def test_view_categories_success(mock_read_query):
    mock_read_query.return_value = [(1, 'Category 1', 1), (2, 'Category 2', 1)]
        
    result = view_categories(user_id=1)
        
    assert len(result) == 2
    assert isinstance(result[0], Categories)
    assert isinstance(result[1], Categories)
    assert result[0].id == 1
    assert result[0].title == 'Category 1'
    assert result[0].user_id == 1
    assert result[1].id == 2
    assert result[1].title == 'Category 2'
    assert result[1].user_id == 1


@patch('services.category_service.read_query')
@patch('services.category_service.update_query')
def test_link_transaction_to_category_success(mock_update_query, mock_read_query):
    mock_read_query.side_effect = [
        [(1,)],  
        [(1,)]   
    ]

    result = link_transaction_to_category(user_id=1, transaction_id=1, category_id=1)

    assert result == 'Transaction linked to category successfully.'

    mock_update_query.assert_called_once_with(
        ANY,  
        (1, 1)  
    )


@patch('services.category_service.read_query')
def test_link_transaction_to_category_transaction_not_found(mock_read_query):
    mock_read_query.side_effect = [[]]

    with pytest.raises(HTTPException) as excinfo:
        link_transaction_to_category(user_id=1, transaction_id=1, category_id=1)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == 'Transaction not found.'


@patch('services.category_service.read_query')
def test_link_transaction_to_category_category_not_found(mock_read_query):
    mock_read_query.side_effect = [[(1,)], []]

    with pytest.raises(HTTPException) as excinfo:
        link_transaction_to_category(user_id=1, transaction_id=1, category_id=1)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == 'Category not found.'