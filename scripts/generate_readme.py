from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README_FILE = ROOT / "README.md"

START_MARKER = "<!-- INDEX:START -->"
END_MARKER = "<!-- INDEX:END -->"


def display_name(path: Path) -> str:
    name = path.stem if path.suffix.lower() == ".md" else path.name
    return name.replace("_", " ").replace("-", " ").strip().title()


def generate_index(directory: Path, level: int = 0) -> list[str]:
    lines = []

    items = sorted(
        directory.iterdir(),
        key=lambda p: (p.is_file(), p.name.lower())
    )

    for item in items:
        # Ignore hidden files/folders
        if item.name.startswith("."):
            continue

        # Ignore the README and scripts folder
        if item.resolve() == README_FILE.resolve():
            continue

        if item.is_dir():
            # Don't include scripts in the index
            if item.name.lower() == "scripts":
                continue

            heading_level = min(level + 2, 6)
            lines.append(f"{'#' * heading_level} {display_name(item)}")
            lines.append("")

            lines.extend(generate_index(item, level + 1))

        elif item.suffix.lower() == ".md":
            relative_path = item.relative_to(ROOT).as_posix()
            title = display_name(item)

            indent = "  " * level
            lines.append(f"{indent}- [{title}]({relative_path})")

    return lines


def main():
    index = generate_index(ROOT)
    index_content = "\n".join(index)

    new_index = (
        f"{START_MARKER}\n"
        f"## Index\n\n"
        f"{index_content}\n"
        f"{END_MARKER}"
    )

    if README_FILE.exists():
        readme = README_FILE.read_text(encoding="utf-8")

        if START_MARKER in readme and END_MARKER in readme:
            before = readme.split(START_MARKER)[0]
            after = readme.split(END_MARKER, 1)[1]

            readme = before + new_index + after
        else:
            readme = readme.rstrip() + "\n\n" + new_index + "\n"

    else:
        readme = f"# Study Notes\n\n{new_index}\n"

    README_FILE.write_text(readme, encoding="utf-8")

    print("README index updated successfully.")


if __name__ == "__main__":
    main()