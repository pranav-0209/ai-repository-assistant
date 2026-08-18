from app.indexing.models import Repository, RepositorySummary


class RepositorySummaryFormatter:
    """
    Converts a repository summary into human-readable text.
    """

    def format(
        self,
        repository: Repository,
        summary: RepositorySummary,
    ) -> str:

        lines = [
            "Repository Summary",
            "=" * 50,
            "",
            f"Repository: {repository.path}",
            "",
            f"Total files : {summary.total_files}",
            f"Total lines : {summary.total_lines:,}",
            f"Total size  : {self._format_size(summary.total_size_bytes)}",
            "",
            "Languages",
            "-" * 50,
        ]

        for language, count in sorted(
            summary.files_by_language.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            lines.append(
                f"{language:<20} {count}"
            )

        lines.extend([
            "",
            "Largest Files",
            "-" * 50,
        ])

        for file in summary.largest_files:
            lines.append(
                f"{str(file.path):<40} "
                f"{file.line_count:,} lines"
            )

        return "\n".join(lines)

    def _format_size(self, size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"

        if size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.2f} KB"

        if size_bytes < 1024 ** 3:
            return f"{size_bytes / (1024 ** 2):.2f} MB"

        return f"{size_bytes / (1024 ** 3):.2f} GB"