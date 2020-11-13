# @DataSciBun Twitter Bot

### Quickstart

Runs forever with the command:

```
$ nohup python datascibun.py > datascibun.out &
```

Note: the `nohup` prefix and `> datascibun.out &` suffixes are optional and pertain to additional logging, as well as backgrounding and detaching the process from the terminal so it can run forever. You can just as easily run `python datascibun.py` by itself.

### Dependencies

In a nutshell:
 - Python 3.7+ (since f-strings are involved)
 - NumPy (for random number generators)
 - [markovify](https://github.com/jsvine/markovify)
 - [pybot](https://github.com/magsol/pybot)

See `environment.yml` for a full list of dependencies.

### Credentials

You'll need to go to `dev.twitter.com` and create an app. From there, you'll need to generate OAuth credentials and populate the following fields in `datascibun.py`:

```
self.config['api_key'] = 'your api key here'
self.config['api_secret'] = 'your api secret here'
self.config['access_key'] = 'your access key here'
self.config['access_secret'] = 'your access secret here'
```

### Acknowledgements

In addition to those [on the pybot repo](https://github.com/magsol/pybot#acknowledgements), also inspired by [Amelia Gapin](https://twitter.com/EntirelyAmelia)'s [bot](https://twitter.com/barelyamelia).

Finally, credit to [Cathryn](https://twitter.com/write2run) for the tweeting ideas, bio, and profile pic.
