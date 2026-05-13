# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
__conda_activate () {
	if [ -n "${CONDA_PS1_BACKUP:+x}" ]
	then
		PS1="$CONDA_PS1_BACKUP" 
		\unset CONDA_PS1_BACKUP
	fi
	\local ask_conda
	ask_conda="$(PS1="${PS1:-}" __conda_exe shell.posix "$@")"  || \return
	\eval "$ask_conda"
	__conda_hashr
}
__conda_exe () {
	(
		if [ -n "${_CE_M:+x}" ] && [ -n "${_CE_CONDA:+x}" ]
		then
			"$CONDA_EXE" $_CE_M $_CE_CONDA "$@"
		else
			"$CONDA_EXE" "$@"
		fi
	)
}
__conda_hashr () {
	if [ -n "${ZSH_VERSION:+x}" ]
	then
		\rehash
	elif [ -n "${POSH_VERSION:+x}" ]
	then
		:
	else
		\hash -r
	fi
}
__conda_reactivate () {
	echo "'__conda_reactivate' is deprecated and will be removed in 25.9. Use '__conda_activate reactivate' instead." >&2
	__conda_activate reactivate
}
conda () {
	\local cmd="${1-__missing__}"
	case "$cmd" in
		(activate | deactivate) __conda_activate "$@" ;;
		(install | update | upgrade | remove | uninstall) __conda_exe "$@" || \return
			__conda_activate reactivate ;;
		(*) __conda_exe "$@" ;;
	esac
}
pyenv () {
	local command=${1:-} 
	[ "$#" -gt 0 ] && shift
	case "$command" in
		(rehash | shell) eval "$(pyenv "sh-$command" "$@")" ;;
		(*) command pyenv "$command" "$@" ;;
	esac
}
# Shell Options
setopt nohashdirs
setopt login
# Aliases
alias -- get_idf='. /Users/fireowl/.espressif/v5.5.3/esp-idf/export.sh'
alias -- run-help=man
alias -- which-command=whence
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  function rg {
  local _cc_bin="${CLAUDE_CODE_EXECPATH:-}"
  [[ -x $_cc_bin ]] || _cc_bin=$(command -v claude 2>/dev/null)
  if [[ ! -x $_cc_bin ]]; then command rg "$@"; return; fi
  if [[ -n $ZSH_VERSION ]]; then
    ARGV0=rg "$_cc_bin" "$@"
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ARGV0=rg "$_cc_bin" "$@"
  elif [[ $BASHPID != $$ ]]; then
    exec -a rg "$_cc_bin" "$@"
  else
    (exec -a rg "$_cc_bin" "$@")
  fi
}
fi
export PATH='/Users/fireowl/.pyenv/shims:/Users/fireowl/.juliaup/bin:/Applications/Julia-1.12.app/Contents/Resources/julia/bin:/Users/fireowl/Library/Application Support/Code/User/globalStorage/github.copilot-chat/debugCommand:/Users/fireowl/Library/Application Support/Code/User/globalStorage/github.copilot-chat/copilotCli:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/opt/pkg/env/active/bin:/opt/pmk/env/global/bin:/opt/X11/bin:/Applications/VMware Fusion.app/Contents/Public:/Users/fireowl/Library/Application Support/Code/User/globalStorage/github.copilot-chat/debugCommand:/Users/fireowl/Library/Application Support/Code/User/globalStorage/github.copilot-chat/copilotCli:/Users/fireowl/Library/pnpm:/Users/fireowl/.juliaup/bin:/Applications/Julia-1.12.app/Contents/Resources/julia/bin:/opt/miniconda3/bin:/opt/miniconda3/condabin:/Users/fireowl/.cargo/bin:/Applications/Obsidian.app/Contents/MacOS:/Users/fireowl/.vscode/extensions/ms-python.debugpy-2025.18.0-darwin-arm64/bundled/scripts/noConfigScripts:/Applications/Obsidian.app/Contents/MacOS:/Users/fireowl/.claude/plugins/cache/everything-claude-code/everything-claude-code/1.2.0/bin:/Users/fireowl/.claude/plugins/cache/zai-coding-plugins/glm-plan-bug/0.0.1/bin:/Users/fireowl/.claude/plugins/cache/zai-coding-plugins/glm-plan-usage/0.0.1/bin:/Users/fireowl/.claude/plugins/cache/axton-obsidian-visual-skills/obsidian-visual-skills/f934f80c11fc/bin:/Users/fireowl/.claude/plugins/cache/claude-code-plugins/ralph-wiggum/1.0.0/bin:/Users/fireowl/.claude/plugins/cache/webnovel-writer-marketplace/webnovel-writer/5.5.4/bin:/Users/fireowl/.claude/plugins/cache/claude-hud/claude-hud/0.0.10/bin'
