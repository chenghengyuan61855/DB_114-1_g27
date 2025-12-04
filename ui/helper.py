def cancel_check(input_str: str, ui_type: str) -> bool:
    if input_str.strip() == "q":
        print(f"{ui_type} cancelled.")
        return True
    return False