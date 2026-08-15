from app.context.models import ContextItem
from app.rag.metadata_filter import MetadataFilter


def test_metadata_filter_by_single_field():
    metadata_filter = MetadataFilter()

    items = [
        ContextItem(
            content="RAG documentation",
            metadata={
                "category": "documentation",
            },
        ),
        ContextItem(
            content="RAG blog post",
            metadata={
                "category": "blog",
            },
        ),
    ]

    filtered = metadata_filter.filter(
        items,
        filters={
            "category": "documentation",
        },
    )

    assert len(filtered) == 1
    assert filtered[0].content == "RAG documentation"


def test_metadata_filter_by_multiple_fields():
    metadata_filter = MetadataFilter()

    items = [
        ContextItem(
            content="English documentation",
            metadata={
                "category": "documentation",
                "language": "en",
            },
        ),
        ContextItem(
            content="Spanish documentation",
            metadata={
                "category": "documentation",
                "language": "es",
            },
        ),
    ]

    filtered = metadata_filter.filter(
        items,
        filters={
            "category": "documentation",
            "language": "en",
        },
    )

    assert len(filtered) == 1
    assert filtered[0].content == "English documentation"


def test_metadata_filter_returns_all_without_filters():
    metadata_filter = MetadataFilter()

    items = [
        ContextItem(content="Item 1"),
        ContextItem(content="Item 2"),
    ]

    filtered = metadata_filter.filter(
        items,
        filters={},
    )

    assert filtered == items


def test_metadata_filter_returns_empty_when_no_match():
    metadata_filter = MetadataFilter()

    items = [
        ContextItem(
            content="RAG documentation",
            metadata={
                "category": "documentation",
            },
        ),
    ]

    filtered = metadata_filter.filter(
        items,
        filters={
            "category": "video",
        },
    )

    assert filtered == []