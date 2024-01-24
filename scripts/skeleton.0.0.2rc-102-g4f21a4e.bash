#!/usr/bin/env bash
# (C) 2023–present Bartosz Sławecki (bswck)
#
# Interact with bswck/skeleton (current version: https://github.com/bswck/skeleton/tree/0.0.2rc-102-g4f21a4e).
#
# This file was generated from bswck/skeleton@0.0.2rc-102-g4f21a4e.
# Instead of changing this particular file, you might want to alter the template:
# https://github.com/bswck/skeleton/tree/0.0.2rc-102-g4f21a4e/project/scripts/skeleton.%7B%7Bsref%7D%7D.bash.jinja
#
# Usage:
#
# To update to the latest version:
# $ poe skeleton upgrade
#
# To update to version 1.2.3:
# $ poe skeleton upgrade 1.2.3
#
# To make a mechanized repo patch, but keep the current skeleton version:
# $ poe skeleton patch
#
# It's intended to be impossible to make a mechanized repo patch and update the skeleton
# at the same time.

# shellcheck disable=SC2005,SC1091

set -eEuo pipefail

TEMPFILE=$(mktemp)

curl "https://raw.githubusercontent.com/bswck/skeleton/HEAD/setup.bash" > "$TEMPFILE"
trap 'rm -f "$TEMPFILE"' EXIT

# shellcheck disable=SC1090
source "$TEMPFILE"

make_context() {
	export POETRY_VERSION
	POETRY_VERSION=$(cat <<- 'EOF'
		1.7.1
	EOF
	)
	export GIT_USERNAME
	GIT_USERNAME=$(cat <<- 'EOF'
		bswck
	EOF
	)
	export GIT_EMAIL
	GIT_EMAIL=$(cat <<- 'EOF'
		bswck.dev@gmail.com
	EOF
	)
	export VISIBILITY
	VISIBILITY=$(cat <<- 'EOF'
		public
	EOF
	)
	export PUBLIC
	PUBLIC=$(cat <<- 'EOF'
		True
	EOF
	)
	export PRIVATE
	PRIVATE=$(cat <<- 'EOF'
		False
	EOF
	)
	export LATEST_PYTHON
	LATEST_PYTHON=$(cat <<- 'EOF'
		3.12
	EOF
	)
	export PYTHON_AHEAD
	PYTHON_AHEAD=$(cat <<- 'EOF'
		3.13
	EOF
	)
	export PYTHON
	PYTHON=$(cat <<- 'EOF'
		3.8
	EOF
	)
	export PYPY
	PYPY=$(cat <<- 'EOF'
		True
	EOF
	)
	export PYTHONS
	PYTHONS=$(cat <<- 'EOF'
		"3.8", "3.9", "3.10", "3.11", "3.12", "pypy3.8", "pypy3.9", "pypy3.10"
	EOF
	)
	export REPO_URL
	REPO_URL=$(cat <<- 'EOF'
		https://github.com/bswck/autorefine
	EOF
	)
	export COVERAGE_URL
	COVERAGE_URL=$(cat <<- 'EOF'
		https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/autorefine
	EOF
	)
	export DOCS_URL
	DOCS_URL=$(cat <<- 'EOF'
		https://autorefine.readthedocs.io/en/latest/
	EOF
	)
	export PYPI_URL
	PYPI_URL=$(cat <<- 'EOF'
		https://pypi.org/project/autorefine/
	EOF
	)
	export SKELETON
	SKELETON=$(cat <<- 'EOF'
		bswck/skeleton
	EOF
	)
	export SKELETON_URL
	SKELETON_URL=$(cat <<- 'EOF'
		https://github.com/bswck/skeleton
	EOF
	)
	export RAW_SKELETON_URL
	RAW_SKELETON_URL=$(cat <<- 'EOF'
		https://raw.githubusercontent.com/bswck/skeleton
	EOF
	)
	export SKELETON_REF
	SKELETON_REF=$(cat <<- 'EOF'
		0.0.2rc-102-g4f21a4e
	EOF
	)
	export SREF
	SREF=$(cat <<- 'EOF'
		0.0.2rc-102-g4f21a4e
	EOF
	)
	export SKELETON_REV
	SKELETON_REV=$(cat <<- 'EOF'
		https://github.com/bswck/skeleton/tree/0.0.2rc-102-g4f21a4e
	EOF
	)
	export SREV
	SREV=$(cat <<- 'EOF'
		https://github.com/bswck/skeleton/tree/0.0.2rc-102-g4f21a4e
	EOF
	)
	export SKELETON_AND_REF
	SKELETON_AND_REF=$(cat <<- 'EOF'
		bswck/skeleton@0.0.2rc-102-g4f21a4e
	EOF
	)
	export SNREF
	SNREF=$(cat <<- 'EOF'
		bswck/skeleton@0.0.2rc-102-g4f21a4e
	EOF
	)
	export GH_REPO_ARGS
	GH_REPO_ARGS=$(cat <<- 'EOF'
		"bswck/autorefine" --public --source=./ --remote=upstream --description="Scalable semi-automated code quality refining."
	EOF
	)
	export GH_ENSURE_ENV
	GH_ENSURE_ENV=$(cat <<- 'EOF'
		jq -n '{"deployment_branch_policy": {"protected_branches": false,"custom_branch_policies": true}}' | gh api -H "Accept: application/vnd.github+json" -X PUT "/repos/bswck/autorefine/environments/$1" --input -
	EOF
	)
    export LAST_REF="0.0.2rc-102-g4f21a4e"
    export PROJECT_PATH_KEY="$$_skeleton_project_path"
    export NEW_REF_KEY="$$_skeleton_new_ref"
    export LAST_LICENSE_NAME="GPL-3.0"
}

make_context
update_entrypoint "$@"
