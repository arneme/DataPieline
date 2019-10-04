# Start airflow
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

airflow scheduler --daemon
airflow webserver --daemon -p 80

# Wait till airflow web-server is ready
echo "Waiting for Airflow web server..."
while true; do
  _RUNNING=$(ps aux | grep airflow-webserver | grep ready | wc -l)
  if [ $_RUNNING -eq 0 ]; then
    sleep 1
  else
    echo "Airflow web server is ready"
    break;
  fi
done
