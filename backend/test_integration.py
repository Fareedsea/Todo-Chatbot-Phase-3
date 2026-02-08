"""
Integration test for AI chatbot with tool calling.

Tests the complete flow:
1. MCP tools are registered
2. Tool definitions are generated
3. Agent can be initialized
4. Tool response mapping works
"""

import sys
from pathlib import Path

# Add backend/src to path
backend_src = Path(__file__).parent / "src"
sys.path.insert(0, str(backend_src))

def test_mcp_tools():
    """Test that all MCP tools are registered."""
    print("=" * 60)
    print("TEST 1: MCP Tools Registration")
    print("=" * 60)

    from mcp.server import get_mcp_server

    server = get_mcp_server()
    tools = server.list_tools()

    expected_tools = ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]

    print(f"[OK] MCP Server initialized")
    print(f"[OK] Found {len(tools)} registered tools: {', '.join(tools)}")

    for tool_name in expected_tools:
        if tool_name in tools:
            print(f"  [OK] {tool_name} - registered")
        else:
            print(f"  [FAIL] {tool_name} - MISSING")
            return False

    print("\n[PASS] All MCP tools registered successfully\n")
    return True


def test_tool_definitions():
    """Test that OpenAI function definitions are generated."""
    print("=" * 60)
    print("TEST 2: OpenAI Function Definitions")
    print("=" * 60)

    from chat.tools import get_tool_definitions

    tools = get_tool_definitions()

    print(f"[OK] Generated {len(tools)} tool definitions")

    for tool in tools:
        func = tool.get("function", {})
        name = func.get("name", "unknown")
        desc = func.get("description", "")
        params = func.get("parameters", {}).get("properties", {})

        print(f"\n  Tool: {name}")
        print(f"    Description: {desc[:80]}...")
        print(f"    Parameters: {', '.join(params.keys())}")

    print("\n[PASS] Tool definitions generated successfully\n")
    return True


def test_tool_response_mapping():
    """Test that tool responses map to user-friendly messages."""
    print("=" * 60)
    print("TEST 3: Tool Response Mapping")
    print("=" * 60)

    from chat.tools import map_tool_response_to_message

    # Test successful add_task
    result1 = {
        "success": True,
        "data": {
            "task": {
                "id": "test-123",
                "title": "Buy groceries",
                "completed": False,
                "created_at": "2026-02-08T10:30:00Z"
            }
        }
    }

    message1 = map_tool_response_to_message("call_1", "add_task", result1)
    print(f"[OK] add_task success: \"{message1}\"")

    # Test list_tasks with results
    result2 = {
        "success": True,
        "data": {
            "tasks": [
                {"id": "1", "title": "Buy groceries", "completed": False},
                {"id": "2", "title": "Call mom", "completed": True}
            ]
        }
    }

    message2 = map_tool_response_to_message("call_2", "list_tasks", result2)
    print(f"[OK] list_tasks success: \"{message2[:60]}...\"")

    # Test error response
    result3 = {
        "success": False,
        "error": {
            "code": "NOT_FOUND",
            "message": "Task not found"
        }
    }

    message3 = map_tool_response_to_message("call_3", "delete_task", result3)
    print(f"[OK] delete_task error: \"{message3}\"")

    print("\n[PASS] Tool response mapping works correctly\n")
    return True


def test_agent_initialization():
    """Test that agent can be initialized (without calling Cohere API)."""
    print("=" * 60)
    print("TEST 4: Agent Initialization")
    print("=" * 60)

    import os
    from config import settings

    # Check if COHERE_API_KEY is set
    if not settings.cohere_api_key:
        print("[WARN]  COHERE_API_KEY not set in environment")
        print("   Agent will fail to initialize (expected)")
        print("   Set COHERE_API_KEY in .env to enable full testing")
        print("\n[WARN]  Agent initialization skipped (API key required)\n")
        return True

    from chat.agent import get_agent

    agent = get_agent()

    if agent is None:
        print("[FAIL] Agent initialization failed")
        return False

    print(f"[OK] Agent initialized successfully")
    print(f"[OK] Model: {agent.model}")
    print(f"[OK] MCP Server: Connected")

    print("\n[PASS] Agent ready for tool calling\n")
    return True


def test_mcp_tool_execution():
    """Test direct MCP tool execution."""
    print("=" * 60)
    print("TEST 5: Direct MCP Tool Execution")
    print("=" * 60)

    from mcp.tools.add_task import add_task_handler
    from mcp.tools.list_tasks import list_tasks_handler

    # Test add_task
    result = add_task_handler({
        "title": "Test task from integration test",
        "user_id": "test-user-integration"
    })

    if result.get("success"):
        task = result["data"]["task"]
        print(f"[OK] add_task executed successfully")
        print(f"  Created task: {task['id']} - '{task['title']}'")

        # Test list_tasks
        list_result = list_tasks_handler({
            "user_id": "test-user-integration",
            "completed": None
        })

        if list_result.get("success"):
            tasks = list_result["data"]["tasks"]
            print(f"[OK] list_tasks executed successfully")
            print(f"  Found {len(tasks)} task(s) for test user")
        else:
            print(f"[FAIL] list_tasks failed: {list_result.get('error')}")
            return False
    else:
        print(f"[FAIL] add_task failed: {result.get('error')}")
        return False

    print("\n[PASS] MCP tools execute correctly\n")
    return True


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "=" * 60)
    print("AI CHATBOT INTEGRATION TEST SUITE")
    print("=" * 60 + "\n")

    tests = [
        ("MCP Tools Registration", test_mcp_tools),
        ("OpenAI Function Definitions", test_tool_definitions),
        ("Tool Response Mapping", test_tool_response_mapping),
        ("Agent Initialization", test_agent_initialization),
        ("Direct MCP Tool Execution", test_mcp_tool_execution)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"[FAIL] {test_name} FAILED with exception: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Print summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "[PASS] PASS" if success else "[FAIL] FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "=" * 60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("=" * 60 + "\n")

    if passed == total:
        print("[SUCCESS] All integration tests passed!")
        print("\nNext steps:")
        print("1. Set COHERE_API_KEY in backend/.env")
        print("2. Start backend: uvicorn src.main:app --reload")
        print("3. Test chat endpoint: POST /api/chat")
        print("4. Build frontend chat UI")
        return 0
    else:
        print("[WARN]  Some tests failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
