import pytest
import duckdb
from src.database_mod import read_parquet, check_parquet


@pytest.fixture(scope="module")
def test_db():
    """Create a temporary in-memory database for testing."""
    db = duckdb.connect(':memory:')
    yield db
    db.close()

def test_read_parquet(test_db):
    """Test that read_parquet returns a valid DuckDBPyRelation."""
    parquet_file = "tests/test.parquet"
    db_obj = read_parquet(parquet_file=parquet_file)
    assert isinstance(db_obj, duckdb.DuckDBPyRelation)

def test_check_parquet_exists():
    """Test that check_parquet returns True if the Parquet file exists."""
    parquet_file = "tests/test.parquet"
    exists = check_parquet(check_path=parquet_file)
    assert exists == True
    
def test_check_parquet_not_exists():
    """Test that check_parquet returns False if the Parquet file does not exist."""
    parquet_file = "tests/fake.parquet"
    exists = check_parquet(check_path=parquet_file)
    assert exists == False

