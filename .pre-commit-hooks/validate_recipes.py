#!/usr/bin/env python3
"""Pre-commit hook to validate container recipe files.

This script validates .recipe files for common issues and best practices.
It is used both as a pre-commit hook and can be run manually.
"""

import sys
from typing import List

from dockerfile_parse import DockerfileParser


def validate_recipe(recipe_path: str) -> List[str]:
    """Validate a container recipe file for common issues.

    Args:
        recipe_path: Path to the recipe file

    Returns:
        List of validation errors, empty if all checks pass
    """
    errors = []

    try:
        # Parse the recipe file directly
        file = open(recipe_path, 'r')
        parser = DockerfileParser(fileobj=file)

        # Check if FROM instruction exists
        if not parser.baseimage:
            errors.append(f"{recipe_path}: Missing FROM instruction")

        # Check if base image is valid
        if parser.baseimage and not parser.baseimage.startswith(('docker.io/', 'ghcr.io/', 'quay.io/')):
            errors.append(f"{recipe_path}: Base image should use fully qualified name (e.g., docker.io/...)")

        # Check for globus-compute-endpoint installation
        globus_compute_installed = False
        for instruction in parser.structure:
            if instruction['instruction'] == 'RUN':
                cmd = instruction['value']
                if 'pip install' in cmd and 'globus-compute-endpoint' in cmd:
                    globus_compute_installed = True
                    # Check for --no-cache-dir flag
                    if '--no-cache-dir' not in cmd:
                        errors.append(f"{recipe_path}: pip install should use --no-cache-dir flag")

        if not globus_compute_installed:
            errors.append(f"{recipe_path}: Missing globus-compute-endpoint installation")

        # Check for common issues in RUN instructions
        for instruction in parser.structure:
            if instruction['instruction'] == 'RUN':
                cmd = instruction['value']
                # if '&&' in cmd and not cmd.strip().endswith('\\'):
                #     errors.append(f"{recipe_path}: Multi-line RUN command should end with '\\'")

                # Check for common package manager issues
                if 'apt-get' in cmd and not 'apt-get clean' in cmd:
                    errors.append(f"{recipe_path}: apt-get commands should include cleanup")

                if 'conda' in cmd and 'conda install' in cmd:
                    print(f"DEBUG: Checking conda install command: {cmd}")
                    if not any(cleanup in cmd for cleanup in ['conda clean -afy', 'conda clean -a', 'conda clean -f', 'conda clean -y']):
                        errors.append(f"{recipe_path}: conda commands should include cleanup")

        # Check for CMD or ENTRYPOINT
        has_cmd_or_entrypoint = False
        for instruction in parser.structure:
            if instruction['instruction'] in ('CMD', 'ENTRYPOINT'):
                has_cmd_or_entrypoint = True
                # Check if it's set to /bin/bash
                if instruction['value'] != '["/bin/bash"]':
                    errors.append(f"{recipe_path}: CMD/ENTRYPOINT should be set to /bin/bash")

        if not has_cmd_or_entrypoint:
            errors.append(f"{recipe_path}: Missing CMD or ENTRYPOINT instruction")

    except Exception as e:
        errors.append(f"{recipe_path}: Failed to parse - {str(e)}")

    return errors


def main() -> int:
    """Main entry point for the pre-commit hook.

    Returns:
        0 if validation passes, 1 if there are errors
    """
    # Get the list of files from pre-commit
    files = sys.argv[1:]

    if not files:
        print("No files provided")
        return 0

    # Validate each recipe file
    all_errors = []
    for file_path in files:
        if file_path.endswith('.recipe'):
            errors = validate_recipe(file_path)
            if errors:
                all_errors.extend(errors)

    # Report results
    if all_errors:
        print("\nValidation errors found:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print("\nAll recipe files passed validation!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
