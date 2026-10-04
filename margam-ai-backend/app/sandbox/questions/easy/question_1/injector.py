def inject_user_code(user_code: str, output_path: str) -> str:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(user_code)
    return output_path
