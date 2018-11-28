# SNES-Randomizer

A little toy project I wrote because the only solid game randomizer I found was backloggery's, and I didn't want to add every single SNES game to my account just to run fortune cookie streams.

There's a couple of txt files required for this that are in the .gitignore. You will need to put token.txt and host.txt in the bin folder. These contain the igdb auth token and the endpoint that this app will be hosted on, respectively. There should be a default for the host but I haven't configured that just yet.

Made using CherryPy because I knew it well enough from work and just wanted a quick and easy deployment, powered by the igdb database.
