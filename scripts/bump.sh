#!/usr/bin/env bash
# (C) 2023–present Bartosz Sławecki (bswck)
#
# Sync with bswck/skeleton.
# This script was adopted from https://github.com/bswck/skeleton/tree/ae71d66/project/scripts/bump.sh.jinja
#
# Usage:
# $ poe bump

# shellcheck disable=SC2005


# Automatically copied from https://github.com/bswck/skeleton/tree/ae71d66/handle-task-event.sh
make_token() {
    export TOKEN
    TOKEN="$(echo "$(date +%s%N)" | sha256sum | head -c "${1:-10}")"
}

stash() {
    make_token 32
    export STASH_TOKEN="$TOKEN"
    git stash push -m "$STASH_TOKEN"
}

unstash() {
    STASH_ID="$(echo "$("$(git stash list)" | grep "${1:-STASH_TOKEN}" | grep -oP "^stash@{\K(\d)+")")"
    git stash pop "stash@{$STASH_ID}"
}

setup_gh() {
    echo "Calling GitHub setup hooks..."
    supply_smokeshow_key
}

determine_project_path() {
    # Determine the project path set by the preceding copier task process
    export PROJECT_PATH
    PROJECT_PATH=$(redis-cli get "$PROJECT_PATH_KEY")
}

ensure_gh_environment() {
    # Ensure that the GitHub environment exists
    echo "$(jq -n '{"deployment_branch_policy": {"protected_branches": false, "custom_branch_policies": true}}' | gh api -H "Accept: application/vnd.github+json" -X PUT "/repos/bswck/autorefine/environments/$1" --input -)" > /dev/null 2>&1 || return 1
}

supply_smokeshow_key() {
    # Supply smokeshow key to the repository
    echo "Checking if smokeshow secret needs to be created..."
    ensure_gh_environment "Smokeshow"
    if test "$(gh secret list -e Smokeshow | grep -o SMOKESHOW_AUTH_KEY)"
    then
        echo "Smokeshow secret already exists, aborting." && return 0
    fi
    echo "Smokeshow secret does not exist, creating..."
    SMOKESHOW_AUTH_KEY=$(smokeshow generate-key | grep SMOKESHOW_AUTH_KEY | grep -oP "='\K[^']+")
    gh secret set SMOKESHOW_AUTH_KEY --env Smokeshow --body "$SMOKESHOW_AUTH_KEY" 2> /dev/null
    if test $? = 0
    then
        echo "Smokeshow secret created."
    else
        echo "Failed to create smokeshow secret." 1>&2
    fi
}
# End of copied code


determine_new_ref() {
    # Determine the new skeleton revision set by the child process
    export NEW_REF
    NEW_REF=$(redis-cli get "$NEW_REF_KEY")
}

before_update_algorithm() {
    # Stash changes if any
    if test "$(echo "$(git diff --name-only)")"
    then
        echo "There are uncommitted changes in the project."
        stash
    else
        echo "Working tree clean, no need to stash."
    fi
}

run_update_algorithm() {
    # Run the underlying update algorithm
    copier update --trust --vcs-ref "${1:-"HEAD"}" "${@:2}" || return 1
    determine_new_ref
    determine_project_path
}

after_update_algorithm() {
    # Run post-update hooks, auto-commit changes
    cd "$PROJECT_PATH" || exit 1

    echo "Previous skeleton revision: $LAST_REF"
    echo "Current skeleton revision: ${NEW_REF:-"N/A"}"

    local REVISION_PARAGRAPH="Skeleton revision: https://github.com/bswck/skeleton/tree/${NEW_REF:-"HEAD"}"

    git add .
    if test "$LAST_REF" = "$NEW_REF"
    then
        echo "The version of the skeleton has not changed."
        local COMMIT_MSG="Patch .copier-answers.yml at bswck/skeleton@$NEW_REF"
    else
        if test "$NEW_REF"
        then
            local COMMIT_MSG="Upgrade to bswck/skeleton@$NEW_REF"
        else
            local COMMIT_MSG="Upgrade to bswck/skeleton of unknown revision"
        fi
    fi
    redis-cli del "$PROJECT_PATH_KEY" > /dev/null 2>&1
    redis-cli del "$NEW_REF_KEY" > /dev/null 2>&1
    echo "Press ENTER to commit the changes or CTRL+C to abort."
    read -r || exit 1
    git commit --no-verify -m "$COMMIT_MSG" -m "$REVISION_PARAGRAPH"
    setup_gh
    if test "$STASH_TOKEN"
    then
        echo "Unstashing changes..."
        unstash && echo "Done!"
    fi
}

main() {
    export LAST_REF="ae71d66"
    export PROJECT_PATH_KEY="$$_skeleton_project_path"
    export NEW_REF_KEY="$$_skeleton_new_ref"
    export LAST_LICENSE_NAME="GPL-3.0"

    cd "${PROJECT_PATH:=$(git rev-parse --show-toplevel)}" || exit 1
    echo
    echo "--- Last skeleton revision: $LAST_REF"
    echo
    echo "UPDATE ROUTINE [1/3]: Running pre-update hooks."
    echo "[---------------------------------------------]"
    before_update_algorithm || exit 1
    echo "[---------------------------------------------]"
    echo "UPDATE ROUTINE [1/3] COMPLETE. ✅"
    echo
    echo "UPDATE ROUTINE [2/3]: Running the underlying update algorithm."
    echo "[------------------------------------------------------------]"
    run_update_algorithm "$@" || exit 1
    echo "[------------------------------------------------------------]"
    echo "UPDATE ROUTINE [2/3] COMPLETE. ✅"
    echo
    echo "--- Project path: $PROJECT_PATH"
    echo
    echo "UPDATE ROUTINE [3/3]: Running post-update hooks."
    echo "[----------------------------------------------]"
    after_update_algorithm
    echo "[----------------------------------------------]"
    echo "UPDATE ROUTINE [3/3] COMPLETE. ✅"
    echo
    echo "Done! 🎉"
    echo
    echo "Your repository is now up to date with this bswck/skeleton revision:"
    echo "https://github.com/bswck/skeleton/tree/${NEW_REF:-"HEAD"}"
}

main "$@"