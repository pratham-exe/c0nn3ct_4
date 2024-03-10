# Connect 4

Connect 4 game using socket programming.


## Prerequisites

- pygame
- openssl
- generate all the certificates needed


## To generate the certificates

- To generate a CA certificate using openssl
    - Generate the CA Private key
        ```
        openssl genpkey -algorithm RSA -out ca_key.pem
        ```
    - Generate the CA Certificate Signing Request (CSR)
        ```
        openssl req -new -key ca_key.pem -out ca_csr.pem
        ```
    - Self Sign the CA Certificate
        ```
        openssl x509 -req -in ca_csr.pem -signkey ca_key.pem -out ca_cert.pem
        ```
- To generate a Server certificate
    - Generate the Server Private key
        ```
        openssl genpkey -algorithm RSA -out server_key.pem
        ```
    - Generate a CSR for the server
        ```
        openssl req -new -key server_key.pem -out server_csr.pem
        ```
    - Sign the server certificate with the CA
        ```
        openssl x509 -req -in server_csr.pem -CA ca_cert.pem -CAkey ca_key.pem -out server_cert.pem
        ```


After generating all the certificates you are good to go.!
