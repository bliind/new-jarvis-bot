# Config keys
what they are and what they do

_roles and channels are IDs_

_singular key name means only one entry_

| key | description | used by |
| --- | --- | --- |
| moderator_roles | moderator roles | MiscCog |
| caps_prot_immune_channels | channels where caps aren't checked | MiscCog |
| caps_prot_immune_roles | roles who don't have caps checked | MiscCog |
| caps_prot_message | message to users who use too many caps | MiscCog |
| caps_prot_percent | percentage of message that has to be caps to catch | MiscCog |
| auto_publish_channels | channels to auto publish every message | MiscCog |
| no_flag_channels | channels to not allow country flag reactions | ReactionsCog |
| banned_emotes | emotes to automatically remove | ReactionsCog |
| full_react_channels | forum channels where new threads should get all forum reacts | ReactionsCog |
| full_react_emotes | emotes to react to new threads in full_react_channels | ReactionsCog |
| half_react_channels | forum channels to receive half forum reacts | ReactionsCog |
| half_react_emotes | emotes to react to new thread in half_react_channels | ReactionsCog |
| reaction_role_users | users who can grant a role with a reaction | ReactionsCog |
| reaction_role_reaction | the reaction to trigger off of | ReactionsCog |
| reaction_role_role | the role to grant | ReactionsCog |
| wiki_channel | the wiki channel to auto bump archived threads | WikiCog |
| wiki_links | links to common wiki pages for use with /wiki | WikiCog |
| new_account_role | a role to give fresh discord accounts | MembersCog |
| new_account_day_count | how many days old is no longer "fresh" | MembersCog |
| member_role | a role granted to members after member_hour_count hours on the server | MembersCog |
| member_hour_count | how long after join to grant users member_role | MembersCog |
| developer_roles | developer roles | TeamAnswersCog |
| team_answer_channel | the channel to post the devreply posts | TeamAnswersCog |
| team_question_channels | the channels to monitor for dev replies | TeamAnswersCog |
| team_response_tag | the forum tag to apply to answered posts | TeamAnswersCog |
| moderator_response_tag | the forum tag to apply when a mod responds in a team_question_channels | TeamAnswersCog |
| askdevs_message | The message of the ask-the-team guidelines to post with /askdevs | TeamAnswersCog |
| automod_links_name | the name of the automod rule that blocks (discord) links | EventCog |
| auto_pin_channels | channels to automatically pin the OP upon creation | ForumCog |
| alliance_channels | forum channels to check post formatting | ForumCog |
