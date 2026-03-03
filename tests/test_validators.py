"""Tests for validation utilities."""
import pytest
import pandas as pd
from swiss_finance.core.validators import validate_dataframe, validate_rate
from swiss_finance.core.exceptions import DataValidationError


class TestValidateDataframe:
    """Tests for validate_dataframe()"""

    def test_valid_dataframe(self):
        """Ne doit pas lever d'exception sur un DataFrame valide."""
        df = pd.DataFrame({"date": ["2024-01"], "rate": [1.5]})
        validate_dataframe(df, required_columns=["date", "rate"])

    def test_empty_dataframe_raises(self):
        """Doit lever DataValidationError sur DataFrame vide."""
        df = pd.DataFrame()
        with pytest.raises(DataValidationError) as exc_info:
            validate_dataframe(df, required_columns=["date"], min_rows=1)
        assert "empty" in str(exc_info.value).lower()

    def test_missing_column_raises(self):
        """Doit lever DataValidationError si colonne manquante."""
        df = pd.DataFrame({"date": ["2024-01"]})
        with pytest.raises(DataValidationError) as exc_info:
            validate_dataframe(df, required_columns=["date", "rate"])
        assert "Missing" in str(exc_info.value)
        assert "rate" in str(exc_info.value)

    def test_not_dataframe_raises(self):
        """Doit lever DataValidationError si pas un DataFrame."""
        with pytest.raises(DataValidationError):
            validate_dataframe({"date": "2024-01"}, required_columns=["date"])

    def test_insufficient_rows_raises(self):
        """Doit lever DataValidationError si pas assez de lignes."""
        df = pd.DataFrame({"date": ["2024-01"], "rate": [1.5]})
        with pytest.raises(DataValidationError):
            validate_dataframe(df, required_columns=["date", "rate"], min_rows=5)


class TestValidateRate:
    """Tests for validate_rate()"""

    def test_valid_positive_rate(self):
        """Ne doit pas lever d'exception sur un taux positif valide."""
        validate_rate(1.75)

    def test_valid_negative_rate(self):
        """Ne doit pas lever d'exception sur un taux négatif valide."""
        validate_rate(-0.75)

    def test_valid_zero(self):
        """Ne doit pas lever d'exception sur 0%."""
        validate_rate(0.0)

    def test_too_high_raises(self):
        """Doit lever DataValidationError si taux trop élevé."""
        with pytest.raises(DataValidationError):
            validate_rate(25.0)

    def test_too_low_raises(self):
        """Doit lever DataValidationError si taux trop bas."""
        with pytest.raises(DataValidationError):
            validate_rate(-25.0)

    def test_non_numeric_raises(self):
        """Doit lever DataValidationError si pas numérique."""
        with pytest.raises(DataValidationError):
            validate_rate("1.5")