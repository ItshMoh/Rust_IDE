import subprocess

class RustCompiler:
    def compile_project(self, project_path: str) -> tuple[bool, str]:
        try:
            result = subprocess.run(
                ['cargo', 'build'],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            return success, output
        except Exception as e:
            return False, str(e)



