## Update payments

    docker build . -t cors-demo
    docker kill cors-demo && docker rm cors-demo
    docker run -d -p8001:8000 --name cors-demo cors-demo

## Update shop

    aws s3 sync partner-static s3://shop.summerisgone.com

## Live demo

[Example partner shop](https://shop.summerisgone.com/) and [Example payment system site](https://payments.summerisgone.com/)
