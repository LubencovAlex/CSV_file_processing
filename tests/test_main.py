import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

# Пример данных для тестов
test_data = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    {"name": "iphone se", "brand": "apple", "price": "429", "rating": "4.1"},
]

def test_filter_numeric_greater():
    result = main.filter_data(test_data, "price", ">", "500")
    assert len(result) == 2
    assert all(float(row["price"]) > 500 for row in result)

def test_filter_string_equal():
    result = main.filter_data(test_data, "brand", "=", "apple")
    assert len(result) == 2
    assert all(row["brand"].lower() == "apple" for row in result)

def test_aggregate_avg():
    result = main.aggregate(test_data, "rating", "avg")
    expected = round((4.9 + 4.8 + 4.6 + 4.1) / 4, 2)
    assert result == expected

def test_aggregate_min():
    result = main.aggregate(test_data, "price", "min")
    assert result == 199.0

def test_aggregate_max():
    result = main.aggregate(test_data, "price", "max")
    assert result == 1199.0

def test_filter_no_match():
    result = main.filter_data(test_data, "price", "<", "100")
    assert result == []

def test_invalid_column_filter():
    result = main.filter_data(test_data, "nonexistent", "=", "something")
    assert result == []

def test_invalid_column_aggregate():
    result = main.aggregate(test_data, "nonexistent", "avg")
    assert result is None
