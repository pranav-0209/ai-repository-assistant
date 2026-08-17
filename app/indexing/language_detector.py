from pathlib import Path


class LanguageDetector:
    """
    Determines the programming language of a file
    based on its extension.
    """

    _LANGUAGE_MAP = {
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".cpp": "C++",
        ".cc": "C++",
        ".c": "C",
        ".h": "C",
        ".hpp": "C++",
        ".go": "Go",
        ".rs": "Rust",
        ".rb": "Ruby",
        ".php": "PHP",
        ".cs": "C#",
        ".kt": "Kotlin",
        ".swift": "Swift",
        ".sql": "SQL",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".md": "Markdown",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".xml": "XML",
    }

    def detect(self, path: Path) -> str:
        """
        Detect the language based on file extension.

        Returns 'Unknown' when the extension is not recognized.
        """

        return self._LANGUAGE_MAP.get(
            path.suffix.lower(),
            "Unknown",
        )