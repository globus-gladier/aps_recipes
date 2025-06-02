# Container Recipes

This directory contains container recipe files for building scientific computing containers.

## Directory Structure

```
recipes/
├── base/                 # Base recipe templates
│   ├── miniconda.recipe  # Base recipe for Miniconda-based containers
│   └── cuda.recipe      # Base recipe for CUDA-based containers
├── boost_corr-1.0.0.recipe
├── tomopy-1.0.0.recipe
├── gsas2-1.0.0.recipe
├── ssx-1.0.0.recipe
├── nx_refine-1.0.0.recipe
└── eigen-1.0.0.recipe
```

## Recipe Naming Convention

Recipe files should follow this naming convention:
```
<package-name>-<version>.recipe
```

For example:
- `boost_corr-1.0.0.recipe`
- `tomopy-1.0.0.recipe`

## Recipe Metadata

Each recipe file should start with metadata comments:

```dockerfile
# Name: <container-name>
# Version: <version>
# Description: <brief description>
# Maintainer: <maintainer name and email>
# Base Image: <base image name and version>
# Last Updated: <date>
```

## Version Pinning

All dependencies should be pinned to specific versions:

```dockerfile
# Good
RUN pip install numpy==1.24.3

# Bad
RUN pip install numpy
```

## Best Practices

1. **Base Images**:
   - Always use fully qualified image names
   - Pin base image versions
   - Use official images when possible

2. **Package Management**:
   - Use `--no-cache-dir` with pip
   - Clean up package manager caches
   - Combine related RUN commands

3. **Security**:
   - Don't run as root
   - Remove unnecessary packages
   - Scan for vulnerabilities

4. **Size Optimization**:
   - Use multi-stage builds
   - Remove build dependencies
   - Clean up temporary files

## Testing

Each recipe should have an associated test file in the `tests/` directory:

```yaml
# tests/boost_corr-1.0.0.yaml
schemaVersion: '2.0.0'
metadataTest:
  env:
    - key: 'VERSION'
      value: '1.0.0'
commandTests:
  - name: 'python-version'
    command: 'python'
    args: ['--version']
    expectedOutput: ['Python 3.11.*']
```

## Building and Testing

To build and test a recipe:

```bash
# Build
podman build -f recipes/boost_corr-1.0.0.recipe -t boost_corr:1.0.0

# Test
container-structure-test test \
  --image boost_corr:1.0.0 \
  --config tests/boost_corr-1.0.0.yaml
```
