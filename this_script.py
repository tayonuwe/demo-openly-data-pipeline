import json
import pandas as pd
from typing import List, Dict, Any

# ------------------ Core Functions ------------------

def load_data(json_file_path: str) -> List[Dict[str, Any]]:
    """
    Load raw JSON data from a file.

    Args:
        json_file_path (str): Path to the input JSON file.

    Returns:
        List[Dict[str, Any]]: List of raw records.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return data

def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standardize different field names into a consistent schema.

    Args:
        record (Dict[str, Any]): A single unstructured record.

    Returns:
        Dict[str, Any]: Record with unified keys.
    
    Note:
    Input data may have inconsistent field names across different sources,
    so we normalize fields like company name, website, description, etc.
    """
    return {
        'company_name': record.get('company_name') or record.get('company') or record.get('name', ''),
        'website': record.get('website') or record.get('site') or record.get('url', ''),
        'description': record.get('description') or record.get('desc') or record.get('info', ''),
        'tags': record.get('labels') or record.get('tags') or record.get('keywords', ''),
        'products': record.get('products') or record.get('items') or record.get('product_list', [])
    }

def remove_duplicates(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Eliminate duplicate company records based on company name and website.

    Args:
        records (List[Dict[str, Any]]): List of normalized records.

    Returns:
        pd.DataFrame: DataFrame with duplicates removed.

    Note:
    Ensures that companies aren't double-counted in analysis.
    """
    df = pd.DataFrame(records)
    return df.drop_duplicates(subset=['company_name', 'website'])

def score_lead(record: pd.Series) -> int:
    """
    Compute a lead score based on company relevance to the corn-starch supply chain.

    Args:
        record (pd.Series): A single row representing a normalized company record.

    Returns:
        int: Lead score for the company.

    Scoring Criteria:
    - +50 if 'corn-starch' is in tags.
    - +30 if keywords like 'maize powder', 'starch', 'binder', or 'thickener' are found in tags or description.
    - +20 if any product has 'corn starch' listed in ingredients.
    """
    score = 0
    tags = (record.get('tags') or '').lower()
    description = (record.get('description') or '').lower()
    products = record.get('products') or []

    if 'corn-starch' in tags:
        score += 50

    if any(keyword in tags or keyword in description for keyword in ['maize powder', 'starch', 'binder', 'thickener']):
        score += 30

    for product in products:
        ingredients = product.get('ingredients', [])
        if any('corn starch' in (ingredient or '').lower() for ingredient in ingredients):
            score += 20
            break  # only award +20 once per company

    return score

def process_data(json_file_path: str) -> pd.DataFrame:
    """
    Execute the full ETL pipeline:
    1. Load data
    2. Normalize fields
    3. Remove duplicates
    4. Score leads

    Args:
        json_file_path (str): Path to the raw JSON data file.

    Returns:
        pd.DataFrame: Cleaned and scored lead data.
    """
    raw_records = load_data(json_file_path)
    normalized = [normalize_record(record) for record in raw_records]
    deduped = remove_duplicates(normalized)
    deduped['lead_score'] = deduped.apply(score_lead, axis=1)
    return deduped

def export_to_csv(df: pd.DataFrame, filename: str = 'cleaned_leads.csv') -> None:
    """
    Save the cleaned and scored data to a CSV file.

    Args:
        df (pd.DataFrame): Processed DataFrame.
        filename (str, optional): Destination CSV filename. Defaults to 'cleaned_leads.csv'.
    """
    df.to_csv(filename, index=False)

# ------------------ Script Entry ------------------

if __name__ == "__main__":
    # Input file containing messy scraped data
    input_file = 'input_data.json'

    # Process the raw data and generate cleaned, scored leads
    cleaned_df = process_data(input_file)

    # Export the final DataFrame to a CSV file
    export_to_csv(cleaned_df)

    print(" Data cleaning and scoring complete! Results saved to 'cleaned_leads.csv'.")
