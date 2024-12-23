# Contributing to the Project

## Table of Contents
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style and Standards](#code-style-and-standards)
- [Pull Request Process](#pull-request-process)

## Getting Started

Thank you for considering contributing to our project! This document will guide you through the process of making contributions.


## Development Workflow

1. **Find an Issue**
   - Browse through the [GitHub Issues](https://github.com/issues) section
   - Look for issues labeled as "good first issue" or "help wanted"
   - If you want to work on something new, create an issue first to discuss it

2. **Fork and Clone**
   - Fork the repository to your GitHub account
   - Clone your fork locally:
     ```bash
     git clone https://github.com/YOUR-USERNAME/REPOSITORY-NAME.git
     ```

3. **Create a Branch**
   - Create a new branch for your work:
     ```bash
     git checkout -b feature/issue-number-brief-description
     ```
   - Use meaningful branch names, preferably referencing the issue number

4. **Make Changes**
   - Write your code
   - Follow the project's coding standards
   - Keep commits atomic and write meaningful commit messages
   - Test your changes thoroughly

5. **Push Changes**
   - Push your changes to your fork:
     ```bash
     git push origin feature/issue-number-brief-description
     ```

## Code Style and Standards

### Formatting
- Code must be properly formatted according to project standards
- Run formatting checks before committing:
  ```bash
  make format
  ```

### Code Quality
- All code must pass the automated linting checks
- The project uses CI/CD pipelines to verify code quality
- Ensure all linting checks pass locally before pushing:
  ```bash
  make lint
  ```

## Pull Request Process

1. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with all required information

2. **PR Requirements**
   - Reference the related issue(s)
   - Provide a clear description of changes
   - Include any necessary documentation updates
   - Ensure all CI checks pass
   - Screenshots/GIFs for UI changes (if applicable)

3. **Code Review**
   - Request review from maintainers
   - Address any feedback promptly
   - Make requested changes if necessary
   - Maintain a respectful and collaborative attitude

4. **Merging**
   - PRs will be merged once they:
     - Have required approvals
     - Pass all CI checks (including linting)
     - Meet project quality standards
     - Have no unresolved discussions

---

Remember that all contributions are valued, no matter how small. If you're unsure about anything, don't hesitate to ask for help in the issue comments or PR discussion.
