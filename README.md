# Checkbox checker

This GitHub action can be setup like this :
```
on:
  pull_request:
    types:
      - closed

jobs:
  if_merged:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
    - uses: Djipyy/amd-pr-checkbox@v1
      with:
        pat: ${{ secrets.PAT }}
        merging_pr_number: ${{ github.event.pull_request.number }}
        merging_pr_repository: ${{ github.event.pull_request.head.repo.full_name }}
```

When enabled, this action runs when a Pull Request (PR) is merged.

Once it is merged, it checks all the linked PRs. For each mention, it will check all comments and edit them if they match a certain template and checks the box.

The templates are :
``` - [] $PR_URL```
``` - [ ] $PR_URL```

This action could be improved by adding error handling, and adding a way to limit the scope of the edits. Right now, it tries to go through all the linked PRs even if they do not belong to us.