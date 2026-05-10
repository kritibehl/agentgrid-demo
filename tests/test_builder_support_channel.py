from support_channel.triage_builder_request import classify, triage_requests


def test_classifies_tool_failure():
    assert classify("Tool-call failure during retrieval") == "tool_call_failure"


def test_classifies_missing_docs_context():
    assert classify("Missing docs context for deployment failure") == "missing_docs_context"


def test_repeat_request_flag():
    requests = [
        {
            "request_id": "a",
            "builder": "b1",
            "message": "Missing docs context for deployment failure",
        },
        {
            "request_id": "b",
            "builder": "b2",
            "message": "Again missing docs context for deployment failure",
        },
    ]

    results = triage_requests(requests)

    assert all(item["repeat_request_flag"] for item in results)
    assert results[0]["recommended_doc_link"] == "docs/troubleshooting_guide.md"
