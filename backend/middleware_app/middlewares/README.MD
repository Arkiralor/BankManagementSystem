# Middleware Application

This middleware application contains some critical analytical and security modules that process incoming requests and outgoing responses.

Unless specified otherwise, the middlewares described within use [MongoDB](https://www.mongodb.com/) for read/write operations as it was observed that even on locally hosted instances of relational tables, the overhead added on `write` to a request process was __~70 milliseconds__ and since we do not require [ACID](https://www.ibm.com/docs/en/cics-ts/5.4?topic=processing-acid-properties-transactions) compliance in these implementations but __do__ require fast read/write times and flexibility, we opted to forego relational data stores.

Since our system uses `JWT Authentication` via [Django Restframework-SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/), the requesting user's identity can be deciphered by decrypting the bearer token in the `Authorization` field of an incoming request.

The current application has two components:

1. __User IP Address Logger__
2. __Request Logger__

## [IP Adress Logger](ip_checker.py)

Due to the current [scenario(s) in web-applications](https://www.google.com/search?q=youtube+channel+hacked&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjQjsGO5L_-AhWtTWwGHfoZDjQQ_AUoA3oECAEQBQ&biw=1366&bih=667&dpr=1) security has become a topic of utmost importance.

The most common security vulnerabilty in today's web applications is the theft of the `accessToken` which can be used to authenticate the user
from any location and client in the known universe. For the sake of keeping the article to the point, I will not go into the details of how an access token works, the most common of which is a `JSON Web Token`. You can read further on the subject [here](https://jwt.io/introduction).

### Working Theory

1. Whenever a user successfully logs into the system using any of the available APIs, we call the `user_app.utils.UserModelUtils.log_login_ip()` just before returning the access and refresh tokens as an API response, to log the user's IP address to a collection in MongoDB we have named `userIpAdresses`. Now we have proof that this particular user can actually be found at that particular IP address as they have successfully logged in from that IP address.

    - We can expand upon this concept further by providing the user with an API that they can use to manually add a list of whitelisted IP addresses to the collection mentioned above and those IP addresses will only be viable for them.

2. Whenever a user's access token is sent in an API request, we check the `UserIpAddress` collection to count the instances where that particular user has logged in from that particular IP address. If the count is greater than 0, we know that that IP address is valid for that user, otherwise we return a `HttpResponseForbidden` response, asking the user to relogin with their credentials from that IP address.

In this way we refrain from asking the user to go through hoops in the sky just to use the system, while at the same time highly limiting the viability of stealing their access token.

#### Notes

1. If you check the source-code, you can see that we have omitted administrators and staff from the scope of this middleware as the URLs and Endpoints that can be accesses by them will be protected by firewall and reverse-proxy rules _(most commonly by [nGinX](https://www.nginx.com/))_.

2. Also, if for some reason the frontend/app isn't sending you the user's current IP address, kindly rectify it __immediately__ by following [these](https://www.thetechplatform.com/post/how-to-get-user-ip-address-in-react-js) steps, if necessary, to attach the current IP address to the correct fields in the request header _(of course, this is only an example, you can determine the user's IP address in multitudes of ways, but this should offer a good starting point)_.

#### Addendum

_It should be noted that we would want to set up a [Celery](https://docs.celeryq.dev/) or [Airflow](https://airflow.apache.org/) task to automatically delete all records older than around six months or so._

### Final Thoughts

Of cource this is a very crude and simple implementation of the logic and can be modified further. Afterall, this entire repository is only to be used as a template to set up your own codebase. For example, you can replace the `noSQL` database with a `Graph` database to take the distance between nodes (user IP adresses) into consideration when rejecting or accepting an access token.


## [Request Logger](request_logger.py)

Logging which endpoints are accessed/requested by which user is essential for today's RESTful web-applications as they form a core component of your site-wide analytics. The logged-data can be used to predict traffic for certain resources (APIs) at certain time-periods and when certain outside criteria are met; this can be used to provide additional load-balances to those resources if the additional traffic is desired or rate-limiters can be placed on those endpoints if the additional traffic is undesired. Similarly, a reduction in traffic can be further handled by revoking additional load balancers and/or rate-limiters.

These logs also help to identify the critical resources of the backend i.e, the top ~10% of the APIs that see ~90% of the traffic, irrespective of the time-period; in any web-application, these are the resources that merit the most optimization from a cost-vs-profit metric.

### Working Theory

1. Whenever a request is recieved by the backend, they "pass-through" all the middlewares described in the `settings.py` file in order of their listing in said module; our `request_logger` is listed towards the very bottom of the list so that the request only reaches it after it has already been recieved by the bulk of the security-related middlewares.

2. Once it reaches the middleware of concern, the request is dissected into its constituent elements namely, the following.

    1. `method`
    2. `path`
    3. `cookies`
    4. `headers`
    5. `params`
    6. `user`

    The user can be extracted similiarly to the middleware above, by decripting the `Authorization` field in the `header`.

3. From there, it can either be stored in the prescribed `MongoDB` collection or the `PostgreSQL` table.

#### Addendum

It should be noted that the APIs and functionality to parse these logs are available in the `analytics_app` and the `admin_app`, via REST APIs.