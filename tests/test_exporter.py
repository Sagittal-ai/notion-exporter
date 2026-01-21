import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from notion_exporter.exporter import NotionExporter


@pytest.fixture
def notion_exporter():
    """Create a NotionExporter instance for testing."""
    return NotionExporter(notion_token="test_token")


@pytest.mark.asyncio
async def test_get_page_meta_with_database_parent_new_api(notion_exporter):
    """Test _get_page_meta with new API structure where parent has database_id attribute."""
    page_object = {
        "id": "test-page-id",
        "url": "https://notion.so/test-page",
        "created_by": {"id": "user-1"},
        "last_edited_by": {"id": "user-2"},
        "last_edited_time": "2023-01-01T00:00:00.000Z",
        "parent": {
            "database_id": "test-database-id"
        },
        "properties": {
            "Name": {
                "type": "title",
                "title": [{"plain_text": "Test Page"}]
            },
            "Status": {
                "type": "select",
                "select": {"name": "In Progress"}
            }
        }
    }
    
    with patch.object(notion_exporter.notion.pages, 'retrieve', new_callable=AsyncMock) as mock_retrieve:
        mock_retrieve.return_value = page_object
        
        with patch.object(notion_exporter, '_get_user', new_callable=AsyncMock) as mock_get_user:
            mock_get_user.side_effect = ["User One", "User Two"]
            
            result = await notion_exporter._get_page_meta("test-page-id")
            
            assert result["page_id"] == "test-page-id"
            assert result["parent_id"] == "test-database-id"
            assert result["title"] == "Test Page"
            assert result["url"] == "https://notion.so/test-page"
            assert result["created_by"] == "User One"
            assert result["last_edited_by"] == "User Two"
            assert "properties" in result


@pytest.mark.asyncio
async def test_get_page_meta_with_page_parent_old_api(notion_exporter):
    """Test _get_page_meta with old API structure where parent uses type as key."""
    page_object = {
        "id": "test-page-id",
        "url": "https://notion.so/test-page",
        "created_by": {"id": "user-1"},
        "last_edited_by": {"id": "user-2"},
        "last_edited_time": "2023-01-01T00:00:00.000Z",
        "parent": {
            "type": "page_id",
            "page_id": "parent-page-id"
        },
        "properties": {
            "title": {
                "type": "title",
                "title": [{"plain_text": "Test Page"}]
            }
        }
    }
    
    with patch.object(notion_exporter.notion.pages, 'retrieve', new_callable=AsyncMock) as mock_retrieve:
        mock_retrieve.return_value = page_object
        
        with patch.object(notion_exporter, '_get_user', new_callable=AsyncMock) as mock_get_user:
            mock_get_user.side_effect = ["User One", "User Two"]
            
            result = await notion_exporter._get_page_meta("test-page-id")
            
            assert result["page_id"] == "test-page-id"
            assert result["parent_id"] == "parent-page-id"
            assert result["title"] == "Test Page"
            assert "properties" not in result


@pytest.mark.asyncio
async def test_get_database_meta_with_database_parent_new_api(notion_exporter):
    """Test _get_database_meta with new API structure where parent has database_id attribute."""
    database_object = {
        "id": "test-database-id",
        "url": "https://notion.so/test-database",
        "created_by": {"id": "user-1"},
        "last_edited_by": {"id": "user-2"},
        "last_edited_time": "2023-01-01T00:00:00.000Z",
        "parent": {
            "database_id": "parent-database-id"
        },
        "title": [{"plain_text": "Test Database"}]
    }
    
    with patch.object(notion_exporter.notion.databases, 'retrieve', new_callable=AsyncMock) as mock_retrieve:
        mock_retrieve.return_value = database_object
        
        with patch.object(notion_exporter, '_get_user', new_callable=AsyncMock) as mock_get_user:
            mock_get_user.side_effect = ["User One", "User Two"]
            
            result = await notion_exporter._get_database_meta("test-database-id")
            
            assert result["page_id"] == "test-database-id"
            assert result["parent_id"] == "parent-database-id"
            assert result["title"] == "Test Database"
            assert result["url"] == "https://notion.so/test-database"
            assert result["created_by"] == "User One"
            assert result["last_edited_by"] == "User Two"


@pytest.mark.asyncio
async def test_get_database_meta_with_page_parent_old_api(notion_exporter):
    """Test _get_database_meta with old API structure where parent uses type as key."""
    database_object = {
        "id": "test-database-id",
        "url": "https://notion.so/test-database",
        "created_by": {"id": "user-1"},
        "last_edited_by": {"id": "user-2"},
        "last_edited_time": "2023-01-01T00:00:00.000Z",
        "parent": {
            "type": "page_id",
            "page_id": "parent-page-id"
        },
        "title": [{"plain_text": "Test Database"}]
    }
    
    with patch.object(notion_exporter.notion.databases, 'retrieve', new_callable=AsyncMock) as mock_retrieve:
        mock_retrieve.return_value = database_object
        
        with patch.object(notion_exporter, '_get_user', new_callable=AsyncMock) as mock_get_user:
            mock_get_user.side_effect = ["User One", "User Two"]
            
            result = await notion_exporter._get_database_meta("test-database-id")
            
            assert result["page_id"] == "test-database-id"
            assert result["parent_id"] == "parent-page-id"
            assert result["title"] == "Test Database"
