from pathlib import Path

class FileService:
    @staticmethod
    async def read_test_file() -> str:
        try:
            file_path = Path("test.txt")
            if not file_path.exists():
                return "File not found"
            return file_path.read_text()
        except Exception as e:
            return f"Error reading file: {str(e)}" 