# test of cloudfront

This is a tiny project, meant to test:

Does placing a cloudfront distribution in front of a load balanced web service in AWS meaningfully improve network timings (i.e. transfer and roundtrip time) across geography.

Thus, resources are as follows.

- 1 webservice (ECS) behind an ALB in a region (default is eu-west-1) with a cloudfront distribution
- 1 lambda in a different region (default is us-west-1) which queries both the load balancer and the cloudfront distro.

And of course various meta resources surrounding this.

TLS/SSL is not part of this - we don't care as such about setting up certs and so on, we only care about raw transfer.

## How to!

* Deploy it!
* Go to the lambda function in the remote region and set the CF + LB endpoints as environment variables
* Fire the lambda function!
* Check the logs, consider saving them, and shut it all down.

Hurra!