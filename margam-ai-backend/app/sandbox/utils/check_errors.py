import ast

def check_code_validity(code: str) -> dict:
    try:
        ast.parse(code)
        return {"valid": True, "error": None}
    except SyntaxError as e:
        return {"valid": False, "error": f"Syntax Error on line {e.lineno}: {e.msg}"}
    except Exception as e:
        return {"valid": False, "error": f"Compilation Error: {str(e)}"}
