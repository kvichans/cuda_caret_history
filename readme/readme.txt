Plugin for CudaText.
Plugin tracks changes of caret position, and when caret jumps long (more than 10 lines, option), it adds history point. So plugin keeps history of long caret jumps. It gives 2 commands: move backward, move forward, they change caret using this history. Short caret movements don't add to history (but they correct current history item). History length is 5 items by default (option).

The following scenario is working: you open file, jump to the end of file, history point is added, then "move backward" moves to begin of file. Then short editings don't change history, and "move forward" jumps to file end. Then short editings don't change history, and "move backward" jumps to file begin.

Options, which must be in the user.json:
- "carethistory_gap_size"
  Minimal difference (default: 10) of line-index from previous value, to store the new history item.
- "carethistory_max_history"
  Maximal history size (default: 5) for each document.

Author of idea: 
	github.com/eastorwest
Author: 
	Andrey Kvichanskiy (kvichans, at forum)
