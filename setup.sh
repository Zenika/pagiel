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

python3 setup-script/smartwatts-conf.py $host $port $org $token $bucket

docker-compose --profile setup up -d
