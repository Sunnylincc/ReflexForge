def mutation_label(seed: int) -> str:
    return "local_patch" if seed % 2 == 0 else "operator_rewrite"
