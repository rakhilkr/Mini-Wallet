# Mini-Wallet

Use this documentation to build an API backend service, for managing a simple mini wallet. 

Submit a working executable program that can be run in localhost that is based on this documentation as close as you can. The source code should be shared as a publicly accessible repo on either GitHub, GitLab, Bitbucket, etc. Please provide steps on how to "install" and "run" the program.
If working code is not possible, submit detailed technical design specs on the logic and framework that would allow any engineer to implement as with minimal time and supervision.
The idea is that this API is exposed by the wallet service for a wallet feature. Please assume that the customer verification was already done and information/profile was already stored in a separate customer service.

For authentication to this wallet service, pass it as a header called Authorization with the content in the format of Token <my token>.

The API is a HTTP REST API and the responses are returned in JSON with structure based on JSend.
  
POST --> Initialize my account for wallet

POST --> Enable my wallet

GET --> View my wallet balance

POST --> Add virtual money to my wallet

POST --> Use virtual money from my wallet

PATCH --> Disable my wallet
