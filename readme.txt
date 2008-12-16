Readme o:

Admins defined in `variables.admins` are developer only commands, Quit, Raw, Debug, Hop, Load etc. This is separate from the DB driven user system.

A little explanation of the Hooks/Plugin system:
All form of user authentication is handled inside `Core.chanusertracker` and `Core.loadable`. Hooks should superclass `Core.modules.M.loadable.loadable`.
Hooks' docstrings are used for help.
Hooks should define an access list, bitwise ORing different values from the `variables.access` dictionary. Not defining an access value will allow ANYONE access. Setting the value to zero (the default is -1) gives any active users access (even if they have zero access) (suitable for galmate access, see below).
Hooks should compile a regex for searching for their parameters if any are required.
Hooks can also edit a string provided for usage information of the command.
"	def execute(self, message):
		user, params = loadable.execute(self, message) or (None,None)
		if not params:
			return"
This code snippet will handle user authentication, parameters etc. If the user doesn't have access to the command, None is returned, which loses out to (None, None), meaning that params will also be set to None. If no parameters are required (and a parameter regex has not been set - thus defaulting to the command regex), the result of the command regex is returned in params, so the check here is still valid.
A hook could also write it's own has_access method. I don't recommend this though! Adduser uses it own has_access.
Hooks can be grouped together in a package. This means they can only be reloaded together (a pro and a con), but it makes things better organised I think.

The user system:
Instead of deleting users, we can/should unset the user's active field.
Asc style galmate access can be provided by having a user added with the active field set, but the access field being zero.
Access column is an integer, a value calculated from the "flags" defined in `variables.access`. (Asc might only need two levels, member and admin (I've refrained from calling this HC!) (remember this admin is different from the list of Pnicks defined in `variables.admins`).
I will perhaps code two different usercontrol plugins; one Asc style sponsor/invite/gimps, the other for a more "traditional" alliance structure. (You guys don't need to worry about the latter though if you don't want to.) (I've since ported my old code for a traditional alliance, porting Munin's code should be fairly straight forward with this as a guideline.)
Regarding user passwords, they are currently hashed using the DB's native MD5 (no salt). This is coded in two different places (both in the User class) if you want to change the hash and/or add salts: a validator for setting the password (when you do User.passwd = "lol", this will be passed to the validator and the result is an MD5'd "lol") and in load() as a comparison (there's a way to change SQLA's handling of comparisons but it's not worth the effort for this one example).

Some notes/thoughts on what needs doing etc.
`Core.callbacks`        - Function and variable naming has lost all readability as this has been modified multiple times. It is functional though.
`Core.modules`          - Untested functionality, based on qebab's idea.
`Core.db`               - I hope this code can be reused. So ideally if we make a Django webby, it will be able to simply do "import Core.db" and reuse all the same mappings, and even use the same loading code (for example, logging in would just be a case of "Core.db.maps.User.load(name=..., passwd=...)"!
`Core.maps`             - I've not even begun to scratch the surface here. Jotted some ideas down in it. Some of Zawze's code can be used here. Do we want to continue with Munin's current planet_cannon etc system? (I don't know what the pros/cons are of this or alternate ways.) Do we want to avoid SQL procedures and stick purely to SQLA? (Yes!)
`Core.chanusertracker`  - This used to be a hook, ported it to part of the core, untested in this new form. Originally used for some basic usercaching (this isn't useful), it now just keeps a list of channels and nicks that the bot is aware of, and the user associated with a nick. This is useful for reverse lookup: i.e. send a message to the nick that is a specified user.
`Hooks.chanusertracker` - Hook interface to the above.
`Hooks.relaybot.*`      - Fairly self explanatory. Run a separate instance of the bot without the majority of the plugins, and this package will relay messages over Robocop (see below), as well as part/joining all the channels just under every 24 hours (P will leave a channel if there are no joins in a 24 hour period - this is pretty retarded).
`Hooks.relay`           - Receives input from the secondary relaybot (see above). This is not a galstatus parser. This and the package above are just simple code I've already written for Rock.
`Hooks.ships.*`         - Quick port of a few of Munin's commands, examples to look through etc.
`Hooks.robocop`         - See below.
`Hooks.user.*`		- User code for a "traditional" alliance. Not fully feature complete. Whois can be modified for Asc (add sponsor, invites), as can Phone (add pubphone). Add/Edituser should give some guidance for coding !invite and !getanewdaddy (sponsor system runs off a separate table I think, so no similar code really). Also Pref should be (almost) identical for traditional and Asc, but it will need updating once the planet system is decided.

RoBoCoP:
Robocop is a system based on a Unix socket for providing the bot with live updates. It could be reworked to use a standard TCP/IP socket for Windows compatibility.
There's currently two main uses for this that I see, the first is accepting relay messages from a second bot running as a separate process (see the relaybot package).
The other option is accepting live updates from people's interaction with any website tools we can create. An example is someone not being able to access IRC, so they can put in a request for a scan on the website and it'll relay the request instantly to IRC. Or vice-versa, it can allow scanners to complete requests for scans that are requested on IRC even if the scanner can't get on IRC. Ascendancy doesn't have this problem because we can all mail everyone in the alliance, but this idea was originally for Rock, and I don't see any reason to discontinue it.
If you're curious, the name stems from someone's description of the system after I first explained it to them: Rock Bot Command Protocol. It's a bit lame, but I can't be arsed to change it now.
There are probably higher chances of instability introduced by using threading here, especially when considering SQLA. On the upside, this adds some cool possibilites (in my opinion) so I don't care.

Enjoy hacking!
ell