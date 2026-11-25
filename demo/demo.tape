Output demo/demo.gif

Set WaitTimeout 90s
Set Shell "bash"
Set FontFamily "DejaVu Sans Mono"
Set FontSize 18
Set Width 1200
Set Height 650
Set Padding 20
Set Theme "Catppuccin Mocha"
Set TypingSpeed 50ms

# Hidden preparation: not recorded
Hide
Type "source ./env.sh > /dev/null && export TOOLED_AI_AGENT_HOME=$(mktemp -d) && export PS1='$ ' && clear"
Enter
Sleep 1s
Show

Type "tooled"
Enter
Wait /❯/

Type "/help"
Enter
Wait /❯$/
Sleep 3s

Type "/models"
Enter
Wait /❯$/
Sleep 3s

Type "Calculate 15% of 2400, then add 7% VAT to the result"
Enter
Sleep 2s
Hide
Wait /❯$/
Show
Sleep 3s

Type "What time is it in Kyiv?"
Enter
Sleep 2s
Hide
Wait /❯$/
Show
Sleep 3s

Type "/usage"
Enter
Wait /❯$/
Sleep 2s

Type "/search VAT"
Enter
Wait /❯$/
Sleep 3s
