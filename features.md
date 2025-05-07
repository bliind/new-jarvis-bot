# Feature List

- Main:
  - All config items are housed in a sqlite3 database
  - Similarly themed actions are grouped together in Cogs
  - All errors caught and logged to terminal with details

- ConfigCog:
  - Handles looking at, modifying, and deleting configuration keys

- EventCog:
  - Updates an automod rule to exclude event links from a discord link block rule

- ForumCog:
  - Auto pin OP on thread creation
  - Alliance recruitment post format check

- MemberCog:
  - Gives server members a role after a specified amount of hours on the server
  - Gives fresh discord accounts a role and removes it after the specified age has been reached

- MiscCog:
  - Checks posts for too many caps and deletes them with a message
  - Auto publish new posts in specified announcement channels

- ReactionsCog:
  - Handles removing country flag reacts in specified channels
  - Auto removes specified emotes
  - Adds emotes to new threads in specified forum channels

- TeamAnswersCog:
  - Monitors for developer replies to forum channels and posts them with the question in a designated answers channel
  - Also monitors for edited or deleted answers and updates the answers channel accordingly
  - A command (ContextMenu) to manually post a developer reply, in the event it is in a forum we do not monitor
  - Adds tags to posts with replies from developers or moderators to questions forum channels

- WikiCog:
  - Automatically un-archives threads in specified wiki channel
  - A command for linking commonly used wiki pages
