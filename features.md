## feature / todo list
### if it's not checked it still needs ported

main:
- [x] use database for all config
- [x] separate like-actions into cogs
- [x] catch and log errors

new:
- [x] commands to change config - ConfigCog

loops:
- [x] new account role - MemberCog
- [x] member role - MemberCog
- [x] bump archived wiki posts - WikiCog

commands:
- [x] ask devs rules - TeamAnswersCog
- [x] wiki links - WikiCog
- [ ] post dev reply (not needed - contextmenu infinitely better)

context menu:
- [x] post dev reply - TeamAnswersCog

on_member_join:
- [x] New Account Role - MemberCog

on_raw_reaction_add:
- [x] auto remove  - ReactionsCog
- [x] reaction role - ReactionsCog
- [ ] monitor (still needed?)

on_scheduled_event_create:
- [x] add event ID to automod whitelist

on_raw_reaction_remove:
- [ ] monitor (still needed?)

on_message:
- [x] cheeky me check - MiscCog
- [x] check caps percent - MiscCog
- [x] auto publish - MiscCog
- [x] team answers - TeamAnswersCog
- [x] moderator tag ask-the-team - TeamAnswersCog

on_message_delete:
- [x] team answers - TeamAnswersCog

on_message_edit:
- [x] check caps percent - MiscCog
- [x] team answers - TeamAnswersCog

on_thread_create:
- [ ] LFG post checker - ForumCog
- [ ] support post auto reply - ForumCog
- [ ] auto pin - ForumCog
- [x] add reactions (full/half) - ReactionsCog

on_member_update:
- [ ] remove booster-related roles when booster removed (is this needed?)
