# Container Recipes

This repository contains container recipe files for building containers used in scientific computing workflows.

## Prerequisites

- Podman installed on your system
- pre-commit (for development)

## Repository Structure

```
.
├── recipes/              # Container recipe files
│   ├── boost_corr-1.0.0.recipe
│   ├── boost_corr-cuda-1.0.0.recipe
│   ├── dials-1.0.0.recipe
│   ├── eigen-1.0.0.recipe
│   ├── gsas2-1.0.0.recipe
│   ├── midas-beta.recipe
│   ├── nx_refine-1.0.0.recipe
│   ├── tomocupy-beta.recipe
│   ├── tomopy-1.0.0.recipe
│   └── xrf_maps-beta.recipe
├── scripts/             # Utility scripts
└── .github/            # GitHub Actions workflows
```

## Available Containers

- **Boost Correlation** (`recipes/boost_corr-1.0.0.recipe`)
  - Based on: miniconda-base
  - Includes: boost correlation analysis tools
  - Environment: Python 3.11 with scientific computing stack

- **Boost Correlation CUDA** (`recipes/boost_corr-cuda-1.0.0.recipe`)
  - Based on: nvidia/cuda:12.8.0-runtime-ubuntu24.04
  - Includes: boost correlation analysis tools with CUDA support
  - Environment: Python 3.11 with CUDA and PyTorch

- **DIALS** (`recipes/dials-1.0.0.recipe`)
  - Based on: miniconda-base
  - Includes: DIALS for X-ray diffraction data analysis
  - Environment: Python 3.11 with crystallography tools

- **XPCS-Eigen** (`recipes/eigen-1.0.0.recipe`)
  - Based on: miniconda-base
  - Includes: xpcs-eigen, numpy, h5py
  - Environment: Python 3.11 with C++ development tools

- **GSAS2** (`recipes/gsas2-1.0.0.recipe`)
  - Based on: miniconda-base
  - Includes: GSAS2 and crystallographic analysis tools
  - Environment: Python 3.11 with scientific computing stack

- **MIDAS** (`recipes/midas-beta.recipe`)
  - Based on: miniconda-base
  - Includes: MIDAS data processing tools
  - Environment: Python 3.11 with scientific computing stack

- **NX Refine** (`recipes/nx_refine-1.0.0.recipe`)
  - Based on: miniconda-base
  - Includes: nxrefine and related dependencies
  - Environment: Python 3.11 with scientific computing stack

- **TomoCuPy** (`recipes/tomocupy-beta.recipe`)
  - Based on: miniconda-base
  - Includes: tomocupy and related dependencies
  - Environment: Python 3.11 with scientific computing stack

- **Tomopy** (`recipes/tomopy-1.0.0.recipe`)
  - Based on: miniconda-base
  - Includes: tomopy and related dependencies
  - Environment: Python 3.11 with scientific computing stack

- **XRF Maps** (`recipes/xrf_maps-beta.recipe`)
  - Based on: miniconda-base
  - Includes: XRF maps processing tools
  - Environment: Python 3.11 with scientific computing stack

## Building Containers

To build a container from a recipe file:

```bash
# Build a specific container
podman build -f recipes/boost_corr-1.0.0.recipe -t boost_corr:1.0.0

# Build all containers
for recipe in recipes/*.recipe; do
    name=$(basename "$recipe" .recipe | cut -d'-' -f1)
    version=$(basename "$recipe" .recipe | cut -d'-' -f2)
    podman build -f "$recipe" -t "$name:$version"
done
```

## Running Containers

To run a container interactively:

```bash
podman run -it <container_name>:<version> /bin/bash
```

## Pulling Pre-built Containers

Pre-built containers are available on GitHub Container Registry (ghcr.io):

```bash
podman pull ghcr.io/globus-gladier/aps_recipes/<container-name>:<version>
```

For example:

```bash
podman pull ghcr.io/globus-gladier/aps_recipes/boost_corr:1.0.0
```

## Development

### Setup

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Recipe Validation

The repository includes pre-commit hooks that validate recipe files for best practices:

- Base image must use a fully qualified name (e.g., `docker.io/...`)
- `apt-get` commands must include cleanup (`apt-get clean`)
- `conda install` commands must include cleanup (`conda clean -afy`)
- `pip install` commands must use `--no-cache-dir` flag
- Each container must have a `CMD` or `ENTRYPOINT` set to `/bin/bash`
- Each container must include `globus-compute-sdk` installation

To run validation manually:
```bash
pre-commit run --all
```

## Building and Publishing via GitHub Actions

The containers are built and published using GitHub Actions. Each container has its own workflow that can be triggered independently, or you can build all containers at once using the main workflow.

### Building Individual Containers

1. Go to the "Actions" tab in the GitHub repository
2. Select the workflow for the container you want to build
3. Click the "Run workflow" button
4. Select the branch and version
5. Click "Run workflow"

### Building All Containers

1. Go to the "Actions" tab
2. Select the "Build and Publish All Containers" workflow
3. Click "Run workflow"
4. Select the branch
5. Click "Run workflow"

## Notes

- Make sure you have sufficient disk space for building the containers
- The build process may take several minutes depending on your system
- Pre-built containers are automatically published to GitHub Container Registry
- Some containers require significant system resources for building

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file.
