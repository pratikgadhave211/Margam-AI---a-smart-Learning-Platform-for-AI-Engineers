import ast
import io
from pyflakes.api import check
from pyflakes.reporter import Reporter

def check_code_validity(user_code: str) -> dict:
    """
    Statically analyzes the user's code for syntax errors and required structures.
    Returns: {"valid": bool, "error": str}
    """
    # 1. Linter Check: Catch undefined variables (like C++ compiler) statically
    out = io.StringIO()
    err = io.StringIO()
    reporter = Reporter(out, err)
    
    check(user_code, filename="editor.py", reporter=reporter)
    linter_errors = out.getvalue() + err.getvalue()
    
    if linter_errors:
        critical_errors = []
        for line in linter_errors.strip().split("\n"):
            # Ignore harmless warnings, we only want critical compilation errors
            if "imported but unused" not in line:
                critical_errors.append(line.replace("editor.py:", "Line "))
        
        if critical_errors:
            return {"valid": False, "error": f"Compilation Error:\n" + "\n".join(critical_errors)}

    try:
        tree = ast.parse(user_code)
    except SyntaxError as e:
        line_text = e.text.strip() if e.text else ""
        return {"valid": False, "error": f"Syntax Error on line {e.lineno}: {e.msg}\n\n{line_text}"}
    except Exception as e:
        return {"valid": False, "error": f"Compilation Error: {str(e)}"}

    has_function = False
    has_class = False

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "analyze_support_ticket":
            has_function = True
            
            body_nodes = node.body
            if not body_nodes:
                return {"valid": False, "error": "Validation Error: Your analyze_support_ticket function is empty."}
                
            if len(body_nodes) == 1 and isinstance(body_nodes[0], ast.Pass):
                return {"valid": False, "error": "Validation Error: Your analyze_support_ticket function only contains 'pass'. Please implement the logic."}

            # Find all return statements
            returns = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
            if not returns:
                return {"valid": False, "error": "Validation Error: Your analyze_support_ticket function is missing a return statement."}
                
            # Check if any return statement is empty
            for ret in returns:
                if ret.value is None:
                    return {"valid": False, "error": "Validation Error: You have an empty 'return' statement. You must return a SupportTicket object."}

        if isinstance(node, ast.ClassDef) and node.name == "SupportTicket":
            has_class = True
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                return {"valid": False, "error": "Validation Error: You must define the required fields inside the SupportTicket class."}

    if not has_class:
        return {"valid": False, "error": "Validation Error: You must define a Pydantic class named 'SupportTicket'."}
        
    if not has_function:
        return {"valid": False, "error": "Validation Error: You must define a function named 'analyze_support_ticket'."}

    return {"valid": True, "error": None}
