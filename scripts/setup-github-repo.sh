#!/bin/bash

# WebWaka Digital Operating System - GitHub Repository Setup Script
# This script automates the creation and configuration of the GitHub repository

set -e  # Exit on any error

echo "🚀 WebWaka GitHub Repository Setup Starting..."

# Check if required environment variables are set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable not set"
    echo "Please set it with: export GITHUB_TOKEN=your_token_here"
    exit 1
fi

if [ -z "$GITHUB_ORG" ]; then
    echo "❌ Error: GITHUB_ORG environment variable not set"
    echo "Please set it with: export GITHUB_ORG=your_organization_name"
    exit 1
fi

# Repository configuration
REPO_NAME="webwaka-digital-operating-system"
REPO_DESCRIPTION="WebWaka Digital Operating System - Africa's Premier AI-Powered Partner-Driven Digital Transformation Operating System"

echo "📋 Configuration:"
echo "  Organization: $GITHUB_ORG"
echo "  Repository: $REPO_NAME"
echo "  Description: $REPO_DESCRIPTION"

# Create the repository using GitHub CLI or curl
echo "🔨 Creating GitHub repository..."

# Create repository using curl (GitHub REST API)
REPO_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"$REPO_DESCRIPTION\",
    \"private\": true,
    \"has_issues\": true,
    \"has_projects\": true,
    \"has_wiki\": true,
    \"auto_init\": false,
    \"allow_squash_merge\": true,
    \"allow_merge_commit\": true,
    \"allow_rebase_merge\": true,
    \"delete_branch_on_merge\": true
  }" \
  "https://api.github.com/orgs/$GITHUB_ORG/repos")

# Check if repository was created successfully
if echo "$REPO_RESPONSE" | grep -q "\"name\": \"$REPO_NAME\""; then
    echo "✅ Repository created successfully!"
else
    echo "❌ Failed to create repository. Response:"
    echo "$REPO_RESPONSE"
    exit 1
fi

# Add remote repository
echo "🔗 Adding remote repository..."
git remote add origin "git@github.com:$GITHUB_ORG/$REPO_NAME.git"

# Push to remote repository
echo "📤 Pushing code to GitHub..."
git push -u origin master

# Set up branch protection rules
echo "🛡️ Setting up branch protection..."
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -X PUT \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": ["continuous-integration"]
    },
    "enforce_admins": false,
    "required_pull_request_reviews": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews": true,
      "require_code_owner_reviews": false
    },
    "restrictions": null,
    "allow_force_pushes": false,
    "allow_deletions": false
  }' \
  "https://api.github.com/repos/$GITHUB_ORG/$REPO_NAME/branches/master/protection"

echo "✅ Branch protection rules configured!"

# Create development branch
echo "🌿 Creating development branch..."
git checkout -b development
git push -u origin development

# Switch back to master
git checkout master

echo "🎉 GitHub repository setup completed successfully!"
echo ""
echo "📋 Repository Details:"
echo "  URL: https://github.com/$GITHUB_ORG/$REPO_NAME"
echo "  SSH: git@github.com:$GITHUB_ORG/$REPO_NAME.git"
echo "  Branches: master (protected), development"
echo ""
echo "🔗 Next Steps:"
echo "  1. Configure team access in GitHub repository settings"
echo "  2. Set up Netlify deployment"
echo "  3. Configure CI/CD pipeline"
echo "  4. Add team members to repository"
echo ""
echo "✅ Zero-Loss Development Framework: ACTIVE"

