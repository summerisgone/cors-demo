## Update payments

    docker build . -t cors-demo
    docker run -d -p8001:8000 cors-demo

## Update shop

    aws s3 sync partner-static s3://shop.summerisgone.com