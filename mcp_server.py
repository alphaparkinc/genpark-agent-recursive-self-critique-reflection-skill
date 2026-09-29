import sys, json
from client import AgentRecursiveSelfCritiqueReflection

def handle_mcp():
    reflex = AgentRecursiveSelfCritiqueReflection()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(reflex.run_reflection_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-agent-recursive-self-critique-reflection-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "evaluate_draft_critique", "description": "Evaluate draft and output structured verbal critique.", "inputSchema": {"type": "object", "properties": {"draft": {"type": "string"}}}},
                    {"name": "apply_iterative_refinement", "description": "Execute reflection loop until verified.", "inputSchema": {"type": "object", "properties": {"initial_draft": {"type": "string"}}}},
                    {"name": "run_reflection_benchmark", "description": "Run self-critique reflection benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "evaluate_draft_critique":
                    res = reflex.evaluate_draft_critique(args.get("draft", ""))
                elif tname == "apply_iterative_refinement":
                    res = reflex.apply_iterative_refinement(args.get("initial_draft", ""))
                else:
                    res = reflex.run_reflection_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
