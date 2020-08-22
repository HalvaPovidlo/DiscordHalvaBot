

def collect_song(message):
    content = message.content
    print(content)
    if content.startswith('**Playing**'):
        # **Playing** 🎶 `Some song name` - Now!
        name = content[content.find('`') + 1:content.rfind('`')]
        print('name: ' + name)
    elif len(message.embeds) == 1:
        description = message.embeds[0].description

        linkStartIndex = description.find('https://www.youtube.com')
        if linkStartIndex == -1:
            return

        nameEndIndex = linkStartIndex - 2  # [song name](https://....
        if description[nameEndIndex] != ']':
            return

        name = description[description.find('[') + 1:nameEndIndex]
        link = description[linkStartIndex:description.rfind(')')]
        print('name: ' + name)
        print('link: ' + link)

if __name__ == '__main__':
    print("Hello World!!!")