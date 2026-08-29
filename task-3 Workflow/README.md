Git & Collaboration Workflow

Overview

This project demonstrates a basic Git and GitHub collaboration workflow for managing software projects.

The workflow includes repository initialization, meaningful commits, branch creation, feature development, merging, and documentation.

Git Workflow

The workflow followed in this project is:

1. Create a Git repository.
2. Add project files.
3. Make meaningful commits.
4. Create a feature branch.
5. Make changes on the feature branch.
6. Commit the changes.
7. Merge the feature branch into the main branch.
8. Push the project to GitHub.

Branches

Main Branch

The main branch contains the stable version of the project.

Feature Branch

A separate feature branch is used for making changes without directly modifying the main branch.

Example:

git checkout -b feature/documentation

Meaningful Commits

Example commit messages used in the workflow:

Initial project setup
Add project documentation
Update README with setup instructions

Each commit describes the change made instead of using unclear messages such as update or changes.

Useful Git Commands

Initialize repository:

git init

Check repository status:

git status

Add files:

git add .

Commit changes:

git commit -m "Initial project setup"

Create a branch:

git checkout -b feature/documentation

Switch branches:

git checkout main

Merge a branch:

git merge feature/documentation

View commit history:

git log --oneline

Repository Structure

task-3-git-workflow/
└── README.md

Collaboration Practices

The workflow demonstrates:

* Separate feature development
* Meaningful commit messages
* Branch-based development
* Merging completed work into the main branch
* Documentation through README
* GitHub repository management

Conclusion

This project demonstrates a basic Git and GitHub workflow that can be used for organized and collaborative software development.
## Version

Version 1.0 - Initial documented workflow.