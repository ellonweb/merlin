{% extends "base.tpl" %}
{% block content %}
<table cellspacing="0" cellpadding="0" width="70%" class="black">
<tr class="datahigh"><th>
Introduction to {{ bot }}
</th></tr>
<td>{% filter force_escape|linebreaks %}
Things you need to do as soon as you join {{ alliance }}:
!pref password=xxx - Do this in PM with {{ bot }}, this will allow you to use {{ alliance }}.tv and !letmein if P is down.

!pref planet=x:y:z - This will allow {{ bot }} to use your co ords for things such as !lookup, !xp, !basher etc.

!pref phone=#### - Will add your phone-number to {{ bot }}.

!pref pubphone=(T/F) - Toggles whether your phone number is public or private.
!phone allow/deny <nick> - Allows you to create a list of people who can see your phone number even when it is private.

Different prefixes (!lookup, -lookup, @lookup):
~, - or . - {{ bot }} will notice you the response
@ - {{ bot }} will PM you the response
! - {{ bot }} will respond in the channel

Try not to use ! in public to prevent spamming the channel
{% endfilter %}</td>
<tr class="datahigh"><th>
Basic Commands
</th></tr>
<td>{% filter force_escape|linebreaks %}
!lookup <x:y:z/nick/alliance> - Shows basic information on planets/alliances. Leave blank to use your co ords, nick only works for those who have set !pref planet

!intel <x:y:z> - Shows intel for a planet. Add nick=, alliance= or comment= to the end of the line to modify intel.

!search <nick/alliance> - Searches intel for a phrase.
{% endfilter %}</td>
<tr class="datahigh"><th>
Propositions and Cookies
</th></tr>
<td>{% filter force_escape|linebreaks %}
Cookies are used to give out carebears. Carebears are rewards for carefaces. Give cookies to people when you think they've done something beneficial for you or for the alliance in general.

A proposition is a vote to do something. For now, you can raise propositions to invite or kick someone. Once raised the proposition will stand until you expire it.  Make sure you give everyone time to have their say. Votes for and against a proposition are weighted by carebears. You must have at least 1 carebear to vote.

!cookie [howmany] <receiver> <reason> | [stat]

!prop <invite|kick> <pnick> <comment>
!prop vote <number> <yes|no|abstain>
!prop show <number>
!prop cancel <number>
!prop expire <number> - Close the proposition and count the votes.

!prop list - List active propositions.
!prop recent - List recently expired propositions.
!prop search <pnick> - Search all active and expired propositions related to <pnick>.
{% endfilter %}</td>
<tr class="datahigh"><th>
Setting up your Gal
</th></tr>
<td>{% filter force_escape|linebreaks %}
!galchan <#channel> - Add {{ bot }} to your channel. Make sure {{ bot }} is added to P with 24 access first!
!remchan <#channel>
!galmate <pnick> - Add your galmates to the bot with low level access, they can store their planet, phone, etc.
!remuser <pnick>
{% endfilter %}</td>
<tr class="datahigh"><th>
Phone
</th></tr>
<td>{% filter force_escape|linebreaks %}
!pref phone=#### - Will add your phone-number to {{ bot }}.

!phone <allow/deny> <nick> - Add or remove a user to those able to see your number.
!phone list - List those able to see your number, as set by allow/deny. This list is ignore if you set !pref pubphone=yes.
!phone show <nick> - Show someone's number.

!sms <nick> <message> - Sends an SMS to the specified user. Your username will be appended to the end of each sms. The user must have their phone correctly added and you must have access to their number.
{% endfilter %}</td>
<tr class="datahigh"><th>
Scans
</th></tr>
<td>{% filter force_escape|linebreaks %}
Scanners should paste scan urls (group or individual) in any channel {{ bot }} is in, or in PM

!scans <x:y:z> - Shows most recent scan of every type of a planet.
!planet <x:y:z> - Shows most recent planet scan of the planet.
!dev <x:y:z> - Shows most recent development scan of the planet.
!unit <x:y:z> - Shows most recent unit scan of the planet.
!news <x:y:z> - Shows most recent news scan of the planet.
!jgp <x:y:z> - Shows most recent jumpgate scan of the planet.
!au <x:y:z> - Shows most recent advanced unit scan of the planet.
{% endfilter %}</td>
<tr class="datahigh"><th>
Defence
</th></tr>
<td>{% filter force_escape|linebreaks %}
!mydef <# of fleets>x <ship count> <ship name> <comment> - Use this to update what you have free for defence.

!searchdef <minimum ship count> <ship name> - Use this to search for available ships and fleets.

!showdef <pnick> - Show a user's available ships and fleets.

!usedef <pnick> <ship> - Remove a user's ship from the available defence ships.
{% endfilter %}</td>
<tr class="datahigh"><th>
Attacking
</th></tr>
<td>{% filter force_escape|linebreaks %}
!launch - <class|eta> <land_tick> - Calculate launch tick, launch time, prelaunch tick and prelaunch modifier for a given ship class or eta, and land tick.

!book <x:y:z> <land tick/eta> - Books a target with {{ bot }}. Please book all your targets to avoid piggies/miscommunications.
!unbook <x:y:z> <land tick/eta>

!status [<nick|user>|<x:y[:z]>] [tick] - Show bookings made by nick/user or on gal/planet, at optional landing tick.

!bitches [minimum eta] - Shows number of active bookings by galaxy and by alliance.

!gangbang [alliance] [tick] - Shows booking status for specified alliance.
{% endfilter %}</td>
<tr class="datahigh"><th>
Ship Calcs
</th></tr>
<td>{% filter force_escape|linebreaks %}
!ship <shipname> - Show stats for a ship.

!eff <number> <shipname> [t1|t2|t3] - Ship efficiencies.
!stop <number> <ship to stop> [t1|t2|t3] - Reverse ship efficiencies.

!cost <number> <shipname> - Resource cost to build this ship, and how much value it adds.

!afford <x:y:z> <shipname> - Will tell you how many of a certain ship the specified planet can build based on unspent and in production resources in the most recent planet scan.

!prod <number> <shipname> <factories> - Calculate the amount of time it will take to prod <n> <ship> with <factories>.
{% endfilter %}</td>
<tr class="datahigh"><th>
Planet
</th></tr>
<td>{% filter force_escape|linebreaks %}
!bashee <x:y:z> - Score/value limits to hit specific planet.
!basher <x:y:z> - Score/value limits specific planet can hit.

!value <x:y:z> - Shows value and roid change over the last 72 ticks.
!exp <x:y:z> - Shows xp and roid change over the last 72 ticks.

!maxcap (<total roids>|<x:y:z>) - Shows how many roids you will cap.
!xp <x:y:z> [a:b:c] - Shows how much XP you will gain by landing first wave, option second planet to specify attacking planet (defaults to your planet).

!roidcost <roids> <_value_ cost> [mining_bonus] - Tells you how long it will take to repay your lost value from the capped roids.
!roidsave <roids> <ticks> [mining_bonus] - Tells you how much value will be mined by a number of roids in that many ticks. M=Max, F=Feudalism, D=Democracy.
{% endfilter %}</td>
<tr class="datahigh"><th>
Target Search
</th></tr>
<td>{% filter force_escape|linebreaks %}
A few commands are available for searching for a target:
!cunts [alliance] [race] [<|>][size] [<|>][value] [bash] - Limited to planets currently attacking us, useful for retals.
!idler [alliance] [race] [<|>][size] [<|>][value] [bash] - Sort by idle ticks.
!victim [alliance] [race] [<|>][size] [<|>][value] [bash] - Sort by potential roids.
!whore [alliance] [race] [<|>][size] [<|>][value] [bash] - Sort by potential xp.
{% endfilter %}</td>
<tr class="datahigh"><th>
Alliance
</th></tr>
<td>{% filter force_escape|linebreaks %}
!bumchums <alliance> <number> - Shows galaxies with at least this number of players from the specified alliance.

!info [alliance] - All information taken from intel, for tag information use the lookup command.

!racism <alliance> - Racial breakdown of an alliance based on intel.
{% endfilter %}</td>
<tr class="datahigh"><th>
Misc
</th></tr>
<td>{% filter force_escape|linebreaks %}
!epenis <user> - Score growth of user's planet over 72 ticks.
!apenis <alliance>
!galpenis <x:y>
!bigdicks - Shows the current top five epenis in the alliance

!exile - Shows information regarding chances of landing in desired galaxies.

!surprisesex [<[x:y[:z]]|[alliancename]>] - Shows total incoming on the planet/gal/alliance from the whole round, sorted by alliance.
!topcunts [<[x:y[:z]]|[alliancename]>] - Shows total incoming on the planet/gal/alliance from the whole round, sorted by planet.
{% endfilter %}</td>
</th></tr>
</table>
{% endblock %}
