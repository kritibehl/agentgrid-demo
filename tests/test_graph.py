from src.graph import run_document


def test_rfi_routes_to_engineering_with_high_or_medium_risk() -> None:
    text = """
    RFI 102: foundation section detail is unclear. Inspector approval is pending
    and this may delay footing pour by 2 days.
    """
    result = run_document(text)
    assert result["document_type"] == "rfi"
    assert result["owner"] == "engineering"
    assert "inspection_dependency" in result["issues"]
    assert result["severity"] in {"medium", "high"}


def test_change_order_routes_to_procurement() -> None:
    text = """
    Change Order 7: steel package shows cost impact due to supplier price increase
    and extended lead time.
    """
    result = run_document(text)
    assert result["document_type"] == "change_order"
    assert result["owner"] == "procurement"
    assert "cost_risk" in result["issues"]


def test_safety_notice_is_critical() -> None:
    text = """
    Safety incident report: scaffold access created a fall hazard and unsafe condition.
    Immediate correction required.
    """
    result = run_document(text)
    assert result["document_type"] == "safety_notice"
    assert result["owner"] == "safety"
    assert result["severity"] == "critical"
