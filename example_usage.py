from client import AgentRecursiveSelfCritiqueReflection
import json

reflex = AgentRecursiveSelfCritiqueReflection()
print("=== AGENT RECURSIVE SELF-CRITIQUE BENCHMARK ===")
res = reflex.run_reflection_benchmark()
print(json.dumps(res, indent=2))
