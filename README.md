.\sc    # shell-options

##TO RUN IN DEBGGER##
uvicorn src.main:app --reload

##TODO##

1.  Replace implied_vol as calc input, with call to database
2.  Create an upsert for vol inserts (so that dupes can't ne inserted)
3.  Error handling
4.  Unit tests
5.  Remove DB connection info


docker build -t optionpricerservice:latest .

docker run -p 8003:8003 -p 8506:8506 optionpricerservice