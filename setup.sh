# check if files exist
if [ ! -f .env ]
then
    echo "Env file is missing"
    exit 1
fi

if [ ! -f ./smartwatts/config-default.json ]
then
    echo "Smartwatts config file is missing"
    exit 1
fi

#git submodule init
git submodule init
git submodule update

# grep variable from .env
token=`grep INFLUXDB_TOKEN .env`
token=${token#*=}
org=`grep INFLUXDB_ORG_NAME .env`
org=${org#*=}
port=`grep INFLUXDB_PORT .env`
port=${port#*=}
bucket=`grep INFLUXDB_BUCKET_NAME .env`
bucket=${bucket#*=}
host=`grep INFLUXDB_HOST .env`
host=${host#*=}

# dealing with json is easier with python
python3 scripts/smartwatts-conf.py $host $port $org $token $bucket
python3 scripts/sitespeed-conf.py $host $port $org $token $bucket
