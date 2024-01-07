import discord

def send_vx_twitter(message: discord.Message):
    domain = ""
    if "twitter.com" in message.content:
        domain = "https://twitter.com/"
    elif "x.com" in message.content:
        domain = "https://x.com/"

    if domain == "":
        return "No twitter link found."

    author = message.author.display_name
    description = message.content.split(domain)[0]
    if description == "\n":
        description = ""

    if len(message.content.split(domain)) == 1:
        return None
    query = message.content.split(domain)[1]


    result = f"**{author}**\n{description}https://vxtwitter.com/{query}"
    return result
