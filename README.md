# scores

## Build status

[![Build Status](https://travis-ci.org/zesk06/scores.svg?branch=master)](https://travis-ci.org/zesk06/scores)
[![codecov.io](https://codecov.io/github/zesk06/scores/coverage.svg?branch=master)](https://codecov.io/github/zesk06/scores?branch=master)

## cheat

### heroku

enable builpacks on heroku:

    heroku buildpacks:add heroku/python
    heroku buildpacks:add heroku/nodejs
    
## MONGO 

### Common operations

```bash
# mass player rename
# $ is replaced by the element that match the query
db.plays.updateMany({players: { $elemMatch: { login: 'from_name'}}}, {$set: {"players.$.login":"to_name"}})

```
