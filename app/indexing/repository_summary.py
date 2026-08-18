from collections import Counter

from app.indexing.models import Repository, RepositorySummary


class RepositorySummaryService:
    """
    Calculates aggregate statistics for a repository.
    """

    def __init__(self, largest_file_count: int = 5):
        self._largest_file_count = largest_file_count

    def summarize(self, repository: Repository) -> RepositorySummary:
        files = repository.files

        total_files = len(files)

        total_lines = sum(
            file.line_count
            for file in files
        )

        total_size_bytes = sum(
            file.size_bytes
            for file in files
        )

        files_by_language = dict(
            Counter(
                file.language
                for file in files
            )
        )

        largest_files = sorted(
            files,
            key=lambda file: file.line_count,
            reverse=True,
        )[:self._largest_file_count]

        return RepositorySummary(
            total_files=total_files,
            total_lines=total_lines,
            total_size_bytes=total_size_bytes,
            files_by_language=files_by_language,
            largest_files=largest_files,
        )