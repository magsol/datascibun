import argparse
import json
import re

def remove_urls(tweet):
    return re.sub(r"http\S+", "", tweet)

def fix_amp(tweet):
    return tweet.replace("&amp;", "&")

def remove_hashtags(tweet):
    return re.sub(r"#\w+\s*", "", tweet)

def remove_mentions(tweet):
    return re.sub(r"@\w+\s*", "", tweet)

def remove_rt(tweet):
    return tweet[2:] if tweet[:2] == 'RT' else tweet

def remove_emojis(tweet):
    return re.sub(r"[^\x00-\x7F]+", "", tweet)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'JSON tweet converter',
        epilog = 'lol tw33tz', add_help = 'How to use',
        prog = 'python json_to_txt.py <options>')

    # Required arguments.
    parser.add_argument("-i", "--input", required = True,
        help = "JSON file to convert.")

    # Optional arguments.
    parser.add_argument("-o", "--output", default = "output.txt",
        help = "Output file containing tweet content, one per line. [DEFAULT: output.txt]")

    # Parse out the arguments.
    args = vars(parser.parse_args())
    content = json.load(open(args['input'], "r"))

    fp = open(args['output'], "w")
    item = 0
    for obj in content:
        tweet = obj['tweet']['full_text']

        # STEP 1: Strip out RT.
        tweet = remove_rt(tweet)

        # STEP 2: Remove URLs, mentions, hashtags, emojis.
        tweet = remove_urls(tweet)
        tweet = remove_mentions(tweet)
        tweet = remove_hashtags(tweet)
        tweet = remove_emojis(tweet)

        # STEP 3: Other random fixes.
        tweet = tweet.strip()
        tweet = fix_amp(tweet)
        if len(tweet) == 0 or len(tweet) == 1: continue
        tweet = tweet.replace("\"\"", "")
        if tweet[0] == ":":
            tweet = tweet[1:]
        tweet = tweet.replace("\n", " ")
        tweet = tweet.strip()

        # Write out!
        fp.write(f"{tweet}\n")
        item += 1

        if item % 1000 == 0:
            print(f"{item} of {len(content)} done.")
    fp.close()
    print(f"{item} tweets processed!")

