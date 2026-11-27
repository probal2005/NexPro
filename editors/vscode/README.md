# NexPro for VS Code

NexPro syntax highlighting for `.pa` files, plus a command to check the active
file and its imports using the installed NexPro CLI.

## Install

1. Install the NexPro CLI with Python 3.11 or later. See the
   [CLI installation guide](https://github.com/probal2005/NexPro/blob/main/docs/HELP.md).
2. Download `nexpro-1.4.0.vsix` from the
   [NexPro 1.4.0 release](https://github.com/probal2005/NexPro/releases/tag/v1.4.0).
3. Run `code --install-extension nexpro-1.4.0.vsix`, or choose
   **Extensions → … → Install from VSIX…**.

Open a `.pa` file and select **NexPro: Check Syntax** from the Command Palette.
The command saves the file, runs `nexpro check`, and reports syntax errors in
the **Problems** panel. If VS Code cannot find the CLI, set
`nexpro.executablePath` in User Settings to the executable in your Python
environment. Paths containing spaces are passed directly to the executable.
