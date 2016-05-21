[![](https://travis-ci.org/adalekin/python-vex.svg?branch=master)](https://travis-ci.org/adalekin/python-vex)

# Features
- Retreive metadata from any URL (not only direct YouTube link)
- Retreive metadata such as viewcount, title, description, author, thumbnail, keywords
- Supported providers: YouTube, Vimeo, Facebook, Instagram.
- Save thumbnails into the Django-like storage
- Works with Python 2.6+

# Installation
vex can be installed via pip:
```
pip install python-vex
```
# Usage examples
Here is how to use the module in your own python code.
```python
from vex.factory import Factory
```
create a factory instance:
```python
factory = Factory()
```

extract video metadata from url:
```python
url = "https://geektimes.ru/post/272084/"
video = factory.extract(url)
```

get certain attributes from video variable:

```python
import pprint
pprint.pprint(video)
```

```python
[{'category': u'Entertainment',
  'created_at': datetime.datetime(2016, 3, 3, 13, 55, 8),
  'description': u'Academy Award\xae-nominated director Orlando von Einsiedel, Executive Producer J.J. Abrams, Bad Robot and Epic Digital have joined forces with Google and XPRIZE to create a documentary web series about the people competing for the Google Lunar XPRIZE (http://lunar.xprize.org). The Google Lunar XPRIZE is the largest prize competition of all time with a reward of $30 million and aims to incentivize entrepreneurs to create a new era of affordable access to the Moon and beyond, while inspiring the next generation of scientists, engineers, and explorers.\n\nThis character-driven, emotional, awe-inspiring series of 9 short films will follow a selection of the teams currently racing to complete their missions.  It will explore the lives of their charismatic, quirky members, the sacrifices they have made to get to where they are today, and crucially, what drives them on this incredible journey.\n\nFollow us here to catch the series, and on:\n\nTwitter: \nhttp://twitter.com/glxp\nFacebook:\nhttp://facebook.com/googlelunarxprize\nGoogle+:\nhttps://plus.google.com/+googlelunarxprize\n\nDirector \nOrlando von Einsiedel\n\nExecutive Producer\nJ.J. Abrams\n\nProducers\nJoshua Davis\nLindsey Weber\nJoshuah Bearman \nAndrew Lee \n\nCo-Producers \nJon Drever \nBecca Perry \nBen Rosenblatt\n\nStory Producer \nSteven Leckart\n\nLine Producer \nAdam Mitchenall\n\nDirector of Photography \nFranklin Dow\n\nEditors\nKatie Bryer \nAndy Cardy \nRebecca Valente \nNathan Orloff\n\nComposer\nPatrick Jonsson\n\nProduction Managers\nSunny Dimitriadou \nElena Andreicheva\nJosie Wicks\n\nCamera Assistants\nWill Hadley \nJamie Ackroyd\nNaomi Hancock\n\nSound Recordist\nSara Lima\n\nAssistant Editors \nYoussef Bouhassis \nAilene Roberts \nLaura Creecy\n\nPost-Production Management \nAmelia Franklin \nPhilip Hoang\n\nGraphics\nSal Sciortino\n\nColorist \nJuan Ignacio Cabrera\n\nConform Artist \nPeter Amies\n\nSound Re-Recording Mixers\nLindsey Alvarez\nCraig Henighan\n\nProduction Services \nGrain Media\n\nVisual Effects\nKelvin Optical, Inc.\n\nGoogle Brand Marketing\nMichael Tabtabai\nCameron Luby\nYasemin Denari Southworth \nBen Quesnel\nMatt Hirst\n\nProduction Support\nMike Silver\nCory Bennett Lewis\nJosh Tate \nMorgan Dameron \nAmir Mojarradi\nEboni Price\nKristofer Cross\n\nSpecial Thanks\nChanda Gonzales-Mowrer \nDavid Locke \nCharles Scott\nRobby Stambler \nMatt Evans \nJesse Goldsmith \nChrysta Burton \nAli Lowndes\nDiane Coote\nRichard Jephcote\nNick Rowley \nAlice Martineau \n72andSunny\nKelly Vicars \nHarry Spitzer\nNatalie So \n\nRed Whittaker\nCarnegie Mellon University\n\nJackie Erickson\n\nJohn Thornton\nDavid Weinstein\nBrian Solomon\nJohn Williams\n\nAdditional footage provided by:\nNASA\nGoddard Space Flight Center\nArizona State University',
  'keywords': [u'Moon Shot',
               u'moonshot',
               u'google lunar xprize',
               u'glxp',
               u'bad robot',
               u'jj abrams',
               u'Orlando von Einsiedel',
               u'moon',
               u'competition',
               u'google',
               u'exploration',
               u'peter diamandis',
               u'rocket',
               u'lander',
               u'rover',
               u'surface',
               u'payload',
               u'Moon Express',
               u'Hakuto',
               u'SpaceIL',
               u'Astrobotic',
               u'Part-Time Scientists',
               u'Epic Digital'],
  'low_resolution': {'height': '360',
                     'url': u'http://r3---sn-xguxaxjvh-axql.googlevideo.com/videoplayback?ratebypass=yes&signature=3BAA4CB66C540BDB2535BC50D0B2FF6B31CDE5DB.BB1748364B1FD5BD951193BD1E7A2E9D47BBD7F3&upn=FINZsLy2ioo&pcm2cms=yes&itag=18&key=yt6&lmt=1458200476792250&ipbits=0&fexp=9405963%2C9416126%2C9416891%2C9422596%2C9423749%2C9428398%2C9431012%2C9431850%2C9433096%2C9433221%2C9433425%2C9433946%2C9434767%2C9434903%2C9434903%2C9435323%2C9435666%2C9435742%2C9435876%2C9436059%2C9436260%2C9436517%2C9436958%2C9437282&mime=video%2Fmp4&id=o-AA-VyRa3Wx8LB5xe-bFBvjsFmzK_9LRcanX7vGEHFxfZ&pl=22&mm=31&mn=sn-xguxaxjvh-axql&ms=au&mt=1463828594&mv=m&ip=188.187.84.247&initcwndbps=2996250&dur=104.745&expire=1463850488&sver=3&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpcm2cms%2Cpl%2Cratebypass%2Csource%2Cupn%2Cexpire&source=youtube',
                     'width': '640'},
  'provider': 'youtube',
  'remote': 'http://youtube.com/watch?v=cuXxBoSYmfc',
  'standard_resolution': {'height': '720',
                          'url': u'http://r3---sn-xguxaxjvh-axql.googlevideo.com/videoplayback?ratebypass=yes&signature=80470A80BC95EEE722701320FD74BBB8482E5747.9E35AFA79A701936764B586F7B2F70AB93A85B18&upn=FINZsLy2ioo&pcm2cms=yes&itag=22&key=yt6&lmt=1458200444346467&ipbits=0&fexp=9405963%2C9416126%2C9416891%2C9422596%2C9423749%2C9428398%2C9431012%2C9431850%2C9433096%2C9433221%2C9433425%2C9433946%2C9434767%2C9434903%2C9434903%2C9435323%2C9435666%2C9435742%2C9435876%2C9436059%2C9436260%2C9436517%2C9436958%2C9437282&mime=video%2Fmp4&id=o-AA-VyRa3Wx8LB5xe-bFBvjsFmzK_9LRcanX7vGEHFxfZ&pl=22&mm=31&mn=sn-xguxaxjvh-axql&ms=au&mt=1463828594&mv=m&ip=188.187.84.247&initcwndbps=2996250&dur=104.745&expire=1463850488&sver=3&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpcm2cms%2Cpl%2Cratebypass%2Csource%2Cupn%2Cexpire&source=youtube',
                          'width': '1280'},
  'thumbnail': 'http://img.youtube.com/vi/cuXxBoSYmfc/maxresdefault.jpg',
  'title': u'Moon Shot | Official Trailer | Google Lunar XPRIZE',
  'user': {'image': None,
           'name': u'GoogleLunarXPRIZE',
           'uid': u'GoogleLunarXPRIZE'},
  'watch_count': 2437411}]
```
