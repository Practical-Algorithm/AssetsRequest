# Description: This file contains the labels used in the Discord bot

acknowledge  = "👌"  # Content Team has acknowledged this request
complete     = "☺️"   # Request has been completed
defer        = "📲"   # Request has been deferred to Admin

reaction_map = {
    "👌": "acknowledge",
    "☺️": "complete",
    "📲": "defer"
}

# labels = [acknowledge, complete, defer]
labels = reaction_map.values()