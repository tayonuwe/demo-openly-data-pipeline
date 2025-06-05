# tests/this_script.py

import pandas as pd
from this_script import normalize_record, remove_duplicates, score_lead

def test_normalize_record():
    record = {
        'company': 'Test Co',
        'site': 'http://test.com',
        'desc': 'Test description here',
        'labels': 'eco; corn-starch',
        'products': [{'name': 'cake', 'ingredients': ['flour', 'corn starch']}]
    }
    result = normalize_record(record)
    assert result['company_name'] == 'Test Co'
    assert result['website'] == 'http://test.com'
    assert result['description'] == 'Test description here'
    assert result['tags'] == 'eco; corn-starch'
    assert isinstance(result['products'], list)

def test_remove_duplicates():
    records = [
        {'company_name': 'Company A', 'website': 'http://companya.com'},
        {'company_name': 'Company A', 'website': 'http://companya.com'},
        {'company_name': 'Company B', 'website': 'http://companyb.com'}
    ]
    df = remove_duplicates(records)
    assert len(df) == 2

def test_score_lead():
    record = pd.Series({
        'tags': 'eco; corn-starch',
        'description': 'Contains maize powder and starch',
        'products': [{'name': 'cake', 'ingredients': ['corn starch', 'flour']}]
    })
    assert score_lead(record) == 100  # 50 + 30 + 20