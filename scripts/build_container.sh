#!/bin/bash

# Script to build and push containers from recipes
# Usage: ./build_container.sh [recipe_file_path]

set -e  # Exit on error

# Function to check GitHub authentication
check_github_auth() {
    # Check if logged into ghcr.io
    if ! podman login ghcr.io --get-login >/dev/null 2>&1; then
        echo "Error: Not logged into ghcr.io. Please run: podman login ghcr.io"
        exit 1
    fi
    
    # Check if we're in the correct repository
    if ! git config --get remote.origin.url | grep -q "globus-gladier/aps_recipes"; then
        echo "Error: Not in the correct repository (globus-gladier/aps_recipes)"
        exit 1
    fi
}

# Function to display usage information
show_usage() {
    echo "Usage: $0 [recipe_file_path]"
    echo "Example: $0 recipes/tomopy-1.0.0.recipe"
}

# Function to list available recipes
list_recipes() {
    ls -1 recipes/*.recipe 2>/dev/null || echo "No recipe files found in recipes/ directory"
}

# Function to build a container
build_container() {
    local recipe_path=$1
    local container_name=$(basename "$recipe_path" .recipe)
    
    if [ ! -f "$recipe_path" ]; then
        echo "Error: Recipe file not found at ${recipe_path}"
        return 1
    fi
    
    podman build -t "${container_name}" -f "${recipe_path}" .
}

# Function to push a container
push_container() {
    local container_name=$1
    local ghcr_repo="ghcr.io/globus-gladier/aps_recipes"
    local base_name=$(echo "$container_name" | cut -d'-' -f1)
    local version=$(echo "$container_name" | cut -d'-' -f2)
    
    # Tag and push versioned container
    podman tag "${container_name}" "${ghcr_repo}/${base_name}:${version}"
    podman push "${ghcr_repo}/${base_name}:${version}"
    
    # Tag and push latest container
    podman tag "${container_name}" "${ghcr_repo}/${base_name}:latest"
    podman push "${ghcr_repo}/${base_name}:latest"
}

# Main script logic
main() {
    local recipe_path
    
    # Check GitHub authentication first
    check_github_auth
    
    # Check if recipe path was provided as argument
    if [ $# -eq 1 ]; then
        recipe_path=$1
    else
        list_recipes
        read -p "Enter the path to the recipe file (or 'q' to quit): " recipe_path
        [ "$recipe_path" = "q" ] || [ "$recipe_path" = "Q" ] && exit 0
    fi
    
    # Build and push the selected container
    build_container "$recipe_path" && push_container "$(basename "$recipe_path" .recipe)"
}

# Check if help was requested
[ "$1" = "-h" ] || [ "$1" = "--help" ] && show_usage && exit 0

# Run the main function
main "$@" 