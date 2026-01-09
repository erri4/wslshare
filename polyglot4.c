#/*
'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        *:not(iframe) {
            visibility: hidden;
        }
        iframe {
            visibility: visible;
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            border: none;
            display: block;
            background: transparent;
        }
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
        }
    </style>
    <!--
'''#*/
#if __cplusplus /*
"""*/
#include <iostream>
int main(){
    std::cout << "hello from c++";
    return 0;
}
//"""
#endif
#ifndef __cplusplus /*
"""*/
#include <stdio.h>
int main(){
    printf("hullo from c");
    return 0;
}
//"""
#endif
#if 0
print('hia from python')
# python goes here
#endif
#/*
'''-->
</head>
<body>
    <iframe srcdoc="
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <title>Document</title>
        </head>
        <body>
            hi from html
            <!-- html goes here -->
        </body>
        </html>
    " loading="eager"></iframe>
</body>
</html>
'''#*/