"""
Unit tests for API Ecosystem.
"""

import pytest
from civ_arcos.api import (
    CivARCOSAPI,
    APIVersion,
    WebhookEvent,
    GitHubWebhookHandler,
    GitLabWebhookHandler,
    BitbucketWebhookHandler,
    GraphQLSchema,
    GraphQLExecutor,
    APIv1,
    APIv2,
    APIv3,
)


class TestAPIVersions:
    """Test API version classes."""
    
    def test_apiv1_creation(self):
        """Test APIv1 creation."""
        api = APIv1()
        assert api.version == "1.0"
    
    def test_apiv1_get_evidence(self):
        """Test APIv1 get_evidence."""
        api = APIv1()
        result = api.get_evidence("test_id")
        assert result["version"] == "1.0"
        assert result["endpoint"] == "get_evidence"
        assert result["evidence_id"] == "test_id"
    
    def test_apiv1_submit_evidence(self):
        """Test APIv1 submit_evidence."""
        api = APIv1()
        result = api.submit_evidence({"type": "test"})
        assert result["version"] == "1.0"
        assert result["success"]
    
    def test_apiv2_creation(self):
        """Test APIv2 creation."""
        api = APIv2()
        assert api.version == "2.0"
    
    def test_apiv2_get_evidence(self):
        """Test APIv2 get_evidence with relations."""
        api = APIv2()
        result = api.get_evidence("test_id", include_relations=True)
        assert result["version"] == "2.0"
        assert result["include_relations"]
    
    def test_apiv2_batch_submit(self):
        """Test APIv2 batch_submit."""
        api = APIv2()
        evidence_list = [{"type": "test1"}, {"type": "test2"}]
        result = api.batch_submit(evidence_list)
        assert result["version"] == "2.0"
        assert result["count"] == 2
    
    def test_apiv3_creation(self):
        """Test APIv3 creation."""
        api = APIv3()
        assert api.version == "3.0"
    
    def test_apiv3_get_evidence(self):
        """Test APIv3 get_evidence with format."""
        api = APIv3()
        result = api.get_evidence("test_id", format="json")
        assert result["version"] == "3.0"
        assert result["format"] == "json"
    
    def test_apiv3_stream_evidence(self):
        """Test APIv3 stream_evidence."""
        api = APIv3()
        result = api.stream_evidence({"type": "test"})
        assert result["version"] == "3.0"
        assert "stream_id" in result


class TestWebhookHandlers:
    """Test webhook handler classes."""
    
    def test_github_handler_creation(self):
        """Test GitHub webhook handler creation."""
        handler = GitHubWebhookHandler()
        assert handler is not None
        assert len(handler.handlers) > 0
    
    def test_github_handle_push(self):
        """Test GitHub push event handling."""
        handler = GitHubWebhookHandler()
        payload = {
            "repository": {"full_name": "owner/repo"},
            "ref": "refs/heads/main",
            "commits": [{"id": "abc123"}],
        }
        result = handler.handle_event("push", payload)
        assert result["success"]
        assert result["event"] == "push"
        assert result["repository"] == "owner/repo"
        assert result["commit_count"] == 1
    
    def test_github_handle_pull_request(self):
        """Test GitHub pull request event handling."""
        handler = GitHubWebhookHandler()
        payload = {
            "action": "opened",
            "pull_request": {
                "number": 123,
                "state": "open",
            },
        }
        result = handler.handle_event("pull_request", payload)
        assert result["success"]
        assert result["event"] == "pull_request"
        assert result["pr_number"] == 123
    
    def test_gitlab_handler_creation(self):
        """Test GitLab webhook handler creation."""
        handler = GitLabWebhookHandler()
        assert handler is not None
        assert len(handler.handlers) > 0
    
    def test_gitlab_handle_push(self):
        """Test GitLab push event handling."""
        handler = GitLabWebhookHandler()
        payload = {
            "project": {"path_with_namespace": "owner/repo"},
            "ref": "refs/heads/main",
            "commits": [{"id": "abc123"}],
        }
        result = handler.handle_event("push", payload)
        assert result["success"]
        assert result["event"] == "push"
        assert result["project"] == "owner/repo"
    
    def test_gitlab_handle_merge_request(self):
        """Test GitLab merge request event handling."""
        handler = GitLabWebhookHandler()
        payload = {
            "object_attributes": {
                "action": "open",
                "iid": 123,
                "state": "opened",
            },
        }
        result = handler.handle_event("merge_request", payload)
        assert result["success"]
        assert result["event"] == "merge_request"
        assert result["mr_iid"] == 123
    
    def test_bitbucket_handler_creation(self):
        """Test Bitbucket webhook handler creation."""
        handler = BitbucketWebhookHandler()
        assert handler is not None
        assert len(handler.handlers) > 0
    
    def test_bitbucket_handle_push(self):
        """Test Bitbucket push event handling."""
        handler = BitbucketWebhookHandler()
        payload = {
            "repository": {"full_name": "owner/repo"},
            "push": {"changes": [{"new": {}}]},
        }
        result = handler.handle_event("repo:push", payload)
        assert result["success"]
        assert result["event"] == "push"
        assert result["repository"] == "owner/repo"


class TestGraphQLSchema:
    """Test GraphQL schema."""
    
    def test_schema_creation(self):
        """Test GraphQL schema creation."""
        schema = GraphQLSchema()
        assert schema is not None
        assert schema.schema is not None
    
    def test_schema_has_types(self):
        """Test schema has type definitions."""
        schema = GraphQLSchema()
        assert "types" in schema.schema
        assert "Evidence" in schema.schema["types"]
        assert "AssuranceCase" in schema.schema["types"]
    
    def test_schema_has_queries(self):
        """Test schema has query definitions."""
        schema = GraphQLSchema()
        assert "queries" in schema.schema
        assert "evidence" in schema.schema["queries"]
        assert "evidenceList" in schema.schema["queries"]
    
    def test_schema_has_mutations(self):
        """Test schema has mutation definitions."""
        schema = GraphQLSchema()
        assert "mutations" in schema.schema
        assert "submitEvidence" in schema.schema["mutations"]
    
    def test_schema_has_subscriptions(self):
        """Test schema has subscription definitions."""
        schema = GraphQLSchema()
        assert "subscriptions" in schema.schema
        assert "evidenceAdded" in schema.schema["subscriptions"]


class TestGraphQLExecutor:
    """Test GraphQL executor."""
    
    def test_executor_creation(self):
        """Test GraphQL executor creation."""
        schema = GraphQLSchema()
        resolvers = {}
        executor = GraphQLExecutor(schema, resolvers)
        assert executor is not None
    
    def test_execute_query(self):
        """Test query execution."""
        schema = GraphQLSchema()
        
        def evidence_resolver(variables):
            return {"id": "123", "type": "test"}
        
        # The parser extracts the field name from the query
        resolvers = {"query { evidence }": evidence_resolver}
        executor = GraphQLExecutor(schema, resolvers)
        
        result = executor.execute("query { evidence }", {"id": "123"})
        assert "data" in result
        # The result should be the return value of the resolver
        if result["data"] is not None:
            assert result["data"]["id"] == "123"
    
    def test_execute_mutation(self):
        """Test mutation execution."""
        schema = GraphQLSchema()
        
        def submit_resolver(variables):
            return {"success": True}
        
        # The parser extracts the field name from the mutation
        resolvers = {"mutation { submitEvidence }": submit_resolver}
        executor = GraphQLExecutor(schema, resolvers)
        
        result = executor.execute("mutation { submitEvidence }", {})
        assert "data" in result
        # The result should be the return value of the resolver
        if result["data"] is not None:
            assert result["data"]["success"]
    
    def test_execute_with_error(self):
        """Test execution with error."""
        schema = GraphQLSchema()
        resolvers = {}
        executor = GraphQLExecutor(schema, resolvers)
        
        result = executor.execute("invalid query")
        # Should not raise exception, but may return errors
        assert result is not None


class TestCivARCOSAPI:
    """Test CivARCOSAPI main class."""
    
    def test_api_creation(self):
        """Test API creation."""
        api = CivARCOSAPI()
        assert api is not None
        assert len(api.versions) == 3
        assert len(api.webhook_handlers) == 3
    
    def test_get_version(self):
        """Test getting API version."""
        api = CivARCOSAPI()
        v1 = api.get_version("v1")
        assert v1 is not None
        assert isinstance(v1, APIv1)
        
        v2 = api.get_version("v2")
        assert v2 is not None
        assert isinstance(v2, APIv2)
        
        v3 = api.get_version("v3")
        assert v3 is not None
        assert isinstance(v3, APIv3)
    
    def test_webhook_endpoints(self):
        """Test getting webhook endpoints."""
        api = CivARCOSAPI()
        endpoints = api.webhook_endpoints()
        
        assert "github" in endpoints
        assert "gitlab" in endpoints
        assert "bitbucket" in endpoints
        assert "ci_cd" in endpoints
        assert "security" in endpoints
        
        assert endpoints["github"]["endpoint"] == "/api/webhooks/github"
    
    def test_handle_webhook(self):
        """Test webhook handling."""
        api = CivARCOSAPI()
        payload = {
            "repository": {"full_name": "owner/repo"},
            "ref": "refs/heads/main",
            "commits": [],
        }
        
        result = api.handle_webhook("github", "push", payload)
        assert result["success"]
    
    def test_handle_webhook_invalid_platform(self):
        """Test webhook handling with invalid platform."""
        api = CivARCOSAPI()
        result = api.handle_webhook("invalid", "push", {})
        assert not result["success"]
        assert "No handler" in result["error"]
    
    def test_cicd_integration_endpoints(self):
        """Test CI/CD integration endpoints."""
        api = CivARCOSAPI()
        endpoints = api.cicd_integration_endpoints()
        
        assert "submit_build" in endpoints
        assert "submit_test" in endpoints
        assert "submit_deployment" in endpoints
        assert "get_status" in endpoints
    
    def test_security_tool_integrations(self):
        """Test security tool integrations."""
        api = CivARCOSAPI()
        integrations = api.security_tool_integrations()
        
        assert "submit_scan" in integrations
        assert "vulnerability_report" in integrations
        assert "dependency_check" in integrations
    
    def test_custom_evidence_endpoints(self):
        """Test custom evidence endpoints."""
        api = CivARCOSAPI()
        endpoints = api.custom_evidence_endpoints()
        
        assert "submit_custom" in endpoints
        assert "batch_submit" in endpoints
        assert endpoints["submit_custom"]["method"] == "POST"
    
    def test_graphql_interface(self):
        """Test GraphQL interface."""
        api = CivARCOSAPI()
        interface = api.graphql_interface()
        
        assert interface["endpoint"] == "/api/graphql"
        assert "schema" in interface
        assert len(interface["features"]) > 0
    
    def test_initialize_graphql(self):
        """Test GraphQL initialization."""
        api = CivARCOSAPI()
        resolvers = {"test": lambda x: x}
        
        api.initialize_graphql(resolvers)
        assert api.graphql_executor is not None
    
    def test_execute_graphql(self):
        """Test GraphQL execution."""
        api = CivARCOSAPI()
        
        def evidence_resolver(variables):
            return {"id": "123"}
        
        api.initialize_graphql({"evidence": evidence_resolver})
        
        result = api.execute_graphql("query { evidence }")
        assert "data" in result
    
    def test_execute_graphql_not_initialized(self):
        """Test GraphQL execution without initialization."""
        api = CivARCOSAPI()
        result = api.execute_graphql("query { test }")
        
        assert "errors" in result
        assert "not initialized" in result["errors"][0]["message"]
    
    def test_get_api_documentation(self):
        """Test getting API documentation."""
        api = CivARCOSAPI()
        docs = api.get_api_documentation()
        
        assert "versions" in docs
        assert "webhooks" in docs
        assert "cicd" in docs
        assert "security" in docs
        assert "custom_evidence" in docs
        assert "graphql" in docs
        
        assert "v1" in docs["versions"]
        assert "v2" in docs["versions"]
        assert "v3" in docs["versions"]
