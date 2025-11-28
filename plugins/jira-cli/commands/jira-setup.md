# Jira CLI Setup Command

Initialize and configure jira-cli for seamless Jira integration.

## Instructions

Guide the user through the complete jira-cli setup process, from installation to configuration.

### Step 1: Check Installation

First, verify if jira-cli is installed:

```bash
which jira
jira version
```

If not installed, provide platform-specific installation instructions:

**macOS (Homebrew):**
```bash
brew install ankitpokhrel/jira-cli/jira-cli
```

**Linux (using install script):**
```bash
curl -sL https://raw.githubusercontent.com/ankitpokhrel/jira-cli/main/install.sh | sh
```

**Go install:**
```bash
go install github.com/ankitpokhrel/jira-cli/cmd/jira@latest
```

**Manual download:**
- Visit: https://github.com/ankitpokhrel/jira-cli/releases
- Download the appropriate binary for the user's platform
- Extract and move to PATH

### Step 2: Gather Jira Information

Ask the user for necessary Jira details:

1. **Jira Installation Type**
   - Cloud (https://yourcompany.atlassian.net)
   - Server/Data Center (https://jira.yourcompany.com)

2. **Jira Server URL**
   - Full URL to their Jira instance
   - Example: `https://company.atlassian.net` or `https://jira.company.com`

3. **Authentication Method**
   - **Cloud**: Typically uses API tokens
   - **Server**: May use basic auth or PAT (Personal Access Token)

4. **Project Key**
   - Default project key (e.g., PROJ, DEV, TEAM)
   - Users can configure multiple projects later

### Step 3: Initialize Configuration

Run the interactive initialization:

```bash
jira init
```

This will prompt for:
1. Installation type (Cloud or Local)
2. Jira URL
3. Login email (for Cloud) or username (for Server)
4. API token or password
5. Default project

**IMPORTANT**: Inform users:
- For **Jira Cloud**: They need to create an API token
  - Go to: https://id.atlassian.com/manage-profile/security/api-tokens
  - Click "Create API token"
  - Give it a name (e.g., "jira-cli")
  - Copy the token (they won't be able to see it again)

- For **Jira Server**: They might need to enable API access or use credentials

### Step 4: Set Environment Variables (Optional but Recommended)

For enhanced security, users can set environment variables instead of storing credentials in config:

```bash
# Add to ~/.bashrc or ~/.zshrc
export JIRA_API_TOKEN="your-api-token-here"
export JIRA_AUTH_TYPE="bearer"  # For PAT authentication
```

### Step 5: Verify Configuration

Test the configuration:

```bash
# List projects to verify connection
jira project list --plain

# List issues in default project
jira issue list --plain

# View current configuration
cat ~/.config/.jira/.config.yml
```

If any command fails, troubleshoot:
- Check URL is correct (including https://)
- Verify API token is valid
- Ensure user has correct permissions
- Check network connectivity

### Step 6: Configure Multiple Projects (Optional)

For users working with multiple projects:

1. **Create named config files:**
   ```bash
   jira init --config ~/.config/.jira/.config.project1.yml
   jira init --config ~/.config/.jira/.config.project2.yml
   ```

2. **Use different configs:**
   ```bash
   jira issue list -c ~/.config/.jira/.config.project1.yml
   jira issue list -c ~/.config/.jira/.config.project2.yml
   ```

3. **Set via environment variable:**
   ```bash
   export JIRA_CONFIG_FILE=~/.config/.jira/.config.project1.yml
   jira issue list
   ```

4. **Create aliases for convenience:**
   ```bash
   alias jira-proj1='jira -c ~/.config/.jira/.config.project1.yml'
   alias jira-proj2='jira -c ~/.config/.jira/.config.project2.yml'
   ```

### Step 7: Shell Completion (Optional)

Enable shell completion for better UX:

**Bash:**
```bash
echo 'eval "$(jira completion bash)"' >> ~/.bashrc
source ~/.bashrc
```

**Zsh:**
```bash
echo 'eval "$(jira completion zsh)"' >> ~/.zshrc
source ~/.zshrc
```

**Fish:**
```bash
jira completion fish > ~/.config/fish/completions/jira.fish
```

### Step 8: Test Common Operations

Run through basic operations to ensure everything works:

```bash
# 1. List recent issues
jira issue list --plain

# 2. View a specific issue (use actual issue key from list)
jira issue view PROJ-123 --plain

# 3. Check sprints (if using Scrum)
jira sprint list --plain

# 4. View boards
jira board list --plain
```

## Troubleshooting

### Common Issues and Solutions

**1. "jira: command not found"**
- Solution: Install jira-cli using one of the methods above
- Verify installation: `which jira`
- Ensure binary is in PATH

**2. "unauthorized" or "401" error**
- Solution: Check API token or credentials
- For Cloud: Regenerate API token at https://id.atlassian.com/manage-profile/security/api-tokens
- For Server: Verify username/password

**3. "project not found" or "404" error**
- Solution: Verify project key is correct
- List available projects: `jira project list`
- Check user has access to project

**4. "forbidden" or "403" error**
- Solution: User lacks permissions
- Contact Jira administrator
- Verify user is added to project

**5. Configuration file not found**
- Solution: Run `jira init` to create config
- Check config location: `~/.config/.jira/.config.yml`
- Set custom location: `export JIRA_CONFIG_FILE=/path/to/config.yml`

**6. SSL/TLS certificate errors (Server only)**
- Solution: For self-signed certs, may need to configure mtls
- Check with system administrator
- See: https://github.com/ankitpokhrel/jira-cli#mtls

**7. Slow performance**
- Solution: Reduce query scope
- Use specific project filters
- Limit number of results: Add `--limit` flag
- Use `--plain` instead of default interactive mode for scripts

## Configuration File Structure

The config file (`~/.config/.jira/.config.yml`) contains:

```yaml
installation: Cloud # or Local for Server
server: https://company.atlassian.net
login: your-email@company.com # or username for Server
project:
  key: PROJ
  type: scrum # or kanban
```

Users can manually edit this file if needed.

## Security Best Practices

1. **Never commit config files** to version control
   ```bash
   echo ".jira/" >> ~/.gitignore
   ```

2. **Use environment variables** for sensitive data
   ```bash
   export JIRA_API_TOKEN="token-here"
   unset JIRA_API_TOKEN  # Clear when done
   ```

3. **Restrict config file permissions**
   ```bash
   chmod 600 ~/.config/.jira/.config.yml
   ```

4. **Rotate API tokens** regularly
   - Cloud: Regenerate at Atlassian
   - Server: Update in settings

5. **Use separate tokens** for different purposes
   - Personal use
   - CI/CD automation
   - Shared scripts

## Advanced Configuration

### Custom Fields

If using custom fields:

```bash
jira init --custom-field-key=customfield_10001
```

### Proxy Settings

For corporate proxies:

```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
jira issue list
```

### Debug Mode

Enable debug output for troubleshooting:

```bash
jira issue list --debug
```

## Definition of Done

- [ ] jira-cli is installed and accessible in PATH
- [ ] Configuration file created with correct Jira URL and credentials
- [ ] Successfully authenticated to Jira instance
- [ ] Can list projects: `jira project list --plain`
- [ ] Can list issues: `jira issue list --plain`
- [ ] Can view an issue: `jira issue view PROJ-123 --plain`
- [ ] Shell completion configured (optional)
- [ ] Multiple project configs set up (if needed)
- [ ] User understands how to use --plain and --raw flags
- [ ] Security best practices discussed and implemented

## Next Steps

After successful setup, suggest:

1. **Explore commands**: Run `jira --help` to see all available commands
2. **Use agents**: Leverage the jira-manager, jira-sprint-master, and jira-query-builder agents
3. **Create workflows**: Use `/jira-issue-workflow` for common issue operations
4. **Sprint planning**: Use `/jira-sprint-planning` for agile ceremonies
5. **Learn JQL**: Use jira-query-builder agent for advanced queries

## Notes

- Configuration is stored in `~/.config/.jira/`
- API tokens for Cloud never expire unless revoked
- Server tokens may have expiration policies
- Users can have multiple config files for different projects
- The `--config` or `-c` flag allows switching between configurations

Inform the user that they can always run `jira init` again to reconfigure or add new projects.
