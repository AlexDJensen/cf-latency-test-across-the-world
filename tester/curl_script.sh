#!/bin/sh

attempt_counter=0
max_attempts=5

# Check for AWS_LAMBDA_FUNCTION_VERSION environment variable to test that we're in AWS Lambda ENV.
# If we are, don't wait around, just run.
# Else, wait for the endpoint to be ready before running.

if [ -z "$AWS_LAMBDA_FUNCTION_VERSION" ]; then
until $(curl --output /dev/null --silent --fail $ENDPOINT_1/); do
    if [ ${attempt_counter} -eq ${max_attempts} ];then
      echo "Max attempts reached"
      exit 1
    fi

    printf '.\n'
    attempt_counter=$(($attempt_counter+1))
    sleep 5
done
fi

# Loop over this for endpoints:
for ENDPOINT in $ENDPOINT_1 $ENDPOINT_2; do
  echo "Timing for endpoint $ENDPOINT"

  echo "TIMING FOR BIG ENDPOINT:"
  curl -w "@curl-format.txt" -o /dev/null $ENDPOINT/lorem_on_hit

  echo "TIMING FOR BIG PREPPED ENDPOINT:"
  curl -w "@curl-format.txt" -o /dev/null $ENDPOINT/lorem_prepped

  echo "TIMING FOR SMALL ENDPOINT:"
  curl -w "@curl-format.txt" -o /dev/null $ENDPOINT/

  echo "-------------------------------"

done

echo "Done"
exit 0