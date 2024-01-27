# KlipperRPC

KlipperRPC is an independent project that I made over the course of about an hour, expect **HORRIBLE**, **BODGED TOGETHER CODE**... *and issues, of course!*

KlipperRPC allows you to flex on all your Discord friends that you own a 3D printer and know how to use it. In all seriousness, KlipperRPC is an application that uses the Klipper web APIs to display information about your printer as a neat little rich presence widget on your profile, letting all your friends know how *awesome* you are.

# Stuff that I might do
 - Proper config file(s)
	 - Better, more awesome customization features
 - Snapshot uploading to Imgur with a "View snapshot" button embedded in the rich presence widget
	 - This requires an API key and I really don't wanna do all thattttt
	 - By the way, I did the math. Imgur's daily image rate limits *should* allow for a snapshot every ~70 seconds
 - Make the code *somewhat* readable
	 - Rewrite entire application, probably

## The story of KlipperRPC
All these other really awesome repos have origin stories, so I'll try that out...

I was just getting done making another horrible project of mine, a Flask app that lets me press keyboard shortcuts via an API, so I can do all sorts of things with shortcuts on my phone, like muting, deafening, disconnecting, or screen sharing in Discord! Then, I realized another project of mine that I wanted to get done that night. You see, many hours earlier, I had gone to my local Goodwill and found a **MASSIVE** water bottle, of course, I had to buy it. But unbeknownst to me, the most terrible, inhumane, downright **VILE** tragedy would happen to me right as I got home... The bottle didn't fit in the cup holder on my backpack... **OH THE HUMANITY!** "I must rectify this immediately!" I thought to myself. Anyway, after that, I forgot about it for a while. *(But not without realizing that these cool little flavored water bottle filter thingies screw right onto it, that's pretty neat.)* Anyway, after I used a measuring tape that was probably used by seamstresses in the 1920's to measure the bottle, modeled a *(not so)* little cup holder for it, and then sliced it, I realized that the full print would take around 6 hours, it was already 9 PM and I **REALLY** didn't wanna leave my printer running while I slept, the only fire extinguisher in my house is through a door... behind the printer. *(also, I don't really trust it yet)* So, to fix this, I made a mini version that was just the footprint of the model just to test the dimensions of the container cradling apparatus, still, this would take around about an hour to complete... 

<img src="https://github.com/404CrypticNotFound/KlipperRPC/blob/main/images/mini-cupholder.jpg?raw=true" width="250" height="330">

*Hello little cupholder!*

Whatever, I usually stay up late, anyway. So I went ahead and started the print, and after chasing my cat out of the room in fear she would sit on the printer and burst into flames, I began looking for something to do to pass the time, after about 3 minutes of YouTube, I got bored and looked through Discord, so bored in fact, I was looking at ***MY OWN PROFILE***... And that's when it hit me. Seeing that Visual Studio Code rich presence on my profile made me think. "Why can't my 3D printer do that?" and after a bit of searching to see if anyone else had thought this same thought, I began making a new folder on my **AWESOME DRIVE™** called "KlipperDiscordRPC", and began writing the most terrible, drafty code known to man. After a while of browsing the Klipper web API docs, I found some endpoints that had the information that I wanted. I then implemented them "gracefully" and had a working prototype *(production ready code)* by the time the print was finished. Oh, and when I wrote this README, I made the final name, "KlipperRPC".

## Oh, and requirements...

You'll need...
 - discordrp
 - pyyaml
 - requests

That's it.
